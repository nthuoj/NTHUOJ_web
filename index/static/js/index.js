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
var displayinfo=false;
var logininfo=false;

window.onload = function() {
    alert("You have new messages!");
}
function info() {
    if(displayinfo==false){	
        document.getElementById("information").style.display="block";
        displayinfo=!displayinfo;
    }
    else{
        document.getElementById("information").style.display="none";	
        displayinfo=!displayinfo;
    }
}
function sendinfo() {
    var text=document.getElementById("txt").value;
    var orgintext=document.getElementById("information").innerHTML;
    document.getElementById("information").innerHTML=orgintext+'<li class="divider">'+text+'</li>'
    //alert(orgintext);
    alert("You have new messages!"+text);
}
function log_in() {
    //alert('1');	
    document.getElementById("notlogin").style.display="none";	
    //document.getElementById("notlogin").innerHTML
    //document.getElementById("notlogin").style.display="none";	
}
$(function() {
    setInterval(function() {
        $.get('/get_time/', function(data) {
            $('#time').html(data);
        });
    }, 450);
})
