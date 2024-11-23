let locale; // Active locale

let translations = {}; // Filled with active locale translations

function delay(ms) {
  return new Promise((res) => {
    setTimeout(res, ms);
  });
}

function calmDown(el) {
  const banner = el.appendChild(document.createElement("strong"));
  banner.innerHTML = t("calm_down");

  const timer = el.appendChild(document.createElement("div"));
  timer.classList.add("timer");

  let i = 10;

  let x = setInterval(function () {
    timer.innerHTML = i.toString();

    if (i < 1) {
      clearInterval(x);
      el.removeChild(banner);
      el.removeChild(timer);
    }
    i--;
  }, 1000);
}

// Retrieve translations JSON for given locale
async function fetchTranslationsFor(newLocale) {
  const response = await fetch(`/static/lang/${newLocale}.json`);
  return await response.json();
}

// Replace inner text with corresponding translation
function translateElement(element) {
  const key = element.getAttribute("data-i18n-key");
  const translation = translations[key];
  element.innerText = translation;
}

// Replace each element with corresponding translation
function translatePage() {
  document.querySelectorAll("[data-i18n-key]").forEach(translateElement);
}

async function notifyBackend(newLocale) {
  await fetch("/set-locale", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ locale: newLocale }),
  });
}

// Load translations and translate page to given locale
async function setLocale(newLocale) {
  if (newLocale === locale) return;

  await notifyBackend(newLocale);

  const newTranslations = await fetchTranslationsFor(newLocale);
  locale = newLocale;
  translations = newTranslations;
  translatePage();
}

// Load locale translations and update page
function bindLocaleSwitcher(initialValue) {
  const switcher = document.querySelector("[data-i18n-switcher]");
  switcher.value = initialValue;
  switcher.onchange = (e) => {
    // Set locale to selected option
    setLocale(e.target.value);
  };
}

function t(key, placeholders = {}) {
  let translation = translations[key] || key; // Fallback if no translation

  // Replace placeholders
  Object.keys(placeholders).forEach((placeholder) => {
    const value = placeholders[placeholder];
    translation = translation.replace(`{${placeholder}}`, value);
  });

  return translation;
}

document.addEventListener("DOMContentLoaded", async () => {
  // Translate page to default locale
  setLocale(defaultLocale);
  bindLocaleSwitcher(defaultLocale);

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
          .then((resultContainer.innerHTML = t("analysing")))
          .then((res) => res.json())
          .then((msg) => {
            switch (msg.message) {
              case "neu":
                resultContainer.innerHTML =
                  t("detected_emotion") + " " + t("neutral");
                break;
              case "hap":
                resultContainer.innerHTML =
                  t("detected_emotion") +
                  " " +
                  '<span class="happy">' +
                  t("happy") +
                  "</span>";
                break;
              case "ang":
                resultContainer.innerHTML = resultContainer.innerHTML =
                  t("detected_emotion") +
                  " " +
                  '<span class="angry">' +
                  t("angry") +
                  "</span>";
                calmDown(document.getElementById("calm-down"));
                break;
              case "sad":
                resultContainer.innerHTML = resultContainer.innerHTML =
                  t("detected_emotion") +
                  " " +
                  '<span class="sad">' +
                  t("sad") +
                  "</span>";
                break;
            }
          })
          .catch((err) => console.error(t("error_processing_audio"), err));

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
    .catch((err) => console.error(t("error_accessing_microphone"), err));
});
