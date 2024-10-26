function startRecording(el, rec) {
  el.innerHTML = "Recording\u2026";
  el.disabled = true;

  console.log("Recording started.");
}

document.addEventListener("DOMContentLoaded", async () => {
  const btnStart = document.getElementById("rec-start");

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);

      btnStart.addEventListener(
        "click",
        startRecording(btnStart, mediaRecorder)
      );
    })
    .catch((err) => console.error("Error accessing microphone:", err));
});
