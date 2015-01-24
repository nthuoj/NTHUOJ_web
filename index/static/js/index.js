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
var displayInfo = false;
var loginInfo = false;

window.onload = function() {

    var volume = document.getElementById("volume_num").innerHTML;
    volume = Number(volume);    
    document.getElementById("volume_num").innerHTML = "";
    for (i=1;i<=volume;i++){
        var origin = document.getElementById("volume_num").innerHTML;
        document.getElementById("volume_num").innerHTML = 
        origin + '<li><a href="#">' + 'volume ' + i + '</a></li>';
    }

    var contest_content = document.getElementById("contest_content").innerHTML;
    contest_content = contest_content.replace(/<td>/,'');
    contest_content = contest_content.replace(/<\/td>/,'');
    contest_content = contest_content.replace(/<tr>/,'');
    contest_content = contest_content.replace(/<\/tr>/,'');
    contest_content = contest_content.replace(/\s/g,'');
    contest_content = contest_content.replace(/\'/g,'');
    contest_content = contest_content.split('#');
    var contest_num = contest_content[0];
    var contest_event = contest_content[1];
    var contest_time = contest_content[2];
    contest_event = contest_event.replace(/\[/,'');
    contest_event = contest_event.replace(/\]/,'');
    contest_event = contest_event.split(',');
    contest_time = contest_time.replace(/\[/,'');
    contest_time = contest_time.replace(/\]/,'');
    contest_time = contest_time.split(',');

    document.getElementById("contest_content").innerHTML = '';    
    for (i=1;i<= contest_num;i++){
        var ori = document.getElementById("contest_content").innerHTML;
        if(i != contest_num){
            document.getElementById("contest_content").innerHTML = 
            ori + '<td>' + i + '</td>' + 
            '<td>' + 
            contest_event[Math.floor(Math.random() * contest_num)] + 
            '</td>' +
            '<td>' + Math.floor((Math.random() * 10) + 1) + 
            ' ' + contest_time[Math.floor(Math.random() * contest_num)] + 
            '</td>' + 
            '<td>' + '</td>';
        }
        else{
            document.getElementById("contest_content").innerHTML = 
            ori + '<td>' + i + '</td>' + 
            '<td>' + 
            contest_event[Math.floor(Math.random() * contest_num)] + 
            '</td>' + '<td>' + '</td>' + 
            '<td>' + Math.floor((Math.random() * 10) + 1) + 
            ' ' + contest_time[Math.floor(Math.random() * contest_num)] + 
            '</td>' ;
        }
    }
    alert("You have new messages!");
}
function info() {
    if(displayInfo == false){
        document.getElementById("information").style.display = "block";
        displayInfo = !displayInfo;
    }
    else{
        document.getElementById("information").style.display = "none";
        displayInfo = !displayInfo;
    }
}
function sendinfo() {
    var text = document.getElementById("txt").value;
    var orgintext = document.getElementById("information").innerHTML;
    document.getElementById("information").innerHTML = 
    orgintext + '<li class="divider">' + text + '</li>';
    alert("You have new messages!" + text);
}
function log_in() {
    document.getElementById("notlogin").style.display = "none";
}
$(function() {
    setInterval(function() {
        $.get('/get_time/', function(data) {
            $('#time').html(data);
        });
    }, 450);
})
