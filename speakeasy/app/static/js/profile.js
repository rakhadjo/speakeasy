function outputUpdate(speed) {
    document.querySelector('#selected-age').value = Math.trunc(speed);
}

function updateKeyboards() {
	let keyboards = [];
	let keyboard_elements = document.getElementsByClassName("keyboardsetting show");
	for (let i = 0; i < keyboard_elements.length; i++) {
		let k = [];
		k.push(document.getElementById("keyboardicon" + i).innerHTML);
		let phrases = [];
		for (let j = 0; j < 3; j++) {
			phrases.push(document.getElementById("phrasesetting" + i + j).value);
		}
		k.push(phrases);
		keyboards.push(k);
	}
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
	console.log(response);
}
