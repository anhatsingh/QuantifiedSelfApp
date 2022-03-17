function create_line_chart(name, chart_data, xkey, ykeys, labels){
    new Morris.Line({
        // ID of the element in which to draw the chart.
        element: name,
        // Chart data records -- each entry in this array corresponds to a point on
        // the chart.
        data: chart_data,
        // The name of the data record attribute that contains x-values.
        xkey: xkey,
        // A list of names of data record attributes that contain y-values.
        ykeys: ykeys,
        // Labels for the ykeys -- will be displayed when you hover over the
        // chart.
        labels: labels,
        parseTime: false
      });
}


function create_donut_chart(name, chart_data){
    new Morris.Donut({
        // ID of the element in which to draw the chart.
        element: name,
        // Chart data records -- each entry in this array corresponds to a point on
        // the chart.
        data: chart_data
      });
}