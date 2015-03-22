/*
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
var read_id;
var active_tab;
var notification_type;
function write_content(id, type){
    read_id = id;
    element = id + '_content';

    if(type == 'True')
        notification_type = 'read';
    else
        notification_type = 'unread';
    var message = document.getElementById(element).textContent;
    document.getElementById("area").textContent = message;
}
function readify(){
    window.location.href = "http://" + window.location.host +
    "/users/readify/" + read_id + '/' + active_tab;
}
$(function(){
    active_tab = document.getElementById("current-tab").value;
    if(active_tab == 'all')
        $('#notification-tab-type a[href="#all"]').tab('show');
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        active_tab = $(e.target).text();
        if(active_tab == 'All Notifications')
            active_tab = 'all';
        else
            active_tab = 'unread';
    });
});
$.magnificPopup.instance.close = function() {
    $(document).trigger('mfp-global-close');
    $.magnificPopup.proto.close.call();
    if(notification_type == 'unread')
        readify();
};
function delete_notification(delete_checkbox) {
    var delete_ids = "";
    if(delete_checkbox.length){
        for(var i=0;i<delete_checkbox.length;i++){
            if(delete_checkbox[i].checked == true){
                delete_ids = delete_ids + delete_checkbox[i].value + ",";
            }
        }
    }
    else{
        if(delete_checkbox.checked == true)
            delete_ids = delete_ids + delete_checkbox.value + ",";
    }
    delete_ids = delete_ids.slice(0,-1);
    window.location.href = "http://" + window.location.host +
    "/users/delete_notification/" + delete_ids + '/' +active_tab;
}

function check_all(obj, names) {
     var checkboxs = document.getElementsByName(names);
    for(var i=0;i<checkboxs.length;i++){
        checkboxs[i].checked = obj.checked;
    }
}
