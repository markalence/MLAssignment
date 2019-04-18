import ast
import numpy as np
from node import Node

downtree = ['buying', 'maint', 'doors', 'persons', 'lug', 'safety']
buying = ['low', 'med', 'high', 'vhigh']
maint = ['low', 'med', 'high', 'vhigh']
doors = ['2', '3', '4', '5more']
persons = ['2', '4', 'more']
lug = ['small', 'med', 'big']
safety = ['low', 'med', 'high']
attributes = [buying, maint, doors, persons, lug, safety]
darr = []
data = open('training', 'r')
for i in data:
    darr.append(ast.literal_eval(i))
data.close()
table = np.array(darr)
data = open('testing', 'r')
test_arr = []
for i in data:
    test_arr.append(ast.literal_eval(i))
data.close()
test_arr = np.array(test_arr)


def create_outcome_list():
    return ['unacc', 'acc', 'good', 'vgood']


def get_entropy(table):
    N = len(table)
    if N == 0:
        return 0
    n = len(table[0])
    ovalues = create_outcome_list()
    occurences = []
    for o in ovalues:
        occurences.append([x[n - 1] for x in table].count(o))
    return -sum([(x / N) * np.log2(x / N) for x in occurences if x != 0])


init_ent = get_entropy(table)


def max_gain(node):
    globals()
    n = len(table[0]) - 1
    N = len(table)
    gains = []
    i = 0
    for att in attributes:
        fent = []
        if node.visited[i] == 1:
            gains.append(-1)
            i += 1
            continue
        for v in att:
            c1 = [x for x in table[:, attributes.index(att)] if x == v]
            c2 = [x[n] for x in table[:] if x[attributes.index(att)] == v]
            mtable = np.transpose([c1, c2])
            fent.append([get_entropy(mtable), len(mtable)])
        gains.append(init_ent - (1 / N) * sum(x[0] * x[1] for x in fent))
        i += 1
    return gains.index(max(gains))


def split_table(node, index):
    node.visited[index] = 1
    return len(attributes[index])


def traverse_tree(root, input, mtable):
    counts = [0] * 4
    olist = create_outcome_list()
    if len(root.children) == 0:
        for i in olist:
            counts[olist.index(i)] += [x for x in mtable[len(mtable) - 1]].count(i)
        return olist[counts.index(max(counts))]
    for child in root.children:
        if child.value == input[downtree.index(child.label)]:
            if len([x for x in mtable if x[downtree.index(child.label)] == child.value]) == 0:
                for i in olist:
                    counts[olist.index(i)] += [x for x in mtable[len(mtable) - 1]].count(i)
                return olist[counts.index(max(counts))]
            mtable = [x for x in mtable if x[downtree.index(child.label)] == child.value]
            return traverse_tree(child, input, mtable)


def makeTree(root):
    if root.visited == [1] * 6:
        return
    globals()
    index = max_gain(root)
    new_tables = split_table(root, index)
    label = downtree[index]
    for i in range(new_tables):
        child = Node(label, attributes[index][i], root.visited.copy())
        i += 1
        root.add_child(child)
        makeTree(child)


root = Node('root', ' ', [0] * 6)
makeTree(root)
k = 0
for i in test_arr:
    if traverse_tree(root, i[0:6], table) == i[6]:
        k += 1
print('Accuracy = ', k/len(test_arr))
