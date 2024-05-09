$(document).ready(function() {
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
});

function openModal(imageUrl) {
    var modal = document.getElementById('resultModal');
    var img = document.getElementById('resultImage');
    var span = document.getElementsByClassName("close")[0];

    img.src = imageUrl;
    modal.style.display = "block";

    span.onclick = function() {
        modal.style.display = "none";
        document.body.classList.remove('blurred');
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
            document.body.classList.remove('blurred');
        }
    }

    // document.body.classList.add('blurred');
}

function shareOnWhatsApp() {
    var imgSrc = document.getElementById('resultImage').src;
    var whatsappUrl = `https://wa.me/?text=Check out this message! ${encodeURIComponent(imgSrc)}`;
    window.open(whatsappUrl, '_blank');
}
