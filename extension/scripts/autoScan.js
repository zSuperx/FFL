if (window.location.href.includes("youtube.com/watch")) {
  navigator.clipboard.writeText(window.location.href).catch((err) => {
    console.error("Failed to copy URL to clipboard:", err);
  });
}
