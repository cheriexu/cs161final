import sys
import numpy as np
np.set_printoptions(threshold='nan')



def LCS(A,B,arr):
	m = len(A)
	n = len(B)

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])
	print arr
	return arr[m][n]
def pathReconstruction (A,B,arr):
	path = {} #keys are columns, items are rows
	i = len(A)
	j = len(B)
	while i > 0 and j > 0:
		if A[i-1] == B[j-1]:
			coord = path.get(j - 1, [])
			coord.append(i-1)
			path[j-1] = coord
			i-=1
			j-=1
		elif arr[i-1][j] > arr[i][j-1]:
			print "case 2"
			coord = path.get(j, [])
			if len(coord) != 0 :
				print j,"more than 1"
			coord.append(i-1)
			path[j] = coord
			i-=1
		else:
			print "case 3"
			coord = path.get(j - 1, [])
			if len(coord) != 0 :
				print j,"more than 1"
			coord.append(i)
			path[j - 1] = coord
			j-=1
	return path
def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print A,B
		arr = np.zeros((len(A)+1, len(B)+1), dtype=int)
		print LCS(A,B,arr)
		print pathReconstruction (A,B,arr)
	return

if __name__ == '__main__':
	main()
