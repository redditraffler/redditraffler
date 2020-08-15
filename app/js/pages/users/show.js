import $ from "jquery";
import axios from "redaxios";
import { Endpoint } from "~/config";

require("datatables-bulma");

document.addEventListener("DOMContentLoaded", () => {
  const username = window.location.pathname.split("/").pop();

  axios.get(Endpoint.getRafflesForUser(username)).then(({ data: raffles }) => {
    if (raffles.length === 0) {
      // The table will not be present when raffles is empty
      return;
    }

    const table = document.getElementById("raffles");
    const tbody = table.querySelector("tbody");

    raffles.forEach(
      ({
        submission_id,
        submission_title,
        subreddit,
        created_at,
        created_at_readable,
      }) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${submission_title}</td>
          <td>${subreddit}</td>
          <td data-sort='${created_at}'>${created_at_readable}</td>
        `;

        row.addEventListener("click", () => {
          window.location.href = Endpoint.showRaffle(submission_id);
        });

        tbody.appendChild(row);
      }
    );

    $(table).DataTable({
      pageLength: 5,
      lengthChange: false,
      order: [[2, "desc"]],
    });
  });
});
