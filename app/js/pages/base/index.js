import React from "react";
import ReactDOM from "react-dom";

import "@assets/css/base/index.css";

import RaffleStats from "@js/components/RaffleStats";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(
    <RaffleStats />,
    document.getElementById("raffle-stats-root")
  );
});
