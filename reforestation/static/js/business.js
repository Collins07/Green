$(document).ready(function() {
    $('.like-button').click(function() {
      var post_id = $(this).data('post-id');
      $.ajax({
        url: '{% url "post_like_ajax" %}',
        data: { 'post_id': post_id },
        method: 'POST',
        success: function(response) {
          if (response.result == 'liked') {
            $('.like-button[data-post-id=' + post_id + ']').addClass('liked');
          } else {
            $('.like-button[data-post-id=' + post_id + ']').removeClass('liked');
          }
        }
      });
    });
  });
  