function escapeHTML(str) {
	return $('<div/>').text(str).html();
}

function addTag() {
    newTag = escapeHTML($("#newTag").val());
    if (newTag.trim() != '')
        $("div #tags").append("<span class='label label-info'>" + newTag + "</span>");
    $("#newTag").val("");
    $("#addTagButton").blur();
    return false;
}
