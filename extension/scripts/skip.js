let skippedSegments = new Set();

const skipTimes = [
	[10, 5],
	[30, 3],
	[90, 10]
];

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	alert("Skip received message")
	if (message.type === "received") {
		alert("Skip received: "+message.data)
		// skipTimes = message.data
	}

	sendResponse({ status: "ok" });
});

function startSkipLogic() {
  const video = document.querySelector('video');
  if (!video) return;

  video.addEventListener('timeupdate', () => {
    const currentTime = video.currentTime;

    for (let i = 0; i < skipTimes.length; i++) {
      const [startTime, jumpAmount] = skipTimes[i];

      if (
        !skippedSegments.has(i) &&
        currentTime >= startTime &&
        currentTime < startTime + 0.5
      ) {
        video.currentTime = currentTime + jumpAmount;
        skippedSegments.add(i);
        break;
      }
    }
  });
}

function setup() {
  // Always check in a valid content context
  if (typeof chrome !== "undefined" && chrome.storage) {
    chrome.storage.sync.get(['skipEnabled'], (result) => {
      if (!result.skipEnabled) return;

      const interval = setInterval(() => {
        const video = document.querySelector('video');
        if (video) {
          startSkipLogic();
          clearInterval(interval);
        }
      }, 500);
    });
  } else {
    console.warn('Chrome extension context not available.');
  }
}

// Watch for YouTube's SPA changes
const observer = new MutationObserver(() => {
  skippedSegments = new Set(); // Reset for new page load
  setup();
});

observer.observe(document.body, { childList: true, subtree: true });

// setup(); // Initial run
