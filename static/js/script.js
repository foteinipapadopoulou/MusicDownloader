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
            let disposition = xhr.getResponseHeader("Content-Disposition")
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                   var filename = matches[1].replace(/['"]/g, '');
                }
            }
            var a = document.createElement("a");
            a.style = "display: none";
            document.body.appendChild(a);
            var url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = filename;
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert("Error: " + xhr.statusText);
        }
    };
    xhr.send("url=" + encodeURIComponent(url));
});