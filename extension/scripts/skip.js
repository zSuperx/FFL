let skippedSegments = new Set();

// Example skip segments: [ [10, 5], [30, 3], [90, 10] ]
const skipTimes = [
  [10, 5],
  [30, 3],
  [90, 10]
];

function setup() {
  chrome.storage.sync.get(['skipEnabled'], (result) => {
    if (!result.skipEnabled) return;

    const interval = setInterval(() => {
      const video = document.querySelector('video');

      if (video) {
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
              break; // avoid skipping multiple at once
            }
          }
        });

        clearInterval(interval);
      }
    }, 500);
  });
}

const observer = new MutationObserver(() => {
  setup();
});

observer.observe(document.body, { childList: true, subtree: true });

setup();
