function outputUpdate(speed) {
    document.querySelector('#selected-age').value = Math.trunc(speed);
}

function updateKeyboards() {
	let keyboards;
	sendKeyboards(keyboards)
	.then((response) => display_response(response))
	.catch((error) => alert("Error: could not connect to database"))
}

async function sendKeyboards(keyboards) {
	let response = await fetch("/updateKeyboards", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(keyboards)
	});
	return await response.json();
}

function display_response(response) {
}
