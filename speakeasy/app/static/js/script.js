//let button = document.getElementById("speech_text_button");
//button.addEventListener("click", click_handler);
window.addEventListener('keydown', windowKeydownHandler, true);
let last_key_was_space = false;

function windowKeydownHandler(e) {
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        if (e.target.id == "speech_text_input") {
            play_mp3(e.target.value);
        }
    } else if (e.keyCode == 32) {
		if (e.target.id == "speech_text_input") {
			if (!last_key_was_space) {
				//The way I deal with symbols and whitespace depends on /suggest spec.
				let words = e.target.value.split(" ");
				let user_word = words[words.length - 1];
				update_suggested_words(user_word);
				last_key_was_space = true;
			}
		}
    } else {
		last_key_was_space = false;
	}
}

function click_handler(e) {
    let input_text = document.getElementById("speech_text_input");
    play_mp3(input_text.value);
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
        alert("Error: Could not receive the speech audio.");
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

function update_suggested_words(user_word) {
	get_suggested_words(user_word)
	.then((suggested_words) => display_words(suggested_words))
	.catch((error) => alert("Error: Could not receive suggested words."));
}

async function get_suggested_words(word) {
	let response = await fetch("/suggest", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({"user_word": word})
	});
	return (await response.json())["suggested_words"];
}

function display_words(words) {
	/* This function is to be used for displaying new words and showing
	 * the transition of them becoming ones. Code within the block can be
	 * removed without consequences. */
	for (let i = 1; i <= 3; i++) {
		let span = document.getElementById("suggest" + String(i));
		span.textContent = words[i - 1];
	}
}
