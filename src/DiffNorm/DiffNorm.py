from src.DiffNorm.CodeTable import CodeTable
from src.DiffNorm.DataBase import DataBase
from src.DiffNorm.Pattern import Pattern
from src.DiffNorm.DiffNormUtils import universal_code_len, log_gamma
from src.DiffNorm.PatternSet import PatternSet
from src.DiffNorm.PatternSet import ItemSet
from os import path
from math import log2


class DiffNorm:

    alphabet_id = -1
    # Minimum usage to filter the candidates before
    # adding them to potential candidates
    min_usage = 5
    # Candidate will be added if he reduces the cost of encoded size
    # of a database for at least 1 bit
    min_gain = 1.0

    def __init__(self, nom_db, nom_u):
        data_directory_path = "../../test/data/DiffNorm/"
        dn_dir = path.dirname(__file__)
        abs_file_path = path.join(dn_dir, data_directory_path)
        self.num_iterations = 0
        self.candidates = []
        self.rejected_candidates = []
        self.accepted_candidates = []
        self.databases = []
        # List of Ci
        self.coding_sets_i = []
        # List of Sj
        self.coding_set_patterns = []
        # Will change the upper one,
        # was done to not to break already working envirenement
        self.coding_set_patterns1 = []
        # Groups of i from Ci to form j from Sj
        self.u = []
        self.alphabet = []
        self.current_candidate = None
        # |D cursive|
        self.all_db_card = 0
        self.candidate_accepted = False
        # List of Sj where previous candidate was added in the last loop
        self.commit_sj_id = []

        file_db = open(abs_file_path + nom_db, "r")
        databases = file_db.readline().split(" ")
        db_id = 0
        for database in databases:
            new_db = DataBase(database, db_id)
            self.databases.append(new_db)
            self.coding_sets_i.append(CodeTable(new_db))
            self.u.append([db_id])
            self.all_db_card += new_db.db_card
            db_id += 1

        file_u = open(abs_file_path + nom_u, "r")
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

    # Initialize the alphabet I by going through all the transactions
    # and saving all unique items = Standard Code Table
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
        for cs in self.coding_sets_i:
            cs.set_encoded_db_size(cs.calculate_db_encoded_size())

    # Initialize all Ci with the items of I and sorting it in SCO
    def init_all_ct_i(self):
        j = 0
        for cs in self.coding_sets_i:
            for itemset in self.alphabet:
                cs.add(itemset.copy())
            cs.sort_in_sco()
            cs.update_t_data()
            cs.update_usage()
            cs.update_usages()
            self.coding_set_patterns.append(cs.copy())
            sj = PatternSet([cs], self.databases, j)
            sj.sort_in_sco()
            self.coding_set_patterns1.append(sj)
            j += 1
        self.calc_db_sizes_all()
        self.set_initial_encoded_size()
        for group in self.u:
            if len(group) > 1:
                list_of_cs = []
                for cs_id in group:
                    list_of_cs.append(self.coding_sets_i[cs_id])
                sj = PatternSet(list_of_cs, self.databases, j)
                sj.sort_in_sco()
                self.coding_set_patterns1.append(sj)
                j += 1

    def load_next_candidate(self):
        self.current_candidate = self.candidates.pop(0)

    def already_generated(self, candidate):
        return candidate in self.candidates

    def already_rejected(self, candidate):
        return candidate in self.rejected_candidates

    def already_accepted(self, candidate):
        return candidate in self.accepted_candidates

    #  Calculate delta ^L(Sj + X union Y) +
    #  sum(delta ^Lprime(Di|Ci + X union Y)
    #  aka estimation of candidates gain in Ci
    def estimate_db_gain(self, candidate, coding_set_id):
        constant = 0.5
        coding_set = self.coding_sets_i[coding_set_id]
        len_old_cs = coding_set.size
        len_new_cs = len_old_cs + 1
        usage_new_cand = self.estimate_max_usage_for_known_cs(candidate,
                                                              coding_set_id)
        usage_old_left = len(coding_set.gather_usages(candidate.left_is))
        usage_old_right = len(coding_set.gather_usages(candidate.right_is))
        usage_new_left = usage_old_left - usage_new_cand
        usage_new_right = usage_old_right - usage_new_cand
        usage_old_cs = coding_set.usage
        usage_new_cs = \
            usage_old_cs - usage_old_right - usage_old_left + \
            usage_new_right + usage_new_left + usage_new_cand
        db_gain = \
            log_gamma(usage_old_cs + constant * len_old_cs) \
            - log_gamma(usage_new_cs + constant * len_new_cs) + \
            log_gamma(usage_new_left + constant) \
            - log_gamma(usage_old_left + constant) + \
            log_gamma(usage_new_right + constant) \
            - log_gamma(usage_old_right + constant) + \
            log_gamma(usage_new_cand + constant) - log_gamma(constant) + \
            log_gamma(constant * len_new_cs) - log_gamma(constant * len_old_cs)
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

    # Estimate candidate's usage for a known coding set:
    # union of usages of left and right parent of this pattern
    def estimate_max_usage_for_known_cs(self, candidate, cs_id):
        usages_left = \
            self.coding_sets_i[cs_id].gather_usages(candidate.left_is)
        usages_right = \
            self.coding_sets_i[cs_id].gather_usages(candidate.right_is)
        return len(usages_left & usages_right)

    # Estimate candidate's usage for an arbitrary coding set
    def estimate_max_usage(self, candidate):
        max_usage = 0
        if candidate.sj_id == candidate.right_cs_id == self.alphabet_id:
            for cs_left in self.coding_sets_i:
                for cs_right in self.coding_sets_i:
                    usages_left = cs_left.gather_usages(candidate.left_is)
                    usages_right = cs_right.gather_usages(candidate.right_is)
                    usage = len(usages_left & usages_right)
                    if usage > max_usage:
                        max_usage = usage
        else:
            if candidate.sj_id >= len(self.coding_sets_i):
                for cs_left_id in self.u[candidate.sj_id]:
                    for cs_right_id in self.u[candidate.sj_id]:
                        usages_left = \
                            self.coding_sets_i[cs_left_id].gather_usages(
                                candidate.left_is)
                        usages_right = \
                            self.coding_sets_i[cs_right_id].gather_usages(
                                candidate.right_is)
                        usage = len(usages_left & usages_right)
                        if usage > max_usage:
                            max_usage = usage
            else:
                usages_left = \
                    self.coding_sets_i[candidate.left_cs_id].gather_usages(
                        candidate.left_is)
                usages_right = \
                    self.coding_sets_i[candidate.right_cs_id].gather_usages(
                        candidate.right_is)
                max_usage = len(usages_left & usages_right)
        return max_usage

    #  Estimate candidate's gain for Sj: delta ^L(Sj + X union Y)
    #  + sum of estimate_db_gain for all Ci in the Sj
    def estimate_gain(self, candidate):
        max_gain = 0.0
        candidate_len = universal_code_len(len(candidate))
        freq_x_in_all_db = self.get_freq_in_all(candidate)
        estimate_diff_sj = candidate_len + freq_x_in_all_db
        if candidate.sj_id == candidate.right_cs_id == self.alphabet_id:
            for j in self.u:
                gain_sj = estimate_diff_sj
                for i in j:
                    gain_sj += self.estimate_db_gain(candidate, i)
                if gain_sj > max_gain:
                    max_gain = gain_sj
        else:
            gain_sj = estimate_diff_sj
            for i in self.u[candidate.sj_id]:
                gain_ci = self.estimate_db_gain(candidate, i)
                gain_sj += gain_ci
                if gain_ci > max_gain:
                    max_gain = gain_ci
            if gain_sj > max_gain:
                max_gain = gain_sj
        candidate.set_est_gain(max_gain)

    def reestimate_gain(self):
        for candidate in self.candidates:
            self.estimate_gain(candidate)

    """Create and check if the candidate hasn't been already created, 
    rejected or accepted, filter low usage candidates and estimate 
    their gain"""
    def create_candidate(self, left, right, left_cs_id, right_cs_id, sj_id):
        new_candidate = Pattern(left, right, left_cs_id, right_cs_id, sj_id)
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
        # At first we generate candidates in I x I,
        # these candidates can be accepted in any Sj.
        if self.num_iterations == 0:
            x_id = 0
            while x_id < len(self.alphabet):
                y_id = x_id + 1
                while y_id < len(self.alphabet):
                    self.create_candidate(
                        self.alphabet[x_id],
                        self.alphabet[y_id], self.alphabet_id,
                        self.alphabet_id, self.alphabet_id)
                    y_id += 1
                x_id += 1
        else:
            # Then we permute previously added candidate with items of I
            # and the patterns of sj in which it was added
            for j in self.commit_sj_id:
                for y in self.alphabet:
                    if y not in self.current_candidate:
                        self.create_candidate(
                            self.current_candidate, y, j, j, j)
                for y in self.coding_set_patterns1[j].patterns:
                    if y != self.current_candidate:
                        self.create_candidate(
                            self.current_candidate, y, j, j, j)
                """else:
                    cs_x_id = 0
                    while cs_x_id < len(self.coding_set_patterns1[j].patterns):
                        for y in self.alphabet:
                            if y not in self.coding_set_patterns1[j].patterns[
                            cs_x_id]:
                                self.create_candidate(
                                self.coding_set_patterns1[j].patterns[
                                cs_x_id], y, j, j, j)
                        cs_y_id = cs_x_id + 1
                        while cs_y_id < \
                        len(self.coding_set_patterns1[j].patterns):
                            self.create_candidate(
                            self.coding_set_patterns1[j].patterns[cs_x_id],
                                                  self.coding_set_patterns1[
                                                  j].patterns[cs_y_id],
                                                  j, j, j)
                            cs_y_id += 1
                        cs_x_id += 1"""
        self.candidates.sort(key=lambda z: z.get_est_gain(), reverse=True)

    """Add the candidate to all concerned Sj, i.e. if the candidate is I x I 
    then he can be added anywhere, but if it's
    Sj x I or Sj x Sj, it can be added only in Sj"""
    def add_candidate_to_all(self):
        if self.current_candidate.left_cs_id == \
                self.current_candidate.right_cs_id == self.alphabet_id:
            for c_i in self.coding_sets_i:
                c_i.try_add(self.current_candidate)
            self.calc_db_sizes_all()
        else:
            for i in self.u[self.current_candidate.sj_id]:
                self.coding_sets_i[i].try_add(self.current_candidate)
                self.coding_sets_i[i].set_encoded_db_size(
                    self.coding_sets_i[i].calculate_db_encoded_size())

    # Filter the candidate by minimum gain
    def add_to_chosen(self, w):
        self.candidate_accepted = False
        self.commit_sj_id = []
        print("HERE IS W:")
        print(w)
        print("FOR CANDIDATE: ")
        print(self.current_candidate)
        print(" ")
        if self.current_candidate.left_cs_id == \
                self.current_candidate.right_cs_id == self.alphabet_id:
            w_id = 0
            for j in self.u:
                if len(j) > 1:
                    if w[w_id] > self.min_gain:
                        better_in_specific_sj = False
                        ids_of_better = []
                        for i in j:
                            if w[i] > w[w_id]:
                                better_in_specific_sj = True
                                ids_of_better.append(i)
                        if not better_in_specific_sj:
                            self.accepted_candidates.append(
                                self.current_candidate)
                            self.candidate_accepted = True
                            self.commit_sj_id.append(w_id)
                            self.coding_set_patterns1[w_id].try_add(
                                self.current_candidate)
                        else:
                            deleted = False
                            for i in j:
                                if i not in ids_of_better:
                                    deleted = True
                                    self.coding_sets_i[i].delete_pattern(
                                        self.current_candidate)
                                    self.coding_sets_i[i].rollback()
                            if deleted:
                                if self.current_candidate not in \
                                        self.rejected_candidates:
                                    self.rejected_candidates.append(
                                        self.current_candidate)
                else:
                    if w[w_id] > self.min_gain:
                        if self.current_candidate not in \
                                self.accepted_candidates:
                            self.accepted_candidates.append(
                                self.current_candidate)
                        self.candidate_accepted = True
                        self.commit_sj_id.append(w_id)
                        self.coding_set_patterns1[w_id].try_add(
                            self.current_candidate)
                    else:
                        exist_cmn_in_need = False
                        other_w_id = 0
                        for other_j in self.u:
                            if len(other_j) > 1 and w_id in other_j and \
                                    w[other_w_id] > self.min_gain:
                                exist_cmn_in_need = True
                            other_w_id += 1
                        if not exist_cmn_in_need:
                            self.coding_sets_i[w_id].delete_pattern(
                                self.current_candidate)
                            self.coding_sets_i[w_id].rollback()
                            if self.current_candidate not in \
                                    self.rejected_candidates:
                                self.rejected_candidates.append(
                                    self.current_candidate)
                w_id += 1
        else:
            if len(self.u[self.current_candidate.sj_id]) > 1:
                if w[self.current_candidate.sj_id] > self.min_gain:
                    better_in_specific_sj = False
                    ids_of_better = []
                    for i in self.u[self.current_candidate.sj_id]:
                        if w[i] > w[self.current_candidate.sj_id]:
                            better_in_specific_sj = True
                            ids_of_better.append(i)
                    if not better_in_specific_sj:
                        self.accepted_candidates.append(self.current_candidate)
                        self.candidate_accepted = True
                        self.commit_sj_id.append(self.current_candidate.sj_id)
                        self.coding_set_patterns1[
                            self.current_candidate.sj_id].try_add(
                            self.current_candidate)
                    else:
                        deleted = False
                        accepted = False
                        for i in self.u[self.current_candidate.sj_id]:
                            if i in ids_of_better:
                                accepted = True
                                self.candidate_accepted = True
                                self.commit_sj_id.append(i)
                                self.coding_set_patterns1[i].try_add(
                                    self.current_candidate)
                            else:
                                deleted = True
                                self.coding_sets_i[i].delete_pattern(
                                    self.current_candidate)
                                self.coding_sets_i[i].rollback()
                        if deleted:
                            if self.current_candidate not in \
                                    self.rejected_candidates:
                                self.rejected_candidates.append(
                                    self.current_candidate)
                        if accepted:
                            if self.current_candidate not in \
                                    self.rejected_candidates:
                                self.accepted_candidates.append(
                                    self.current_candidate)
                else:
                    for cs_id in self.u[self.current_candidate.sj_id]:
                        self.coding_sets_i[cs_id].delete_pattern(
                            self.current_candidate)
                        self.coding_sets_i[cs_id].rollback()
                    if self.current_candidate not in self.rejected_candidates:
                        self.rejected_candidates.append(self.current_candidate)
            else:
                if w[self.current_candidate.sj_id] > self.min_gain:
                    self.accepted_candidates.append(self.current_candidate)
                    self.candidate_accepted = True
                    self.commit_sj_id.append(self.current_candidate.sj_id)
                    self.coding_set_patterns1[
                        self.current_candidate.sj_id].try_add(
                        self.current_candidate)
                else:
                    self.coding_sets_i[
                        self.current_candidate.sj_id].delete_pattern(
                        self.current_candidate)
                    self.coding_sets_i[self.current_candidate.sj_id].rollback()
                    if self.current_candidate not in self.rejected_candidates:
                        self.rejected_candidates.append(self.current_candidate)

    # Calculate ∆L(D, S ⊕j Z) for all Sj
    def check_gain_in_each(self):
        gain = []
        """candidate_len = universal_code_len(len(self.current_candidate))
        freq_x_in_all_db = self.get_freq_in_all(self.current_candidate)
        estimate_diff_sj = candidate_len + freq_x_in_all_db"""
        if self.current_candidate.left_cs_id == \
                self.current_candidate.right_cs_id == self.alphabet_id:
            for j in self.u:
                """gain_group = estimate_diff_sj"""
                gain_group = 0.0
                for i in j:
                    gain_group += (self.coding_sets_i[i].old_db_size
                                   - self.coding_sets_i[i].encoded_db_size)
                    """print("-----------------" + repr(i) + 
                    "-----------------")
                    print("OLD CSS")
                    print(self.coding_sets_i[i].old_db_size)
                    print("NEW")
                    print(self.coding_sets_i[i].encoded_db_size)
                    print("GAIN GROUP")
                    print(gain_group)"""
                gain.append(gain_group)
        else:
            concerned_cs = 0
            for j in self.u:
                gain_group = 0.0
                if concerned_cs == self.current_candidate.sj_id:
                    """gain_group = estimate_diff_sj"""
                    if len(j) > 1:
                        for i in j:
                            gain_alone = (
                                    self.coding_sets_i[i].old_db_size
                                    - self.coding_sets_i[i].encoded_db_size)
                            gain_group += gain_alone
                            gain[i] = gain_alone
                            """print("-----------------" + repr(i) + 
                            "-----------------")
                            print("OLD CSS")
                            print(self.coding_sets_i[i].old_db_size)
                            print("NEW")
                            print(self.coding_sets_i[i].encoded_db_size)
                            print("GAIN GROUP")
                            print(gain_group)"""
                    else:
                        gain_group = (
                                self.coding_sets_i[j[0]].old_db_size
                                - self.coding_sets_i[j[0]].encoded_db_size)
                gain.append(gain_group)
                concerned_cs += 1
        return gain

    def prune(self):
        for cs in self.coding_sets_i:
            cs.pp()
            candidates = []
            for pattern in cs:
                if pattern.old_usage > pattern.usage and len(pattern) > 1:
                    candidates.append(pattern)
            candidates.sort(key=lambda x: x.old_usage - x.usage, reverse=True)
            while candidates:
                candidate = candidates.pop(0)
                j = 0
                while j < len(self.coding_set_patterns1):
                    if candidate in self.coding_set_patterns1[j]:
                        print()
                        print(candidate)
                        print("J HERE " + repr(j))
                        total_diff = 0.0
                        for c_i in self.coding_set_patterns1[j].coding_sets:
                            old_db_size = c_i.calculate_db_encoded_size()
                            c_i.try_del(candidate)
                            new_db_size = c_i.calculate_db_encoded_size()
                            total_diff += old_db_size - new_db_size
                        print("TOTAL")
                        print(total_diff)
                        if total_diff > 0:
                            print("Less")
                            self.coding_set_patterns1[j].try_del(candidate)
                            self.coding_set_patterns1[j].pp()
                            cs_to_del_candidate = \
                                self.coding_set_patterns1[j].get_cs_ids()
                            print("DELETE FROM THESE ")
                            print(cs_to_del_candidate)
                            for sj in self.coding_set_patterns1:
                                if candidate in sj:
                                    for cs_id in sj.get_cs_ids():
                                        if cs_id in cs_to_del_candidate:
                                            cs_to_del_candidate.remove(cs_id)
                            for cs_id in \
                                    self.coding_set_patterns1[j].get_cs_ids():
                                if cs_id not in cs_to_del_candidate:
                                    self.coding_sets_i[cs_id].try_add(
                                        candidate)
                            print("DELETE FROM THESE ")
                            print(cs_to_del_candidate)
                            for cs_id in cs_to_del_candidate:
                                self.coding_sets_i[cs_id].pp()
                                self.coding_sets_i[cs_id].set_encoded_db_size(
                                    self.coding_sets_i[
                                        cs_id].calculate_db_encoded_size())
                            self.reestimate_gain()
                            self.candidates.sort(
                                key=lambda z: z.get_est_gain(), reverse=True)
                        else:
                            for c_i in \
                                    self.coding_set_patterns1[j].coding_sets:
                                c_i.try_add(candidate)
                    j += 1
                """old_db_size = cs.calculate_db_encoded_size()
                candidate = candidates.pop(0)
                cs.try_del(candidate)
                new_db_size = cs.calculate_db_encoded_size()
                if old_db_size < new_db_size:
                    cs.try_add(candidate)
                else:
                    cs.set_encoded_db_size(cs.calculate_db_encoded_size())
                    self.reestimate_gain()
                    self.candidates.sort(
                    key=lambda z: z.get_est_gain(), reverse=True)
                    group_id = 0
                    for group in self.u:
                        if j in group:
                            print("HERE")
                            print(candidate)
                            self.coding_set_patterns1[group_id].pp()
                            #  self.coding_set_patterns[j].try_del(candidate)
                            if candidate in 
                            self.coding_set_patterns1[group_id]:
                                self.coding_set_patterns1[group_id].try_del(
                                candidate)
                        group_id += 1"""
                for pattern in cs:
                    if pattern.old_usage > pattern.usage and pattern not in \
                            candidates and len(pattern) > 1:
                        candidates.append(pattern)
                candidates.sort(
                    key=lambda x: x.old_usage - x.usage, reverse=True)

    def run(self):
        self.init_alphabet()
        self.init_all_ct_i()
        self.generate_candidates()
        while self.candidates:
            """for c in self.candidates:
                print(c)"""
            self.load_next_candidate()
            """print("LOADED NEW CANDIDATE")
            print(self.current_candidate)"""
            print("CANDIDATES LEFT: " + repr(len(self.candidates)))
            self.add_candidate_to_all()
            w = self.check_gain_in_each()
            self.add_to_chosen(w)
            self.num_iterations += 1
            if self.candidate_accepted:
                print("ADDED")
                print(self.commit_sj_id)
                self.prune()
                for el in self.coding_set_patterns1:
                    el.pp()
                for candidate in self.candidates:
                    self.estimate_gain(candidate)
                self.reestimate_gain()
                self.generate_candidates()
            else:
                self.rejected_candidates.append(self.current_candidate)
        self.set_final_encoded_size()
        self.pp_db()
        """for c in self.rejected_candidates:
            print(c)"""

    def pp_db(self):
        print("NИNИNИNИNИNИNИ alphabet NИИNИNИNИNИNИN")
        print(self.alphabet)
        for cs in self.coding_sets_i:
            cs.pp()
        print("@@@@@@@@@@@@@@@ model @@@@@@@@@@@@@@@")
        for sj in self.coding_set_patterns1:
            sj.pp()
