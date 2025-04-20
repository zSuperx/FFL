// const endpoint = "https://immortal-hot-cat.ngrok-free.app/"

// function openSocket() {
// 	console.log("In openSocket")
// 	var socket = io.connect(endpoint+'process');
// 	console.log(socket)
// }

function send(url) {
	chrome.runtime.sendMessage({ type: "send", data: url });
}

document.addEventListener("DOMContentLoaded", () => {
	const scanButton = document.getElementById("scanButton");
	const message = document.getElementById("message");

	chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
		const currentUrl = tabs[0]?.url || "";
		const isYouTube = currentUrl.includes("youtube.com/watch");

		if (isYouTube) {
			scanButton.disabled = false;
			message.textContent = "";
		} else {
			scanButton.disabled = true;
			message.textContent = "Navigate to a YouTube video to use this extension!";
		}

		scanButton.addEventListener("click", () => {
			if (currentUrl) {
				navigator.clipboard.writeText(currentUrl)
				send(currentUrl)
			} else {
				alert("Unable to get tab URL.");
			}
		});
	});
});
