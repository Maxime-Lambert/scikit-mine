from src.DiffNorm.CodeTable import *
from src.DiffNorm.DataBase import *
from src.DiffNorm.Pattern import *
from src.DiffNorm.DiffNormUtils import *

data_directory_path = "test/data/DiffNorm/"


class DiffNorm:

    global data_directory_path
    alphabet_id = -1
    # Minimum usage to filter the candidates before adding them to potential candidates
    min_usage = 120
    # Candidate will be added if he reduces the cost of encoded size of a database for at least 1 bit
    min_gain = 1.0

    def __init__(self, nom_db, nom_u):
        self.num_iterations = 0
        self.candidates = []
        self.rejected_candidates = []
        self.accepted_candidates = []
        self.databases = []
        # List of Ci
        self.coding_sets_i = []
        # List of Sj
        self.coding_set_patterns = []
        # Groups of i from Ci to form j from Sj
        self.u = []
        self.alphabet = []
        self.current_candidate = None
        # |D cursive|
        self.all_db_card = 0
        self.candidate_accepted = False
        # List of Sj where previous candidate was added in the last loop
        self.commit_sj_id = []

        file_db = open(data_directory_path + nom_db, "r")
        databases = file_db.readline().split(" ")
        db_id = 0
        for database in databases:
            new_db = DataBase(database, db_id)
            self.databases.append(new_db)
            self.coding_sets_i.append(CodeTable(new_db))
            self.u.append([db_id])
            self.all_db_card += len(new_db)
            db_id += 1

        file_u = open(data_directory_path + nom_u, "r")
        groupes = file_u.readlines()
        for line in groupes:
            if line[-1:] == '\n':
                line = line[:-1]
            group = line.split(" ")
            cs_param = []
            for db_id in group:
                if int(db_id) - 1 not in cs_param:
                    cs_param.append(int(db_id) - 1)
            if set(cs_param) not in self.u:
                if len(cs_param) > 1:
                    self.u.append(cs_param)

    # Initialize the alphabet I by going through all the transactions and saving all unique items = Standard Code Table
    def init_alphabet(self):
        for database in self.databases:
            for transaction in database:
                for item in transaction:
                    candidate = ItemSet([item])
                    if candidate not in self.alphabet:
                        self.alphabet.append(candidate)

    def set_initial_encoded_size(self):
        for cs in self.coding_sets_i:
            cs.initial_encoded_size = cs.encoded_db_size

    def set_final_encoded_size(self):
        for cs in self.coding_sets_i:
            cs.final_encoded_size = cs.encoded_db_size

    # For all Di in D cursive calculate and store L(Di|Ci).
    def calc_db_sizes_all(self):
        i = 0
        for cs in self.coding_sets_i:
            cs.set_encoded_db_size(cs.calculate_db_encoded_size())
            i += 1

    # Initialize all Ci with the items of I and sorting it in SCO
    def init_all_ct_i(self):
        for cs in self.coding_sets_i:
            for itemset in self.alphabet:
                cs.add(itemset.copy())
            cs.sort_in_sco()
            cs.update_t_data()
            cs.update_usage()
            cs.update_usages()
            self.coding_set_patterns.append(cs.copy())
        self.calc_db_sizes_all()
        self.set_initial_encoded_size()

    def init_s_j(self):
        for group in self.u:
            if len(group) > 1:
                self.coding_set_patterns.append(CodeTable(None))

    def load_next_candidate(self):
        self.current_candidate = self.candidates.pop(0)

    def already_generated(self, candidate):
        return candidate in self.candidates

    def already_rejected(self, candidate):
        return candidate in self.rejected_candidates

    def already_accepted(self, candidate):
        return candidate in self.accepted_candidates

    #  Calculate delta ^L(Sj + X union Y) + sum(delta ^Lprime(Di|Ci + X union Y) aka estimation of candidates gain in Ci
    def estimate_db_gain(self, candidate, coding_set_id):
        constant = 0.5
        coding_set = self.coding_sets_i[coding_set_id]
        len_old_cs = coding_set.size
        len_new_cs = len_old_cs + 1
        usage_new_cand = self.estimate_max_usage_for_known_cs(candidate, coding_set_id)
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

    #  Calculate sum(log(freq_in_D_cursive(x)))
    def get_freq_in_all(self, pattern):
        freq = 0.0
        for item in pattern:
            support = 0
            for database in self.databases:
                support += database.get_support(item)
            freq += log2(support / self.all_db_card)
        return freq

    """def get_freq_in_all(self, pattern):
        log_of_freq = 0.0
        for item in pattern:
            total_freq = 0.0
            for database in self.databases:
                total_freq += database.get_support(item) / database.db_card
            log_of_freq += log2(total_freq)
        return log_of_freq"""

    # Estimate candidate's usage for a known coding set: union of usages of left and right parent of this pattern
    def estimate_max_usage_for_known_cs(self, candidate, cs_id):
        usages_left = self.coding_sets_i[cs_id].gather_usages(candidate.left_is)
        usages_right = self.coding_sets_i[cs_id].gather_usages(candidate.right_is)
        return len(usages_left & usages_right)

    # Estimate candidate's usage for an arbitrary coding set
    def estimate_max_usage(self, candidate):
        max_usage = 0
        if candidate.left_cs_id == candidate.right_cs_id == self.alphabet_id:
            for cs_left in self.coding_sets_i:
                for cs_right in self.coding_sets_i:
                    usages_left = cs_left.gather_usages(candidate.left_is)
                    usages_right = cs_right.gather_usages(candidate.right_is)
                    usage = len(usages_left & usages_right)
                    if usage > max_usage:
                        max_usage = usage
        else:
            if candidate.left_cs_id > len(self.coding_sets_i):
                for cs_left_id in self.u[candidate.left_cs_id]:
                    for cs_right_id in self.u[candidate.left_cs_id]:
                        usages_left = self.coding_sets_i[cs_left_id].gather_usages(candidate.left_is)
                        usages_right = self.coding_sets_i[cs_right_id].gather_usages(candidate.right_is)
                        usage = len(usages_left & usages_right)
                        if usage > max_usage:
                            max_usage = usage
            else:
                usages_left = self.coding_sets_i[candidate.left_cs_id].gather_usages(candidate.left_is)
                usages_right = self.coding_sets_i[candidate.right_cs_id].gather_usages(candidate.right_is)
                max_usage = len(usages_left & usages_right)
        return max_usage

    #  Estimate candidate's gain for Sj: delta ^L(Sj + X union Y) + sum of estimate_db_gain for all Ci in the Sj
    def estimate_gain(self, candidate):
        max_gain = 0.0
        candidate_len = universal_code_len(len(candidate))
        freq_x_in_all_db = self.get_freq_in_all(candidate)
        estimate_diff_sj = candidate_len + freq_x_in_all_db
        """print("CANDIDATE ITSELF")
        print(candidate)
        print("CAND LEN:")
        print(candidate_len)
        print("FREQ IN ALL")
        print(freq_x_in_all_db)"""
        if candidate.left_cs_id == candidate.right_cs_id == self.alphabet_id:
            for j in self.u:
                gain_sj = estimate_diff_sj
                for i in j:
                    gain_sj += self.estimate_db_gain(candidate, i)
                """print("GAIN S" + repr(j))
                print(gain_sj)
                print("MAX")
                print(max_gain)"""
                if gain_sj > max_gain:
                    max_gain = gain_sj
        else:
            gain_sj = estimate_diff_sj
            for i in self.u[candidate.right_cs_id]:
                gain_sj += self.estimate_db_gain(candidate, i)
            if gain_sj > max_gain:
                max_gain = gain_sj
        candidate.set_est_gain(max_gain)

    """Create and check if the candidate hasn't been already created, rejected or accepted, 
    filter low usage candidates and estimate their gain"""
    def create_candidate(self, left, right, left_cs_id, right_cs_id):
        new_candidate = Pattern(left, right, left_cs_id, right_cs_id)
        if not (self.already_generated(new_candidate)
                or self.already_rejected(new_candidate)
                or self.already_accepted(new_candidate)):
            if self.estimate_max_usage(new_candidate) > self.min_usage:
                self.estimate_gain(new_candidate)
                self.candidates.append(new_candidate)
            else:
                self.rejected_candidates.append(new_candidate)

    #  Generate a list of candidates to consider
    def generate_candidates(self):
        # At first we generate candidates in I x I, these candidates can be accepted in any Sj.
        if self.num_iterations == 0:
            x_id = 0
            while x_id < len(self.alphabet):
                y_id = x_id + 1
                while y_id < len(self.alphabet):
                    self.create_candidate(self.alphabet[x_id], self.alphabet[y_id], self.alphabet_id, self.alphabet_id)
                    y_id += 1
                x_id += 1
        else:
            # Then we permute previously added candidate with the patterns and items of sj in which it was added
            for j in self.commit_sj_id:
                for pattern in self.coding_sets_i[j]:
                    if len(pattern) == 1:
                        if pattern not in self.current_candidate:
                            self.create_candidate(pattern, self.current_candidate, j, j)
                    else:
                        self.create_candidate(pattern, self.current_candidate, j, j)
        self.candidates.sort(key=lambda z: z.get_est_gain(), reverse=True)

    """Add the candidate to all concerned Sj, i.e. if the candidate is I x I then he can be added anywhere, but if it's
    Sj x I or Sj x Sj, it can be added only in Sj"""
    def add_candidate_to_all(self):
        if self.current_candidate.left_cs_id == self.current_candidate.right_cs_id == self.alphabet_id:
            for c_i in self.coding_sets_i:
                c_i.try_add(self.current_candidate)
            self.calc_db_sizes_all()
        else:
            for i in self.u[self.current_candidate.left_cs_id]:
                self.coding_sets_i[i].try_add(self.current_candidate)
                self.coding_sets_i[i].set_encoded_db_size(self.coding_sets_i[i].calculate_db_encoded_size())

    # Filter the candidate by minimum gain
    def add_to_chosen(self, w):
        self.candidate_accepted = False
        self.commit_sj_id = []
        w_id = 0
        """print("HERE IS W:")
        print(w)
        print("FOR CANDIDATE: ")
        print(self.current_candidate)
        print(" ")"""
        if self.current_candidate.left_cs_id == self.current_candidate.right_cs_id == self.alphabet_id:
            for group in self.u:
                if w[w_id] > self.min_gain:
                    self.accepted_candidates.append(self.current_candidate)
                    self.candidate_accepted = True
                    self.commit_sj_id.append(w_id)
                    self.coding_set_patterns[w_id].try_add(self.current_candidate)
                else:
                    for cs in group:
                        self.coding_sets_i[cs].delete_pattern(self.current_candidate)
                        self.coding_sets_i[cs].rollback()
                    self.rejected_candidates.append(self.current_candidate)
                w_id += 1
        else:
            if w[self.current_candidate.left_cs_id] > self.min_gain:
                self.accepted_candidates.append(self.current_candidate)
                self.candidate_accepted = True
                self.commit_sj_id.append(self.current_candidate.left_cs_id)
                self.coding_set_patterns[self.current_candidate.left_cs_id].try_add(self.current_candidate)
            else:
                for cs in self.u[self.current_candidate.left_cs_id]:
                    self.coding_sets_i[cs].delete_pattern(self.current_candidate)
                    self.coding_sets_i[cs].rollback()
                self.rejected_candidates.append(self.current_candidate)

    # Calculate ∆L(D, S ⊕j Z) for all Sj
    def check_gain_in_each(self):
        gain = []
        candidate_len = universal_code_len(len(self.current_candidate))
        freq_x_in_all_db = self.get_freq_in_all(self.current_candidate)
        estimate_diff_sj = candidate_len + freq_x_in_all_db
        if self.current_candidate.left_cs_id == self.current_candidate.right_cs_id == self.alphabet_id:
            for j in self.u:
                gain_group = estimate_diff_sj
                for i in j:
                    #  print("-----------------" + repr(i) + "-----------------")
                    gain_group += (self.coding_sets_i[i].old_db_size - self.coding_sets_i[i].encoded_db_size)
                    '''print("OLD CSS")
                    print(self.coding_sets_i[i].old_db_size)
                    print("NEW")
                    print(self.coding_sets_i[i].encoded_db_size)
                    print("DIFF SJ")
                    print(estimate_diff_sj)
                    print("GAIN GROUP")
                    print(gain_group)'''
                gain.append(gain_group)
        else:
            concerned_cs = 0
            for j in self.u:
                gain_group = 0.0
                if concerned_cs == self.current_candidate.right_cs_id:
                    gain_group = estimate_diff_sj
                    for i in j:
                        gain_group += (self.coding_sets_i[i].old_db_size - self.coding_sets_i[i].encoded_db_size)
                gain.append(gain_group)
                concerned_cs += 1
        return gain

    def prune(self):
        j = 0
        for cs in self.coding_sets_i:
            candidates = []
            for pattern in cs:
                if pattern.old_usage > pattern.usage and len(pattern) > 1:
                    candidates.append(pattern)
            candidates.sort(key=lambda x: x.old_usage - x.usage, reverse=True)
            while candidates:
                old_db_size = cs.calculate_db_encoded_size()
                candidate = candidates.pop(0)
                cs.try_del(candidate)
                new_db_size = cs.calculate_db_encoded_size()
                if old_db_size < new_db_size:
                    cs.try_add(candidate)
                else:
                    self.candidates.sort(key=lambda z: z.get_est_gain(), reverse=True)
                    for group in self.u:
                        if j in group:
                            self.coding_set_patterns[j].try_del(candidate)
                for pattern in cs:
                    if pattern.old_usage > pattern.usage and pattern not in candidates and len(pattern) > 1:
                        candidates.append(pattern)
                candidates.sort(key=lambda x: x.old_usage - x.usage, reverse=True)
            j += 1

    def run(self):
        self.init_alphabet()
        self.init_all_ct_i()
        self.init_s_j()
        self.generate_candidates()
        while self.candidates:
            print("CANDIDATES LEFT: " + repr(len(self.candidates)))
            self.load_next_candidate()
            # print("LOADED NEW CANDIDATE")
            # print(self.current_candidate)
            self.add_candidate_to_all()
            w = self.check_gain_in_each()
            self.add_to_chosen(w)
            self.num_iterations += 1
            if self.candidate_accepted:
                #  print("ADDED")
                self.prune()
                for candidate in self.candidates:
                    self.estimate_gain(candidate)
                self.generate_candidates()
            else:
                self.rejected_candidates.append(self.current_candidate)
        self.set_final_encoded_size()
        self.pp_db()

    def pp_db(self):
        """for database in self.databases:
            database.pp()"""
        print("NИNИNИNИNИNИNИ alphabet NИИNИNИNИNИNИN")
        print(self.alphabet)
        """print("NИNИNИNИNИNИИ candidates NИИNИNИNИNИNИ")
        for x in self.candidates:
            if x.max_gain > -10:
                print(repr(x) + " | " + repr(x.left_cs_id) + " | " + repr(x.right_cs_id) + " | " + repr(x.max_gain))"""
        for cs in self.coding_sets_i:
            cs.pp()
        print("NИNИNИNИNИNИИ model NИИNИNИNИNИNИ")
        j = 1
        for sj in self.coding_set_patterns:
            print("S" + repr(j) + ": ")
            sj.pp()
            j += 1
