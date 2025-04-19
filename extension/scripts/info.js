document.addEventListener("DOMContentLoaded", () => {
  const scanButton = document.getElementById("scanButton");

  scanButton.addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentUrl = tabs[0]?.url;
      if (currentUrl) {
        navigator.clipboard.writeText(currentUrl)
      } else {
        alert("Unable to get tab URL.");
      }
    });
  });
});
