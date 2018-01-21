

# 项目总结

这个项目使用1994年美国人口普查收集的数据，选用几个监督学习算法以准确地建模被调查者的收入。

目标是建立一个能够准确地预测被调查者年收入是否超过50000美元的模型。

关键词：监督学习；分类问题

## 过程

1. 探索数据，获取特征和标签
2. 特征工程： 对一些分布奇怪的特征做处理（capital-gain和capital-loss），
3. 归一化数字特征.
4. 非数字特征/category类型特征， One-Hot Encoding。
5. 混洗、切分数据： 训练集、验证集、测试集
6. Naive Classifier：即对所有输入预测一种结果。作为分类器的baseline
7. 监督学习模型
  1. 高斯朴素贝叶斯
  2. 决策树
  3. 集成方法
  4. K近邻
  5. 随机梯度下降分类器（SGDC），这个实际是GDC的一种方式
  6. 支持向量机（SVM)
  7. Logistic回归
8. 从训练时间和模型评分角度选择一个合适的算法模型
9. 模型调优： GridSearchCV， RandomSearchCV
10. 特征重要性，可以从AdaBoost分类器的 `feature_importances_` 得到。这里需要注意的是，由于One-Hot Encoding，一些category特征被打散了。

以建立一个能够准确预测的模型为目的，其实还是跟数据分析那一套差不多，大致分为几步：
1. 初步分析数据、探索数据、做一些数据预处理
2. 选择合适的算法模型， **训练调参**
3. 从模型中获取一些知识，比如 特征重要性排序。

## 知识点

### 1. [UCI机器学习知识库](https://archive.ics.uci.edu/ml/datasets/Census+Income)

这个数据集是由Ron Kohavi和Barry Becker在发表文章"Scaling Up the Accuracy of Naive-Bayes Classifiers: A Decision-Tree Hybrid"之后捐赠的，你可以在Ron Kohavi提供的[在线版本](https://www.aaai.org/Papers/KDD/1996/KDD96-033.pdf)中找到这个文章。我们在这里探索的数据集相比于原有的数据集有一些小小的改变，比如说移除了特征`'fnlwgt'` 以及一些遗失的或者是格式不正确的记录。

### 2. 知识点

一些知识点：

- <a href="https://en.wikipedia.org/wiki/Data_transformation_(statistics)">对数转换</a>
- 归一化数字特征， [`sklearn.preprocessing.MinMaxScaler`](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
- 独热编码[`pandas.get_dummies()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html?highlight=get_dummies#pandas.get_dummies)
- 评分： F-beta score，这个主要是权衡 precision和recall指标。
- GridSearchCV， RandomizedSearchCV


没搞明白的，需要进一步理解
- 高斯朴素贝叶斯（GaussianNB），基于朴素贝叶斯分类器理论
- 决策树（DecisionTree），原理， ID3，CART算法
- 集成方法（AdaBoost），基本原理可以说上来，并不熟悉
- K近邻，需要复习一下
- 随机梯度下降分类器（SGDC），这个没啥
- 支持向量机（SVM），不懂原理。
- Logistic回归，比较简单。



## Review

### Review1

1. 一些小错误

2. 建议用 [随机调参](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html) 方式调参。参考[论文](http://www.jmlr.org/papers/volume13/bergstra12a/bergstra12a.pdf)

3. 一个概念上的错误： education-level经过独热编码后被打散成多个特征。在用AdaBoost训练时，这些小特征的重要性就排不上号了。 education-num 实际上是education-level的 LabelEncoding， 二者是完全相关的。

### Review2 通过及建议

1. [资源](https://www.datacamp.com/community/data-science-cheatsheets?page=3)

2. [字典](https://www.analyticsvidhya.com/glossary-of-common-statistics-and-machine-learning-terms/#one)

3. [sklearn gallery](http://scikit-learn.org/stable/auto_examples/index.html)

4. [sklearn 算法地图](http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html)

5. 建议用随机抽样的方式选取 1%， 10%， 100%的数据训练

6. 使用直方图观察 education-num 对分类标签的影响。
