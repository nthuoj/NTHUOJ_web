function switchTab(t) {
    $("a[role='tab']").parent().removeClass("active");
    $(t).parent().addClass("active");
    $(".tab-pane").removeClass("active");
    $($(t).attr("href")).addClass("active");
}

$("a[role='tab']").click(function(e) {
    e.preventDefault()
    switchTab(this);
});

var tags = [];

function escapeHTML(str) {
	var div = document.createElement('div');
	div.appendChild(document.createTextNode(str));
	return div.innerHTML;
}

function addTag() {
    var newTag = escapeHTML($('#newTag').val());
    if (newTag.trim() == "") {
        alert('empty');
        return false;
    }
    if ($.inArray(newTag.trim().toLowerCase(), tags) != -1) {
        alert('tag repeated');
        return false;
    }
    document.getElementById('newTag').value = "";

    var click = "onclick=\"return deleteTag('" + newTag + "')\""
    $('#tagTable').append(
        "<tr id='" + newTag + "'><td>" + newTag + "</td><td><button " + click + " class='btn btn-primary'>Delete</button></td></tr>");
    tags[tags.length] = newTag.toLowerCase();
    return false;
}

function deleteTag(tagName) {
    $("tr[id='" + tagName + "']").hide();
    tags.splice(tags.indexOf(tagName), 1);
    return false;
}

function submitTag() {
    var len = tags.length;
    for (var i = 0; i < len; i++) {
        $("form").append("<input type='hidden' name='tag" + i + "' value='" + tags[i] + "'>");
    }
    return false;
}
