import React from "react";
import ReactDOM from "react-dom";

import "@assets/css/base/index.css";

import RaffleMetrics from "@js/components/RaffleMetrics";
import RecentRaffles from "@js/components/RecentRaffles";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(
    <RaffleMetrics />,
    document.getElementById("raffle-stats-root")
  );

  ReactDOM.render(
    <RecentRaffles />,
    document.getElementById("recent-raffles-root")
  );
});
