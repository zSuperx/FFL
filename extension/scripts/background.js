chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "downloadVideo",
    title: "Download This Video",
    contexts: ["video"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "downloadVideo" && info.srcUrl) {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (videoUrl) => {
        const a = document.createElement("a");
        a.href = videoUrl;
        a.download = "video.mp4";
        document.body.appendChild(a);
        a.click();
        a.remove();
      },
      args: [info.srcUrl]
    });
  }
});
