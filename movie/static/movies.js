function addMessage(text, extra_tags) {
    var message = $('<li class="' + extra_tags + '">' + text + '</li>').hide();
    $("#messages").append(message);
    message.fadeIn(500);

    setTimeout(function () {
        message.fadeOut(500, function () {
            message.remove();
        });
    }, 3000);
}

function create_tag() {
    var frm = $('#create-tag-form');
    $.ajax({
        url: frm.attr('action'),
        method: frm.attr('method'),
        data: frm.serialize(),
        dataType: 'json'
    }).done(function (json) {
        console.log(json['status']);
        console.log(json['name']);
        console.log(json['tagpk']);
        if (json.status == 'sucess') {
            $tag = $('span.label:first');
            $klon = $tag.clone(false);
            // $klon.children('.remove').attr('id', json['tagpk']);
            $klon.attr('id', json['tagpk']);
            $klon.children('.tagname').text(json['name']);

            $('div.panel-body#tags').append($klon);

            $('.panel-body').on('click',  function () {
                console.log($(this).text());
            });
        }
    })
}

function toggle_tag(movie_pk, tag_pk) {
    $.ajax({
        url: '/toggle_tag/',
        data: {'tag_pk': tag_pk, 'movie_pk': game_pk},
        dataType: 'json',
        method: 'POST',
        success: function (json) {
            if (json.status == 'sucess_add') {
                $('span.tag-toggle#' + tag_pk).removeClass('label-default').addClass('label-success');
                $.ionSound.play("water_droplet");
            } else {
                $('span.tag-toggle#' + tag_pk).removeClass('label-success').addClass('label-default');
                $.ionSound.play("water_droplet");
            }
        }
    });
}

function closeSnoAlertBox() {
    window.setTimeout(function () {
        $("#snoAlertBox").fadeOut(300)
    }, 3000);
}

$(document).ready(function () {

    // init bunch of sounds
    ion.sound({
        sounds: [
            {name: "water_droplet"}
        ],

        // main config
        path: "/static/sounds/",
        preload: true,
        multiplay: true,
        volume: 0.9
    });

    //
    // Handler for show Django's messages from ajax call
    //
    $('#messages').ajaxComplete(function (e, xhr, settings) {
        var contentType = xhr.getResponseHeader("Content-Type");

        if (contentType == "application/javascript" || contentType == "application/json") {
            var json = $.evalJSON(xhr.responseText);

            $.each(json['django_messages'], function (i, item) {
                addMessage(item.message, item.extra_tags);
            });
        }
    }).ajaxError(function (e, xhr, settings, exception) {
        addMessage("There was an error processing your request, please try again.", "error");
    });


    //
    // Handle tooltip
    //
    $("[data-toggle='tooltip']").tooltip();


    //
    // Confirmation for delete movie
    //
    $('[data-toggle="confirmation-delete-movie"]').confirmation({
        title: "Are you sure to remove?",
        placement: "right",
        singleton: "True",
        popout: "True",
        container: 'body',
        btnOkLabel: "&nbsp;Delete",
        btnOkClass: "btn-xs btn-danger",
        btnOkIcon: "glyphicon glyphicon-remove",
        btnCancelLabel: "&nbsp;Cancel",
        btnCancelIcon: "glyphicon glyphicon-repeat",
        rootSelector: '[data-toggle=confirmation-delete-movie]',
        onConfirm: function (event, element) {
            var movie_pk = $(this).attr('id');
            $.post("/delete_movie/", {movie_pk: movie_pk})
                .done(function (json) {
                    if (json['status']=='sucess') {
                        // json.redirect contains the string URL to redirect to
                        window.location.replace(json['redirect']);
                    }
                })
                .fail(function () {

                });
            $(this).confirmation('destroy');
        }
    });


    //
    // Confirmation for delete tag
    //
    $('[data-toggle="confirmation-delete-tag"]').confirmation({
        title: "Are you sure to delete tag?",
        placement: "bottom",
        singleton: "True",
        popout: "True",
        container: 'body',
        btnOkLabel: "&nbsp;Delete",
        btnOkClass: "btn-xs btn-danger",
        btnOkIcon: "glyphicon glyphicon-remove",
        btnCancelLabel: "&nbsp;Cancel",
        btnCancelIcon: "",
        rootSelector: '[data-toggle=confirmation-delete-tag]',
        onConfirm: function (event, element) {
            // var pk = $(this).attr('id'); This work if ID in I tag (in html)
            var pk = $(this).closest('.tag').attr('id');
            var tag = $(this).closest('span.label');

            $.ajax({
                url: '/delete_tag_ajax/',
                type: 'POST',
                data: {pk: pk},
                dataType: 'json'
            })
                .done(function (json) {
                    if (json['status'] == 'sucess') {
                        tag.empty();
                        $("#snoAlertBox")
                            .removeClass('alert-danger')
                            .addClass("alert-success")
                            .text('Список ' + json['name'] + ' успешно удален')
                            .fadeIn();
                    } else if (json['status'] == 'exist') {
                        $("#snoAlertBox")
                            .removeClass("alert-success")
                            .addClass("alert-danger")
                            .text('Список ' + json['name'] + ' не может быть удален - он содержит игры!')
                            .fadeIn();
                    }
                    closeSnoAlertBox();
                })
                .fail(function () {
                    // $("#snoAlertBox")
                    //     .addClass("alert-danger")
                    //     .text('Вы должны авторизироваться.')
                    //     .fadeIn();
                    // closeSnoAlertBox();
                    alert('fail')
                });

            $(this).confirmation('destroy');
        }
    });

});


