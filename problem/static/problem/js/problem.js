/*
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
function unix2dos(text) {
    var ret = [];
    for (var i=0, ch; i<text.length; ++i) {
        ch = text[i];
        if (ch == "\n")
            ch = "\r\n";
        ret.push(ch);
    }
    return ret.join("");
}

function isBrowser(name) {
    return navigator.userAgent.indexOf(name) != -1;
}

function isMSBrowser () {
    var MSBrowsers = ["MSIE ", "Trident/", "Edge/"];
    var ret = false;
    for (var i=0; i<MSBrowsers.length && !ret; ++i)
        ret = ret || isBrowser(MSBrowsers[i]);
    return ret;
}

function MSBrowserDownloadHandler (file, filename) {
    return function(e) {
        window.navigator.msSaveOrOpenBlob(file, filename);
    };
}

function setDownloadSampleButton(button, suffix, isIE) {
    var pid = button.getAttribute("pid");
    var filename = pid + suffix;
    var text = $("#"+filename).val();

    // convert end-of-line symbol and filename if on windows system
    if (navigator.appVersion.indexOf("Win") != -1) {
        text = unix2dos(text);
        filename += ".txt";
    }

    // use specific API for download when dealing with IE, Edge browsers
    if (isIE) {
        var file = new Blob([text], {type: 'text/plain'});
        button.onclick = MSBrowserDownloadHandler(file, filename);
    }
    else {
        button.setAttribute("href", "data:text/plain;charset=utf-8,"+encodeURIComponent(text));
        button.setAttribute("download", filename);
    }
}
function resizeTextarea (textarea) {
    if(textarea.clientHeight < textarea.scrollHeight)
        textarea.style.height = textarea.scrollHeight +"px";
}

function resizeAllTextareas () {
    var textareas = $("textarea");
    for (var i=0; i<textareas.length; ++i)
        resizeTextarea(textareas[i]);
}

$(function() {
    // updates each textarea's height to fit their default content
    resizeAllTextareas();

    var browserFlag = isMSBrowser();
    // set download sample input button(s)
    var downloadSampleInputButtons = $(".downloadSampleInputButton");
    for (var i=0; i<downloadSampleInputButtons.length; ++i)
        setDownloadSampleButton(downloadSampleInputButtons[i], "_sampleIn", browserFlag);

    // set download sample output button(s)
    var downloadSampleOutputButtons = $(".downloadSampleOutputButton");
    for (var i=0; i<downloadSampleOutputButtons.length; ++i)
        setDownloadSampleButton(downloadSampleOutputButtons[i], "_sampleOut", browserFlag);

    $('#addTagButton').click(function() {
        var new_tag = $('#id_tag_name').val().trim();
        if (new_tag == '') return false;
        $.ajax({
            url: '/problem/' + pid + '/tag/',
            data: $('#addTag').serialize(),
            type: 'POST',
            success: function(msg) {
              var new_tag_span = "<span class='label label-info'>" +
                      new_tag + '</span>';
              $('#tags').append(new_tag_span);
            }
        });
        $('#newTag').val('');
        return false;
    });
});

