let skipped = false;

function setup() {
  const interval = setInterval(() => {
    const video = document.querySelector('video');

    if (video) {
      video.addEventListener('timeupdate', () => {
        const currentTime = video.currentTime;

        if (!skipped && currentTime >= 10) {
          video.currentTime = currentTime + 5; // Jump forward 5 seconds
          skipped = true;
        }
      });

      clearInterval(interval);
    }
  }, 500);
}

const observer = new MutationObserver(() => {
  setup();
});

observer.observe(document.body, { childList: true, subtree: true });

setup();
