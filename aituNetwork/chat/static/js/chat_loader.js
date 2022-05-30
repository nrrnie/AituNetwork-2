let last_offset = 0
load_messages(last_offset, 25);

function load_messages(offset, limit) {
    console.log('loading');
    $.ajax({
        url: '/utils/get-messages',
        method: 'POST',
        data: {
            chat_id: chat_id,
            offset: offset,
            limit: limit,
            with_html: true
        },
        success: function (data) {
            let html = data.html;
            html.forEach(message => $('#dialogBox').append(message));
            last_offset += html.length;
        }
    });
}


$('#dialogBox').scroll(function () {
    let div = $(this).get(0);
    let position = div.scrollTop * -1;

    if(position + div.clientHeight >= div.scrollHeight) {
        load_messages(last_offset, 25);
    }
});
