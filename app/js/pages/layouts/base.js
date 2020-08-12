import dayjs from "dayjs";
import dayjs_utc from "dayjs/plugin/utc";

dayjs.extend(dayjs_utc);

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
  document.getElementById("year").innerHTML = dayjs().utc().format("YYYY");
  setInterval(() => {
    document.getElementById("clock").innerHTML = dayjs()
      .utc()
      .format("MMMM D, YYYY h:mm:ss a");
  }, 1000);
});
