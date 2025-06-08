const btn = document.getElementById("generate-btn");
const resultDiv = document.getElementById("result");

btn.addEventListener("click", async () => {
  resultDiv.textContent = "جاري إنشاء الحساب... يرجى الانتظار";

  try {
    const response = await fetch("/generate"); // هذا مسار الـ API في الباكند
    if (!response.ok) throw new Error("فشل في الاتصال بالخادم");

    const data = await response.json();

    if (data.error) {
      resultDiv.textContent = "فشل في إنشاء الحساب: " + data.error;
    } else {
      resultDiv.innerHTML = `
        <p><strong>البريد:</strong> ${data.email}</p>
        <p><strong>اسم المستخدم:</strong> ${data.username}</p>
        <p><strong>كلمة المرور:</strong> ${data.password}</p>
      `;
    }
  } catch (err) {
    resultDiv.textContent = "حدث خطأ أثناء الاتصال بالخادم";
  }
});