import random
from statistics import mean
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

f = open('dataset2.txt')
# lists of datapoint pairs
xList = []
yList = []

for l in f:
    row = l.split()
    xList.append(float(row[0]))
    yList.append(float(row[1]))

# Datapoints-plot
plt.scatter(xList, yList)
plt.show()

# Model
x = 0
y = 0
r = 0

# n – minimum number of data points required to estimate model parameters
# k – maximum number of iterations allowed in the algorithm
# t – threshold value to determine data points that are fit well by model
# d – number of close data points required to assert that a model fits well to data

n = 10
k = 10000
t = 0.015
d = len(xList) / 100

iterations = 0

# Updated model
x_b = 0
y_b = 0
r_b = 0
bestErr = 999
updateErrCount = 1

print("Estimation:")
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

    # adds inliers if they are < t
    for i in range(0, len(xList)):
        if i in maybeInliers:
            continue

        # t_0 - current point's threshold value
        t_0 = abs(math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2) - r)
        if t > t_0:
            alsoInliers.append(i)

    # if alsoInliers are bigger than the closed data points required
    if len(alsoInliers) > d:

        inliers = maybeInliers + alsoInliers

        # model based on inliers
        x = mean([xList[i] for i in inliers])
        y = mean([yList[i] for i in inliers])
        r = 0


        for i in inliers:
            r += math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2)
        r = r/len(inliers)

        # calculating lsm for the inliers
        lsm = 0
        for i in inliers:
            lsm += (math.sqrt((x - xList[i]) ** 2 + (y - yList[i]) ** 2) - r) ** 2

        # if the calculated lsm is smaller than the previous error,
        # it updates the better model and bestErr value
        if lsm < bestErr:
            x_b = x
            y_b = y
            r_b = r
            bestErr = lsm
            print("Number of updated errors: " + str(updateErrCount) + " - updated to: " + str(bestErr))
            updateErrCount += 1


# printout
print(" ")
print("Inliers: " + str(len(inliers)))
print("Iterations: " + str(iterations))
print(" ")
print("Estimated model parameters:")
print("Radius: " + str(r_b) + ", X: " + str(x_b) + ", Y: " + str(y_b))

# Plot
# Points
plt.scatter(xList, yList, c='b', marker='o', label='Datapoints')
plt.scatter([xList[i] for i in inliers], [yList[i] for i in inliers], c='r', marker='x', label='Inliers')

# Model
circle = plt.Circle((x_b, y_b), r_b, color='r', linewidth=2, fill=False)
plt.gcf().gca().add_artist(circle)
circle_leg = mpatches.Patch(color='r', label="Model")

plt.legend(loc='upper left')
plt.show()
