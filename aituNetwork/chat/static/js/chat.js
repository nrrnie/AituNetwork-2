let socket = io.connect('http://' + window.location.host, {query: "user_id=" + current_user});

socket.on('message', data => {
    add_message(data['from_user_id'], data['message'])
});

$('document').ready(function () {
    $('#sendMessage').on('click', function () {
        let message_text_element = $('#messageText');
        let message = message_text_element.val();
        message_text_element.val('');
        add_message(current_user, message);

        socket.emit('message', {
            chat_id: chat_id,
            from_user_id: current_user,
            user_id: chat_user,
            message_text: message
        })
    });

    $('#messageText').on('input', function () {
        if (this.scrollHeight <= 156) {
            this.style.height = "";
            this.style.height = this.scrollHeight + "px";
        }
    })


})

function add_message(user_id, message) {
    $.ajax({
        url: '/utils/generate-message',
        method: 'POST',
        data: {
            user_id: user_id,
            message: message
        },
        success: function (data) {
            $('#dialogBox').prepend(data);
        }
    })

}