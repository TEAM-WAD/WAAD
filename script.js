function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("open");
}

function showLogin() {
  document.getElementById("loginModal").style.display = "flex";
}

function hideLogin() {
  document.getElementById("loginModal").style.display = "none";
  document.getElementById("username").value = "";
  document.getElementById("password").value = "";
  document.getElementById("loginMessage").textContent = "";
}

function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const message = document.getElementById("loginMessage");

  if (username === "dev2025" && password === "dev2025") {
    message.textContent = "✅ تم تسجيل دخول المطور";
    message.style.color = "green";
    setTimeout(() => {
      hideLogin();
      window.location.href = "developer.html";
    }, 1000);
  } else if (username && password) {
    message.textContent = "✅ تسجيل دخول المستخدم";
    message.style.color = "green";
    setTimeout(hideLogin, 1000);
  } else {
    message.textContent = "❌ الرجاء إدخال بيانات صحيحة";
    message.style.color = "red";
  }
}
