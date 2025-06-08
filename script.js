// إشعار ترحيبي
// القائمة الجانبية
// القائمة الجانبية
// فتح النافذة الجانبية
function openSidebar() {
  document.getElementById("sidebar").classList.add("open");
}

// غلق النافذة الجانبية
function closeSidebar() {
  document.getElementById("sidebar").classList.remove("open");
}

// عرض مودال تسجيل الدخول
function showLogin() {
  closeSidebar();
  document.getElementById("loginModal").style.display = "flex";
}

// إخفاء مودال تسجيل الدخول
function hideLogin() {
  document.getElementById("loginModal").style.display = "none";
  clearLoginFields();
}

// تنظيف الحقول ورسالة الخطأ
function clearLoginFields() {
  document.getElementById("username").value = "";
  document.getElementById("password").value = "";
  document.getElementById("loginMessage").textContent = "";
}

// عملية تسجيل الدخول (مستخدم أو مطور)
function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const message = document.getElementById("loginMessage");

  // بيانات تسجيل دخول المطور
  if (username === "dev2025" && password === "dev2025") {
    message.style.color = "green";
    message.textContent = "تم تسجيل دخول المطور بنجاح ✅";
    localStorage.setItem("devLoggedIn", "true");
    setTimeout(() => {
      hideLogin();
      window.location.href = "developer.html";
    }, 1200);
    return;
  }

  // بيانات تسجيل دخول المستخدم العادي (
