import random
from statistics import mean
import math
import matplotlib.pyplot as plt


f = open('dataset2.txt')
#lists of datapoint pairs
xList = []
yList = []

for l in f:
    row = l.split()
    xList.append(float(row[0]))
    yList.append(float(row[1]))

#Datapooints-plot
plt.scatter(xList, yList)
plt.show()

#Model
r = 0
x = 0
y = 0

#n – minimum number of data points required to estimate model parameters
#k – maximum number of iterations allowed in the algorithm
#t – threshold value to determine data points that are fit well by model
#d – number of close data points required to assert that a model fits well to data

n = 10
k = 10000
t = 0.01
d = len(xList) / 100

iterations = 0

x_b = 0
y_b = 0
r_b = 0
bestErr = 999
betterCount = 1
while iterations < k:

    iterations += 1
    maybeInliers = random.sample(range(0, len(xList)), n)
    alsoInliers = []

    x = mean([xList[i] for i in maybeInliers])
    y = mean([yList[i] for i in maybeInliers])
    r = 0

    for i in maybeInliers:
        r += math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2)
    r = r/len(maybeInliers)

    #adds inliers if they are < t
    for i in range(0, len(xList)):
        if i in maybeInliers:
            continue

        #t_0 - current point's treshold value
        t_0 = abs(math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2) - r)
        if t > t_0:
            alsoInliers.append(i)

    #if alsoInliers
    if len(alsoInliers) > d:

        inliers = maybeInliers + alsoInliers

        #model
        x = mean([xList[i] for i in inliers])
        y = mean([yList[i] for i in inliers])
        r = 0


        for i in inliers:
            r += math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2)
        r = r/len(inliers)

        #calculate lsm
        lsm = 0
        for i in inliers:
            lsm += (math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2) - r) ** 2

        if lsm < bestErr:
            x_b = x
            y_b = y
            r_b = r
            bestErr = lsm
            print(str(betterCount) + ": found better estimation: " + str(bestErr) )
            betterCount += 1

print("Inliers: " + str(len(inliers)))
plt.scatter(xList, yList, c='b', marker='o', label='Datapoints')
plt.scatter([xList[i] for i in inliers], [yList[i] for i in inliers], c='r', marker='x', label='Inliers')
plt.legend(loc='upper left')
plt.show()
