const API_URL = "https://pagepulse-api.onrender.com/audit";

const urlInput = document.getElementById("urlInput");
const auditBtn = document.getElementById("auditBtn");

const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const results = document.getElementById("results");

auditBtn.addEventListener("click", auditWebsite);

async function auditWebsite() {

    const url = urlInput.value.trim();

    if (!url) {
        showError("Please enter a website URL.");
        return;
    }

    hideError();
    results.classList.add("hidden");
    loading.classList.remove("hidden");

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });

        const data = await response.json();

        loading.classList.add("hidden");

        if (!response.ok) {

            if (data.detail) {

                if (typeof data.detail === "string") {
                    showError(data.detail);
                } else {
                    showError(JSON.stringify(data.detail));
                }

            } else {
                showError("Something went wrong.");
            }

            return;
        }

        document.getElementById("status").textContent =
            data.status;

        document.getElementById("responseTime").textContent =
            `${data.response_time_ms} ms`;

        document.getElementById("title").textContent =
            data.title ?? "N/A";

        document.getElementById("metaDescription").textContent =
            data.meta_description ?? "N/A";

        document.getElementById("h1Count").textContent =
            data.h1_count;

        document.getElementById("missingAlt").textContent =
            data.images_missing_alt;

        document.getElementById("wordCount").textContent =
            data.word_count;

        results.classList.remove("hidden");

    }
    catch {

        loading.classList.add("hidden");

        showError("Unable to connect to the backend.");

    }

}

function showError(message) {

    errorBox.textContent = message;
    errorBox.classList.remove("hidden");

}

function hideError() {

    errorBox.classList.add("hidden");

}