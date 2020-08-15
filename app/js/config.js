export const Endpoint = {
  postFormSubmit: "/api/raffles/new",
  getSubmission: "/api/submission",
  getSubmissionsForCurrentUser: "/api/submissions",
  getJobStatus: "/api/job_status",
  getRafflesForUser: (username) => `/api/users/${username}/raffles`,
  showRaffle: (raffleId) => `/raffles/${raffleId}`,
};
