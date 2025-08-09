// === frontend/main.js ===

const video = document.getElementById("video");
const alertBox = document.getElementById("alert");

function startCamera() {
  fetch("http://localhost:5000/start")
    .then(() => {
      video.src = "http://localhost:5000/video_feed";
      video.style.display = "block";
    })
    .catch((error) => {
      console.error("Error starting camera:", error);
    });
}

function stopCamera() {
  fetch("http://localhost:5000/stop")
    .then(() => {
      video.src = "";
      video.style.display = "none";
      alertBox.classList.add("hidden");
      alertBox.classList.remove("visible");
    })
    .catch((error) => {
      console.error("Error stopping camera:", error);
    });
}

function stopAlarm() {
  fetch("http://localhost:5000/stop_alarm", {
    method: "POST",
  })
    .then(() => {
      alertBox.classList.add("hidden");
      alertBox.classList.remove("visible");
    })
    .catch((error) => {
      console.error("Error stopping alarm:", error);
    });
}

async function checkAlarm() {
  try {
    const res = await fetch("http://localhost:5000/alarm_status");
    const data = await res.json();

    if (data.alarm === true) {
      alertBox.classList.remove("hidden");
      alertBox.classList.add("visible");
    } else {
      alertBox.classList.add("hidden");
      alertBox.classList.remove("visible");
    }
  } catch (error) {
    console.error("Error checking alarm status:", error);
  }
}

setInterval(checkAlarm, 100);
