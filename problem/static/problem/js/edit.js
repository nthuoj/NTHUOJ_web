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
    $(".tab-pane").hide();
    $($(t).attr("href")).show();
}

$(document).ready(function() {
    $(".tab-pane").hide();
    $("#info").show();
    hide_field();
    show_field($("#id_judge_source").val());
    show_field($("#id_judge_type").val());
    $("a[role='tab']").click(function(e) {
        e.preventDefault()
        switchTab(this);
    });
    CKEDITOR.replace("des", {
    	fontSize_sizes: '12/12px;16/16px;24/24px;48/48px;'
    });
    CKEDITOR.replace("inText", {
    	fontSize_sizes: '12/12px;16/16px;24/24px;48/48px;'
    });
    CKEDITOR.replace("outText", {
    	fontSize_sizes: '12/12px;16/16px;24/24px;48/48px;'
    });

    $("#add_testcase").submit(function (e) {
        e.preventDefault();
        add_new_testcase(pid, new FormData(this));
    });
    $("#update_testcase").submit(function (e) {
        e.preventDefault();
        $.ajax({
          type: "POST",
          url: "/problem/pid/testcase/" + update_tid + "/",
          data: new FormData(this),  
          processData: false,
          contentType: false,
          success: function(data) {
            alert("testcase updated");
          }
        });
    });
    refreshTestcaseEvent();
});


function add_new_tag(pid) {
    var new_tag = $('#newTag').val().trim();
    if (new_tag == '') return false;
    $.ajax({
        url: "/problem/" + pid + "/tag/",
        data: $("#addTag").serialize(),
        type: "POST",
        success: function(msg) {
          var new_tag_row = $("<tr data-target='" + msg.tag_id + "'>");
          new_tag_row.append($("<td>" + new_tag + "</td>"));
          new_tag_row.append($("<td><button class='btn btn-primary del_tag_btn'>Delete</button></td>"));
          $("#tagTable").append(new_tag_row);
        }
    });    
    $("#newTag").val("");
    return false;
}

function add_new_testcase(pid, data) {
      var time_limit = $("#new_time_limit").val();
      var memory_limit = $("#new_memory_limit").val();
      $.ajax({
          type: 'POST',
          url: '/problem/' + pid + '/testcase/',
          data: data, 
          processData: false,
          contentType: false,
          success: function(data) {
              var tid = data.tid;
              var new_row = $("<tr data-target="+tid+">");
              new_row.append($("<td>").append(
                  $("<a>" + tid + ".in</a>")));
              new_row.append($("<td>").append(
                  $("<a>" + tid + ".out</a>")));
              new_row.append($("<td>").append(
                  $("<input type='number' id='" + tid
                      + "_time' name='time_limit' value='" + time_limit +
		      "' min='0'></td>")));
              new_row.append($("<td>").append(
                  $("<input type='number' id='" + tid
                      + "_memory' name='memory_limit' value='" + memory_limit
		      + "' min='0'></td>")));
              new_row.append("<td><button class='btn btn-primary' onclick='return false'\
                    data-toggle='modal' data-target='#edit_testcase'>ReUpload</button></td>");
              new_row.append("<td><button class='btn btn-primary update_btn'>Update</button></td>");
              new_row.append("<td><button class='btn btn-danger del_testcase_btn'>Delete</button></td>");
              $("#testcase_table tr:last-child").before(new_row);
          }
      });
}

$("#preview_button").click(function() {
    var data = $("#problem_info :input").serialize();
    MyWindow = window.open('/problem/preview?' + data,
        "MyWindow",
        "toolbar=no,location=no,directories=no,status=no,menubar=no, \
        scrollbars=yes,resizable=yes,width=600,height=30"
    );
    return false;
});

function hide_field() {
  $("#id_error_torrence").parent().hide();
  $("#id_other_judge_id").parent().hide();
  $("#id_partial_judge_code").parent().hide();
  $("#id_special_judge_code").parent().hide();
}

function show_field(option) {
    if (option == "ERR_TOLERANT")
        $("#id_error_torrence").parent().show();
    else if (option == "OTHER")
        $("#id_other_judge_id").parent().show();
    else if (option == "PARTIAL")
        $("#id_partial_judge_code").parent().show();
    else if (option == "SPECIAL")
        $("#id_special_judge_code").parent().show();
}

$("select").on("change", function(e) {
    hide_field();
    show_field(this.value);
});

function refreshTestcaseEvent() {
    $("body").on("click", ".reupload_btn", function(e) {
        update_tid = $(this).parents("tr").attr('data-target');
    });
    $("body").on("click", ".update_btn", function(e) {
        var tid = $(this).parents("tr").attr('data-target');
        var time = $("#" + tid + "_time").serialize();
        var memory = $("#"+tid+"_memory").serialize();
        if ($("#" + tid + "_time").val() < 0) {
            alert("time limit can't be negative");
            return false;
        }
        if ($("#" + tid +"_memory").val() < 0) {
            alert("memory limit can't be negative");
            return false;
        }
        $.ajax({
            type: "POST",
            url: "/problem/" + pid + "/testcase/" + tid + "/",
            data: time + "&" + memory + "&" + csrf,
            success: function(data) {
              alert('testcase updated')
            }
        });
        return false;
    });
    $("body").on('click', '.del_testcase_btn', function(e) {
        var row = $(this).parents("tr");
        var tid = $(this).parents("tr").attr('data-target');
        $.ajax({
            type: 'GET',
            url: '/problem/' + pid + '/testcase/' + tid + '/delete/',
            success: function(data) {
              row.hide();
            }
        });
        return false;
    });
}
