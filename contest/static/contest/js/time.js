< script >
    function startTime() {
        var today = new Date();
        var h = today.getHours();
        var m = today.getMinutes();
        var s = today.getSeconds();
        m = checkTime(m);
        s = checkTime(s);
        document.getElementById('clock').innerHTML = h + ":" + m + ":" + s;
        var t = setTimeout(function() {
            startTime()
        }, 500);
    }

function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }; // add zero in front of numbers < 10
    return i;
}

function getRestTime(start, end) {
    if (Date.now() < end.getTime()) {
        var result = (end.getTime() - Date.now()) / 1000;
        var s = parseInt(result % 60);
        result /= 60;
        var m = parseInt(result % 60);
        result /= 60;
        var h = parseInt(result % 60);
        m = checkTime(m);
        s = checkTime(s);
        h = checkTime(h);
        var percentage = (Date.now() - start.getTime()) / (end.getTime() - start.getTime());
        document.getElementById('clock').innerHTML = h + ":" + m + ":" + s;
        document.getElementById('timeline').style.width = percentage * 100 + "%";
        var t = setTimeout(function() {
            getRestTime()
        }, 500);
    } else {
        document.getElementById('timeline').style.width = "100%";
        document.getElementById('clock').innerHTML = "Contest Ended";
    }
} < /script>