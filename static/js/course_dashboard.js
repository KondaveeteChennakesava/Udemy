document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        this.classList.add('active');
        
        const tabId = this.dataset.tab + '-tab';
        document.getElementById(tabId).classList.add('active');
    });
});

document.querySelectorAll(".mark-complete-form").forEach((form) => {
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const button = this.querySelector(".complete-btn");
        const lessonId = this.querySelector('input[name="lesson_id"]').value;

        button.disabled = true;
        button.innerHTML = "<span>⏳</span> Marking Complete...";

        const csrfToken = document.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

        const formData = new FormData();
        formData.append("lesson_id", lessonId);
        formData.append("csrfmiddlewaretoken", csrfToken);

        fetch(window.location.pathname + "complete/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken,
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    const lessonCard = this.closest(".lesson-card");
                    lessonCard.classList.add("completed");

                    const statusIcon =
                        lessonCard.querySelector(".status-icon");
                    statusIcon.classList.remove("pending");
                    statusIcon.classList.add("completed");
                    statusIcon.textContent = "✅";

                    this.outerHTML =
                        '<button class="lesson-btn completed-btn" disabled><span>✅</span> Completed</button>';

                    setTimeout(() => {
                        location.reload();
                    }, 500);
                } else {
                    throw new Error(
                        data.error || "Failed to mark lesson as complete"
                    );
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error marking lesson as complete. Please try again.");

                button.disabled = false;
                button.innerHTML = "<span>✓</span> Mark Complete";
            });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const progressCircle = document.querySelector(".progress-ring-fill");
    const progressElement = document.querySelector(".progress-percentage");

    if (progressCircle && progressElement) {
        const progress = parseInt(progressElement.textContent) || 0;
        const circumference = 2 * Math.PI * 52;
        const offset = circumference - (progress / 100) * circumference;

        progressCircle.style.strokeDasharray = circumference;
        progressCircle.style.strokeDashoffset = offset;

        setTimeout(() => {
            progressCircle.style.transition =
                "stroke-dashoffset 1s ease-in-out";
            progressCircle.style.strokeDashoffset = offset;
        }, 100);
    }
});