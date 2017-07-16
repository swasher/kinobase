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
            // $tag = $('span.badge:first');
            // $klon = $tag.clone(false);
            // // $klon.children('.remove').attr('id', json['tagpk']);
            // $klon.attr('id', json['tagpk']);
            // $klon.children('.tagname').text(json['name']);
            // $klon.find("i").attr("data-tag-pk", json['tagpk']);
            // $klon.find("i").attr("data-tag-name", json['name']);



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


    // $("[data-toggle='tooltip']").tooltip();
    $('[data-toggle="popover"]').popover({
        trigger: 'hover',
        placement: 'bottom',
        animation: false
        // constraints: [{to: 'scrollParent', pin: true}]
    });



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
    // Handle create tag button
    //
    $('#add-tag-submit').on('click', function () {
        create_tag()
    });

/*
    // Confirmation for delete tag
    //
    $('.jqueryconfirm').on('click', function () {

        var tagpk = $(this).attr('data-tag-pk');
        var tagname = $(this).attr('data-tag-name');
        // var tagobj = $(this).closest('span.badge');
        var tagobj = $("span#" + tagpk);

        $.confirm({
            title: 'Deleting "'+ tagname + '" tag',
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
                cancel: function () {}
            }
        })
    })
*/


    // Confirmation for delete tag
    //
    // Мы мспользуем Event delegation (https://learn.javascript.ru/event-delegation), иначе только что созданные
    // теги не будет иметь хандлера удаления на крестике. Поэтому хадлер висит на объекте-родителе, и при клике
    // мы проверяем, на каком элементе был клик, и уже тогда выполняем удаление соотв. тега.
    //
    $('.jqueryconfirm-parent').on('click', function () {

        var target = event.target;

        // Нужно кликнуть по элементу I (крестику), чтобы выполнить удаление тега
        if (target.tagName !== 'I') return;

        var tagpk = $(target).attr('data-tag-pk');
        var tagname = $(target).attr('data-tag-name');
        // var tagobj = $(this).closest('span.badge');
        var tagobj = $("span#" + tagpk);
        // var tagobj = $(target);

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


    // DEPRECATED: BOOTSTRAP-CONFIRMATION2
    //
    // Confirmation for delete movie
    //
    // $('[data-toggle="confirmation-delete-movie"]').confirmation({
    //     title: "Are you sure to remove?",
    //     placement: "right",
    //     singleton: "True",
    //     popout: "True",
    //     container: 'body',
    //     btnOkLabel: "&nbsp;Delete",
    //     btnOkClass: "btn-xs btn-danger",
    //     btnOkIcon: "glyphicon glyphicon-remove",
    //     btnCancelLabel: "&nbsp;Cancel",
    //     btnCancelIcon: "glyphicon glyphicon-repeat",
    //     rootSelector: '[data-toggle=confirmation-delete-movie]',
    //     onConfirm: function (event, element) {
    //         var movie_pk = $(this).attr('id');
    //         $.post("/delete_movie/", {movie_pk: movie_pk})
    //             .done(function (json) {
    //                 if (json['status']=='sucess') {
    //                     // json.redirect contains the string URL to redirect to
    //                     window.location.replace(json['redirect']);
    //                 }
    //             })
    //             .fail(function () {
    //
    //             });
    //         $(this).confirmation('destroy');
    //     }
    // });


    // DEPRECATED: BOOTSTRAP-CONFIRMATION2
    //
    // Confirmation for delete tag
    //
    // $('[data-toggle="confirmation-delete-tag"]').confirmation({
    //     title: "Are you sure to delete tag?",
    //     placement: "bottom",
    //     singleton: "True",
    //     popout: "True",
    //     container: 'body',
    //     btnOkLabel: "&nbsp;Delete",
    //     btnOkClass: "btn-xs btn-danger",
    //     btnOkIcon: "glyphicon glyphicon-remove",
    //     btnCancelLabel: "&nbsp;Cancel",
    //     btnCancelIcon: "",
    //     rootSelector: '[data-toggle=confirmation-delete-tag]',
    //     onConfirm: function (event, element) {
    //         // var pk = $(this).attr('id'); This work if ID in I tag (in html)
    //         var pk = $(this).closest('.tag').attr('id');
    //         var tag = $(this).closest('span.label');
    //
    //         $.ajax({
    //             url: '/delete_tag_ajax/',
    //             type: 'POST',
    //             data: {pk: pk},
    //             dataType: 'json'
    //         })
    //             .done(function (json) {
    //                 if (json['status'] == 'sucess') {
    //                     tag.empty();
    //                     $("#snoAlertBox")
    //                         .removeClass('alert-danger')
    //                         .addClass("alert-success")
    //                         .text('Список ' + json['name'] + ' успешно удален')
    //                         .fadeIn();
    //                 } else if (json['status'] == 'exist') {
    //                     $("#snoAlertBox")
    //                         .removeClass("alert-success")
    //                         .addClass("alert-danger")
    //                         .text('Список ' + json['name'] + ' не может быть удален - он содержит игры!')
    //                         .fadeIn();
    //                 }
    //                 closeSnoAlertBox();
    //             })
    //             .fail(function () {
    //                 // $("#snoAlertBox")
    //                 //     .addClass("alert-danger")
    //                 //     .text('Вы должны авторизироваться.')
    //                 //     .fadeIn();
    //                 // closeSnoAlertBox();
    //                 alert('fail')
    //             });
    //
    //         $(this).confirmation('destroy');
    //     }
    // });

});