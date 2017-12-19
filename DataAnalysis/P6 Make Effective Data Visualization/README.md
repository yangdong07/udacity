

# 概要

Prosper是一个P2P借贷平台。这个可视化项目展示了Prosper借贷平台从2005年到2014年的贷款总额在美国各州的分布趋势

# 设计

在P4项目中做的就是对Prosper数据的EDA分析，有观察到美国各州的借贷人数分布，因此希望演示借贷数额随着年份的变化在美国各州的分布变化情况。

类似于世界杯地图中那样，绘制美国各州地图，以每年借贷数额对应一种color，来显示出各州贷款总额的分布变化情况。

根据反馈所做的修改：

1. 添加legend，参考了 [color legend](https://bl.ocks.org/starcalibre/6cccfa843ed254aa0a0d)

2. 鼠标悬浮时显示详细数据，参考 [美国地图](http://bl.ocks.org/NPashaP/a74faf20b492ad377312)

3. 关于颜色区分不明显这一点，在v3版本中，感觉上已经能很好的反映出几个主要州的变化。其他州虽然变化较小，但也能勉强观察出，另外也反应了这些州的贷款并不活跃。这是数据的真实表现。 我尝试了一些其他方案，比如将 color scale 从线性的改成了log scale； 参考使用 mix-hue的color scheme（[color brewer](http://colorbrewer2.org/#type=sequential&scheme=GnBu&n=7)） ；取所有数据的中位数（median）对应分割色； 得到最终版本。虽然区分更为明显，但是似乎有些失真。


# 反馈

1. 缺少颜色数值的图例。

2. 颜色辨识度不高，考虑进一步提供数据信息，比如用鼠标悬浮显示的方式，方便读者获取信息。

3. 颜色区分不明显，除了个别州的变化较明显（如加州、德州等）外，其他州的变化几乎观察不到。


# 参考资源

- [美国地图](http://bl.ocks.org/NPashaP/a74faf20b492ad377312)
- [color legend](https://bl.ocks.org/starcalibre/6cccfa843ed254aa0a0d)
- [color brewer](http://colorbrewer2.org/#type=sequential&scheme=GnBu&n=7)


# 说明
simple.py是处理原始数据的脚本文件，只取了LoanOriginalAmount,LoanOriginationDate,BorrowerState三个字段。

在当前目录下启动python server：  `python -m SimpleHTTPServer 8000`

数据文件是共享的。对应各个版本的访问路径：

http://127.0.0.1:8000/v1/index.html

http://127.0.0.1:8000/v2/index.html

http://127.0.0.1:8000/v3/index.html

http://127.0.0.1:8000/last/index.html
