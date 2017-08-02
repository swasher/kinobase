function addMessage(text, extra_tags) {
    var message = $('<li class="alert alert-' + extra_tags + '">' + text + '</li>').hide();
    $("#messages").append(message);
    message.fadeIn(1000);

    setTimeout(function () {
        message.fadeOut(500, function () {
            message.remove();
        });
    }, 300);
}

function closeSnoAlertBox() {
    window.setTimeout(function () {
        $("#snoAlertBox").fadeOut(300)
    }, 3000);
}

function create_tag() {
    var frm = $('#create-tag-form');
    var skelet = "";
    skelet += "<span id=\"\" class=\"badge badge-default badge px-2\">";
    skelet += "<span class=\"tagname\"><\/span>";
    skelet += "<a href=\"#\" tabindex=\"-1\">";
    skelet += "   <i data-tag-pk=\"\"";
    skelet += "      data-tag-name=\"\"";
    skelet += "      class=\"jqueryconfirm fa fa-times\" aria-hidden=\"true\"><\/i>";
    skelet += "<\/a>";
    skelet += "<\/span>";
    newtag = $(skelet);

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

            $(newtag).attr('id', json['tagpk']);
            $(newtag).children('.tagname').text(json['name'] + ' [0]');
            $(newtag).find("i").attr("data-tag-pk", json['tagpk']);
            $(newtag).find("i").attr("data-tag-name", json['name']);

            if ($('h4.card-title').length) {
                // $skelet.removeAttr('hidden');
                $('h4.card-title').attr({'hidden': 'True'});
                $('div.card-block').append(newtag);
            } else {
                console.log('This is not first tag');
                $('div.card-block').append(newtag);
            }

            $('.panel-body').on('click',  function () {
                console.log($(this).text());
            });
        }
    })
}

function toggle_tag_ajax(movie_pk, tag_pk) {
    $.ajax({
        url: '/toggle_tag_ajax/',
        data: {'movie_pk': movie_pk, 'tag_pk': tag_pk},
        dataType: 'json',
        method: 'POST',
        success: function (json) {
            if (json.status == 'sucess_add') {
                $('span.tag-toggle#' + tag_pk).removeClass('badge-default').addClass('badge-success');
                $.ionSound.play("water_droplet");
            } else {
                $('span.tag-toggle#' + tag_pk).removeClass('badge-success').addClass('badge-default');
                $.ionSound.play("water_droplet");
            }
        }
    });
}

function update_messages(messages) {
    $("#div_messages").html("");
    $.each(messages, function (i, m) {
        $("#div_messages").append("<div class='alert alert-" + m.level + "''>" + m.message + "</div>");
    })
}

function toggle_favorite_state(button) {
    movie_pk = $(button).parent().parent().attr("data-moviepk");

    $.ajax({
        url: '/toggle_favorite_state/',
        data: {'movie_pk': movie_pk},
        dataType: 'json',
        method: 'POST',
        success: function (json) {
            if (json.status === 'switch_on') {
                // switch button on
                $(button).removeClass('btn-outline-secondary').addClass('btn-danger');
                $.ionSound.play("water_droplet");
            } else if (json.status === 'switch_off') {
                // switch button off
                $(button).removeClass('btn-danger').addClass('btn-outline-secondary');
                $.ionSound.play("water_droplet");
            } else if (json.status === 'error') {
                addMessage('error!', 'danger')
            }
        }
    });
}


function toggle_like_state(button) {
    var movie_pk = $(button).parent().parent().attr("data-moviepk");
    var buttonid = $(button).attr("id");

    var likebutton = $('#like');
    var dislikebutton = $('#dislike');

    $.ajax({
        url: '/toggle_like_state/',
        data: {'movie_pk': movie_pk, 'button': buttonid},
        dataType: 'json',
        method: 'POST',
        success: function (json) {
            if (json.status === 'success')
                if (json.like)
                    $(likebutton).removeClass('btn-outline-secondary').addClass('btn-success');
                else
                    $(likebutton).removeClass('btn-success').addClass('btn-outline-secondary');

                if (json.dislike)
                    $(dislikebutton).removeClass('btn-outline-secondary').addClass('btn-success');
                else
                    $(dislikebutton).removeClass('btn-success').addClass('btn-outline-secondary');

                // $(button).removeClass('btn-outline-secondary').addClass('btn-danger');
                $.ionSound.play("water_droplet");

        }
    });
}

function toggle_person(portrait) {
    var person_tmdbid = $(portrait).attr('id');

    $.ajax({
        url: '/toggle_person/',
        data: {'person_tmdbid': person_tmdbid},
        dataType: 'json',
        method: 'POST',
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
            // Add loader animation classes
            $(portrait).find(".loader").addClass('loader-spinner');
            $(portrait).addClass('loader-shading')
        }
    })
    .done(function (json) {
        // console.log('state:', json['status']);
        if (json.status === 'in_database') {
            $(portrait).find(".face-inner").addClass('face-favorite');
            $.ionSound.play("water_droplet");
        } else if (json.status === 'deleted') {
            $(portrait).find(".face-inner").removeClass('face-favorite');
            $.ionSound.play("water_droplet");
        } else if (json.status === 'failed') {
            $("#snoAlertBox")
                .removeClass('alert-success')
                .addClass('alert-danger')
                .text('ERROR: ' + json['error_code'])
                .fadeIn();
            closeSnoAlertBox();
        }
    })
    .always(function () {
        // Remove loader animation classes
        $(portrait).find(".loader").removeClass('loader-spinner');
        $(portrait).removeClass('loader-shading')
    })
}

