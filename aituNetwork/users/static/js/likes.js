$('.like').on('click', function () {
    let post = $(this).parent().parent().parent();
    let like_count_element = $(this).find('.like-count');
    let heart = $(this).find('svg');

    console.log(post.attr('class').search('likedasd'))

    if (post.attr('class').search('liked') === -1) {
        like(post, like_count_element, heart);
    } else {
        unlike(post, like_count_element, heart);
    }
})

function like(post, like_count_element, heart) {
    let post_id = post.attr('id').replace('post-', '');

    $.ajax({
        url: '/utils/like',
        method: 'POST',
        data: {
            'post-id': post_id,
            'user-id': current_user
        }
    });

    // increase like count
    let like_count = like_count_element.text();
    like_count_element.text(parseInt(like_count) + 1);

    // color heart
    heart.attr('style', 'filter: invert(25%) sepia(94%) saturate(1682%) hue-rotate(333deg) brightness(95%) contrast(88%);');

    // add `liked` class to post
    post.addClass('liked');
}

function unlike(post, like_count_element, heart) {
    let post_id = post.attr('id').replace('post-', '');

    $.ajax({
        url: '/utils/unlike',
        method: 'POST',
        data: {
            'post-id': post_id,
            'user-id': current_user
        }
    });

    // increase like count
    let like_count = like_count_element.text();
    like_count_element.text(parseInt(like_count) - 1);

    // color heart
    heart.attr('style', '');

    post.removeClass('liked');
}