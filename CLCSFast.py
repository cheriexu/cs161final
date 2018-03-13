import sys
import numpy as np
np.set_printoptions(threshold="nan")
sys.setrecursionlimit(1500)


m, n = 0, 0

# input: path index, upper or lower
def getPath(start, bound, paths):
	p = [0 for x in range(n + 1)]
	for j in range(n + 1):
		if bound is "upper":
			p[j] = max(paths[start][j])
		else:
			p[j] = min(paths[start][j])
	return p

def pathReconstruction (A,B,start, arr, lower_path=[], upper_path=[]):
	path = {} #keys are columns, items are starts
	i,j = start + m, n
	path[j] = [i]
	allTrue = start is 0 or start is m
	def inRange(row, col, arr=arr,lower_path=lower_path,upper_path=upper_path,allTrue=allTrue):
		if allTrue:
			return True
		return lower_path[col] >= row and upper_path[col] <= row
	while i >= start and j > 0:
		# moving diagonally
		if inRange(i-1,j-1) and A[(i-1)%m] == B[j-1]:
			path[j - 1] = [i-1]
			i-=1
			j-=1
		# moving left
		elif inRange(i,j-1) and arr[i-1][j] <= arr[i][j-1]:
			path[j-1] = path.get(j - 1, []) + [i]
			j-=1
		else:
			path[j] = [i-1]
			i-=1
	# moving up
# if final col is greater than final start
	if j > 0:
		for x in range(j+1):
			path[x] = [0]

	return path

# arr has (start, col) indexing
def shortestpath(A, B, idx, l, u, arr, paths):
	arr[idx] = [0 for i in range(n + 1)]
	for i in range(2*m + 1):
		arr[i][0] = 0
	lower_path = getPath(l, "lower", paths)  #lower bound, you want the min
	upper_path = getPath(u, "upper", paths) #uppser boudn you want the max
	def inRange(row, col, lower_path=lower_path,upper_path=upper_path):
		return lower_path[col] >= row and upper_path[col] <= row
	for i in range(len(upper_path)):
		arr[upper_path[i]][i] = 0
		arr[max(upper_path[i]-1,0)][i] = 0
	for j in range(1,n+1):#changed 2 to 1
		for i in range(max(idx+1,upper_path[j]),min(lower_path[j]+1,2*m+1)):
			 # this seem to work but  think of exceptions
			if A[(i-1)%m] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
				#print arr[i][j]
			else:
				'''if inRange(i-1, j ):
				arr[i][j] = arr[i - 1][j]'''
				if inRange(i, j - 1):
					arr[i][j] = max(arr[i-1][j] , arr[i][j - 1])
				else:
					arr[i][j] = arr[i-1][j]
					#print "max", arr[i-1][j] , arr[i][j - 1]
					#print "upper", upper_path[j-1], lower_path[j-1]
#	print arr
	path = pathReconstruction(A,B,idx,arr,lower_path,upper_path) #changed A[idx:]+A[0:idx] to A

#	print path
	value = arr[m+idx][n]
#	print value
	return path, value



def CLCS(A,B, arr, paths, values, l=m,u=0,):
	#print("l, u is %s") %str((l,u))
	if l-u <= 1: return
	mid = (u+l)/2
	s = shortestpath(A,B,mid,l,u, arr, paths)
	paths[mid], values[mid] = s
	CLCS(A,B,arr,paths,values,l, mid)
	CLCS(A,B,arr,paths,values,mid,u)
	return values

def LCS(A,B,start, arr):
	arr[start] = [0 for i in range(n + 1)]
	for i in range(2*m + 1):
		arr[i][0] = 0
	
	for i in range(start+1,start+m+1):
		for j in range(1,n+1):
			if A[(i-1)%m] == B[(j-1)]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])
	return arr[start+m][n]


def main():
	global A, B, m, n
	finals = []
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')

	for idx, l in enumerate(sys.stdin):
		A,B = l.split()
		m, n = len(A), len(B)
		if m < 2:
			finals.append(1 if A in B else 0)
			print(1 if A in B else 0)
		else:
			values = {}
			paths = {}
			arr = np.zeros((2*m+1, n+1), dtype=int)
			LCS(A,B,0,arr)
			
			paths[0] = pathReconstruction(A,B,0,arr)#Path traced by LCS(a,b)
			LCS(A,B,m,arr)
			
			paths[m] = pathReconstruction(A,B,m,arr)
			CLCS(A,B,arr, paths, values, m, 0)
			print(values)
			maxval = max([values[key] for key in values.keys()])
			print maxval
			finals.append(maxval)
	print(finals)



if __name__ == '__main__':
	main()

