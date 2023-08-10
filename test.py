import numpy as np
# x = np.array([1,2,3])
# y =np.array([3,5])
# print(np.concatenate((x,y)))

print(np.arange(5))
x = np.array([[1,2], [6, 7]])
print(x[1,-1])
x = [100, 15, 9, 5, 4, 3, 1]
print(x[-1:1:-2])
print(int('1110',2))


x = 10
if x > 7 and x <=10:
	print("Pass", end="")
	print("Fail")
	
if (3+8//2 != 7):
	print("H")
else:
	print("B")