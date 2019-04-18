import math
import ast

ocount = []
buying = ['low', 'med', 'high', 'vhigh']
maint = ['low', 'med', 'high', 'vhigh']
doors = ['2', '3', '4', '5more']
persons = ['2', '4', 'more']
lug = ['small', 'med', 'big']
safety = ['low', 'med', 'high']
attributes = [buying, maint, doors, persons, lug, safety]


def create_data_array(file, delim, ypos):
    text = open(file, 'r')
    data_array = []
    for line in text:
        review = [(x.strip()) for x in line.split(delim)]
        temp = review[ypos]
        del review[ypos]
        review.insert(0, temp)
        data_array.append(review)

    return data_array


def prepare_array(data_arr):
    for i in data_arr:
        t = i[len(i) - 1]
        del i[len(i) - 1]
        i.insert(0, t)
    return data_arr


def create_outcome_list():
    return ['unacc', 'acc', 'good', 'vgood']


def create_prob_table(encoded_array):
    ptable = []
    ovalues = create_outcome_list()
    x = len(encoded_array[0]) - 1
    for o in ovalues:
        orow = [0] * x
        n = 0
        for entry in encoded_array:
            if entry[0] == o:
                orow = [a + b for (a, b) in zip(orow, entry[1:x + 1])]
                n += 1
        ocount.append(n)
        ptable.append(orow)
    for row in ptable:
        i = ptable.index(row)
        ptable[i] = [(x + 1) / (ocount[i] + 2) for x in ptable[i]]

    return ptable


def calc_probability(ptable, encoded_arr):
    plist = []
    psum = 0
    for row in ptable:
        p = 0
        index = ptable.index(row)
        for i in range(1, len(encoded_arr)):
            if encoded_arr[i] == 1:
                p += math.log10(row[i - 1])
            else:
                p += math.log10(1 - row[i - 1])
        p += math.log10(ocount[index] / sum(ocount))
        plist.append(p)
        psum += p + math.log10(1 + (10 ** psum / 10 ** p))

    return [(math.pow(10, x) / sum([10 ** y for y in plist])) for x in plist]


def encode_data(data_array):
    encoded_matrix = []
    attindex = 0
    globals()
    for entry in data_array:
        encoded_list = [0] * 22
        encoded_list[0] = entry[0]
        for att in entry[1:]:
            encoded_list[attributes[attindex].index(att) + sum(len(x) for x in attributes[0:attindex]) + 1] = 1
            attindex += 1
        encoded_matrix.append(encoded_list)
        attindex = 0
    return encoded_matrix


def confusion_matrix(test_matrix, ptable):
    ovalues = create_outcome_list()
    cmat = [[0] * len(ovalues) for _ in range(len(ovalues))]
    for i in test_matrix:
        probs = calc_probability(ptable, i)
        mindex = probs.index(max(probs))
        cmat[mindex][ovalues.index(i[0])] += 1
    for i in cmat:
        print(i)
    accuracy = sum([cmat[x][x] for x in range(len(create_outcome_list()))])
    print('Accuracy = ', accuracy / len(test_matrix))
    return cmat


data_arr = []
data = open('training', 'r')
for i in data:
    data_arr.append(ast.literal_eval(i))
data.close()
data_arr = prepare_array(data_arr)
matrix = encode_data(data_arr)

ptable = create_prob_table(matrix)

test_array = []
data = open('testing', 'r')
for i in data:
    test_array.append(ast.literal_eval(i))
test_array = prepare_array(test_array)
test_matrix = encode_data(test_array)

confusion_matrix(test_matrix, ptable)
