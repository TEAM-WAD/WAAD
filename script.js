// إشعار ترحيبي
function hideWelcomePopup() {
  document.getElementById("welcome-popup").style.display = "none";
}

window.onload = function () {
  if (!sessionStorage.getItem("welcomeShown")) {
    document.getElementById("welcome-popup").style.display = "flex";
    sessionStorage.setItem("welcomeShown", "true");
  }

  // إظهار إشعار التحديث
  const bar = document.getElementById("page-notification");
  bar.style.display = "block";
  setTimeout(() => {
    bar.style.display = "none";
  }, 5000);
};

// إشعار "قريباً"
function showPopup(serviceName) {
  document.getElementById("popup-text").innerText = `خدمة ${serviceName} سيتم فتحها قريباً`;
  document.getElementById("popup").style.display = "flex";
}

function hidePopup() {
  document.getElementById("popup").style.display = "none";
}
