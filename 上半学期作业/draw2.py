#with open('/home/ppw/Documents/pycode/requests_dot/result.txt', 'r') as f:
with open('/home/ppw/Documents/resultallcommit.txt', 'r') as f:
    line = f.readlines()

import re

k = []
cosine = []
for i in range(0, len(line)):
    kvalue = re.match('k value in y=k.x  : (.*)', line[i])
    if not kvalue is None:
        x = kvalue.group(1)
        k.append(float(kvalue.group(1)))

    cosinevalue = re.match('cosine similirity : (.*)', line[i])
    if not cosinevalue is None:
        x = cosinevalue.group(1)
        cosine.append(float(cosinevalue.group(1)))

import matplotlib.pyplot as plt
import matplotlib
from pylab import *
#draw ro picture
#np.random.seed(2000)
#y = np.random.standard_normal((10, 2))
cosine.sort()
y = cosine
plt.figure(figsize=(7,5))
#plt.plot(y, lw = 1.5,label = 'similarity')
#plt.plot(y[:,1], lw = 1.5, label = '2st')




plt.plot(y,'b', lw=1.5)
#plt.plot(y,'ro')
plt.grid(True)
plt.legend(loc = 0) #图例位置自动
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('similarity')
plt.show()

#draw func

'''
x = linspace(0, 5, 10)
#y = x**2
y = k * x
fig = plt.figure()
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
axes.plot(x, y, 'r')

axes.set_xlabel('x')
axes.set_ylabel('y')
axes.set_title('title')

plt.show()
'''





x = np.linspace(0,10, 5)
plt.figure(figsize=(7,5))

count = 0
count1 = 0
count2 = 0
print(k)
print(len(k))
for i in range(1,len(k)):
    if k != 0:
        labelkx = 'y = ' + str(k[i])+ ' * x'
        y = k[i] * x
        plt.plot(x,y,label=labelkx)
    else:
        plt.plot(0,x)


#plt.legend(loc=0)  # 图例位置自动
plt.xlabel('x')
plt.ylabel('y')
plt.xlim((0,10))
plt.ylim((0,10))



ax = plt.gca()
# 设置右边框和上边框
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 设置x坐标轴为下边框
ax.xaxis.set_ticks_position('bottom')
# 设置y坐标轴为左边框
ax.yaxis.set_ticks_position('left')

plt.show()
