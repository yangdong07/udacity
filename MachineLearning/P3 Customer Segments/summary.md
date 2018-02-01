# 项目总结

数据集包含很多客户针对不同类型产品的年度采购额（用金额表示）。
这个项目的任务之一是根据这些数据，将客户分为不同的类型。 属于非监督学习任务，从数据中寻找模式。

关键词：
- 非监督学习
- 创建用户分类
- 聚类算法（K-means，高斯混合模型）
- 特征工程，特征相关性
- PCA 降维
- 分析数据集内在结构、模式


## 流程

机器学习一般流程也就是：
1. 获取数据，分析数据，清洗数据，预处理，特征工程
2. 选择合适的算法，训练模型
3. 数据知识挖掘


## 知识点

### 【X】决策树回归CART
CART： Classification and Regression Tree
决策树不仅可以用来分类（Classification），还可以用来做回归（regression）。具体方法不清楚。

### 【O】回归拟合评分，R2的意义

可以参考PCA，或者PCA参考这个。 R2表示Y的方差有多少可以用X的方差解释，以此判断统计模型的解释力。

explained variance

### 【O】特征相关性分析

有些特征相关性较强，可以通过PCA降维

### 【X】散布矩阵（scatter matrix）

散步矩阵对角线上面是pdf？？

### 【O】特征缩放

### 【O】异常值检测
[Tukey的定义异常值的方法](http://datapigtechnologies.com/blog/index.php/highlighting-outliers-in-your-data-with-the-tukey-method/)

### 【O】PCA，主成分分析， 解释方差比


### 【X】双标图？
### 【O】聚类算法
#### 【O】K-means
#### 【O】高斯混合模型， EM算法

#### 【X】轮廓系数


### 【X】A/B test
大概知道方法。没仔细看。

https://en.wikipedia.org/wiki/A/B_testing

## Review

### Review1

1. 解释样本点以及聚类后的中心点，需要基于数据的统计特征来分析。大概是分析消费水平（平均水平、中位数水平等），和主要消费产品。

2. 关于异常点，去掉多维异常点，保留一维的异常点。主要原因是数量较多，影响较小，希望保留更多信息。
