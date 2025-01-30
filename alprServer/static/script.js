function loadFile(event, type) {
    const file = event.target.files[0];
    console.log(file, type);
    if (!file) return;

    const previewImage = document.getElementById("previewImage");
    const previewVideo = document.getElementById("previewVideo");
    const fileInfo = document.getElementById("fileInfo");

    const fileURL = URL.createObjectURL(file);

    if (type === "image") {
        previewImage.src = fileURL;
        previewImage.classList.remove("hidden");
        previewVideo.classList.add("hidden");
    } else if (type === "video") {
        previewVideo.src = fileURL;
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

});
