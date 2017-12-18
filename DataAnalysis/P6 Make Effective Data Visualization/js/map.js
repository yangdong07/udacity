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

  function statistic(leaves) {
    return {
      'count': d3.sum(leaves, function(d) {
        return 1;
      }),
      'LoanAmount': d3.sum(leaves, function(d) {
        return d.LoanAmount;
      }),
    };
  }

  var nested = d3.nest()
    .key(function(d) {
      return d['BorrowerState'];
    })
    .rollup(statistic)
    .entries(data);

  var year_nested = d3.nest()
    .key(function(d) {
      return d['date'].getUTCFullYear();
    })
    .key(function(d) {
      return d['BorrowerState'];
    })
    .rollup(statistic)
    .entries(data);

  // debugger;

  var statisticData = {}; /* Sample random data. */
  var amounts = [];

  year_nested.forEach(function(d) {
    var yearData = {};
    d.values.forEach(function(v) {
      var count = v.values.count,
        amount = v.values.LoanAmount;
      yearData[v.key] = {
        count: v.values.count,
        amount: v.values.LoanAmount,
        avg: Math.round(v.values.LoanAmount / count),
        // color: d3.interpolate("#ffffcc", "#800026")(count / 10000)
      };
      amounts.push(v.values.LoanAmount);
    });
    statisticData[d.key] = yearData;
  });

  var max_amount = d3.max(amounts);
  var median_amount = d3.median(amounts);
  var min_amount = d3.min(amounts);
  var color_scale = d3.scale.linear()
    .domain([0, max_amount])
    .range(['beige', 'red']);
  // .domain([min_amount, median_amount, max_amount])
  // .range(['blue', 'beige', 'red']);

  // debugger;

  // nested.forEach(function(d) {
  //   var count = d.values.count,
  //     amount = d.values.LoanAmount;
  //   sampleData[d.key] =
  //     count: count,
  //     amount: (amount / 1000000).toFixed(2),
  //     avg: Math.round(amount / count),
  //     color: d3.interpolate("#ffffcc", "#800026")(count / 10000)
  //   };
  // });

  // debugger;

  function tooltipHtml(n, d) { /* function to create html content string in tooltip div. */
    if (d) {
      return "<h4>" + n + "</h4><table>" +
        "<tr><td>Amount</td><td>$" + (d.amount / 1000000).toFixed(2) + "m</td></tr>" +
        "<tr><td>Count</td><td>" + (d.count) + "</td></tr>" +
        "<tr><td>Average</td><td>" + (d.avg) + "</td></tr>" +
        "</table>";
    } else {
      return "<h4>" + n + "</h4><table>";
    }
  }

  /* draw states on id #statesvg */
  uStates.draw("#main-svg", statisticData['2013'], color_scale, tooltipHtml);

  d3.select(self.frameElement).style("height", "600px");

  // add the legend now
  var legendFullHeight = 400;
  var legendFullWidth = 50;
  var legendMargin = {
    top: 20,
    bottom: 20,
    left: 5,
    right: 20
  };
  // use same margins as main plot
  var legendWidth = legendFullWidth - legendMargin.left - legendMargin.right;
  var legendHeight = legendFullHeight - legendMargin.top - legendMargin.bottom;

  var legendSvg = d3.select('#legend-svg')
    .attr('width', legendFullWidth)
    .attr('height', legendFullHeight)
    .append('g')
    .attr('transform', 'translate(' + legendMargin.left + ',' +
      legendMargin.top + ')');

  legendSvg.append('rect')
    .attr('x1', 0)
    .attr('y1', 0)
    .attr('width', legendWidth)
    .attr('height', legendHeight)
    .style('fill', 'url(#gradient)');

}
