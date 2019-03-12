from src.DiffNorm.DiffNorm1 import DiffNorm1


if __name__ == '__main__':
    #  d = DiffNorm1("all", "u")
    d = DiffNorm1("gen_all", "gen_u")
    d.run()
    """a1 = log_gamma(50)
    a2 = log_gamma(42.5)
    a3 = log_gamma(0.5)
    a4 = log_gamma(8.5)
    a5 = log_gamma(3.5)
    a6 = log_gamma(11.5)
    a7 = log_gamma(8.5)
    a8 = log_gamma(0.5)
    a9 = log_gamma(3.5)
    a10 = log_gamma(3)
    print(a1)
    print(a2)
    print(a3)
    print(a4)
    print(a5)
    print(a6)
    print(a7)
    print(a8)
    print(a9)
    print(a10)
    print()
    print(a1 - a2 + a3 - a4 + a5 - a6 + a7 - a8 + a9 - a10)

    databases = []

    db1 = DataBase("dbd1", 1)
    db2 = DataBase("dbd2", 2)

    databases.append(db1)
    databases.append(db2)
    alphabet = []

    for database in databases:
        for transaction in database:
            for item in transaction:
                candidate = ItemSet([item])
                if candidate not in alphabet:
                    alphabet.append(candidate)

    ct1 = CodeTable(db1)
    ct2 = CodeTable(db2)

    for item in alphabet:
        ct1.add(item.copy())
        ct2.add(item.copy())

    ct1.sort_in_sco()
    ct2.sort_in_sco()

    candidates = []

    for x in ct1:
        for y in ct1:
            p = Pattern(x, y, 0, 0, 0)
            if len(p) > 1:
                if p not in candidates:
                    candidates.append(p)

    for x in ct2:
        for y in ct2:
            p = Pattern(x, y, 0, 0, 0)
            if len(p) > 1:
                if p not in candidates:
                    candidates.append(p)

    ct1.update_t_data()
    ct1.update_usage()
    ct1.update_usages()
    ct2.update_t_data()
    ct2.update_usage()
    ct2.update_usages()

    for p in candidates:
        constant = 0.5
        len_old_cs = ct1.size
        len_new_cs = len_old_cs + 1
        usages_left = ct1.gather_usages(p.left_is)
        usages_right = ct1.gather_usages(p.right_is)
        usage_new_cand = len(usages_left & usages_right)
        usage_old_left = len(ct1.gather_usages(p.left_is))
        usage_old_right = len(ct1.gather_usages(p.right_is))
        usage_new_left = usage_old_left - usage_new_cand
        usage_new_right = usage_old_right - usage_new_cand
        usage_old_cs = ct1.usage
        usage_new_cs = \
            usage_old_cs - usage_old_left - usage_old_right + \
            usage_new_right + usage_new_left + usage_new_cand
        db_gain = \
            log_gamma(usage_old_cs + constant * len_old_cs) - log_gamma(usage_new_cs + constant * len_new_cs) + \
            log_gamma(usage_new_left + constant) - log_gamma(usage_old_left + constant) + \
            log_gamma(usage_new_right + constant) - log_gamma(usage_old_right + constant) + \
            log_gamma(usage_new_cand + constant) - log_gamma(constant) + \
            log_gamma(constant * len_new_cs) - log_gamma(constant * len_old_cs)
        p.set_est_gain(db_gain)

    candidates.sort(reverse=True, key=lambda x: x.max_gain)
    for p in candidates:
        print(repr(p) + " " + repr(p.max_gain))

    ct1.pp()
    ct2.pp()"""
