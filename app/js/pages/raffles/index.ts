/* eslint-disable @typescript-eslint/ban-ts-comment */
// https://datatables.net/forums/discussion/43042/uncaught-typeerror-cannot-set-property-of-undefined/p2

import $ from "jquery";
import dt from "datatables.net-dt";

require("datatables-bulma");

// @ts-ignore
$.fn.DataTable = dt;

$(() => {
  // @ts-ignore
  $("#raffles").DataTable({
    lengthChange: false,
    order: [[2, "desc"]],
  });

  $("#raffles tbody tr").click(function () {
    const raffle_id = $(this).attr("data-raffle-id");
    if (raffle_id) {
      window.location.href = `raffles/${raffle_id}`;
    }
  });
});
