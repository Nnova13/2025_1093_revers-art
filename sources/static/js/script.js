const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const imagePreview = document.getElementById('imagePreview');

fileInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
        fileName.textContent = `Fichier sélectionné : ${this.files[0].name}`;
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(this.files[0]);
    } else {
        fileName.textContent = "Aucun fichier sélectionné";
        imagePreview.style.display = 'none';
    }
});