function addMessage(text, extra_tags) {
    let message = $('<li class="alert alert-fadeout alert-' + extra_tags + '">' + text + '</li>').hide();
    $("#messages").append(message);
    message.fadeIn(1000); // время 'проявления' алерта

    setTimeout(function (time) {
        message.fadeOut(1000, function () {  // время 'исчезновения' алерта
            message.remove();
        });
    }, 3000);  // время 'показа' алерта
}