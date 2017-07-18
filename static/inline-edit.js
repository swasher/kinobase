function enableEditing() {
    var editableElems = getElementsByClassName(document, "editable");
    var numElems = editableElems.length;
    for (var i = 0; i < numElems; i++) {
        observeEvent(editableElems[i], "dblclick", editElem);
    }
}

function editElem(e) {
    var target = getTarget(e);
    var input;
    var textLen = target.innerHTML.length;
    if (textLen > 30) {
        target.innerHTML = "<textarea cols='120' rows='6'>" + target.innerHTML + "</textarea>";
    } else {
        target.innerHTML = "<input value='" + target.innerHTML + "'>";
    }
    var input = target.firstChild;
    input.select();
    observeEvent(input, "blur", saveCell);
}

function saveCell(e) {
    var target = getTarget(e);
    var td = target.parentNode;
    var tr = td.parentNode;
    var field = td.title;
    var value = target.value;
    var pid = tr.id;

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "SaveCell", true);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            td.innerHTML = target.value;
            blinkText(td, 1000, "Saved", "Normal");
        }
    }
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
    xmlhttp.send("field=" + field + "&value=" + value + "&pid=" + pid);
}

function blinkText(elem, time, on, off, timePast) {
    var timePast = timePast + 100 || 0;
    if (hasClassName(elem, on)) {
        removeClass(elem, on);
    } else {
        addClass(elem, on);
    }

    if (timePast < time) {
        setTimeout(function () {
            blinkText(elem, time, on, off, timePast)
        }, 100);
    } else {
        removeClass(elem, on);
        removeClass(elem, off);
    }
}