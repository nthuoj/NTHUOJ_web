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
