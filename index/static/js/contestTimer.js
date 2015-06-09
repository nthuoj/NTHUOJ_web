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
$(function(){
    getRestTime();
});
function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }; // add zero in front of numbers < 10
    return i;
}
function getRestTime() {
    var serverTime = new Date(document.getElementById("time").innerHTML).getTime();
    var remaining_time = new Array();
    var upcoming_time = new Array();
    var contest_id = new Array();
    var freezes = new Array();
    var end_time = new Array();
    var start_time = new Array();
    var id_list = new Array();
    var freeze_time = new Array();
    var remainings = new Array();
    var upcomings = new Array();
    var flag = 0;

    end_time = document.getElementsByName("end");
    remainings = document.getElementsByName("remain");
    id_list = document.getElementsByName("contest_id");
    freeze_time = document.getElementsByName("freeze_time");

    for(var i=0;i<end_time.length;i++){
        remaining_time[i] = new Date(end_time[i].textContent).getTime();
        contest_id[i] = id_list[i].textContent;
        freezes[i] = Number(freeze_time[i].textContent);
    }

    start_time = document.getElementsByName("start");
    upcomings = document.getElementsByName("upcome");
    for(var i=0;i<start_time.length;i++)
        upcoming_time[i] = new Date(start_time[i].textContent).getTime();


    for(var i=0;i<remaining_time.length;i++){
        var result = (remaining_time[i] - serverTime) / 1000;

        if(result <= freezes[i]*60){
            document.getElementById("contest_" + contest_id[i]).className = "danger";
        }
        if (serverTime <= remaining_time[i]){
            var s = parseInt(result % 60);
            result /= 60;
            var m = parseInt(result % 60);
            result /= 60;
            var h = parseInt(result % 24);
            result /= 24;
            var d = parseInt(result);
            m = checkTime(m);
            s = checkTime(s);
            h = checkTime(h);
            var day = "";
            if(d > 1)
                day = d + " days, ";
            else if(d == 1)
                day = d + " day, ";

            remainings[i].innerHTML = day + h + ":" + m + ":" + s;
        }
    }
    for(var i=0;i<upcoming_time.length;i++){
        var result = (upcoming_time[i] - serverTime) / 1000;

        if (serverTime <= upcoming_time[i]){
            var s = parseInt(result % 60);
            result /= 60;
            var m = parseInt(result % 60);
            result /= 60;
            var h = parseInt(result);
            m = checkTime(m);
            s = checkTime(s);
            h = checkTime(h);
            upcomings[i].innerHTML = h + ":" + m + ":" + s;
        }
    }
    for(var i=0;i<remaining_time.length;i++){
        if(serverTime <= remaining_time[i]){
            flag = 1;
            break;
        }
    }
    for(var i=0;i<upcoming_time.length;i++){
        if(serverTime <= upcoming_time[i]){
            flag = 1;
            break;
        }
    }
    var one_second = 1000;
    if(flag == 1){
        var t = setTimeout(function() {
            getRestTime();
        }, one_second);
    }
}
