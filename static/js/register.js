function togglePassword(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const toggleIcon = document.getElementById(iconId);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.textContent = "🙈";
    } else {
        passwordInput.type = "password";
        toggleIcon.textContent = "👁️";
    }
}

document
    .querySelector(".register-form")
    .addEventListener("submit", function (e) {
        const submitBtn = document.querySelector(".auth-btn");
        const btnText = submitBtn.querySelector(".btn-text");
        const btnIcon = submitBtn.querySelector(".btn-icon");

        btnText.textContent = "Creating Account...";
        btnIcon.textContent = "⏳";
        submitBtn.disabled = true;
    });

document.getElementById("id_password1").addEventListener("input", function () {
    const password = this.value;
    const strengthIndicator = document.getElementById("password-strength");

    if (password.length === 0) {
        strengthIndicator.style.display = "none";
        return;
    }

    strengthIndicator.style.display = "block";

    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    const strengthLevels = ["Very Weak", "Weak", "Fair", "Good", "Strong"];
    const strengthColors = [
        "#ff4757",
        "#ff6b7a",
        "#ffa726",
        "#66bb6a",
        "#4caf50",
    ];

    strengthIndicator.textContent =
        strengthLevels[strength - 1] || "Very Weak";
    strengthIndicator.style.color = strengthColors[strength - 1] || "#ff4757";
});
