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
var plot_piechart;
var confirm_change_userlevel;
$(function() {
  plot_piechart = function(data) {
    var statisticsTotal = 0;
    for (var i = 0; i < data.length; i++) {
      statisticsTotal += data[i].value;
      // Generate random color to each data
      data[i].color = "#" + Math.random().toString(16).slice(2, 8);
    }
    var ctx = $("#piechart").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var pieChart = new Chart(ctx).Pie(data, {
      legendTemplate: '<ul class="pie-legend">' +
        '<% for (var i=0; i<segments.length; i++){%><li>' +
        '<span style="background-color:<%=segments[i].fillColor%>"></span>' +
        '<%if(segments[i].label){%><%=segments[i].label%>: <%=segments[i].value%><%}%>' +
        '</li><%}%></ul>'
    });
    var legend = pieChart.generateLegend();
    $("#piechart-legend").html(legend);
    if (statisticsTotal == 0) {
      // If no statistics available, appear this notification.
      $('#statistics').html('No statistics yet.');
    }
  }

  confirm_change_userlevel = function() {
    return confirm('Are you sure you want to change ' +
      $('#id_username').val() + ' to ' +
      $("#id_user_level option:selected" ).text() + '?')
  }
})
