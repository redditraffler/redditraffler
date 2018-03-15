def update_job_status(job, status):
    job.meta['status'] = status
    job.save_meta()


def set_job_error(job, is_error):
    job.meta['error'] = is_error
    job.save_meta()
