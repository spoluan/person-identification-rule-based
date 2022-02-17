# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 15:26:27 2019

@author: Sevendi Eldrige Rifki Poluan
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

add = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\Person identification\\Accuracy'
file = os.listdir(add)

spec = '{}/{}' . format(add, file[0])
dataframe = pd.read_csv(spec)
split = dataframe['Split'].values.tolist()

data = []
for i in range(len(file)):
    spec = '{}/{}' . format(add, file[i])
    dataframe = pd.read_csv(spec)
    data.append(dataframe['Accuracy'].values.tolist())

fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(data)):
    ax.plot(data[i], 'o-')

ax.set_xticklabels(split)

for i in range(len(file)):
    file[i] = file[i].replace('.csv', '')
    
ax.legend((file), loc='lower right') # upper left, right, best, upper right, upper center, lower center, center, center left, lower left, lower right, center right
plt.show()