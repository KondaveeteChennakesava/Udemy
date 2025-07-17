function togglePassword() {
    const passwordInput = document.getElementById("password");
    const toggleIcon = document.getElementById("toggle-icon");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.textContent = "🙈";
    } else {
        passwordInput.type = "password";
        toggleIcon.textContent = "👁️";
    }
}

document.querySelector(".login-form").addEventListener("submit", function (e) {
    const submitBtn = document.querySelector(".auth-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnIcon = submitBtn.querySelector(".btn-icon");

    btnText.textContent = "Signing in...";
    btnIcon.textContent = "⏳";
    submitBtn.disabled = true;
});
