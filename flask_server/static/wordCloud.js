// set the dimensions and margins
var margin = {top: 10, right: 10, bottom: 10, left: 10},
width = 500 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom;

// global variables used to store the svg and cloud layout objects
var svgDem;
var layoutDem;
var svgRep;
var layoutRep;


/**
 * Constructs the word clouds
 * @param dem Democratic word data
 * @param rep Republican word data
 */
function call_layout(dem, rep) {
    // append the svg objects to the respective div
    svgDem = d3.select("#demWordCloud").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    svgRep = d3.select("#repWordCloud").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    // factor used to scaled the font sizes of the words
    var scaleFactorDem = 75/dem[0].size;
    var scaleFactorRep = 75/rep[0].size;

    // create new cloud layouts
    layoutDem = d3.layout.cloud()
    .size([width, height])
    .words(dem)
    .padding(5)
    .rotate(function() { return ~~(Math.random() * 2) * 90; })
    .font("Impact")
    .fontSize(function(d) { return d.size * scaleFactorDem; })
    .on("end", drawDem);

    layoutRep = d3.layout.cloud()
    .size([width, height])
    .words(rep)
    .padding(5)
    .rotate(function() { return ~~(Math.random() * 2) * 90; })
    .font("Impact")
    .fontSize(function(d) { return d.size * scaleFactorRep; })
    .on("end", drawRep);

    // build the word cloud layouts
    layoutDem.start();
    layoutRep.start();
}

/**
 * Draws democratic words onto the layout
 * @param word Democratic words inserted into the layout
 */
function drawDem(words) {
    svgDem.append("g")
      .attr("transform", "translate(" + layoutDem.size()[0] / 2 + "," + layoutDem.size()[1] / 2 + ")")
        .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("fill", "#4682B4")
      .style("font-family", "Impact")
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.word; });
}

/**
 * Draws republican words onto the layout
 * @param word Republican words inserted into the layout
 */
function drawRep(words) {
    svgRep.append("g")
      .attr("transform", "translate(" + layoutRep.size()[0] / 2 + "," + layoutRep.size()[1] / 2 + ")")
        .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("fill", "#FF0000")
      .style("font-family", "Impact")
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.word; });
}