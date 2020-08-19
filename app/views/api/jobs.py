from flask import abort, jsonify, request

from app.extensions import rq


def get_job_status():
    """ Returns the job status for a given raffle job. """
    job = rq.get_queue().fetch_job(request.args.get("job_id"))
    if not job:
        abort(404)

    status = job.meta.get("status") if "status" in job.meta else "Waiting to process..."

    return jsonify({"status": status, "error": job.meta.get("error")})


RouteConfigs = [{"rule": "/job_status", "view_func": get_job_status}]
