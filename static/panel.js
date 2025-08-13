document.addEventListener('DOMContentLoaded', function() {
    const dragDropArea = document.getElementById('dragDropArea');
    const fileInput = document.getElementById('file');
    const fileName = document.getElementById('fileName');
    if (dragDropArea && fileInput) {
        dragDropArea.addEventListener('click', () => fileInput.click());
        dragDropArea.addEventListener('dragover', e => {
            e.preventDefault();
            dragDropArea.classList.add('dragover');
        });
        dragDropArea.addEventListener('dragleave', e => {
            e.preventDefault();
            dragDropArea.classList.remove('dragover');
        });
        dragDropArea.addEventListener('drop', e => {
            e.preventDefault();
            dragDropArea.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                fileName.textContent = fileInput.files[0]?.name || '';
            }
        });
        fileInput.addEventListener('change', function() {
            fileName.textContent = fileInput.files[0]?.name || '';
        });
    }
});
function generateKey() {
    fetch('https://www.random.org/cgi-bin/randbyte?nbytes=32&format=h')
        .then(r => r.text())
        .then(hex => {
            const arr = hex.trim().split(/\s+/).map(h => parseInt(h, 16));
            const key = btoa(String.fromCharCode.apply(null, arr));
            document.getElementById('key').value = key;
        })
        .catch(() => {
            // fallback to local random
            const arr = new Uint8Array(32);
            window.crypto.getRandomValues(arr);
            const key = btoa(String.fromCharCode.apply(null, arr));
            document.getElementById('key').value = key;
        });
}
function toggleMode() {
    const mode = document.getElementById('mode').value;
    document.getElementById('encDataInput').style.display = (mode === 'decrypt') ? 'block' : 'none';
}
function toggleType() {
    const type = document.getElementById('type').value;
    document.getElementById('textInput').style.display = (type === 'text') ? 'block' : 'none';
    document.getElementById('fileInput').style.display = (type === 'file') ? 'block' : 'none';
    const fileInput = document.getElementById('file');
    if (type === 'file') {
        fileInput.required = true;
    } else {
        fileInput.required = false;
    }
}
