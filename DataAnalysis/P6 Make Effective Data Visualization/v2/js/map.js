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

  // 数据按年分组
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
        amount: v.values.LoanAmount / 1e6,
        avg: Math.round(v.values.LoanAmount / count),
      };
      amounts.push(v.values.LoanAmount / 1e6);
    });
    statisticData[d.key] = yearData;
  });

  var max_amount = d3.max(amounts);
  var median_amount = d3.median(amounts);
  var min_amount = d3.min(amounts);
  var color_scale = d3.scale.linear()
    .domain([min_amount, max_amount])
    .range(['white', 'blue']);

  // debugger;

  // 根据年份绘制地图
  function update(year) {
    d3.select("#title").text("Loan Amount Distribution in " + year);
    uStates.draw("#main-svg", statisticData[year], color_scale);
    d3.select(self.frameElement).style("height", "600px");
  }

  // debugger;
  update(2005);

  // 设置定时器，定时出发更新年份； 结束后插入button组
  var years = d3.range(2005, 2015);
  var year_idx = 1;
  var year_interval = setInterval(function() {
    update(years[year_idx]);
    year_idx++;
    if (year_idx >= years.length) {
      clearInterval(year_interval);

      var buttons = d3.select("body")
        .append("div")
        .attr("class", "years_buttons")
        .selectAll("button")
        .data(years)
        .enter()
        .append("button")
        .text(function(d) {
          return d;
        });

      buttons.on("click", function(d) {
        d3.select(".years_buttons")
          .selectAll("button")
          .transition()
          .duration(500)
          .style("color", "black")
          .style("background", "rgb(251, 201, 127)");

        d3.select(this)
          .transition()
          .duration(500)
          .style("background", "lightBlue")
          .style("color", "white");
        update(d);
      });
    }
  }, 1500);

  // debugger;

  // 绘制 legend
  var legendFullHeight = 400;
  var legendFullWidth = 130;
  var legendMargin = {
    top: 20,
    bottom: 20,
    left: 5,
    right: 100
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

  // clear current legend
  legendSvg.selectAll('*').remove();
  // append gradient bar
  var gradient = legendSvg.append('defs')
    .append('linearGradient')
    .attr('id', 'gradient')
    .attr('x1', '0%') // bottom
    .attr('y1', '100%')
    .attr('x2', '0%') // to top
    .attr('y2', '0%')
    .attr('spreadMethod', 'pad');

  var colourPct = d3.zip(["0%", "100%"], ['white', 'blue']);

  colourPct.forEach(function(d) {
    gradient.append('stop')
      .attr('offset', d[0])
      .attr('stop-color', d[1])
      .attr('stop-opacity', 1);
  });

  legendSvg.append('rect')
    .attr('x1', 0)
    .attr('y1', 0)
    .attr('width', legendWidth)
    .attr('height', legendHeight)
    .style('fill', 'url(#gradient)');

  // create a scale and axis for the legend
  var legendScale = d3.scale.linear()
    .domain([min_amount, max_amount])
    .range([legendHeight, 0]);

  var legendAxis = d3.svg.axis()
    .scale(legendScale)
    .orient("right")
    // .tickValues(d3.range(0, 100, 10))
    .tickValues([min_amount, (max_amount + min_amount) / 2, max_amount])
    .tickFormat(function(d) {
      return "$" + Math.round(d) + " million";
    });

  legendSvg.append("g")
    .attr("class", "legend axis")
    .attr("transform", "translate(" + legendWidth + ", 0)")
    .call(legendAxis);


}
