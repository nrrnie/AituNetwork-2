$('document').ready(function () {
    $('#sendMessage').on('click', function () {
        let message_text_element = $('#messageText');
        let message = message_text_element.val();
        message_text_element.val('');
        add_message(message);
    });

    $('#messageText').on('input', function () {
        if (this.scrollHeight <= 156) {
            this.style.height = "";
            this.style.height = this.scrollHeight + "px";
        }
    })

    function add_message(message) {
        $.ajax({
            url: '/utils/generate-message',
            method: 'POST',
            data: {
                user_id: 7,
                message: message
            },
            success: function(data) {
                $('#dialogBox').prepend(data);
            }
        })

    }
})


