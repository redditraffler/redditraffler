import axios from "redaxios";

export const Endpoint = {
  postFormSubmit: "/api/raffles/new",
  getSubmission: "/api/submission",
  getSubmissionsForCurrentUser: "/api/submissions",
  getJobStatus: "/api/job_status",
  getRafflesForUser: (username) => `/api/users/${username}/raffles`,
  showRaffle: (raffleId) => `/raffles/${raffleId}`,
  getRaffleMetrics: "/api/raffles/metrics",
  getRecentRaffles: "/api/raffles/recent",
};

export const getRaffleMetrics = async () => {
  const { data } = await axios.get(Endpoint.getRaffleMetrics);
  return data;
};

export const getRecentRaffles = async () => {
  const { data } = await axios.get(Endpoint.getRecentRaffles);
  return data;
};
