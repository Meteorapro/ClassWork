# 鸢尾花数据集二分类任务
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 用于显示进度条信息
from tqdm import tqdm

## logistic函数
def f(x,sita):
    return 1.0/(1+np.exp(-np.dot(x,sita)))

## 损失函数
def loss_function(x,sita,y):
    return y*np.log(f(x,sita))+(1.0-y)*np.log(1-f(x,sita))

# 读入鸢尾花数据集
data_iris = pd.read_csv("shuffle.data", header=None)

# 将分类变量转化为数值变量
data_iris[4] = data_iris[4].replace({'Iris-setosa':0, 'Iris-versicolor':1})

# 划分训练集和测试集，前九千为训练集，后一千为验证集
train_data  = data_iris.iloc[0:9001]
test_train  = data_iris.iloc[9001:]

# 记录损失值的列表
loss_data = []

# 初始化sita
sita = [0.0,0.0,0.0,0.0]

# 学习率设置
learn_rate = 0.001

## 训练过程
for i in tqdm(range(len(train_data)),):
    x = np.array(train_data.iloc[i,:4])
    y = np.array(train_data.iloc[i,4])
    loss = loss_function(x,sita,y)
    loss_data.append(loss)
    ## 更新sita
    sita = sita + learn_rate*(y-f(x,sita))*x

plt.plot(loss_data)
plt.show()

# 输出sita参数
print(sita)

scores = 0
for i in range(len(test_train)):
    x = np.array(test_train.iloc[i, :4])
    y = np.array(test_train.iloc[i, 4])
    f_1 = f(x, sita)

    if f_1 >= 0.5:
        f_1 = 1.0
    else:
        f_1 = 0.0
    if y == f_1:
        scores += 1

print('模型在验证集上的精确程度为:')
print(scores / len(test_train))