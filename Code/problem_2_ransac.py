import csv
import numpy as np
import matplotlib.pyplot as plt
import random


THRESHOLD = 30
N = 25730



def check_inlier(a,b,c,xi,yi,t):
   
    distance = yi -(a*(xi**2)) - (b*xi) - c
   
    if abs(distance) <= t:
        return 1
   
    else:
        return 0


datadict = {}
with open('data_2.csv') as csvfile:
	data = csv.reader(csvfile, delimiter = ',')
	for row in data:
		datadict[row[0]] = row[1]

#Creating a matrix of each type to further compute
matrix_y = []
matrix_x = []
for i in datadict:
	try:
		matrix_y.append(float(datadict[i]))
		matrix_x.append([float(i)*float(i), float(i), 1])
	except ValueError:
		#The value found is not a float
		continue

y = np.array(matrix_y)
x = np.array(matrix_x)

xcoords = []
ycoords = matrix_y
for xi in x:
	# yi.append(xi[0]*B[0] + xi[1]*B[1] + xi[2]*B[2])
	xcoords.append(xi[1])

nPoints = len(y)
for _ in range(N):

	#Selecting three random points to generate the plot for the Parabola
	pntsList = random.sample(range(len(matrix_y)), 3)
	mat_x = []
	mat_y = []

	for i in pntsList:
		mat_y.append(matrix_y[i])
		mat_x.append(matrix_x[i])


	y = np.array(mat_y)
	x = np.array(mat_x)

	one = np.linalg.inv(x)
	two = y

	B = np.matmul(one, two)

	max_inliers = 0
	curr_inliers = 0

	for pointID in range(nPoints):

		if check_inlier(B[0], B[1], B[2], xcoords[pointID], ycoords[pointID], THRESHOLD):
			curr_inliers += 1

	if curr_inliers > max_inliers:
		max_inliers = curr_inliers
		best_model = [max_inliers, B[0], B[1], B[2]]


print(best_model)

yi = []
for xi in matrix_x:
	yi.append(xi[0]*B[0] + xi[1]*B[1] + xi[2]*B[2])

plt.plot(xcoords, matrix_y, 'bo')
plt.plot(xcoords, yi, 'ro')
plt.show()