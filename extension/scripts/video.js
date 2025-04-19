// Add right-click download option for videos
document.querySelectorAll("video").forEach(video => {
  video.addEventListener("contextmenu", event => {
    event.preventDefault();

    // Remove any existing custom menu
    document.querySelectorAll(".custom-context-menu").forEach(el => el.remove());

    const menu = document.createElement("div");
    menu.textContent = "⬇️ Download Video";
    menu.className = "custom-context-menu";
    menu.style.position = "absolute";
    menu.style.top = `${event.clientY}px`;
    menu.style.left = `${event.clientX}px`;
    menu.style.background = "#fff";
    menu.style.border = "1px solid #ccc";
    menu.style.padding = "8px";
    menu.style.cursor = "pointer";
    menu.style.zIndex = 10000;
    menu.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
    menu.style.borderRadius = "4px";

    menu.addEventListener("click", () => {
      const videoSrc = video.currentSrc || video.src;
      if (videoSrc) {
        const a = document.createElement("a");
        a.href = videoSrc;
        a.download = "video.mp4";
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
      menu.remove();
    });

    document.body.appendChild(menu);

    // Remove menu on click elsewhere
    document.addEventListener("click", () => {
      menu.remove();
    }, { once: true });
  });
});
