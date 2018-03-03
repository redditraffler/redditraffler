from app.extensions import db, rq
from app.db.models import Raffle, Winner
from app.jobs.util import update_job_status
from app.util import reddit
from app.util.raffler import Raffler
from rq import get_current_job


@rq.job
def raffle(raffle_params, user):
    job = get_current_job()
    submission = reddit.get_submission(sub_url=raffle_params['submission_url'])

    update_job_status(job, 'Fetching submission...')
    r = Raffler(**raffle_params)
    update_job_status(job, 'Fetching comments...')
    r.fetch_comments()
    update_job_status(job, 'Selecting winners...')
    r.select_winners()
    update_job_status(job, 'Saving results to our database...')
    _save_results_to_db(raffle_params=raffle_params,
                        winners=r.get_serialized_winners(),
                        submission=submission,
                        user=user)
    update_job_status(job, 'Done!')


def _save_results_to_db(raffle_params, winners, submission, user):
    raffle = Raffle(submission_id=submission['id'],
                    submission_title=submission['title'],
                    submission_author=submission['author'],
                    subreddit=submission['subreddit'],
                    winner_count=raffle_params['winner_count'],
                    min_account_age=raffle_params['min_account_age'],
                    min_comment_karma=raffle_params['min_comment_karma'],
                    min_link_karma=raffle_params['min_link_karma'],
                    user_id=user.id if user else None)

    for winner in winners:
        user = winner['user']
        w = Winner(username=user['username'],
                   account_age=user['age'],
                   comment_karma=user['comment_karma'],
                   link_karma=user['link_karma'],
                   comment_url=winner['comment_url'])
        raffle.winners.append(w)

    db.session.add(raffle)
    db.session.commit()
