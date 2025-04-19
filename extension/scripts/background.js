chrome.runtime.onInstalled.addListener(() => {
  // Create the "Copy link to this page" context menu item
  chrome.contextMenus.create({
    id: "copyLink",
    title: "Copy link to this page",
    contexts: ["page"] // Only available when right-clicking on the page itself
  });
});

// Handle context menu item clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "copyLink" && tab.url) {
    // Trigger content script (copy.js) to copy the page URL to clipboard
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: copyUrlToClipboard
    });
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "copyUrl") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          func: copyUrlToClipboard
        }).then(() => {
          sendResponse({ success: true });
        }).catch(() => {
          sendResponse({ success: false });
        });
      } else {
        sendResponse({ success: false });
      }
    });

    // Keep the message channel open for async `sendResponse`
    return true;
  }
});


// Function to be injected into the page to copy the URL
function copyUrlToClipboard() {
  const currentUrl = window.location.href;
  navigator.clipboard.writeText(currentUrl).then(() => {
    console.log("Page URL copied to clipboard:", currentUrl);
  }).catch(err => {
    console.error("Failed to copy page URL:", err);
  });
}
