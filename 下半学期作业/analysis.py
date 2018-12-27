import csv

browser = 'chrome'
filename1 = 'errorlist-chrome.csv'
# browser = 'firefox'
filename2 = 'errorlist-firefox.csv'
errorlist1 = []
errorlist2 = []
with open(filename1, encoding='utf8') as f:
    reader = csv.reader(f)
    errorlist1 = (list(reader))

with open(filename2, encoding='utf8') as f:
    reader = csv.reader(f)
    errorlist2 = (list(reader))

count = [0,0,0,0]
sum = 757

print(len(errorlist1))
print(len(errorlist2))

infos1 = []
infos2 = []

for err1 in errorlist1:
    infos1.append(err1[0]+err1[1])

for err2 in errorlist2:
    infos2.append(err2[0]+err2[1])

errorset1 = set(infos1).intersection(set(infos2))
errorset2 = set(infos1).union(set(infos2))
print(len(errorset1))
print(len(errorset2))
# print(errorset1)
print('sames ',len(errorset1))
diff = []
for err1 in errorlist1:
    title = err1[0]
    url = err1[1]
    for err2 in errorlist2:
        if title == err2[0] and url == err2[1]:
            for i in range(2,6):
                if err1[i] != err2[i]:
                    diff.append(err1[0]+err1[1]+','+err1[i]+','+err2[i]+'\n')

print(diff)
print(len(diff))

# with open('similarity.csv','w',encoding='utf8') as ff:



# browser = 'chrome'
# filename1 = 'errorlist-chrome.csv'
# browser = 'firefox'
# filename2 = 'errorlist-firefox.csv'
# errorlist = []
#
# with open(filename2, encoding='utf8') as f:
#     reader = csv.reader(f)
#     errorlist = (list(reader))
# for item in errorlist:
#     if item[2]!= '':
#         count[0] = count[0]+1
#     if item[3] != '':
#         count[1] = count[1]+1
#     if item[4] != '':
#         count[2] = count[2]+1
#     if item[5] != '':
#         count[3] = count[3]+1
#
# print(count)
#
# import numpy as np
import matplotlib.pyplot as plt
# labels = [['http','https'],['diff','no diff'],['not belong','belong'],['not loaded','loaded']]
# fracs = [[count[0], sum-count[0]], [count[1], sum-count[1]],
#          [count[2], sum-count[2]], [count[3], sum-count[3]]]
# plt.axes(aspect=1)
#
#
# for i in range(4):
#     plt.pie(x=fracs[i], labels=labels[i], shadow=True, autopct='%3.2f %%')
#
#     plt.savefig(browser+str(i)+'.png')
#     plt.show()

labels = ['same','not same']
fracs = [635-45,45]
plt.axes(aspect=1)
plt.pie(x=fracs, labels=labels, shadow=True, autopct='%3.2f %%')
plt.savefig('compatibility.png')
plt.show()