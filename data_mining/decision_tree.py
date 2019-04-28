#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: decision_tree.py
@time: 2019-04-23 22:05
@desc:
'''
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,mean_squared_error,r2_score,mean_absolute_error,mean_squared_log_error
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.datasets import load_iris,load_boston
from sklearn.tree import export_graphviz
import graphviz

def cart_tree():
    # load datasets
    iris = load_iris()
    # get feature_sets and classifier_labels
    features = iris.data
    labels = iris.target
    # set 33% of datasets as test_sets ,others as train_sets
    train_f, test_f, train_l, test_l = train_test_split(features,labels,test_size=0.3,random_state=0)
    # cart classification tree
    clf = DecisionTreeClassifier(criterion='gini')
    # using cart classification tree to predict
    clf = clf.fit(train_f,train_l)
    test_p = clf.predict(test_f)
    # comparing with test_sets
    score = accuracy_score(test_l,test_p)
    print("cart 分类树准确率 %.4lf"%score)

def boston_predict():
    boston = load_boston()
    fts = boston.data
    prs = boston.target

    f_train, f_test, p_train, p_test = train_test_split(fts,prs,test_size=0.3)

    dtr = DecisionTreeRegressor()
    dtr.fit(f_train,p_train)

    p_predict = dtr.predict(f_test)
    print('回归树二乘偏差均值:', mean_squared_error(p_test,p_predict))
    print('回归树绝对值偏差均值:', mean_absolute_error(p_test,p_predict))
    draw_tree(dtr)

def draw_tree(dtr):
    dot_data = export_graphviz(dtr,out_file=None)
    graph = graphviz.Source(dot_data)
    # render 方法会在同级目录下生成 Boston PDF文件，内容就是回归树。
    graph.render('Boston')


def main():
    cart_tree()
    boston_predict()


if __name__ == '__main__':
    main()