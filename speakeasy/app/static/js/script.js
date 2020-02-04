let button = document.getElementById("speech_text_button");
button.addEventListener("click", handler);
window.addEventListener('keydown', windowKeydownHandler, true);
let clicks = 0;

function windowKeydownHandler(e) {
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        if (e.target.nodeName == 'TEXTAREA' && e.target.type == 'textarea' && e.target.id == "speech_text_input") {
            e.preventDefault();
            play_mp3(e.target.value);
            return false;
        }
    } else if (e.keyCode == 32) {
		if (e.target.id == "speech_text_input") {
			//There should be much more checks in order to determine whether to send
			let words = e.target.value.split(" ");
			let word = words[words.length - 1];
			update_suggested_words(word);
			return false;
		}
    }
}

function handler(e) {
    let input_text = document.getElementById("speech_text_input");
    play_mp3(input_text.value);
    return false;
}

function play_mp3(val) {
    get_mp3(val)
    .then((blob) => {
        let url = window.URL.createObjectURL(blob)
        window.audio = new Audio();
        window.audio.src = url;
        window.audio.play();
    })
    .catch((error) => {
        alert("Some error occured");
    });
}

async function get_mp3(val) {
    let payload = new FormData();
    payload.append("speech_text", val);
    let response = await fetch("/speak", {
        method: "POST",
        headers: {
            "Content-Type": 'application/json'
        },
        body: JSON.stringify({"speech_text": val})
    });
    return await response.blob();
}

function update_suggested_words(word) {
	get_suggested_words(word)
	.then((wordsJSON) => {
		let words = wordsJSON["suggested_words"];
		display_words(words);
	})
	.catch((error) => alert("Some other error occured"));
}

function display_words(words) {
	for (let i = 1; i <= 3; i++) {
		let span = document.getElementById("suggest" + String(i));
		span.textContent = words[i - 1];
	}
}

async function get_suggested_words(word) {
	let response = await fetch("/suggest", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({"user_word": word})
	});
	return await response.json();
}
