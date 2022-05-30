function load_messages(offset, limit) {
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
        }
    });
}

load_messages(0, 10);