$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('.progress').css('overflow', 'inherit');
    $('.del_btn').click(function() {
        return confirm("Are you sure you want to delete?");
    });
    $('.rejudge-btn').click(function() {
        var submission = $(this).attr('data-submission');
        return confirm("\
		The problem has " + submission + " submissions\n\
		Rejudge might take a long time\n\
		Are you sure to rejudge?");
    });
});
