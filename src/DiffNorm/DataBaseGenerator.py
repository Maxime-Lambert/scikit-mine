from random import *

db_num = 5
u = "1 2 3 4 5"
i_len = 20
tr_max_len = 10
tr_min_len = 3
db_min_len = 200
db_max_len = 500

idx = 1
all_db = ""
while idx < db_num + 1:
    seed()
    f = open("test/gen_db" + repr(idx), "w+")
    idz = 0
    while idz < randint(db_min_len, db_max_len):
        trans = ""
        idy = 0
        while idy < randint(tr_min_len, tr_max_len):
            trans += repr(randint(0, i_len - 1)) + " "
            idy += 1
        f.write(trans[:-1] + "\n")
        idz += 1
    all_db += "gen_db" + repr(idx) + " "
    idx += 1
f1 = open("test/gen_all", "w+")
f1.write(all_db[:-1])
f2 = open("test/gen_u", "w+")
f2.write(u)
