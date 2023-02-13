document.getElementById("download-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var url = document.getElementById("url-input").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/download_audio");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.responseType = "blob";
    xhr.onload = function() {
        if (xhr.status === 200) {
            var blob = xhr.response;
            var a = document.createElement("a");
            a.style = "display: none";
            document.body.appendChild(a);
            var url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = "audio.mp3";
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert("Error: " + xhr.statusText);
        }
    };
    xhr.send("url=" + encodeURIComponent(url));
});