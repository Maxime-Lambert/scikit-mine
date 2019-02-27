from src.DiffNorm.CodeTable import *
from src.DiffNorm.DataBase import *
from src.DiffNorm.Pattern import *
from src.DiffNorm.DiffNormUtils import *


class DiffNorm:

    min_usage = 1
    min_gain = 1.0

    def __init__(self, nom_db, nom_u):
        self.num_iterations = 0
        self.candidates = []
        self.rejected_candidates = []
        self.accepted_candidates = []
        self.databases = []
        self.coding_sets_i = []
        self.model = []
        self.u = []
        self.alphabet = []
        self.current_candidate = None
        self.all_db_card = 0
        self.accepted = False

        file_db = open("test/" + nom_db, "r")
        databases = file_db.readline().split(" ")
        dbid = 0
        for database in databases:
            new_db = DataBase(database)
            self.databases.append(new_db)
            self.coding_sets_i.append(CodeTable(new_db, 1))
            self.u.append([dbid])
            self.all_db_card += len(new_db)
            dbid += 1

        file_u = open("test/" + nom_u, "r")
        groupes = file_u.readlines()
        for line in groupes:
            if line[-1:] == '\n':
                line = line[:-1]
            group = line.split(" ")
            cs_param = []
            for dbid in group:
                if int(dbid) - 1 not in cs_param:
                    cs_param.append(int(dbid) - 1)
            if set(cs_param) not in self.u:
                if len(cs_param) > 1:
                    self.u.append(cs_param)
                    self.model.append([])

    def init_alphabet(self):
        for database in self.databases:
            for transaction in database:
                for item in transaction:
                    candidate = ItemSet([item])
                    if candidate not in self.alphabet:
                        self.alphabet.append(candidate)

    def calc_db_sizes_all(self):
        i = 0
        for cs in self.coding_sets_i:
            cs.set_encoded_db_size(self.size_of_dbi_with_ci(cs.database, i))
            i += 1

    def init_all_ct_i(self):
        for cs in self.coding_sets_i:
            for itemset in self.alphabet:
                cs.add(itemset)
            cs.sort_in_sco()
            cs.update_t_data()
            cs.update_usage()
        self.calc_db_sizes_all()

    def load_next_candidate(self):
        self.current_candidate = self.candidates.pop(0)

    def already_generated(self, candidate):
        return candidate in self.candidates

    def already_rejected(self, candidate):
        return candidate in self.rejected_candidates

    def already_accepted(self, candidate):
        return candidate in self.accepted_candidates

    def proba_x(self, x, cs_id):
        cs_ref = self.coding_sets_i[cs_id]
        usages_x = len(cs_ref.gather_usages(x))
        usages_y = 0
        for y in cs_ref:
            if x != y:
                usages_y += len(cs_ref.gather_usages(y))
        return usages_x / usages_y

    def prefix_code(self, x, cs_id):
        return -log(self.proba_x(x, cs_id))

    def size_of_t_with_ci(self, transaction, tid, cs_id):
        t_len = universal_code_len(len(transaction))
        t_cover = self.coding_sets_i[cs_id].get_cover(tid)
        xs_with_ci = t_len
        for x in t_cover:
            xs_with_ci += self.prefix_code(x, cs_id)
        return xs_with_ci

    def size_of_dbi_with_ci(self, database, cs_id):
        db_len = universal_code_len(database.db_card)
        ts_with_ci = db_len
        tid = 0
        for transaction in database:
            ts_with_ci += self.size_of_t_with_ci(transaction, tid, cs_id)
            tid += 1
        return ts_with_ci

    def calculate_db_gain(self, candidate, coding_set_id):
        constant = 0.5
        coding_set = self.coding_sets_i[coding_set_id]
        len_old_cs = coding_set.size
        len_new_cs = len_old_cs + 1
        usage_new_cand = self.estimate_usage(candidate)
        usage_old_left = len(coding_set.gather_usages(candidate.left_is))
        usage_old_right = len(coding_set.gather_usages(candidate.right_is))
        usage_new_left = usage_old_left - usage_new_cand
        usage_new_right = usage_old_right - usage_new_cand
        usage_old_cs = coding_set.usage
        usage_new_cs = \
            usage_old_cs - usage_old_right - usage_old_right + \
            usage_new_right + usage_new_left + usage_new_cand
        db_gain = \
            log_gamma(usage_old_cs + constant * len_old_cs) - log_gamma(usage_new_cs + constant * len_new_cs) + \
            log_gamma(usage_new_left + constant) - log_gamma(usage_old_left + constant) + \
            log_gamma(usage_new_right + constant) - log_gamma(usage_old_right + constant) + \
            log_gamma(usage_new_cand + constant) - log_gamma(constant) + \
            log(constant * len_new_cs) - log_gamma(constant * len_old_cs)
        return db_gain

    def get_freq_in_all(self, pattern):
        freq = 0.0
        for item in pattern:
            support = 0
            for database in self.databases:
                support += database.get_support(item)
            freq += log2(support / self.all_db_card)
        return freq

    def estimate_usage(self, candidate):
        usage = 0
        usages_left = self.coding_sets_i[candidate.left_cs_id].gather_usages(candidate.left_is)
        usages_right = self.coding_sets_i[candidate.right_cs_id].gather_usages(candidate.right_is)
        for transaction in usages_left:
            if transaction in usages_right:
                usage += 1
        return usage

    def estimate_gain(self, candidate):
        total_db_gain_in_other_ct = 0.0
        total_positive_db_gain_in_other_ct = 0.0
        gains = []
        candidate_len = universal_code_len(len(candidate))
        freq_x_in_all_db = self.get_freq_in_all(candidate)
        estimate_diff_sj = candidate_len - freq_x_in_all_db
        if candidate.verify_same_ct() and self.coding_sets_i[candidate.left_cs_id].ct_type != 1:
            for ct_i in self.coding_sets_i:
                db_gain = self.calculate_db_gain(candidate, ct_i)
                gain = db_gain + estimate_diff_sj
                gains.append(gain)
                total_db_gain_in_other_ct += db_gain
                if gain > 0.0:
                    total_positive_db_gain_in_other_ct += gain
            combined_ct_gain = total_db_gain_in_other_ct + estimate_diff_sj
            if total_positive_db_gain_in_other_ct > 0.0:
                max_gain = max(total_positive_db_gain_in_other_ct, combined_ct_gain)
            else:
                max_gain = max(gains)
        else:
            cs_to_check = candidate.left_cs_id
            if not candidate.verify_same_ct():
                if self.coding_sets_i[candidate.left_cs_id].ct_type != 1:
                    cs_to_check = candidate.right_cs_id
            db_gain = self.calculate_db_gain(candidate, cs_to_check)
            max_gain = estimate_diff_sj + db_gain
        candidate.set_est_gain(max_gain)

    def create_candidate(self, left, right, left_cs_id, right_cs_id):
        new_candidate = Pattern(left, right, left_cs_id, right_cs_id)
        if not (self.already_generated(new_candidate)
                or self.already_rejected(new_candidate)
                or self.already_accepted(new_candidate)):
            if self.estimate_usage(new_candidate) > self.min_usage:
                self.estimate_gain(new_candidate)
                self.candidates.append(new_candidate)
            else:
                self.rejected_candidates.append(new_candidate)

    def generate_candidates(self):
        for group in self.u:
            cs_x_id = 0
            for cs_x in group:
                if len(group) > 1:
                    cs_y_id = cs_x_id + 1
                else:
                    cs_y_id = cs_x_id
                while cs_y_id < len(group):
                    for x in self.coding_sets_i[cs_x]:
                        for y in self.coding_sets_i[group[cs_y_id]]:
                            if x != y:
                                self.create_candidate(x, y, cs_x, group[cs_y_id])
                    cs_y_id += 1
                cs_x_id += 1
        self.candidates.sort(key=lambda z: z.get_est_gain(), reverse=True)

    def add_candidate_to_all(self):
        for cs_i in self.coding_sets_i:
            cs_i.try_add(self.current_candidate)

    def add_to_chosen(self, w):
        self.accepted = False
        w_id = 0
        gr_id = 0
        for group in self.u:
            if w[w_id] > self.min_gain:
                self.accepted_candidates.append(self.current_candidate)
                self.model[gr_id].append(self.current_candidate)
                self.accepted = True
            else:
                for cs in group:
                    self.coding_sets_i[cs].rollback()
                self.rejected_candidates.append(self.current_candidate)

    def check_gain_in_each(self):
        gain = []
        candidate_len = universal_code_len(len(self.current_candidate))
        freq_x_in_all_db = self.get_freq_in_all(self.current_candidate)
        estimate_diff_sj = candidate_len - freq_x_in_all_db
        for group in self.u:
            for cs_i in group:
                estimate_diff_sj += (self.coding_sets_i[cs_i].old_db_size - self.coding_sets_i[cs_i].encoded_db_size)
            gain.append(estimate_diff_sj)
        return gain

    def run(self):
        print("NИNИNИNИNИNИNИ étape 0 NИИNИNИNИNИNИN")
        self.init_alphabet()
        self.init_all_ct_i()
        self.generate_candidates()
        print("NИNИNИNИNИNИNИ étape 1 NИИNИNИNИNИNИN")
        while self.candidates:
            self.load_next_candidate()
            self.add_candidate_to_all()
            print("NИNИNИNИNИNИNИ étape 2 NИИNИNИNИNИNИN")
            w = self.check_gain_in_each()
            self.add_to_chosen(w)
            print("NИNИNИNИNИNИNИ étape 3 NИИNИNИNИNИNИN")
            if self.accepted:
                print("ici")
                print(self.current_candidate)
                self.generate_candidates()
            self.pp_db()

    def pp_db(self):
        """for database in self.databases:
            database.pp()
        print("NИNИNИNИNИNИNИ alphabet NИИNИNИNИNИNИN")
        print(self.alphabet)"""
        print("NИNИNИNИNИNИИ candidates NИИNИNИNИNИNИ")
        for x in self.candidates:
            print(x)
        for cs in self.coding_sets_i:
            cs.pp()
        print("NИNИNИNИNИNИИ model NИИNИNИNИNИNИ")
        print(self.model)
