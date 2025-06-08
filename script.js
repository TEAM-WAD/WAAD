// إشعار ترحيبي
// القائمة الجانبية
// القائمة الجانبية
const menuIcon = document.getElementById("menuIcon");
const sideMenu = document.getElementById("sideMenu");

function toggleMenu() {
  if (sideMenu.classList.contains("open")) {
    sideMenu.classList.remove("open");
  } else {
    sideMenu.classList.add("open");
  }
}

// تسجيل دخول المطور
function showLogin() {
  document.getElementById("loginModal").style.display = "flex";
}

function hideLogin() {
  document.getElementById("loginModal").style.display = "none";
}

function loginDev() {
  const username = document.getElementById("devUsername").value.trim();
  const password = document.getElementById("devPassword").value.trim();
  const message = document.getElementById("loginMessage");

  if (username === "dev2025" && password === "dev2025") {
    message.style.color = "green";
    message.textContent = "تم تسجيل الدخول بنجاح ✅";
    setTimeout(() => {
      hideLogin();
      // تخزين حالة تسجيل الدخول في التخزين المحلي
      localStorage.setItem("devLoggedIn", "true");
      window.location.href = "developer.html";
    }, 1200);
  } else {
    message.style.color = "red";
    message.textContent = "اسم المستخدم أو كلمة المرور خاطئة ❌";
  }
}

// تأكيد تسجيل الخروج من لوحة تحكم المطور
function logoutDev() {
  localStorage.removeItem("devLoggedIn");
  alert("تم تسجيل الخروج");
  window.location.href = "index.html";
}

// منطق قفل الموقع (تخزين حالة الصيانة في localStorage)
function toggleMaintenance() {
  const maintenance = localStorage.getItem("maintenanceMode");
  if (maintenance === "on") {
    localStorage.setItem("maintenanceMode", "off");
    alert("تم إلغاء وضع الصيانة");
  } else {
    localStorage.setItem("maintenanceMode", "on");
    alert("تم تفعيل وضع الصيانة");
  }
  // إعادة تحميل الصفحة لتفعيل الوضع
  location.reload();
}

// عرض إحصائيات (أرقام وهمية لمثال)
function showStats() {
  document.getElementById("stats").style.display = "block";
  // بيانات وهمية يمكن استبدالها ببيانات حقيقية من السيرفر
  document.getElementById("visitorCount").textContent = 1200;
  document.getElementById("requestCount").textContent = 350;
}

// عند تحميل الصفحة الرئيسية: التحقق من وضع الصيانة
window.onload = () => {
  if (localStorage.getItem("maintenanceMode") === "on") {
    // تحويل المستخدم لصفحة الصيانة
    window.location.href = "maintenance.html";
  }
  // التحقق من تسجيل دخول المطور
  if (localStorage.getItem("devLoggedIn") === "true" && window.location.pathname.endsWith("index.html")) {
    // لو هو في الصفحة الرئيسية ومسجل دخول يبقى كذلك
  }
};
