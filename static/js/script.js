const downloadForm = document.getElementById("download-form");
const urlInput = document.getElementById("url-input")
const progressElement =  document.querySelector('.progress-group');
const successMessage = document.querySelector('#successMessage');
const failureMessage = document.querySelector('#failureMessage');
const progressBar = document.querySelector('#progressBar');
const songTitleToBeDownloaded = document.querySelector('#songTitleToBeDownloaded');

function getAttachmentFilenameFromDisposition (disposition){
    if (disposition && disposition.indexOf('attachment') !== -1) {
        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        let matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
           return matches[1].replace(/['"]/g, '');
        }
    }
    return "audio.mp3"
}

/*
*  Creating an "a" element without displaying it
*   with href the blob response and download name the filename
*   and finally clicking it
* */
function createAndClickATagElement(blob, filename){
    let a = document.createElement("a");
    a.classList.add("d-none");
    document.body.appendChild(a);
    let url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

//Download Button
downloadForm.addEventListener("submit", function(event) {
    event.preventDefault();
    //Hide any previous message
    successMessage.classList.add("d-none");
    failureMessage.classList.add("d-none");

    let url = urlInput.value;
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/download_audio");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.responseType = "blob";

    xhr.addEventListener('load', function (e) {
         progressElement.classList.add('d-none');
         if (xhr.status === 200){
             let blob = xhr.response;
             successMessage.classList.remove('d-none');
             //Get the title of song
             let disposition = xhr.getResponseHeader("Content-Disposition")
             let songName = getAttachmentFilenameFromDisposition(disposition)
             createAndClickATagElement(blob, songName);
         } else {
             progressElement.classList.add('d-none');
            failureMessage.classList.remove('d-none');
        }
    });


    //Add the progress bar
    progressElement.classList.remove('d-none');
    progressBar.style.width = '10%';

    xhr.addEventListener('progress', function(e) {
      const percent = (e.loaded / e.total) * 100;
      progressBar.style.width = percent + '%';
    });

    xhr.send("url=" + encodeURIComponent(url));
});

urlInput.addEventListener('input', function(e){
    const xhr = new XMLHttpRequest();

      xhr.open('GET', `/get_audio?url=${e.target.value}`, true);

      xhr.addEventListener('load', function(e) {
          if (xhr.status === 200){
              const response = JSON.parse(xhr.responseText);
              songTitleToBeDownloaded.textContent = response.title;
          }
      });

      xhr.send();
})