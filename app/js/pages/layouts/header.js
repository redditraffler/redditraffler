document.addEventListener("DOMContentLoaded", () => {
  // Show/hide functionality for navbar burger
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

  const logoutButton = document.getElementById("logout");
  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      document.getElementById("logout-form").submit();
    });
  }
});
