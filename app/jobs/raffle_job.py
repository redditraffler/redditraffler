from app.extensions import db, rq, cache
from app.db.models import Raffle, Winner
from app.jobs.util import update_job_status, set_job_error
from app.util import reddit
from app.util.raffler import Raffler
from rq import get_current_job
from flask import current_app, escape


@rq.job
def raffle(raffle_params, user):
    try:
        sub_url = raffle_params["submission_url"]
        sub_id = reddit.submission_id_from_url(sub_url)
        submission = reddit.get_submission(sub_url=sub_url)

        current_app.logger.info(
            "[Job %s] Started job %s" % (sub_id, str(raffle_params))
        )
        job = get_current_job()
        set_job_error(job, False)

        current_app.logger.info("[Job %s] Fetching submission" % sub_id)
        update_job_status(job, "Fetching submission...")
        r = Raffler(**raffle_params)

        current_app.logger.info("[Job %s] Fetching comments" % sub_id)
        update_job_status(job, "Fetching comments...")
        r.fetch_comments()

        current_app.logger.info("[Job %s] Selecting winners" % sub_id)
        update_job_status(job, "Selecting winners...")
        r.select_winners()

        if user:
            current_app.logger.info(
                "[Job %s] Searching for any unverified"
                "raffles for this submission..." % sub_id
            )
            _try_remove_unverified(sub_id)

        current_app.logger.info("[Job %s] Saving results" % sub_id)
        update_job_status(job, "Saving raffle results...")
        _save_results_to_db(
            raffle_params=raffle_params,
            winners=r.get_serialized_winners(),
            submission=submission,
            user=user,
        )

        current_app.logger.info("[Job %s] Completed" % sub_id)
        update_job_status(job, "Done!")
    except:
        # TODO: Find possible exceptions raised
        current_app.logger.exception("[Job %s] Error" % sub_id)
        set_job_error(job, True)


def _try_remove_unverified(sub_id):
    """ Removes an unverified raffle for the given sub_id if it exists. """
    unverified_raffle = (
        Raffle.query.filter(Raffle.submission_id == sub_id)
        .filter(Raffle.user_id == None)
        .first()
    )
    if not unverified_raffle:
        return

    try:
        current_app.logger.info("[Job %s] Removing unverified raffle..." % sub_id)
        db.session.delete(unverified_raffle)
        db.session.commit()
        cache.delete("raffle_{}".format(sub_id))
        current_app.logger.info(
            "[Job %s] Successfully removed unverified " "raffle." % sub_id
        )
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "[Job %s] Something went wrong " "while deleting the raffle." % sub_id
        )
        raise


def _save_results_to_db(raffle_params, winners, submission, user):
    raffle = Raffle(
        submission_id=submission["id"],
        submission_title=escape(submission["title"]),
        submission_author=submission["author"],
        subreddit=submission["subreddit"],
        winner_count=raffle_params["winner_count"],
        min_account_age=raffle_params["min_account_age"],
        min_comment_karma=raffle_params["min_comment_karma"],
        min_link_karma=raffle_params["min_link_karma"],
        user_id=user.id if user else None,
        ignored_users=",".join(raffle_params["ignored_users"]),
    )

    for winner in winners:
        user = winner["user"]
        w = Winner(
            username=user["username"],
            account_age=user["age"],
            comment_karma=user["comment_karma"],
            link_karma=user["link_karma"],
            comment_url=winner["comment_url"],
        )
        raffle.winners.append(w)

    db.session.add(raffle)
    db.session.commit()
