bootstrap_alert = function () {};

bootstrap_alert.show = function (message, style, timeout) {
    console.log('bootstrap_alert.show');
    $('<div id="floating_alert" \
            class="alert alert-' + style + ' role="alert"> \
          <button type="button" class="close" data-dismiss="alert" aria-label="Close"> \
              <span aria-hidden="true">&times;</span> \
          </button> \
    ' + message + '&nbsp;&nbsp;</div>').appendTo('body');

    setTimeout(function () {
        $(".alert").alert('close');
    }, timeout);
};