document.addEventListener("DOMContentLoaded", async () => {
  const btnStart = document.getElementById("rec-start");
  const btnStop = document.getElementById("rec-stop");

  let mediaRecorder;
  let chunks = [];

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: "audio/wav" });
        const formData = new FormData();
        const resultContainer = document.getElementById("result");

        formData.append("audio", audioBlob, "recording.wav");

        // Send recorded audio to back-end for processing
        fetch("/analyse", { method: "POST", body: formData })
          .then((resultContainer.innerHTML = "Analysing\u2026"))
          .then((res) => res.json())
          .then((msg) => {
            switch (msg.message) {
              case "neu":
                resultContainer.innerHTML = "Detected emotion: neutral";
                break;
              case "hap":
                resultContainer.innerHTML = "Detected emotion: happy";
                break;
              case "ang":
                resultContainer.innerHTML = "Detected emotion: angry";
                break;
              case "sad":
                resultContainer.innerHTML = "Detected emotion: sad";
                break;
            }
          })
          .catch((err) => console.error("Error processing audio:", err));

        // Reset chunks for next recording
        chunks = [];
      };

      btnStart.addEventListener("click", () => {
        mediaRecorder.start();
        btnStart.disabled = true;
        btnStop.disabled = false;
      });

      btnStop.addEventListener("click", () => {
        mediaRecorder.stop();
        btnStart.disabled = false;
        btnStop.disabled = true;
      });
    })
    .catch((err) => console.error("Error accessing microphone:", err));
});
