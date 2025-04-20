// var socket = null

// if (window.location.href.includes("youtube.com/watch")) {
// 	chrome.tabs.sendMessage(tabs[0].id, { action: "received", data: "123" })

// 	// socket = new WebSocket("wss://bobcat-close-finch.ngrok-free.app/ws");
// 	// socket = new WebSocket("wss://immortal-hot-cat.ngrok-free.app/ws");
// }

// socket.onmessage = (event) => {
// 	console.log("📩 Received from server:", event.data);
// 	// alert(event.data)
	
// 	chrome.runtime.sendMessage({ type: "received", data: event.data })
// };

// socket.onclose = () => {
// 	console.log("❌ WebSocket disconnected");
// };

function send_video_url(input) {
	const message = {
		event: "process-video",
		data: { url: input, type: "youtube" }
	};
	socket.send(JSON.stringify(message));
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	console.log("Listener received message")
	console.log(message)

	alert("Listener received message of type "+message.type)
	// if (message.type === "send") {
	// 	alert("Autoscan received send: "+message.data)
	// 	if (socket.readyState === WebSocket.OPEN) {
	// 		send_video_url(message.data)
	// 	} else {
	// 		alert('[BG] WebSocket not open');
	// 	}
	// }

	sendResponse({ status: "ok" });
});


// socket.onopen = () => {
// 	console.log("✅ WebSocket connected");
	
// 	if (window.location.href.includes("youtube.com/watch")) {
// 		console.log(window.location.href)
// 		send_video_url(window.location.href)
// 	//   navigator.clipboard.writeText(window.location.href).catch((err) => {
// 	// 	console.error("Failed to copy URL to clipboard:", err);
// 	//   });
// 	}
	
// };