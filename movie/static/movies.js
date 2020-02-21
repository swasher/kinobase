function create_tag(frm) {
    console.log('create_tag');

    $.ajax({
        url: frm.attr('action'),
        method: frm.attr('method'),
        data: frm.serialize(),
        dataType: 'json'
    })
    .done(function (json) {
        console.log(json['status']);
        console.log(json['name']);
        console.log(json['tagpk']);
        if (json.success) {

            let skeleton = `` +
            `<li id="${json['tagpk']}" class="list-group-item d-flex justify-content-between">` +
            `<p id="${json['tagpk']}" class="tagname p-0 m-0 flex-grow-1">` +
            `${json["name"]} ` +
            `</p>` +
            `<div class="btn-group btn-group-sm" role="group">` +
            `<button type="button" class="btn btn-outline-light" disabled>0 items</button>` +
            `<button type="button" data-tag-pk="${json['tagpk']}" data-tag-name="" class="btn btn-success btn-rename-click">Rename</button>` +
            `<button type="button" data-tag-pk="${json['tagpk']}" data-tag-name="" class="btn btn-danger btn-delete-click">Delete</button>` +
            `</div>` +
            `</li>`;
            skeleton = $(skeleton);

            if ($('h4.card-title').length) {
                console.log('Creating first tag -> Remove dummy text');
                $('h4.card-title').attr({'hidden': 'True'});
                $('div.card-block').append(skeleton);
            } else {
                console.log('This is not first tag');
                $('div.card-block').append(skeleton);
            }

            $('.panel-body').on('click',  function () {
                console.log($(this).text());
            });
        }
        else {
            alert(json.message)
        }
    })
    .fail(function(jqXHR, textStatus) {
        // alert( "Request failed: " + textStatus );
        alert( "Request failed: " + jqXHR.responseText.split('\n', 2).join('\n') );
    });
}


function delete_tag(tagpk, tagname, tagobj) {
    bootbox.confirm({
        title: 'Delete tag' + tagname,
        message: 'Are you sure?',
        centerVertical: true,
        swapButtonOrder : true,
        buttons: {
            confirm: {
                label: 'Yes',
                className: 'btn-success'
            },
            cancel: {
                label: 'No',
                className: 'btn-danger'
            }
        },
        callback: function (result) {
            if (result) {
                $.ajax({
                    url: '/delete_tag_ajax/',
                    type: 'POST',
                    data: {tagpk: tagpk},
                    dataType: 'json'
                })
                .done(function (json) {
                    if (json['status'] === 'success') {
                        tagobj.remove();
                        addMessage('Список ' + json['name'] + ' успешно удален', 'success');
                        console.log('deleting tag: success')
                    } else if (json['status'] === 'permanent') {
                        addMessage('Список ' + json['name'] + ' системный - не может быть удален', 'warning');
                        console.log('deleting tag: reject')
                    } else if (json['status'] === 'exist') {
                        addMessage('Список ' + json['name'] + ' не удален - имеет фильмы', 'error');
                        console.log('deleting tag: exist')
                    }
                })
                .fail(function () {
                    alert('fail')
                });
            }
        }
    })
}


function rename_tag(tagpk, tagname, tagtext) {
    bootbox.prompt({
        title: "Новое имя тега:",
        centerVertical: true,
        callback: function(result) {
            console.log(result);
            let newName = result;
            if (result) {
                $.ajax({
                    url: '/rename_tag_ajax/',
                    type: 'POST',
                    data: {tag_pk: tagpk, new_name: newName},
                    dataType: 'json'
                })
                .done(function (json) {
                    if (json['status'] === 'success') {
                        tagtext.text(newName);
                        addMessage(`Список ${json['name']} успешно переименован в ${newName}`, 'success');
                        console.log('rename tag: success')
                    } else if (json['status'] === 'failed') {
                        // TODO добавить вывод описание ошибки из exceptions
                        addMessage('failed');
                        console.log('rename tag: failed')
                    }
                })
                .fail(function () {
                    alert('fail')
                });
            }
        }
    });
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
            /* DEPRECATED            $("#snoAlertBox")
                .removeClass('alert-success')
                .addClass('alert-danger')
                .text('ERROR: ' + json['error_code'])
                .fadeIn();
            closeSnoAlertBox();*/
            addMessage('ERROR: ' + json['error_code'], 'danger')
        }
    })
    .always(function () {
        // Remove loader animation classes
        $(portrait).find(".loader").removeClass('loader-spinner');
        $(portrait).removeClass('loader-shading')
    })
}

$(document).ready(function () {

    // DEPRECATED
    // jconfirm.defaults = {
    //     theme: 'dark'
    // };

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
            // DEPRECATED addMessage('Notice changed to: '+json['actual_text'], 'success')
            /* DEPRECATED $("#snoAlertBox")
                .removeClass('alert-danger')
                .addClass('alert-success')
                .text('Notice changed to: ' + json['actual_text'])
                .fadeIn();
            closeSnoAlertBox();*/
            addMessage('Notice changed to: ' + json['actual_text'], 'success')
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
    // Handle tag toggle [movie detail page]
    //
    $('.tag-toggle').on('click', function () {
        movie_pk = $(this).attr("data-moviepk");
        tag_pk = $(this).attr("data-tagpk");
        toggle_tag_ajax(movie_pk, tag_pk)
    });


    //
    // Handle create tag
    //
    $('#add-tag-submit').on('click', function () {
        var form = $('#create-tag-form');
        create_tag(form)
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


    // DEPRECATED
    // Confirmation for delete movie (on movie page) [not implemented]
    //
    // $(".button_delete").confirm({
    //     title: 'What is up?',
    //     content: 'Here goes a little content',
    //     type: 'green',
    //     buttons: {
    //         ok: {
    //             text: "ok!",
    //             btnClass: 'btn-primary',
    //             keys: ['enter'],
    //             action: function () {
    //                 console.log('the user clicked confirm to delete pk' + movie_pk);
    //             }
    //         },
    //         cancel: function () {
    //             console.log('the user clicked cancel, but pk was ' + movie_pk);
    //         }
    //     }
    // });


    // Confirmation for delete tag
    //
    // Мы мспользуем Event delegation (https://learn.javascript.ru/event-delegation), иначе только что созданные
    // теги не будет иметь хандлера удаления на крестике. Поэтому хадлер висит на объекте-родителе, и при клике
    // мы проверяем, на каком элементе был клик, и уже тогда выполняем удаление соотв. тега.
    //
    $('.js-delete').on('click', function () {

        let target = event.target;

        if (target.classList.contains('btn-rename-click')) {
            console.log('rename');
            let tagpk = $(target).attr('data-tag-pk');      // передается в django для удаления из базы
            let tagname = $(target).attr('data-tag-name');  // используется только в всплывающем алерте
            let tagtext = $("li#" + tagpk + " p");          // это jquery-объект, в котором выполняется переименование тега
            rename_tag(tagpk, tagname, tagtext)
        }

        if (target.classList.contains('btn-delete-click')) {
            console.log('delete');
            let tagpk = $(target).attr('data-tag-pk');      // передается в django для удаления из базы
            let tagname = $(target).attr('data-tag-name');  // используется только в всплывающем алерте
            let tagobj = $("li#" + tagpk);                  // это DOM-ветка, которую удаляем с экрана при удалении тга
            delete_tag(tagpk, tagname, tagobj)
        }

    })


});
