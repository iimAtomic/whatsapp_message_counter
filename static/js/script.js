$(document).ready(function() {
    // Toggle menu visibility
    $('#menuToggle').click(function() {
        $('#navbarLinks').toggleClass('show');
    });

    // Form submission handler
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                openModal(data.image_url);
            },
            error: function() {
                alert('Error handling the file.');
            }
        });
    });

    // Open and close modal
    function openModal(imageUrl) {
        var modal = document.getElementById('resultModal');
        var img = document.getElementById('resultImage');
        var span = document.getElementsByClassName("close")[0];
        var downloadButton = document.getElementById('downloadButton');

        img.src = imageUrl;
        downloadButton.onclick = function() {
            // Créer un lien temporaire pour télécharger l'image
            var link = document.createElement('a');
            link.href = imageUrl;
            link.download = imageUrl.split('/').pop(); // Nom de fichier pour le téléchargement
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };
        modal.style.display = "block";

        span.onclick = function() {
            closeModal();
        }

        window.onclick = function(event) {
            if (event.target === modal) {
                closeModal();
            }
        }
    }

    function closeModal() {
        // Close modal
        const modal = document.getElementById('resultModal');
        modal.style.display = 'none';

        // Reset the form
        const form = document.getElementById('uploadForm');
        form.reset();
    }
});
