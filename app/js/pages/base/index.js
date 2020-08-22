import React from "react";
import ReactDOM from "react-dom";

import RaffleStats from "~/components/RaffleStats";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(
    <RaffleStats />,
    document.getElementById("raffle-stats-root")
  );
});
