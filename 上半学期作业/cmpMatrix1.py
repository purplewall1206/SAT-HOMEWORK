import re
import math
import sys


def main(argv):
	listreq1 = []
	listreq2 = []
	req1 = []
	req2 = []
	req = []
	dist = {}
	
	filename = str(argv[1])
	#open 2 files
	with open('/home/ppw/Documents/pycode/requests0.dot', 'r') as f1:
		listreq1 = f1.readlines()
	
	with open(filename, 'r') as f2:
		listreq2 = f2.readlines()
	
	
	#generate 2 node lists
	for i in range(0, len(listreq1)):
		if re.match('(.*)Edge', listreq1[i]):
			break
		item = re.match('(.*)"(.*)";', listreq1[i])
		if not item is None:
			req1.append(item.group(2))
	
	
	for i in range(0, len(listreq2)):
		if re.match('(.*)Edge', listreq2[i]):
			break
		item = re.match('(.*)"(.*)";', listreq2[i])
		if not item is None:
			req2.append(item.group(2))
	
	#sort 2 node lists to make sure == operate is accurate
	req1.sort()
	req2.sort()
	
	
	# combine 2 node list into one list(set)
	if req1 != req2:
		req = list(set(req1).union(set(req2)))
	else:
		req = req1
	
	# arrenge number id to function
	for i in range(0, len(req)):
		dist[req[i]] = i
	
	
	# initiate matrixs
	reqmatrix1 = [0]*(len(req) * len(req))
	reqmatrix2 = [0]*(len(req) * len(req))
	
	#generate matrixs
	for i in range(0, len(listreq1)):
		item = re.match('(.*)"(.*)" -> "(.*)";', listreq1[i])
		if not item is None:
			pos = dist[item.group(2)] * len(req) + dist[item.group(3)]
			reqmatrix1[pos] = reqmatrix1[pos] + 1
	
	
	for i in range(0, len(listreq2)):
		item = re.match('(.*)"(.*)" -> "(.*)";', listreq2[i])
		if not item is None:
			pos = dist[item.group(2)] * len(req) + dist[item.group(3)]
			reqmatrix2[pos] = reqmatrix2[pos] + 1
	
	
	#write matrix 
	matrixpath = '/home/ppw/Documents/pycode/matrixes/'+argv[1]+'.txt'
	with open(matrixpath, 'w') as fff:
		lll = []
		for i in range(0, len(req)):
			for j in range(0, len(req)):
				lll.append(reqmatrix2[i*len(req)+j], end=" ")
			lll.append('\n')
		fff.write(lll)
		
	
	
	
	
	# calculate cosine similirity reqmatrix1 len == reqmatrix2 len
	sum = 0
	sqrtsumpow1 = 0
	sqrtsumpow2 = 0
	for i in range(0, len(reqmatrix1)):
		sum = sum + (reqmatrix1[i] * reqmatrix2[i])
		sqrtsumpow1 = sqrtsumpow1 + pow(reqmatrix1[i], 2)
		sqrtsumpow2 = sqrtsumpow2 + pow(reqmatrix2[i], 2)
	
	cosine = float(sum) / math.sqrt(float(sqrtsumpow1 * sqrtsumpow2))
	
	print(filename+str(':'))
	print(cosine)
	
	k = math.acos(cosine)/math.pi
	
	print(k)
	print('\n\n')
	
	f1.close()
	f2.close()


if __name__ == '__main__':
    main(sys.argv)

'''
0.9778656339992127
0.06709698547794878

0.9766896075556794
0.06886319644553171

#print 2 matrixs

for i in range(0, len(req)):
    for j in range(0, len(req)):
        print(reqmatrix1[i*len(req)+j], end=" ")
    print()

print("\n\n\n")
for i in range(0, len(req)):
    for j in range(0, len(req)):
        print(reqmatrix2[i*len(req)+j], end=" ")
    print()
'''


#print list length,to see the difference
'''
print("length compare list1, list2 ,req1,req1")
print(len(listreq1))
print(len(listreq2))
print(len(req1))
print(len(req2))
'''