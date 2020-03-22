let last_state = null;

hotkeys.filter = function(event){
  var tagName = (event.target || event.srcElement).tagName;
  hotkeys.setScope(/^(INPUT|TEXTAREA|SELECT)$/.test(tagName) ? 'input' : 'other');
  return true;
}

hotkeys('alt+shift+z, alt+shift+x, alt+shift+c, alt+shift+v, alt+shift+b, alt+z, alt+x, alt+c, alt+u, alt+i, alt+o, enter, space', function (e, handler) {
	switch (handler.key) {
		case 'alt+shift+z':
			e.preventDefault();
			switchKeyboardNull(0);
			break;
		case 'alt+shift+x':
			e.preventDefault();
			switchKeyboardNull(1);
			break;
		case 'alt+shift+c': 
			e.preventDefault();
			switchKeyboardNull(2);
			break;
		case 'alt+shift+v': 
			e.preventDefault();
			switchKeyboardNull(4);
			break;
		case 'alt+shift+b': 
			e.preventDefault();
			switchKeyboardNull(5);
			break;
		case 'alt+z': 
			e.preventDefault();
			insert(0, getActivePhrase(0));
			break;
		case 'alt+x':
			e.preventDefault();
			insert(1, getActivePhrase(1));
			break;
		case 'alt+c':
			e.preventDefault();
			insert(2, getActivePhrase(2));
			break;
		case 'alt+u':
			e.preventDefault();
			insert(0, getSuggestedWord(0));
			break;
		case 'alt+i':
			e.preventDefault();
			insert(1, getSuggestedWord(1));
			break;
		case 'alt+o':
			e.preventDefault();
			insert(0, getSuggestedWord(2));
			break;
		case 'enter':
			e.preventDefault();
			play_mp3(e.target.value);
			break;
		case 'space':
			if (last_state != e.target.value.trim()) {
				let words = e.target.value.trim().split(".");
				let user_word = words[words.length - 1];
				update_suggested_words(user_word);
				last_state = e.target.value.trim();
			}
			break;
		default: console.log("charrr"); last_key_was_space = false;
	}
});

function switchKeyboardNull(i) {
	if (document.getElementById("keyboard" + i))
		switchKeyboard(i);
}

function getSuggestedWord(i) {
	return document.getElementById("suggest" + String(i + 1)).textContent;
}

function getActivePhrase(i) {
	let keyboard_id = document.getElementsByClassName("active")[0].id; //Assuming no more actives
	let keyboard_i = Number(keyboard_id[keyboard_id.length - 1]); //keyboards.length <= 5
	let keyboard = document.getElementById("keyboard" + keyboard_i);
	let phrase_elements = keyboard.getElementsByClassName("phrase");
	let phrase = phrase_elements[i].innerHTML;
	return phrase;
}

function insert(i, phrase) {
	let old_text = document.getElementById("speech_text_input").value;
	let new_text;
	if (old_text.length > 0) {
		new_text = old_text.trim() + " " + phrase;
	} else {
		new_text = phrase;
	}
	document.getElementById("speech_text_input").value = new_text;
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
		window.audio.playbackRate = audio_speed;
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
		body: JSON.stringify({"user_words": word})
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
