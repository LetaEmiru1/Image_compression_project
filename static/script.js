document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const progressBar = document.querySelector('.progress-bar');
    const progressContainer = document.querySelector('.progress');
    const alertBox = document.querySelector('.alert');
    const outputImage = document.getElementById('outputImage');
    const downloadLink = document.getElementById('downloadLink');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const imageReceivedAlert = document.getElementById('imageReceivedAlert');
    const fileInput = document.getElementById('imageInput');
    const cardBody = document.querySelector('.card-body');
    
    // Clear previous file size messages
    const previousFileSizeMessages = cardBody.querySelectorAll('.file-size');
    previousFileSizeMessages.forEach(element => element.remove());

    const fileSizeBefore = document.createElement('p');
    fileSizeBefore.classList.add('file-size');
    const fileSizeAfter = document.createElement('p');
    fileSizeAfter.classList.add('file-size');

    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressBar.setAttribute('aria-valuenow', 0);
    loadingSpinner.style.display = 'block';
    imageReceivedAlert.style.display = 'block';

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        fileSizeBefore.textContent = `Original Size: ${(file.size / 1024).toFixed(2)} KB`;
        cardBody.appendChild(fileSizeBefore);
    }

    fetch('/compress', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        const contentLength = response.headers.get('Content-Length');
        const reader = response.body.getReader();

        return new Response(
            new ReadableStream({
                start(controller) {
                    let bytesReceived = 0;

                    function pump() {
                        reader.read().then(({ done, value }) => {
                            if (done) {
                                controller.close();
                                return;
                            }

                            bytesReceived += value.length;
                            progressBar.style.width = `${(bytesReceived / contentLength) * 100}%`;
                            progressBar.setAttribute('aria-valuenow', (bytesReceived / contentLength) * 100);

                            controller.enqueue(value);
                            pump();
                        });
                    }

                    pump();
                }
            })
        ).blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        outputImage.src = url;
        outputImage.style.display = 'block';
        downloadLink.href = url;
        downloadLink.style.display = 'block';
        alertBox.style.display = 'none';
        loadingSpinner.style.display = 'none';
        
        const compressedFileSize = new Blob([blob]).size;
        fileSizeAfter.textContent = `Compressed Size: ${(compressedFileSize / 1024).toFixed(2)} KB`;
        cardBody.appendChild(fileSizeAfter);
    })
    .catch(error => {
        alertBox.innerHTML = `<strong>Error:</strong> ${error.message}`;
        alertBox.style.display = 'block';
        outputImage.style.display = 'none';
        downloadLink.style.display = 'none';
        loadingSpinner.style.display = 'none';
        imageReceivedAlert.style.display = 'none';
    })
    .finally(() => {
        progressContainer.style.display = 'none';
    });
});

