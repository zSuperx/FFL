document.addEventListener('DOMContentLoaded', () => {
  const skipToggle = document.getElementById('skipToggle');
  const autoScanToggle = document.getElementById('autoScanToggle');

  // Restore toggle states
  chrome.storage.sync.get(['skipEnabled', 'autoScanEnabled'], (result) => {
    skipToggle.checked = result.skipEnabled ?? false;
    autoScanToggle.checked = result.autoScanEnabled ?? false;
  });

  // Save skip toggle state
  skipToggle.addEventListener('change', () => {
    chrome.storage.sync.set({ skipEnabled: skipToggle.checked });
  });

  // Save auto scan toggle state
  autoScanToggle.addEventListener('change', () => {
    chrome.storage.sync.set({ autoScanEnabled: autoScanToggle.checked });
  });
});
