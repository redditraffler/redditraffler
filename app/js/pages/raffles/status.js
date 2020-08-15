import axios from "redaxios";
import { Endpoint } from "~/config";

const POLL_RATE_MS = 1000;
const JOB_COMPLETE_REDIRECT_DELAY_MS = 1500;

const $ = (id) => document.getElementById(id);

const ContactUsHTML = (status, jobId) => `
  <p><i class='fas fa-times fa-6x has-text-reddit'></i><p>
  <p class='title'>${status}</p>
  <p>For additional assistance, please <a href='/about#contact'>contact us</a> with the code '${jobId}' and we'll look into it ASAP.</p>
`;

const JobCompleteHTML = `
  <p><i class='fas fa-check fa-6x has-text-reddit'></i></p>
  <p class='title'>Done!</p>
  <p>Redirecting you to the results page...</p>
`;

const pollJobStatus = () => {
  const job_id = window.location.pathname.split("/")[2]; // path is: /raffles/<job_id>/status

  axios
    .get(Endpoint.getJobStatus, { params: { job_id } })
    .then(({ data: { status, error } }) => {
      const loader = $("loader");
      const statusContainer = $("status-container");

      if (error) {
        loader.style.display = "none";
        statusContainer.innerHTML = ContactUsHTML(status, job_id);
      } else if (status == "Done!") {
        loader.style.display = "none";
        statusContainer.innerHTML = JobCompleteHTML;
        setTimeout(
          () => (window.location.href = `/raffles/${job_id}`),
          JOB_COMPLETE_REDIRECT_DELAY_MS
        );
      } else {
        // Still processing
        $("job-status").innerText = status;
        setTimeout(pollJobStatus, POLL_RATE_MS);
      }
    })
    .catch((err) => {
      console.error(err);
    });
};

document.addEventListener("DOMContentLoaded", pollJobStatus);
