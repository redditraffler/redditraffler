import React from "react";
import ReactDOM from "react-dom";

import "@assets/css/base/index.css";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(
    <RaffleStats />,
    document.getElementById("raffle-stats-root")
  );
});