$(document).ready(function () {

    jconfirm.defaults = {
        theme: 'dark'
    };

    //
    // Handle tooltipster
    //
    $('.tooltipster').tooltipster({
        theme: 'tooltipster-punk',
        contentAsHTML: true,
        delay: 0,
        plugins: ['follower']
    });

    //
    // init bunch of sounds
    //
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
    // Inline edit for movie notice
    //
    $("#note-movie").blur(function () {
        var frm = $('#note-movie');
        var movie_pk = frm.attr('data-movie-pk');
        var text = frm.html();

        $.ajax({
            url: '/notice_edit_ajax/',
            data: {'movie_pk': movie_pk, 'text': text},
            dataType: 'json',
            method: 'POST'
        }).done(function (json) {
            console.log(json['status']);
            console.log(json['actual_text']);
            //addMessage('Notice changed to: '+json['actual_text'], 'success')
            $("#snoAlertBox")
                .removeClass('alert-danger')
                .addClass('alert-success')
                .text('Notice changed to: ' + json['actual_text'])
                .fadeIn();
            closeSnoAlertBox();
        });

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
    // Handle toggle favorite person
    //
    $('.face-image-container').on('click', function () {
        portrait  = $(this);
        toggle_person(portrait)
    });


    //
    // Handle tag toggle
    //
    $('.tag-toggle').on('click', function () {
        movie_pk = $(this).attr("data-moviepk");
        tag_pk = $(this).attr("data-tagpk");
        toggle_tag_ajax(movie_pk, tag_pk)
    });


    //
    // Handle create tag button
    //
    $('#add-tag-submit').on('click', function () {
        create_tag()
    });

    //
    // Handle LOVE button
    //
    $('#favorite').on('click', function () {
        toggle_favorite_state($(this))
    });

    //
    // Handle LIKE button
    //
    $('#like').on('click', function () {
        toggle_like_state($(this))
    });

    //
    // Handle DISLIKE button
    //
    $('#dislike').on('click', function () {
        toggle_like_state($(this))
    });


    // Confirmation for delete movie (on movie page) [not implemented]
    //
    $(".button_delete").confirm({
        title: 'What is up?',
        content: 'Here goes a little content',
        type: 'green',
        buttons: {
            ok: {
                text: "ok!",
                btnClass: 'btn-primary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked confirm to delete pk' + movie_pk);
                }
            },
            cancel: function () {
                console.log('the user clicked cancel, but pk was ' + movie_pk);
            }
        }
    });


    // Confirmation for delete tag
    //
    // Мы мспользуем Event delegation (https://learn.javascript.ru/event-delegation), иначе только что созданные
    // теги не будет иметь хандлера удаления на крестике. Поэтому хадлер висит на объекте-родителе, и при клике
    // мы проверяем, на каком элементе был клик, и уже тогда выполняем удаление соотв. тега.
    //
    $('.jquery-confirm-delete').on('click', function () {

        var target = event.target;

        // Нужно кликнуть по элементу I (крестику), чтобы выполнить удаление тега
        if (target.tagName !== 'I') return;

        var tagpk = $(target).attr('data-tag-pk');
        var tagname = $(target).attr('data-tag-name');
        var tagobj = $("span#" + tagpk);

        $.confirm({
            title: 'Deleting "' + tagname + '" tag',
            content: 'Are you sure?',
            buttons: {
                confirm: {
                    text: 'Delete',
                    btnClass: 'btn-danger',
                    action: function () {
                        $.ajax({
                            url: '/delete_tag_ajax/',
                            type: 'POST',
                            data: {tagpk: tagpk},
                            dataType: 'json'
                        })
                            .done(function (json) {
                                if (json['status'] == 'sucess') {
                                    tagobj.empty();
                                    update_messages(json['messages']);
                                    $("#snoAlertBox")
                                        .removeClass('alert-danger')
                                        .addClass("alert-success")
                                        .text('Список ' + json['name'] + ' успешно удален')
                                        .fadeIn();
                                    console.log('DELETE tag: success')
                                } else if (json['status'] == 'exist') {
                                    $("#snoAlertBox")
                                        .removeClass("alert-success")
                                        .addClass("alert-danger")
                                        .text('Список ' + json['name'] + ' не может быть удален - он содержит фильмы!')
                                        .fadeIn();
                                    console.log('DELETE tag: reject')
                                }
                                closeSnoAlertBox();
                            })
                            .fail(function () {
                                alert('fail')
                            });
                    }
                },
                cancel: function () {
                }
            }
        })
    })
});