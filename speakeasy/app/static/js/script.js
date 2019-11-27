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