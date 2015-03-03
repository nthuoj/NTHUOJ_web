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
    $("a[role='tab']").click(function(e) {
        e.preventDefault()
        switchTab(this);
    });
});


function add_new_tag(pid) {
    var new_tag = $('#newTag').val().trim();
    if (new_tag == '') return false;
    $.ajax({
        url: "/problem/"+pid+"/tag/",
        data: $("#addTag").serialize(),
        type: "POST",
        success: function(msg) {
          var new_tag_row = $("<tr data-target='"+msg.tag_id+"'>");
          new_tag_row.append($("<td>"+new_tag+"</td>"));
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
          url: '/problem/'+pid+'/testcase/',
          data: data, 
          processData: false,
          contentType: false,
          success: function(data) {
              var tid = data.tid;
              var new_row = $("<tr data-target="+tid+">");
              new_row.append($("<td>").append(
                  $("<a>"+tid+".in</a>")));
              new_row.append($("<td>").append(
                  $("<a>"+tid+".out</a>")));
              new_row.append($("<td>").append(
                  $("<input type='number' id='"+tid
                      +"_time' name='time_limit' value='"+time_limit+"'></td>")));
              new_row.append($("<td>").append(
                  $("<input type='number' id='"+tid
                      +"_memory' name='memory_limit' value='"+memory_limit+"'></td>")));
              new_row.append("<td><button class='btn btn-primary' onclick='return false'\
                    data-toggle='modal' data-target='#edit_testcase'>ReUpload</button></td>");
              new_row.append("<td><button class='btn btn-primary update_btn'>Update</button></td>");
              new_row.append("<td><button class='btn btn-danger del_testcase_btn'>Delete</button></td>");
              $("#testcase_table tr:last-child").before(new_row);
          }
      });
}
