from random import *
from os import path

db_num = 5
u = "1 2 3 4 5"
i_len = 15
tr_max_len = 8
tr_min_len = 6
db_min_len = 300
db_max_len = 500
patt_min_len = int(i_len/3)
patt_max_len = 3 * patt_min_len
patt_min_num = 1
patt_max_num = 1

idx = 1
all_db = ""
while idx < db_num + 1:
    seed()
    data_directory_path = "../../test/data/DiffNorm/"
    dn_dir = path.dirname(__file__)
    abs_file_path = path.join(dn_dir, data_directory_path)
    patterns = []
    id_patt_num = 0
    while id_patt_num < randint(patt_min_num, patt_max_num):
        patterns.append(set())
        id_patt_len = 0
        while id_patt_len < randint(patt_min_len, patt_max_len):
            patterns[id_patt_num].add(randint(0, i_len - 1))
            id_patt_len += 1
        id_patt_num += 1
    f1 = open(abs_file_path + "gen_db" + repr(idx), "w+")
    f2 = open(abs_file_path + "gen_db" + repr(idx) + "_patterns", "w+")
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
f1 = open(abs_file_path + "gen_all", "w+")
f1.write(all_db[:-1])
f2 = open(abs_file_path + "gen_u", "w+")
f2.write(u)
