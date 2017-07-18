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

function closeSnoAlertBox() {
    window.setTimeout(function () {
        $("#snoAlertBox").fadeOut(300)
    }, 3000);
}

function update_messages(messages) {
    $("#div_messages").html("");
    $.each(messages, function (i, m) {
        $("#div_messages").append("<div class='alert alert-" + m.level + "''>" + m.message + "</div>");
    })
}


$(document).ready(function () {

    jconfirm.defaults = {
        theme: 'dark'
    };


    $('[data-toggle="popover"]').popover({
        trigger: 'hover',
        placement: 'bottom',
        animation: false
        // constraints: [{to: 'scrollParent', pin: true}]
    });


    //
    // Handle tooltip
    //
    $("[data-toggle='tooltip']").tooltip();

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
        var tmdb_id = frm.attr('data-movie-id');
        var text = frm.html();
        console.log(text);
        console.log(tmdb_id);

        $.ajax({
            url: '/notice_edit_ajax/',
            data: {'tmdb_id': tmdb_id, 'text': text},
            dataType: 'json',
            method: 'POST'
        }).done(function (json) {
            console.log(json['status']);
            console.log(json['actual_text']);
        })
    });

    //
    // Handler for X-Editable (for edit notice)
    //
    // $('#editnotice').editable({
    //     url: 'http://www.mysite.com/cgi-bin/art/my-store.cgi',
    //     onblur: "submit",
    //     placeholder: "Click to set a custom URL",
    //     emptytext: "Click to set a custom URL",
    //     params: {action: "update_store_url"},
    //     success: function (response, newValue) {
    //         $('#store-editible-url').editable('setValue', "foo", true);
    //     }
    // });


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
    // Handle create tag button
    //
    $('#add-tag-submit').on('click', function () {
        create_tag()
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