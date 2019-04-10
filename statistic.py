import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D


def load_data_file(filename):
    if not os.path.exists(filename):
        print("Error! score file NOT Find!")
        return
    fo = open(filename, 'r')
    data = fo.read()
    fo.close()
    return data

def analys_data(data):
    analys_data = []
    split_data = data.split("|")
    for i, onedirect in enumerate(split_data):
        oneDirData = []
        data_1 = []
        data_2 = []
        data_3 = []
        split_data2 =  onedirect.split("\n")
        for _, pointData in enumerate(split_data2):
            realData = pointData.split(",")
            if len(realData)>=3:
                x = float(realData[0].strip())
                y = float(realData[1].strip())
                z = float(realData[2].strip())
                data_1.append(x)
                data_2.append(y)
                data_3.append(z)
        oneDirData.append(data_1)
        oneDirData.append(data_2)
        oneDirData.append(data_3)
        analys_data.append(oneDirData)
    return analys_data


def draw_data(ax, data):
    colors = ('tomato', 'red', 'darkcyan', 'chocolate', 'skyblue', 'steelblue', 'navy', 'purple')
    for i, point_array in enumerate(data):
        #for _, point in enumerate(point_array):
        if len(point_array[0])>0 and len(point_array[1])>0 and len(point_array[2])>0:
            ax.scatter3D(point_array[0], point_array[1], point_array[2], color=colors[i])  # 绘制散点图
    return


data = load_data_file("record.txt")
analys_data = analys_data(data)

fig = plt.figure()
ax1 = plt.axes(projection='3d')

draw_data(ax1, analys_data)


#ax1.plot3D(x,y,z,'gray')    #绘制空间曲线
plt.show()






