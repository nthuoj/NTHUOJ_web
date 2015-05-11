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
    if ($(t).length == 0) return;
    $("a[role='tab']").parent().removeClass("active");
    $(t).parent().addClass("active");
    $(".tab-pane").removeClass("active");
    $(t).addClass("active");
    $(".tab-pane").hide();
    $(t).show();
}

$(document).ready(function() {
    $(".tab-pane").hide();
    $("#info").show();
    var judge_type = $("#id_judge_type").val();
    choose_judge_source($("#id_judge_source").val());
    $("#id_judge_type").val(judge_type);
    choose_judge_type($("#id_judge_type").val());
    if (window.location.href.indexOf('?') != -1) {
        var param = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for (var i = 0; i < param.length; i++) {
            if (param[i].split('=')[0] == "tab") {
                switchTab('#' + param[i].split('=')[1]);
                break;
            }
        }
    }
    $("a[role='tab']").click(function(e) {
        e.preventDefault()
        switchTab($(this).attr('href'));
    });

    $("#add_testcase").submit(function(e) {
        e.preventDefault();
        add_new_testcase(pid, new FormData(this));
    });
    $("#update_testcase").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/problem/" + pid + "/testcase/" + update_tid + "/",
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function(data) {
                alert("testcase updated");
            }
        });
    });
    $("body").on("click", ".reupload_btn", function(e) {
        update_tid = $(this).parents("tr").attr('data-target');
    });
    $("body").on("click", ".update_btn", function(e) {
        var tid = $(this).parents("tr").attr('data-target');
        var time = $("#" + tid + "_time").serialize();
        var memory = $("#" + tid + "_memory").serialize();
        if ($("#" + tid + "_time").val() < 0) {
            alert("time limit can't be negative");
            return false;
        }
        if ($("#" + tid + "_memory").val() < 0) {
            alert("memory limit can't be negative");
            return false;
        }
        $.ajax({
            type: "POST",
            url: "/problem/" + pid + "/testcase/" + tid + "/",
            data: time + "&" + memory + "&" + csrf,
            success: function(data) {
                alert('testcase updated');
                window.location.href = "/problem/" + pid + "/edit/?tab=testcase";
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
                alert('testcase deleted');
                window.location.href = "/problem/" + pid + "/edit/?tab=testcase";
            }
        });
        return false;
    });
});


function add_new_tag(pid) {
    var new_tag = $('#id_tag_name').val().trim();
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
            window.location.href = "/problem/" + pid + "/edit/?tab=testcase";
        }
    });
}

$("#preview_button").click(function() {
    var form = $("#problem_info");
    form.attr("target", "_blank");
    form.attr("action", "/problem/preview/");
    var input = $("<input>");
    input.attr("type", "hidden");
    input.attr("name", "tags");
    var tags = []
    $("#tagTable td:first-child").each(function(num, element) {
        tags[tags.length] = element.innerHTML;
    });
    input.val(tags.join());
    $("input[name='tags']").remove();
    form.append(input);
    return true;
});

$("#save_button").click(function() {
    var form = $("#problem_info");
    form.attr("target", "");
    form.attr("action", "");
    return true;
});

function hide_field() {
    $("#id_error_tolerance").parent().parent().hide();
    $("#id_partial_judge_code").parent().parent().hide();
    $("#id_partial_judge_header").parent().parent().hide();
    $("#id_special_judge_code").parent().parent().hide();
    $("#id_judge_language").parent().parent().hide();
}

function choose_judge_type(option) {
    hide_field();
    if (option == "LOCAL_ERR_TOLERANT")
        $("#id_error_tolerance").parent().parent().show();
    else if (option == "LOCAL_PARTIAL") {
        $("#id_partial_judge_code").parent().parent().show();
        $("#id_partial_judge_header").parent().parent().show();
        $("#id_judge_language").parent().parent().show();
    } else if (option == "LOCAL_SPECIAL") {
        $("#id_special_judge_code").parent().parent().show();
        $("#id_judge_language").parent().parent().show();
    }
}

function choose_judge_source(option) {
    if (option == "OTHER") {
        $("#id_other_judge_id").parent().parent().show();
        $("option[value^='OTHER_']").show();
        $("option[value^='LOCAL_']").hide();
        $("#id_judge_type").val($("option[value^='OTHER_']")[0].value);
        $("#id_other_judge_id").parent().parent().show();
    } else if (option == "LOCAL") {
        $("option[value^='OTHER_']").hide();
        $("option[value^='LOCAL_']").show();
        $("#id_judge_type").val($("option[value^='LOCAL_']")[0].value);
        $("#id_other_judge_id").parent().parent().hide();
    }
}

$("#id_judge_source").on("change", function(e) {
    hide_field();
    choose_judge_source(this.value);
});

$("#id_judge_type").on("change", function(e) {
    choose_judge_type(this.value);
});

function refreshTestcaseEvent() {
    $("body").on("click", ".reupload_btn", function(e) {
        update_tid = $(this).parents("tr").attr('data-target');
    });
    $("body").on("click", ".update_btn", function(e) {
        var tid = $(this).parents("tr").attr('data-target');
        var time = $("#" + tid + "_time").serialize();
        var memory = $("#" + tid + "_memory").serialize();
        if ($("#" + tid + "_time").val() < 0) {
            alert("time limit can't be negative");
            return false;
        }
        if ($("#" + tid + "_memory").val() < 0) {
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
                row.remove();
            }
        });
        return false;
    });
}
