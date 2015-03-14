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
function write_content(id){
    read_id = id;
    element = id + '_content';    
    var message = document.getElementById(element).textContent;    
    document.getElementById("area").textContent = message;    
}
function read(){
    window.location.href = "http://" + window.location.host + 
    "/users/u_read_del/" + read_id + "/";
}
$.magnificPopup.instance.close = function() {    
    $(document).trigger('mfp-global-close');
    $.magnificPopup.proto.close.call();
    read();
};
function u_read_del(d_checkbox) {
    
    var d_id = "";
    if(d_checkbox.length){
        for(var i=0;i<d_checkbox.length;i++){
            if(d_checkbox[i].checked == true){
                d_id = d_id + d_checkbox[i].value + ",";
            }
        }
    }
    else{
        if(d_checkbox.checked == true)
            d_id = d_id + d_checkbox.value + ",";
    }    
    d_id = d_id.slice(0,-1);
    window.location.href = "http://" + window.location.host + 
    "/users/u_read_del/" + "/" + d_id;

}

function all_del(d_checkbox) {
  
    var d_id = "";
    if(d_checkbox.length){
        for(var i=0;i<d_checkbox.length;i++){
            if(d_checkbox[i].checked == true){
                d_id = d_id + d_checkbox[i].value + ",";
            }
        }
    }
    else{
        if(d_checkbox.checked == true)
            d_id = d_id + d_checkbox.value + ",";
    }

    d_id = d_id.slice(0,-1);
    window.location.href = "http://" + window.location.host + 
    "/users/all_del/" + d_id;
}

function check_all(obj, names) {
     var checkboxs = document.getElementsByName(names);
    for(var i=0;i<checkboxs.length;i++){
        checkboxs[i].checked = obj.checked;
    }
}
