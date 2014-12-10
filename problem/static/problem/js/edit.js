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
    });

    $('#add_tag_button').click(function() {
        var newTag = escapeHTML($('#newTag').val());
        if (newTag.trim() == "") {
            alert('empty');
            return false;
        }
        if ($.inArray(newTag.trim().toLowerCase(), tags) != -1) {
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
