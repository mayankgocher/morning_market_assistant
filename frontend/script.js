let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;
let currentAudio = null;

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const submitBtn = document.getElementById("submitBtn");
const stopVoiceBtn = document.getElementById("stopVoiceBtn");
const output = document.getElementById("output");
const loader = document.getElementById("loader");
const recordStatus = document.getElementById("recordStatus");
const textInput = document.getElementById("textInput");
const chartsContainer = document.getElementById("chartsContainer");

/* ===============================
   VOICE RECORDING
================================ */
recordBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.start();

    recordStatus.innerText = "🎙 Recording...";
    recordBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
        recordedBlob = new Blob(audioChunks, { type: "audio/webm" });
        recordStatus.innerText = "✅ Recording saved";
    };
    recordBtn.disabled = false;
    stopBtn.disabled = true;
};

/* ===============================
   STOP VOICE
================================ */
stopVoiceBtn.onclick = () => {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
    stopVoiceBtn.disabled = true;
};

/* ===============================
   SUBMIT HANDLER
================================ */
submitBtn.onclick = async () => {
    output.innerText = "";
    chartsContainer.innerHTML = "";
    loader.classList.remove("hidden");
    submitBtn.disabled = true;

    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }

    const text = textInput.value.trim();

    try {
        let data;

        if (text.length > 0) {
            const response = await fetch("http://127.0.0.1:8000/text/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: text })
            });
            data = await response.json();
        } else if (recordedBlob) {
            const formData = new FormData();
            formData.append("file", recordedBlob, "voice.webm");
            const response = await fetch("http://127.0.0.1:8000/voice/query", {
                method: "POST",
                body: formData
            });
            data = await response.json();
        } else {
            output.innerText = "❌ Please type or record a query.";
            return;
        }

        output.innerText = data.response;
        playVoice(data.audio_b64);

        for (const ticker of data.tickers) {
            await renderChart(ticker);
        }

    } catch (err) {
        output.innerText = "❌ Error occurred.";
        console.error(err);
    } finally {
        loader.classList.add("hidden");
        submitBtn.disabled = false;
    }
};

/* ===============================
   DYNAMIC CHART RENDER
================================ */
async function renderChart(ticker) {
    const res = await fetch(`http://127.0.0.1:8000/chart-data/${ticker}`);
    const data = await res.json();

    const canvas = document.createElement("canvas");
    chartsContainer.appendChild(canvas);

    new Chart(canvas.getContext("2d"), {
        type: "line",
        data: {
            labels: data.dates,
            datasets: [{
                label: `${ticker} Price`,
                data: data.prices,
                borderColor: "#2563eb",
                backgroundColor: "rgba(37,99,235,0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
}

/* ===============================
   VOICE PLAYBACK
================================ */
function playVoice(audio_b64) {
    if (!audio_b64) return;
    currentAudio = new Audio("data:audio/mp3;base64," + audio_b64);
    currentAudio.playbackRate = 1.15;
    currentAudio.play();
    stopVoiceBtn.disabled = false;

    currentAudio.onended = () => {
        stopVoiceBtn.disabled = true;
        currentAudio = null;
    };
}
