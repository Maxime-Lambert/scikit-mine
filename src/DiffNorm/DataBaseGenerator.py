from random import *

db_num = 5
u = "1 2 3 4 5"
i_len = 10
tr_max_len = 10
tr_min_len = 3
db_min_len = 700
db_max_len = 1000
patt_min_len = int(i_len/3)
patt_max_len = 3 * patt_min_len
patt_min_num = 2
patt_max_num = 2

idx = 1
all_db = ""
while idx < db_num + 1:
    seed()
    patterns = []
    id_patt_num = 0
    while id_patt_num < randint(patt_min_num, patt_max_num):
        patterns.append(set())
        id_patt_len = 0
        while id_patt_len < randint(patt_min_len, patt_max_len):
            patterns[id_patt_num].add(randint(0, i_len - 1))
            id_patt_len += 1
        id_patt_num += 1
    f1 = open("test/data/gen_db" + repr(idx), "w+")
    f2 = open("test/data/gen_db" + repr(idx) + "_patterns", "w+")
    for pattern in patterns:
        f2.write(repr(pattern) + "\n")
    idz = 0
    while idz < randint(db_min_len, db_max_len):
        trans = ""
        idy = 0
        while idy < randint(tr_min_len, tr_max_len):
            trans += repr(randint(0, i_len - 1)) + " "
            idy += 1
        for item in patterns[randint(0, len(patterns) - 1)]:
            trans += repr(item) + " "
        f1.write(trans[:-1] + "\n")
        idz += 1
    all_db += "gen_db" + repr(idx) + " "
    idx += 1
f1 = open("test/data/gen_all", "w+")
f1.write(all_db[:-1])
f2 = open("test/data/gen_u", "w+")
f2.write(u)
