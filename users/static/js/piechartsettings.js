$(function() {
    /*
     * insert fake data for demo use
     */
    function labelFormatter(label, series) {
        return "<div style='font-size:10pt; text-align:center; padding:2px; color:black;'>" + label + "<br/>" + Math.round(series.percent) + "%</div>";
    }
    var type = ["WA", "AC", "RE", "TLE", "MLE", "OLE", "Others"];
    var data = [],
        series = 7;

    for (var i = 0; i < series; i++) {
        data[i] = {
            label: type[i],
            data: Math.floor(Math.random() * 100) + 50
        }
    }
    
    var placeholder = $("#placeholder");
    $.plot(placeholder, data, {
        series: {
            pie: {
                show: true,
                radius: 180,
                label: {
                    show: true,
                    radius: 0.6,
                    formatter: labelFormatter,
                    background: {
                        opacity: 0
                    }
                }
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        }
    });

    placeholder.bind("plotclick", function(event, pos, obj) {

        if (!obj) {
            return;
        }
        var percent = parseFloat(obj.series.percent).toFixed(2);

        var w = window.open("/status");
    });
})