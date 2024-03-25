const downloadForm = document.getElementById("download-form");
const urlInput = document.getElementById("url-input")
const progressElement =  document.querySelector('.progress-group');
const formGroupElement =  document.querySelector('.form-group');
const successMessage = document.querySelector('#successMessage');
const failureMessage = document.querySelector('#failureMessage');
const progressBar = document.querySelector('#progressBar');
const songTitleToBeDownloadedWrapper = document.querySelector('.songTitleToBeDownloaded-wrapper');
const songTitleToBeDownloaded = document.querySelector('#songTitleToBeDownloaded');
const DEFAULT_SONG_TITLE = "audio.mp3";

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

function showFailureMessage(){
    successMessage.classList.add('d-none');
    progressElement.classList.add('d-none');
    failureMessage.classList.remove('d-none');
}

function hideMessages(){
    successMessage.classList.add("d-none");
    failureMessage.classList.add("d-none");
}

function showInvalidUrlInputPrompt(){
    urlInput.classList.remove('is-valid');
    urlInput.classList.add('is-invalid');
    formGroupElement.classList.remove('has-success');
    formGroupElement.classList.add('has-danger');
}
function showValidUrlInputPrompt(){
    urlInput.classList.remove('is-invalid');
    urlInput.classList.add('is-valid');
    formGroupElement.classList.remove('has-danger');
    formGroupElement.classList.add('has-success');
}
//Download Button
downloadForm.addEventListener("submit", function(event) {
    event.preventDefault();
    //Hide any previous message
    hideMessages();
    if(isInvalidOrEmptyUrl()){
        showInvalidUrlInputPrompt();
        return;
    } else {
        showValidUrlInputPrompt();
    }
    let url = urlInput.value.trim();
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/download_audio");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.responseType = "blob";
    xhr.timeout = 20000;

    xhr.addEventListener('load', function (e) {
         progressElement.classList.add('d-none');
         if (xhr.status === 200){
             let blob = xhr.response;
             successMessage.classList.remove('d-none');
             //Get the title of song
             let disposition = xhr.getResponseHeader("Content-Disposition");
             let songName = DEFAULT_SONG_TITLE;
             if (songTitleToBeDownloaded.textContent) {
                 songName = `${songTitleToBeDownloaded.textContent}.mp3`;
             } else {
                 songName = getAttachmentFilenameFromDisposition(disposition);
             }
             createAndClickATagElement(blob, songName);
         }  else if (xhr.status === 400) {
            showInvalidUrlInputPrompt();
         }  else {
             showFailureMessage();
        }
    });

    xhr.addEventListener('error', function (e) {
        showFailureMessage();
    });
    xhr.addEventListener('abort', function (e) {
        showFailureMessage();
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

urlInput.addEventListener('keyup', function(e){
    const xhr = new XMLHttpRequest();
    if(isInvalidOrEmptyUrl()){
        showInvalidUrlInputPrompt();
        return;
    } else {
        showValidUrlInputPrompt();
    }
    songTitleToBeDownloadedWrapper.classList.add("d-none");

      xhr.open('GET', `/get_audio?url=${e.target.value.trim()}`, true);

      xhr.addEventListener('load', function(e) {
          if (xhr.status === 200){
              const response = JSON.parse(xhr.responseText);
              songTitleToBeDownloaded.textContent = response.title;
              songTitleToBeDownloadedWrapper.classList.remove("d-none");
          } else if (xhr.status === 400) {
            showInvalidUrlInputPrompt();
        }
      });

      xhr.send();
})

function isInvalidOrEmptyUrl(){
     return !urlInput.value || !urlInput.checkValidity();
}