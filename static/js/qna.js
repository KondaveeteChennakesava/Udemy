function toggleReplyForm(formId) {
    const replyForm = document.getElementById(formId + "-reply");
    const allForms = document.querySelectorAll(".reply-form-wrapper");

    allForms.forEach((form) => {
        if (form.id !== formId + "-reply") {
            form.style.display = "none";
        }
    });

    if (replyForm.style.display === "none" || replyForm.style.display === "") {
        replyForm.style.display = "block";
        const textarea = replyForm.querySelector("textarea");
        if (textarea) {
            textarea.focus();
        }
    } else {
        replyForm.style.display = "none";
        const textarea = replyForm.querySelector("textarea");
        if (textarea) {
            textarea.value = "";
        }
    }
}

document.addEventListener("click", function (e) {
    if (
        !e.target.closest(".action-btn") &&
        !e.target.closest(".reply-form-wrapper")
    ) {
        const allForms = document.querySelectorAll(".reply-form-wrapper");
        allForms.forEach((form) => {
            form.style.display = "none";
            const textarea = form.querySelector("textarea");
            if (textarea) {
                textarea.value = "";
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".reply-form, .comment-form");
    forms.forEach((form) => {
        form.addEventListener("submit", function () {
            const button = this.querySelector('button[type="submit"]');
            button.disabled = true;
            button.innerHTML = '<span class="loading">⏳</span> Posting...';
        });
    });
});
