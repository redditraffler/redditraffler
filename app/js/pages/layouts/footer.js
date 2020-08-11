import moment from "moment";

const $ = (identifier) => document.querySelector(identifier);

document.addEventListener("DOMContentLoaded", () => {
  $("#year").innerHTML = moment().utc().format("YYYY");

  setInterval(() => {
    $("#clock").innerHTML = moment().utc().format("MMMM Do YYYY, h:mm:ssa");
  }, 1000);
});
