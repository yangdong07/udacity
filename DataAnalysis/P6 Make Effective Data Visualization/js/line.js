function drawLine(data) {

  "use strict";

  // 数据预处理
  var format = d3.time.format("%Y-%m-%d %H:%M:%S");
  var yearmonth = d3.time.format("%Y-%m");
  // data.forEach(function(d) {
  //   d.date = yearmonth(format.parse(d.LoanOriginationDate));
  //   d.LoanAmount = +d.LoanOriginalAmount;
  //   d.count = 1;
  // });

  var agg_data = data.reduce(function(ad, d) {
    var date = yearmonth(format.parse(d.LoanOriginationDate));
    if (date in ad) {
      ad[date] += (+d.LoanOriginalAmount);
    } else {
      ad[date] = (+d.LoanOriginalAmount);
    }
    return ad;
  }, {})

  var data_array = Object.keys(agg_data).map(function(key) {
    return {
      date: key,
      LoanAmount: agg_data[key]
    };
  });

  // debugger;


  // 创建svg
  var svg = dimple.newSvg("body", 1400, 900);
  svg.append("text")
    .attr("x", (svg[0][0].clientWidth / 2))
    .attr("y", 50)
    .attr("text-anchor", "middle")
    .style("font-size", "24px")
    .style("font-weight", "bold")
    .text("Loan Original Amount");

  // 创建chart
  var myChart = new dimple.chart(svg, data_array);
  myChart.setMargins("10%", "10%", "10%", "20%");

  var x = myChart.addTimeAxis("x", "date");
  x.dateParseFormat = "%Y-%m";
  x.tickFormat = "%Y-%m";
  x.timeInterval = 1;
  x.title = "Loan Origination Date (Month)"
  x.fontSize = 15;
  var y = myChart.addMeasureAxis("y", "LoanAmount");
  y.fontSize = 15;
  y.title = "Loan Original Amount ($)"
  myChart.addSeries(null, dimple.plot.line);
  myChart.addSeries(null, dimple.plot.scatter);
  myChart.draw();



  // //
  // var myChart = new dimple.chart(svg, data);
  // myChart.setMargins("10%", "10%", "10%", "20%");
  // var x = myChart.addCategoryAxis("x", "date");
  // x.addOrderRule("Date");
  // x.title = "Loan Origination Date";
  // x.fontSize = 20;
  // var y = myChart.addMeasureAxis("y", "LoanAmount");
  // y.title = "Total Original Amount per Mounth ($)"
  // y.fontSize = 15;
  //
  // var cleanAxis = function(axis, oneInEvery) {
  //   // modify x, y axis
  //   // This should have been called after draw, otherwise do nothing
  //   if (axis.shapes.length > 0) {
  //     // Leave the first label
  //     var del = 0;
  //     // If there is an interval set
  //     if (oneInEvery > 1) {
  //       // Operate on all the axis text
  //       axis.shapes.selectAll("text").each(function(d) {
  //         d3.select(this).attr("opacity", 1).style("font-size", "15px");
  //         // Remove all but the nth label
  //         if (del % oneInEvery !== 0) {
  //           d3.select(this).attr("opacity", 0);
  //         }
  //         del += 1;
  //       });
  //     }
  //   }
  // };
  //
  // var s = myChart.addSeries(null, dimple.plot.line)
  // s.afterDraw = function() {
  //   cleanAxis(x, 6);
  // };
  // myChart.addSeries(null, dimple.plot.scatter);;
  // myChart.draw();

};
