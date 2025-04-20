document.addEventListener('DOMContentLoaded', () => {
  const skipToggle = document.getElementById('skipToggle');

  // Restore saved toggle state
  chrome.storage.sync.get(['skipEnabled'], (result) => {
    skipToggle.checked = result.skipEnabled ?? false;
  });

  // Save toggle state when user interacts
  skipToggle.addEventListener('change', () => {
    chrome.storage.sync.set({ skipEnabled: skipToggle.checked });
  });
});
