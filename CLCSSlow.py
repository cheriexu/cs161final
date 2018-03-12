import sys
import numpy as np

arr = np.zeros((2048, 2048), dtype=int)
def cut(word, i):
	return word[i:]+word[0:i]
def CLCS(A,B,k):
	max = 0
	for i in range(len(A)):
		editedA = cut(A,i)
		clcs = LCS(editedA,B)
		if clcs > max:
			max = clcs
	return max
def LCS(A,B):
	m = len(A)
	n = len(B)

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])

	return arr[m][n]

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print CLCS(A,B)
	return

if __name__ == '__main__':
	main()
