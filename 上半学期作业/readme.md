# 背景、要解决的问题


Python是一种计算机程序设计语言。是一种动态的、面向对象的解释型脚本语言，最初被设计用于编写自动化脚本(shell)，随着版本的不断更新和语言新功能的添加，越来越多被用于独立的、大型项目的开发。因此项目运行脚本中的调用关系愈发被人们重视，分析调用关系的手段有绘制调用图。
调用图反映了程序函数中的依赖关系，可以通过静态分析代码生成静态调用图或者记录程序运行路径生成动态调用图，静态调用图优点是分析调用关系较为全面，同时可以处理多个函数之间循环调用等复杂问题，然而对动态性执行的代码分析能力较差。由于Python的是一种动态的解释型脚本，因此使用动态调用图能够更好地表征关键执行路径的调用关系，同时能够忽略项目中文件数目对调用图分析的影响。


Requests包是python实现的一种用于处理http协议的工具包，功能点集中，代码量较为适中，该项目一直在http://github.com 网站维护，此外该项目的源代码不存在循环调用等较为复杂的问题，同时项目实现的过程中代码能够兼容python3.x版本和python2.x版本，利于进行分析。
我们通过收集https://github.com 网站上项目的不同开发版本的关键功能模块调用图，和最新发布的release版本生成的关键功能模块动态调用图分别对比相似度。


由于收集到的动态调用图使用pydot绘制，实现过程不清晰，直接对比生成的PNG格式图片像素比较相似性显然准确性欠佳。因此我们应当适当修改pycallgraph项目代码，获得动态调用图的连通图矩阵，并使用余弦三角函数表征不同版本项目之间的相似性。


# 脚本文件设计

## Callgraph.py：

输入为待分析的requests项目版本，调用重新编辑过的pycallgraph包，执行requests获取https://baidu.com 网页，生成dot格式文件并保存在指定目录中。


## cmpMatrix1.py ：

获取全部连续release之间的dot格式文件，与最新发布版本dot文件对比，生成连通图矩阵计算全部余弦相似度。并将相关数据保存到硬盘中。


## cmpMatrix2.py ：

获取全部连续commit之间的dot格式文件，与最新发布版本dot文件对比，生成连通图矩阵计算全部余弦相似度。并将相关数据保存到硬盘中。


## op.sh：

编写shell文件分别对每个requests的release版本执行callgraph.py脚本。


## opsolve.sh：

编写shell文件使git在连续的commit之间切换并在每个版本切换完成后执行callgraph脚本。


## draw1.py：

读取连续release之间的相似度结果文件，绘制折线图和y=kx函数坐标图。


## draw2.py：

读取连续commit之间的相似度结果文件，绘制折线图和y=kx函数坐标图。


## Graphviz.py：

pycallgraph中负责生成dot文件并绘图的脚本，重新编辑其中的generate_node和generate_edge等函数本项目所需格式的dot文件。
 
 
## Commitresult.txt：

连续开发版本之间结果


## Result.txt：

连续的发布版本之间结果


# 结果：

## 连续commit之间

![连续commit之间](https://github.com/purplewall1206/SAT-HOMEWORK/blob/master/%E4%B8%8A%E5%8D%8A%E5%AD%A6%E6%9C%9F%E4%BD%9C%E4%B8%9A/results/consinesimilarity_all3.png)



## 连续release之间

![连续release之间](https://github.com/purplewall1206/SAT-HOMEWORK/blob/master/%E4%B8%8A%E5%8D%8A%E5%AD%A6%E6%9C%9F%E4%BD%9C%E4%B8%9A/results/consinesimilarity2.png)
