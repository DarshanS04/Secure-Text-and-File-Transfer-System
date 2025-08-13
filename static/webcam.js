function captureWebcam() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const fileInput = document.getElementById('face_image');
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Webcam not supported');
        return;
    }
    video.style.display = 'block';
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            video.onloadedmetadata = () => {
                setTimeout(() => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    canvas.toBlob(blob => {
                        const file = new File([blob], 'webcam.jpg', { type: 'image/jpeg' });
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(file);
                        fileInput.files = dataTransfer.files;
                        stream.getTracks().forEach(track => track.stop());
                        video.style.display = 'none';
                    }, 'image/jpeg');
                }, 1500);
            };
        })
        .catch(() => alert('Unable to access webcam'));
}
