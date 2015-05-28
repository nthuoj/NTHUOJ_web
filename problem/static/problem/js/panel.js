$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('.progress').css('overflow', 'inherit');
    $('.del_btn').click(function() {
        return confirm("Are you sure you want to delete?");
    });
    $('.rejudge-btn').click(function() {
        var submission = $(this).attr('data-submission');
        var check = prompt("\
		The problem has " + submission + " submissions\n\
		Rejudge might take a long time\n\
		Enter the submission number of this problem to continue");
	return check == submission;
    });
});
