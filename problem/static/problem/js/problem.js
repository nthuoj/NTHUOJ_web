//$(document).ready(function() {
    $("#addTagButton").click(function() {
        var new_tag = $('#newTag').val().trim();
        if (new_tag == '') return false;
        $.ajax({
            url: "/problem/"+pid+"/tag/",
            data: $("#addTag").serialize(),
            type: "POST",
            success: function(msg) {
              var new_tag_span = "<span class='label label-info'>"+new_tag+"</span>"
              $("#tags").append(new_tag_span);
            }
        });    
        $("#newTag").val("");
        return false;
    });
//});

