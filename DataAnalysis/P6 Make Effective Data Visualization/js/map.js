function drawMap(data) {

  "use strict";

  // 数据预处理
  var format = d3.time.format("%Y-%m-%d %H:%M:%S");
  var yearmonth = d3.time.format("%Y-%m");
  data.forEach(function(d) {
    d.date = format.parse(d.LoanOriginationDate);
    d.LoanAmount = +d.LoanOriginalAmount;
    d.count = 1;
    // d.state = d.BorrowerState;
  });


  var nested = d3.nest()
    // .key(function(d) {
    //   return d['date'].getUTCFullYear();
    // })
    .key(function(d) {
      return d['BorrowerState'];
    })
    .rollup(function(leaves) {
      return {
        'count': d3.sum(leaves, function(d) {
          return 1;
        }),
        'LoanAmount': d3.sum(leaves, function(d) {
          return d.LoanAmount;
        }),
      };
    })
    .entries(data);

  debugger;

  var sampleData = {}; /* Sample random data. */

  nested.forEach(function(d) {
    var count = d.values.count,
      amount = d.values.LoanAmount;
    sampleData[d.key] = {
      count: count,
      amount: (amount / 1000000).toFixed(2),
      avg: Math.round(amount / count),
      color: d3.interpolate("#ffffcc", "#800026")(count / 10000)
    };
  });

  // debugger;

  function tooltipHtml(n, d) { /* function to create html content string in tooltip div. */
    return "<h4>" + n + "</h4><table>" +
      "<tr><td>Amount</td><td>$" + (d.amount) + "m</td></tr>" +
      "<tr><td>Count</td><td>" + (d.count) + "</td></tr>" +
      "<tr><td>Average</td><td>" + (d.avg) + "</td></tr>" +
      "</table>";
  }

  /* draw states on id #statesvg */
  uStates.draw("#statesvg", sampleData, tooltipHtml);

  d3.select(self.frameElement).style("height", "600px");

}
