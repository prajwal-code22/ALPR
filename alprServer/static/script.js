const previewImage = document.getElementById("previewImage");
const previewVideo = document.getElementById("previewVideo");
const fileInfo = document.getElementById("fileInfo");
const form = document.forms["loaderform"];

const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

// Handling videos frames
let si;
function processFrame() {

    si = setInterval(() => {
        canvas.width = previewVideo.videoWidth;
        canvas.height = previewVideo.videoHeight;
        ctx.drawImage(previewVideo, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            sendImage(blob);
        }, "image/jpeg");

    }, 1000 / 2);
}

// Handling uploaded video
previewVideo.onplay = (e) => {
    processFrame();
}

previewVideo.onpause = (e) => {
    clearInterval(si);
}

// Handling live capture
function liveCapture() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            previewVideo.classList.remove("hidden")
            previewVideo.autoplay = true;
            previewVideo.srcObject = stream;
            processFrame();
        });
}

function sendImage(imageBlob) {
    const formdata = new FormData(form);
    formdata.append("image", imageBlob, "img.jpg")
    // formdata.append("csrfmiddlewaretoken", form['csrfmiddlewaretoken'].value);

    fetch(form.action, {
        method: form.method,
        body: formdata
    })
}

function loadFile(event, type) {
    const file = event.target.files[0];
    if (!file) return;

    const fileURL = URL.createObjectURL(file);

    if (type === "image") {
        previewImage.src = fileURL;
        previewImage.classList.remove("hidden");
        previewVideo.classList.add("hidden");
    } else if (type === "video") {
        previewVideo.src = fileURL;
        previewVideo.play();
        previewVideo.classList.remove("hidden");
        previewImage.classList.add("hidden");
    }

    fileInfo.innerHTML = `<p>Name: ${file.name}</p><p>Path: ${file.name}</p>`;
}
// Setting location

const locationSpan = document.querySelector(".location");
let lag, long;

navigator.geolocation.getCurrentPosition((position) => {
    lat = position.coords.latitude;
    long = position.coords.longitude;

    locationSpan.innerText = lat + ", " + long;

    document.querySelector("#long").value = long;
    document.querySelector("#lat").value = lat;

});


// Websocket

const socket = new WebSocket("ws://localhost:8000");

socket.onopen = e => console.log("Connected")
socket.onerror = e => console.log("Error", e)

socket.onmessage = (e) => {
    const jsonData = JSON.parse(e.data);
    const nums = jsonData.numbers;
    for (const num of nums) {
        addNumber(num)
    }

}

const recognizedNumDiv = document.querySelector(".settings-panel");
function addNumber(num) {
    recognizedNumDiv.innerHTML += `<p> ${num} </p>`
}

// Handling form
form.onsubmit = (e) => {
    e.preventDefault();

    const fd = new FormData(form);

    fetch(form.action, {
        method: form.method,
        body: fd
    })

}