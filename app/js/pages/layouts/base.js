import moment from "moment";

document.addEventListener("DOMContentLoaded", () => {
  // Header nav burger
  const navbarBurgers = document.getElementsByClassName("navbar-burger");
  if (navbarBurgers.length > 0) {
    Array.from(navbarBurgers).forEach((burger) => {
      burger.addEventListener("click", function () {
        this.classList.toggle("is-active");
        const menu = document.getElementById(this.getAttribute("data-target"));
        menu.classList.toggle("is-active");
      });
    });
  }

  // Header logout button
  const logoutButton = document.getElementById("logout");
  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      document.getElementById("logout-form").submit();
    });
  }

  // Footer
  document.getElementById("year").innerHTML = moment().utc().format("YYYY");
  setInterval(() => {
    document.getElementById("clock").innerHTML = moment()
      .utc()
      .format("MMMM Do YYYY, h:mm:ssa");
  }, 1000);
});
