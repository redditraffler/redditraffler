from app.db import db
from app.db.models import Raffle, Winner
from app.jobs import rq, update_job_status
from app.util import reddit
from app.util.raffler import Raffler
from rq import get_current_job


@rq.job
def raffle(raffle_params):
    job = get_current_job()
    submission = reddit.get_submission(sub_url=raffle_params['submission_url'])

    update_job_status(job, 'Fetching submission...')
    r = Raffler(**raffle_params)
    update_job_status(job, 'Fetching comments...')
    r.fetch_comments()
    update_job_status(job, 'Selecting winners...')
    r.select_winners()
    update_job_status(job, 'Saving results to our database...')
    _save_results_to_db(winners=r.get_serialized_winners(),
                        submission=submission)
    update_job_status(job, 'Done!')


def _save_results_to_db(winners, submission):
    pass
