from flask_rq2 import RQ

rq = RQ()


def update_job_status(job, status):
    job.meta['status'] = status
    job.save_meta()
