let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const status = document.getElementById("status");

startBtn.onclick = async () => {
  status.innerText = "Recording...";

  chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
    if (!stream) {
      console.error("❌ Failed to capture stream");
      status.innerText = "Failed to capture";
      return;
    }

    console.log("✅ Stream captured");

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: "audio/webm" });

      const url = URL.createObjectURL(blob);

      chrome.downloads.download({
        url: url,
        filename: "meeting-recording.webm",
      });

      status.innerText = "Saved!";
    };

    mediaRecorder.start();
  });
};

stopBtn.onclick = () => {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
    status.innerText = "Stopped";
  }
};
