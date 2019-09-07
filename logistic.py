import ast

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

lam = 0.01
alpha = 0.003


def prepare_data(filename):
    file = open(filename, 'r')
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for line in file:
        l = ast.literal_eval(line)
        if l[2] == 0:
            y1.append(l[0])
            x1.append(l[1])
        else:
            y2.append(l[0])
            x2.append(l[1])

    return x1, y1, x2, y2


def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s


def get_error(w, d1, d2):
    sum = 0
    for i in d1:
        x = np.transpose([1, i[0], i[1]])
        z = np.dot(w, x)
        sum += np.log(1 - sigmoid(z))

    for i in d2:
        x = np.transpose([1, i[0], i[1]])
        z = np.dot(w, x)
        sum += np.log(sigmoid(z))

    return sum


def confusion_matrix(w, d1, d2):
    ones = [0] * 2
    zeros = [0] * 2
    for i in d2:
        x = np.transpose([1, i[0], i[1]])
        z = np.dot(w, x)
        if sigmoid(z) < 0.5:
            ones[1] += 1
        else:
            ones[0] += 1

    for i in d1:
        x = np.transpose([1, i[0], i[1]])
        z = np.dot(w, x)
        if sigmoid(z) > 0.5:
            zeros[0] += 1
        else:
            zeros[1] += 1

    return [zeros, ones]


def update_weights(w, x, a):
    z = sum([(a * b) for (a, b) in zip(w, x)])
    if a == 1:
        w[0] -= alpha * (np.exp(z) / (1 + np.exp(z)) + 2 * lam * w[0])
        w[1] -= alpha * ((np.exp(z) / (1 + np.exp(z))) * x[1] + 2 * lam * w[1])
        w[2] -= alpha * ((np.exp(z) / (1 + np.exp(z))) * x[2] + 2 * lam * w[2])
        return w
    else:
        w[0] -= alpha * ((np.exp(-z) / -(np.exp(-z) + 1)) + 2 * lam * w[0])
        w[1] -= alpha * ((np.exp(-z) / -(np.exp(-z) + 1)) * x[1] + 2 * lam * w[0])
        w[2] -= alpha * ((np.exp(-z) / -(np.exp(-z) + 1)) * x[2] + 2 * lam * w[0])
        return w


def multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)complexity of riemann integration algorithm
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()


def norm(v):
    return np.sqrt(sum([y ** 2 for y in v]))


def do_learn(w, d1, d2):
    wold = [0, 0, 0]
    wnew = w
    while np.abs(norm(wnew) - norm(wold)) > 0.0025:
        wold = wnew.copy()
        for i in data_one:
            wnew = update_weights(wnew, [1, i[0], i[1]], 0)

        for i in data_two:
            wnew = update_weights(wnew, [1, i[0], i[1]], 1)

        # p1 = [0, 3]
        # p2 = [(wnew[0] + wnew[1] * 0) / -wnew[2], (wnew[0] + wnew[1] * 3) / -wnew[2]]
        # figs.append(plt.figure())
        # plt.plot([x for (x, y) in data_one], [y for (x, y) in data_one], 'ro')
        # plt.plot([x for (x, y) in data_two], [y for (x, y) in data_two], 'bo')
        # plt.plot(p1, p2)

    return wnew


arr = prepare_data("trainingscores.txt")
varr = prepare_data("testingscores.txt")

w = [0.5, 0.01, 0.5]
p1 = [0, 3]
p2 = [(w[0] + w[1] * 0) / -w[2], (w[0] + w[1] * 3) / -w[2]]
data_one = list(zip(arr[0], arr[1]))
data_two = list(zip(arr[2], arr[3]))

figs = [plt.figure()]
plt.plot([x for (x, y) in data_one], [y for (x, y) in data_one], 'ro')
plt.plot([x for (x, y) in data_two], [y for (x, y) in data_two], 'bo')
plt.plot(p1, p2)

w = do_learn(w, data_one, data_two)
plt.figure()
p1 = [0, 6]
p2 = [(w[0] + w[1] * 0) / -w[2], (w[0] + w[1] * 6) / -w[2]]
vdata_one = list(zip(varr[0], varr[1]))
vdata_two = list(zip(varr[2], varr[3]))
plt.plot([x for (x, y) in vdata_one], [y for (x, y) in vdata_one], 'ro')
plt.plot([x for (x, y) in vdata_two], [y for (x, y) in vdata_two], 'bo')
plt.plot(p1, p2)
plt.xlabel('maintenance score + buying price score')
plt.ylabel('safety score + luggage score')
plt.title('Logistic Regression Plot')
plt.legend()
plt.show()

print(w)
print(confusion_matrix(w, vdata_one, vdata_two))

multipage("figures.pdf", figs, 200)
