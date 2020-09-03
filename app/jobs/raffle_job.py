from rq import get_current_job
from flask import current_app

from app.extensions import db, rq, cache
from app.db.models.raffle import Raffle
from app.db.models.winner import Winner
from app.jobs.util import update_job_status, set_job_error
from app.services import reddit_service
from app.util.raffler import Raffler


@rq.job
def raffle(raffle_params, user):
    try:
        job = None
        current_app.logger.info(
            "Started raffle creation",
            {
                "raffle_params": raffle_params,
                "username": getattr(user, "username", None),
            },
        )

        sub_url = raffle_params["submission_url"]
        submission = reddit_service.get_submission_by_url(sub_url)
        sub_id = submission["id"]

        job = get_current_job()
        set_job_error(job, False)

        update_job_status(job, "Fetching submission...")
        r = Raffler(**raffle_params)

        update_job_status(job, "Fetching comments...")
        r.fetch_comments()

        update_job_status(job, "Selecting winners...")
        r.select_winners()

        if user:
            _try_remove_unverified(sub_id)

        update_job_status(job, "Saving raffle results...")
        winners = r.get_serialized_winners()
        _save_results_to_db(
            raffle_params=raffle_params,
            winners=winners,
            submission=submission,
            user=user,
        )

        current_app.logger.info(
            "Successfully created and persisted raffle",
            {
                "sub_id": sub_id,
                "raffle_params": raffle_params,
                "winners": winners,
                "username": getattr(user, "username", None),
            },
        )
        update_job_status(job, "Done!")
    except Exception as e:
        current_app.logger.exception(
            "Error while trying to create raffle", {"raffle_params": raffle_params}
        )
        if job:
            update_job_status(job, f"Error: {str(e)}")
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
        db.session.delete(unverified_raffle)
        db.session.commit()
        cache.delete("raffle_{}".format(sub_id))
        current_app.logger.warning("Removed unverified raffle", {"sub_id": sub_id})
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "Something went wrong while trying to delete an unverified raffle",
            {"sub_id": sub_id},
        )
        raise Exception


def _save_results_to_db(raffle_params, winners, submission, user):
    raffle = Raffle(
        submission_id=submission["id"],
        submission_title=submission["title"],
        submission_author=submission["author"],
        subreddit=submission["subreddit"],
        winner_count=raffle_params["winner_count"],
        min_account_age=raffle_params["min_account_age"],
        min_comment_karma=raffle_params["min_comment_karma"],
        min_link_karma=raffle_params["min_link_karma"],
        min_combined_karma=raffle_params["min_combined_karma"],
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
