#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: handwriting_digits.py
@time: 2019-04-24 18:44
@desc:
'''

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from numpy import linspace

def digits_classifier(SIZE):
    digits = load_digits()
    f = digits.data
    l = digits.target

    train_f, test_f, train_l, test_l = train_test_split(f,l,test_size=SIZE,random_state=0)
    clf = DecisionTreeClassifier(criterion='gini')

    clf = clf.fit(train_f,train_l)
    test_p = clf.predict(test_f)
    scores = accuracy_score(test_l,test_p)
    # print("cart 分类树准确率 %.4lf" % scores)
    return scores

def main():
    x = list(linspace(0.05,1,100,endpoint=False))
    y = [0]*len(x)
    times = 20
    for time in range(times):
        print("-"*40)
        print(f"the {time+1} times")
        for i,num in enumerate(x):
            y[i] += digits_classifier(num)
    avg_y = list(map(lambda x:x/times,y))
    plt.plot(x,avg_y)
    plt.show()

if __name__ == '__main__':
    main()