function escapeHTML(str) {
	var div = document.createElement('div');
	div.appendChild(document.createTextNode(str));
	return div.innerHTML;
}

function addTag() {
    newTag = escapeHTML($("#newTag").val());
    if (newTag.trim() != '')
        $("div #tags").append("<span class='label label-info'>" + newTag + "</span>");
    $("#newTag").val("");
    $("#addTagButton").blur();
    return false;
}
