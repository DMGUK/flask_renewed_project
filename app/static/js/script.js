$('#postCarousel').on('slide.bs.carousel', function (e) {
    var $e = $(e.relatedTarget);
    var idx = $e.index();
    var itemsPerSlide = 1;
    var totalItems = $('.carousel-item').length;

    if (idx >= totalItems - (itemsPerSlide - 1)) {
        var it = itemsPerSlide - (totalItems - idx);
        for (var i = 0; i < it; i++) {
            $.get('/api/posts/' + (idx + i), function (data) {
                var newPost = $('<div class="carousel-item"><div class="card" style="width: 18rem;"><div class="card-body"><img class="post-image" style="margin-left: -100px;" src="' + data.image_url + '" width="450px" height="400px"><h4 style="font-size: 32px;" class="card-title"><a class="postAnchor" href="/view_post/' + data.id + '">' + data.title + '</a></h4><h5 style="font-size: 32px;" class="post-type">' + data.type + '</h5><p style="font-size: 28px;" class="card-text">By <span class="post-author">' + data.username + '</span></p></div></div></div>');
                $('#postCarousel .carousel-inner').append(newPost);
            });
        }
    }
});

document.getElementById("{{ update_account_form.image.id }}").addEventListener("change", function() {
    var fileName = this.files[0] ? this.files[0].name : "No file chosen";
    document.getElementById("{{ update_account_form.image.id }}-filename").innerText = fileName;
});