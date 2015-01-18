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
function switchTab(t) {
    $("a[role='tab']").parent().removeClass("active");
    $(t).parent().addClass("active");
    $(".tab-pane").removeClass("active");
    $($(t).attr("href")).addClass("active");
}

var tags = [];

function escapeHTML(str) {
    return $('<div/>').text(str).html();
}

$(document).ready(function() {
    $("a[role='tab']").click(function(e) {
        e.preventDefault()
        switchTab(this);
    });

    $('#merge_tag').click(function() {
        var n = $('input:checked').length;
        for (var i = 1; i < n; i++) {
            var d = $('input:checked').eq(i).attr('data-target');
            delete_tag(d);
        }
        return false;
    });

    $('#add_tag_button').click(function() {
        var newTag = escapeHTML($('#newTag').val()).trim().toLowerCase();
        if (newTag == "") {
            alert('empty');
            return false;
        }
        if ($.inArray(newTag, tags) != -1) {
            alert('tag repeated');
            return false;
        }
        $('#newTag').val("");

        var $delete_button = $("<button>", {
                id: "delete_button",
                class: "btn btn-primary"
            })
            .attr('data-target', newTag).html("Delete")
            .click(function() {
                delete_tag($(this).attr('data-target'));
                return false;
            });
        var $checkbox = $("<input>", {
            type: "checkbox"
        }).attr('data-target', newTag);

        var $new_row = $("<tr>", {
                id: newTag
            })
            .append($("<td>", {
                id: "checkbox_td"
            }).append($checkbox))
            .append("<td>" + newTag + "</td>")
            .append($("<td>").append($delete_button));

        $('#tagTable').append($new_row);

        tags[tags.length] = newTag.toLowerCase();

        return false;
    });
});

function delete_tag(tag_name) {
    $("tr[id='" + tag_name + "']").hide();
    tags.splice(tags.indexOf(tag_name), 1);
}

function submitTag() {
    var len = tags.length;
    for (var i = 0; i < len; i++) {
        $("form").append("<input type='hidden' name='tag" + i + "' value='" + tags[i] + "'>");
    }
    return false;
}
