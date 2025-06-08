function toggleMenu() {
  const menu = document.getElementById("sideMenu");
  menu.style.left = menu.style.left === "0px" ? "-250px" : "0px";
}

function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
}
