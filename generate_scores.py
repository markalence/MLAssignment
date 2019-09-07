import ast
from random import randint

bm = ['low', 'med', 'high', 'vhigh']
safety = ['low', 'med', 'high']
rscore = ['unacc', 'acc', 'good', 'vgood']
lug = ['small', 'med', 'big']
persons = ['2', '4', 'more']


def extract_data():
    text = open("testing", 'r')
    data_arr = []
    for line in text:
        row = ast.literal_eval(line)
        data_arr.append([row[0], row[1], row[5], row[6], row[4], row[3]])
    return data_arr


arr = extract_data()
training_data = []
test_data = []

for i in range(len(arr)):
    r = arr[randint(0, len(arr) - 1)]
    score = 0
    score += bm.index(r[0])
    score += bm.index(r[1])
    score += safety.index(r[2])
    actual_score = 0
    if rscore.index(r[3]) > 1:
        actual_score += 1
    arr.remove(r)
    pscore = 1
    if r[5] == '4':
        pscore = 2
    training_data.append([bm.index(r[0])*1.5 + bm.index(r[1]) , safety.index(r[2]) * 2 + lug.index(r[4]), actual_score])

test_data = arr

trainingFile = open("testingscores.txt", "w")
trainingFile.writelines("%s\n" % item for item in training_data)
trainingFile.close()
