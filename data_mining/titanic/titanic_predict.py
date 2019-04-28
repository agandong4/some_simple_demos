#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: titanic_predict.py
@time: 2019-04-24 20:00
@desc:kaggle 泰坦尼克号预测
'''
import graphviz
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn import tree
def data_explore(train,test):
    print('-'*40)
    print(train.info)
    print('-'*40)
    print(train.describe())
    print('-'*40)
    # print(train.describe(include=['o']))
    print('-'*40)
    print(train.head())
    print('-'*40)
    print(train.tail)

def clean_data(train,test):
    """
    如何处理缺失值是重中之重,特征工程
    :param train:
    :param test:
    :return:
    """
    train['Age'].fillna(train['Age'].mean(),inplace=True)
    test['Age'].fillna(test['Age'].mean(),inplace=True)

    train['Fare'].fillna(train['Fare'].mean(), inplace=True)
    test['Fare'].fillna(test['Fare'].mean(), inplace=True)

    train['Embarked'].fillna('S',inplace=True)
    test['Embarked'].fillna('S',inplace=True)
    # 特征选取
    features =['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']
    train_f = train[features]
    train_l = train['Survived']
    test_f = test[features]

    dvec = DictVectorizer(sparse=False)
    train_f = dvec.fit_transform(train_f.to_dict(orient='record'))
    test_f = dvec.fit_transform(test_f.to_dict(orient='record'))


    return train_f,train_l,test_f

def predict(train_features,train_labels,test_f,**test_l):
    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(train_features,train_labels)

    pred_l = clf.predict(test_f)
    # dot_data = tree.export_graphviz(clf,out_file=None)
    # graph = graphviz.Source(dot_data)
    # graph.view()
    # acc_decision_tree = round(np.mean(cross_val_score(clf,test_f,test_l,cv=10)),6)
    return pred_l
def visual():
    # # 模块6: 决策树可视化
    # from sklearn import tree
    # import pydotplus
    # from sklearn.externals.six import StringIO
    # dot_data = StringIO()
    # tree.export_graphviz(clf, out_file=dot_data)
    # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    # graph.write_pdf("Titanic.pdf")
    pass

def main():
    # load the data
    train_data = pd.read_csv('./train.csv')
    test_data = pd.read_csv('./test.csv')
    data_explore(train_data,test_data)
    train_f,train_l,test_f = clean_data(train_data,test_data)
    pred_l = predict(train_f,train_l,train_f)
    pred_l = pred_l.astype(int)
    passenger_id = test_f['']
    # print(u'ID3 决策树 score 准确率为 %.4lf' % pred_acc)

if __name__ == '__main__':
    main()