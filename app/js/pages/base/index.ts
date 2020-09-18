import React from "react";
import ReactDOM from "react-dom";

import "@assets/css/base/index";

import RaffleMetrics from "@js/components/RaffleMetrics";
import RecentRaffles from "@js/components/RecentRaffles";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(
    React.createElement(RaffleMetrics),
    document.getElementById("raffle-metrics-root")
  );

  ReactDOM.render(
    React.createElement(RecentRaffles),
    document.getElementById("recent-raffles-root")
  );
});
