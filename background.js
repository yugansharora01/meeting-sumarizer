let mediaRecorder;
let audioChunks = [];

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === "START_RECORDING") {
    chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
      if (!stream) {
        console.error("Failed to capture tab audio");
        return;
      }

      mediaRecorder = new MediaRecorder(stream);

      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks, { type: "audio/webm" });

        // TODO: send to backend
        console.log("Recording complete", blob);

        const url = URL.createObjectURL(blob);
        chrome.downloads.download({
          url: url,
          filename: "meeting-recording.webm",
        });
      };

      mediaRecorder.start();
      console.log("Recording started");
    });
  }

  if (message.action === "STOP_RECORDING") {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
      console.log("Recording stopped");
    }
  }
});
