/**
 * Constructs the sentiment time series graph
 * @param timeSeriesData JSON data containing the sentiment ratings for each date
 */
function makeGraph(timeSeriesData) {
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 60, left: 60},
        width = 1000 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#timeSeriesGraph")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Reformat graph data
    var data = []
    var i;
    for (i = 0; i < (timeSeriesData.dates).length; i++) {
        data.push({
            date: d3.timeParse("%m/%d")(timeSeriesData.dates[i]),
            dem: timeSeriesData.dem[i],
            rep: timeSeriesData.rep[i]
        });
    }

    // Add X axis
    var x = d3.scaleTime()
        .domain(d3.extent(data, function (d) {
            return d.date
        }))
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(data.length));

    // text label for the x axis
  svg.append("text")
      .attr("transform",
            "translate(" + (width/2) + " ," +
                           (height + margin.top + 40) + ")")
      .style("text-anchor", "middle")
      .style("font-size", "24px")
      .text("Date");

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([d3.min(data, function (d) {
            return Math.min(d.rep, d.dem);
        }), d3.max(data, function (d) {
            return Math.max(d.rep, d.dem);
        })])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // text label for the y axis
  svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .style("font-size", "24px")
      .text("Avg Sentiment");

    // Add democratic points
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function (d) {
                return x(d.date)
            })
            .y(function (d) {
                return y(d.dem)
            })
        )

    // Add republican points
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function (d) {
                return x(d.date)
            })
            .y(function (d) {
                return y(d.rep)
            })
        )


}