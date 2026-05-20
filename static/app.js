const urlInput = document.getElementById("urlInput");
const scanBtn = document.getElementById("scanBtn");

const loading = document.getElementById("loading");
const resultCard = document.getElementById("resultCard");
const errorBox = document.getElementById("errorBox");

const resultUrl = document.getElementById("resultUrl");
const predictionText = document.getElementById("predictionText");
const confidenceText = document.getElementById("confidenceText");
const confidenceFill = document.getElementById("confidenceFill");
const severityBadge = document.getElementById("severityBadge");
const threatMessage = document.getElementById("threatMessage");


function showLoading() {
    loading.classList.remove("hidden");
    resultCard.classList.add("hidden");
    errorBox.classList.add("hidden");
}

function hideLoading() {
    loading.classList.add("hidden");
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
    resultCard.classList.add("hidden");
}

function updateSeverityBadge(severity, prediction) {
    severityBadge.className = "badge";
    severityBadge.classList.add(severity);
    severityBadge.textContent = prediction;
}
const THREAT_DISPLAY = {
    suspicious: {
        badge: "SUSPICIOUS",
        message: "This URL needs manual verification."
    }
};

function resetConfidenceBar() {
    confidenceFill.style.width = "0%";
}

function validateURL(input) {
    if (!input || input.trim() === "") {
        return "Please enter a URL.";
    }

    if (input.length < 4) {
        return "URL looks too short.";
    }

    return null;
}

async function scanURL() {
    const url = urlInput.value.trim();

    const validationError = validateURL(url);

    if (validationError) {
        showError(validationError);
        return;
    }

    showLoading();
    resetConfidenceBar();

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        hideLoading();

        if (!response.ok) {
            showError(data.error || "Prediction failed.");
            return;
        }

        resultUrl.textContent = data.url;
        predictionText.textContent = data.prediction;
        confidenceText.textContent = `${data.confidence}%`;
        if (data.prediction.toLowerCase() === "suspicious") {
    threatMessage.textContent = THREAT_DISPLAY.suspicious.message;
} else {
    threatMessage.textContent = data.message;
}

        updateSeverityBadge(data.severity, data.prediction);

        resultCard.classList.remove("hidden");

        setTimeout(() => {
            confidenceFill.style.width = `${data.confidence}%`;
        }, 150);

    } catch (error) {
        hideLoading();
        showError("Server unreachable. Make sure Flask is running.");
        console.error(error);
    }
}

scanBtn.addEventListener("click", scanURL);

urlInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        scanURL();
    }
});