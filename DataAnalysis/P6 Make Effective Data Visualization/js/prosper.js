function drawLine(data) {

  "use strict";
  var format = d3.time.format("%Y-%m-%d %H:%M:%S");
  var yearmonth = d3.time.format("%Y-%m");
  data.forEach(function(d) {
    d.date = yearmonth(format.parse(d.LoanOriginationDate));
    d.LoanAmount = +d.LoanOriginalAmount;
  });

  // var nested = d3.nest()
  //   .key(function(d) {
  //     return d['date'].getUTCFullYear();
  //   })
  //   .rollup(function(leaves) {
  //     var total = d3.sum(leaves, function(d) {
  //       return d['LoanAmount'];
  //     });
  //     return {
  //       'LoanAmount': total,
  //     };
  //   })
  //   .entries(data);
  // var total = data.reduce(function(t, d) {
  //   var ym = d.date.getUTCFullYear();
  //   if (ym in t) {
  //     t[ym] += d.LoanAmount;
  //   } else {
  //     t[ym] = d.LoanAmount;
  //   }
  //   return t;
  // }, {});
  //
  // var agg_data = Object.keys(total).map(function(key) {
  //   return {
  //     date: key,
  //     LoanAmount: total[key]
  //   };
  // });
  //
  // debugger;

  var svg = dimple.newSvg("body", 1400, 800);
  var myChart = new dimple.chart(svg, data);
  // myChart.setBounds(60, 30, 505, 305);
  var x = myChart.addCategoryAxis("x", "date");
  x.addOrderRule("Date");
  myChart.addMeasureAxis("y", "LoanAmount");
  var s = myChart.addSeries(null, dimple.plot.line)
  myChart.addSeries(null, dimple.plot.scatter);;
  myChart.draw();

  // //myChart.setBounds(80, 40, "75%", "60%");
  // var x = myChart.addTimeAxis("x", "date", "%Y", "%y");
  // x.showGridlines = true;
  // var y = myChart.addMeasureAxis("y", "Loan Amount");
  // y.showGridlines = true;
  // var s = myChart.addSeries(null, dimple.plot.line, [x, y]);
  // // s.lineWeight = 4;
  // //s.lineMarkers=true;
  // myChart.draw();

  // debugger;
  // var margin = 75,
  //   width = 1400 - margin,
  //   height = 700 - margin;
  //
  // d3.select("body")
  //   .append("h2")
  //   .text("Prosper LoanOriginalAmount")
  //
  // var svg = d3.select("body")
  //   .append("svg")
  //   .attr("width", width + margin)
  //   .attr("height", height + margin)
  //   .append('g')
  //   .attr('class', 'chart');
  //
  // /*
  //   Dimple.js Chart construction code
  // */
  //
  // var time_scale = d3.time.scale()
  //   .range([margin, width])
  //   .domain(d3.extent(data, function(d) {
  //     return d['date'];
  //   }))
  //
  // var amount_scale = d3.scale.linear()
  //   .range([height, margin])
  //   .domain(d3.extent(data, function(d) {
  //     return d['LoanAmount'];
  //   }))
  //
  // var time_axis = d3.svg.axis()
  //   .scale(time_scale)
  //   .ticks(d3.time.years, 1);
  //
  // d3.select("svg")
  //   .append('g')
  //   .attr('class', 'x axis')
  //   .attr('transform', "translate(0," + height + ")")
  //   .call(time_axis);
  //
  // var count_axis = d3.svg.axis()
  //   .scale(count_scale)
  //   .orient("left");
  //
  // d3.select("svg")
  //   .append('g')
  //   .attr('class', 'y axis')
  //   .attr('transform', "translate(" + margin + ",0)")
  //   .call(count_axis);
  //
  // debugger
  //
  // var nested = d3.nest()
  //   .key(function(d) {
  //     return d['date'].getUTCFullYear();
  //   })
  //   .rollup(function(leaves) {
  //     var total = d3.sum(leaves, function(d) {
  //       return d['LoanAmount'];
  //     });
  //     return {
  //       'LoanAmount': total,
  //     };
  //   })
  //   .entries(data);
  //
  // var myChart = new dimple.chart(svg, data);
  // var x = myChart.addTimeAxis("x", "date");
  // myChart.addMeasureAxis("y", "LoanAmount");
  // x.dateParseFormat = "%Y-%m-%d %H:%M:%S";
  // x.tickFormat = "%Y-%m";
  // x.timePeriod = d3.time.months;
  // x.timeInterval = 3;
  // myChart.addSeries(null, dimple.plot.line);
  // // myChart.addSeries(null, dimple.plot.scatter);
  // myChart.draw();
};
