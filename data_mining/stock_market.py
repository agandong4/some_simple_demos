#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: stock_market.py
@time: 2019-04-24 22:13
@desc:
'''

import tushare as ts
from sklearn.linear_model import LinearRegression
data = ts.get_hist_data("601398")
# print(data)
xtrain = []
ytrain = []

for i in range(10,data.shape[0]):
    tmp = []
    tmp.append(data.iloc[i]['open'])
    tmp.append(data.iloc[i]['high'])
    tmp.append(data.iloc[i]['close'])
    tmp.append(data.iloc[i]['low'])
    xtrain.append(tmp)
    tmp2 = (data.iloc[i]['close']-data.iloc[i]['open'])/data.iloc[i]['open']
    ytrain.append(tmp)

xtest = xtrain[:10]

# print(xtrain.shape())
# print(ytrain.shape())

linreg = LinearRegression()
linreg.fit(xtrain,ytrain)

ypred = linreg.predict(xtest)

print(ypred)