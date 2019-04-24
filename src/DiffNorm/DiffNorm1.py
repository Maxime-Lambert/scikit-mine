from src.DiffNorm.CodeTable import CodeTable
from src.DiffNorm.DataBase import DataBase
from src.DiffNorm.Pattern import Pattern
from src.DiffNorm.DiffNormUtils import universal_code_len, log_gamma
from src.DiffNorm.PatternSet import PatternSet
from src.DiffNorm.PatternSet import ItemSet
from os import path
from math import log2


class DiffNorm1:
    """DiffNorm algorithme.

    DiffNorm algorithme class, main loop class
    where all the functions are called.

    todo:
        Get the file reading in another class. Implement kernel classes.
        Implement other feateurs from the research papers, like indexing candidates to
        consider them adding only in the codetables in which they were created and e.t.c.

    Parameters
    ----------
    nom_db: String
        Name of the file(with extension) whith the names of all
        databases that will be treated by this algorithme. Their names are
        separated by empty spaces and no new line in the end of file.
        Exemple:
            db1 db2 db3
    nom_u: String
        Name of the file(with extension) with the indexes of the databases
        to be grouped together. Indexing starts from 1. Indexes will
        be separated by empty spaces and  no new line in the end of file.
        Exemple:
            1 2 3
            1 2
        This will create S1 with (D1, D2, D3) and S2 with (D1, D2)

    Attributes
    ----------
    alphabet_id : int
        Token of id of the alphabet I.
    min_usage : int
        Minimun usage, used to filter low
        usage candidates.
        todo:
            Pass it in the parameters.
    min_gain : float
        Minimum gain in bits. If a candidate
        reduces the size of the model for atleast 1 bit it's accepted.
    num_iterations : int
        Number of iterations done.
    candidates : list of Pattern objects.
        List of candidates to consider adding to the model.
    rejected_candidates : list of Pattern objects
        List of previously rejected candidates.
    accepted_candidates : list of Pattern objects
        List of previously accepted candidates.
    databases : list of DataBase objects
        List of ALL databases.
    coding_sets_i : list of CodeTable objects
        List of ALL coding sets (Ci = I + all Sj, that i in j).
    coding_set_patterns1 : list of PatternSet objects
        List of ALL Sj/ pattern sets.
    u : list of int
        List of index sets, by default contains individual
        indexes of databases.
    alphabet : list of ItemSet objects
        List of all single items found in all the transactions
        of all the databases.
    current_candidate : Pattern object
        Current candidate that is being considered to add.
    all_db_card : int
        Sum of cardinalities of all databases.
    candidate_accepted : bool
        Boolean indicating whether previous candidate was accepted.
    commit_sj_id : list of int
        List of indexes of Sj where previous candidate was accepted.
    """

    def __init__(self, nom_db, nom_u):
        data_directory_path = "../../demo/"
        dn_dir = path.dirname(__file__)
        self.abs_file_path = path.join(dn_dir, data_directory_path)
        self.result_name = nom_db
        self.alphabet_id = -1
        self.min_usage = 150
        self.min_gain = 1.0
        self.num_iterations = 0
        self.candidates = []
        self.rejected_candidates = []
        self.accepted_candidates = []
        self.databases = []
        self.coding_sets_i = []
        self.coding_set_patterns1 = []
        self.u = []
        self.alphabet = []
        self.current_candidate = None
        self.all_db_card = 0
        self.candidate_accepted = False
        self.commit_sj_id = []

        file_db = open(self.abs_file_path + nom_db, "r")
        databases = file_db.readline().split(" ")
        db_id = 0
        for database in databases:
            new_db = DataBase(database, db_id)
            self.databases.append(new_db)
            self.coding_sets_i.append(CodeTable(new_db))
            self.u.append([db_id])
            self.all_db_card += new_db.db_card
            db_id += 1

        file_u = open(self.abs_file_path + nom_u, "r")
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
        """Initializes of the alphabet. We go through
        all databases and seek for the items never seen before.
        If on is found it's added to the alphabet.
        """
        for database in self.databases:
            for transaction in database:
                for item in transaction:
                    candidate = ItemSet([item])
                    if candidate not in self.alphabet:
                        self.alphabet.append(candidate)

    def set_initial_encoded_size(self):
        """Initializes the initial encoded size of all
        coding sets.
        """
        for cs in self.coding_sets_i:
            cs.initial_encoded_size = cs.encoded_db_size

    def set_final_encoded_size(self):
        """Initializes the final encoded size of all
        coding sets.
        """
        for cs in self.coding_sets_i:
            cs.final_encoded_size = cs.encoded_db_size

    def calc_db_sizes_all(self):
        """Call to calculate the encoded size of all
        coding sets.
        """
        for cs in self.coding_sets_i:
            cs.set_encoded_db_size(cs.calculate_db_encoded_size())

    # Initialize all Ci with the items of I and sorting it in SCO
    def init_all_ct_i(self):
        """Initializes all coding sets with items of the alphabet
        and sorts them in SCO. Also intializes list U with the
        indexes of coding set groups.
        """
        j = 0
        for cs in self.coding_sets_i:
            for itemset in self.alphabet:
                cs.add(itemset.copy())
            cs.sort_in_sco()
            cs.update_t_data()
            cs.update_usages()
            cs.update_usage()
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
        """Loads next candidate from the list of candidates.
        """
        self.current_candidate = self.candidates.pop(0)

    def already_generated(self, candidate):
        """Returns a boolean to indicate whether is in
        the list of candidates to consider(= if it was already generated).

        Parameters
        ----------
        candidate : Pattern object
            Candidate to check presense.
        """
        return candidate in self.candidates

    def already_rejected(self, candidate):
        """Returns a boolean to indicate whether is in
        the list of rejected candidates(= if it was already rejected).

        Parameters
        ----------
        candidate : Pattern object
            Candidate to check presense.
        """
        return candidate in self.rejected_candidates

    def already_accepted(self, candidate):
        """Returns a boolean to indicate whether is in
        the list of accepted candidates(= if it was already accepted).

        Parameters
        ----------
        candidate : Pattern object
            Candidate to check presense.
        """
        return candidate in self.accepted_candidates

    def estimate_db_gain(self, candidate, coding_set_id):
        """Returns estimation of candidates database gain,
        delta ^L(Sj + X union Y) + sum(delta ^Lprime(Di|Ci + X union Y).

        Parameters
        ----------
        candidate : Pattern object
            Candidate which estimated gain we want to know.
        coding_set_id : CodeTable object
            Coding set in which we consider adding the pattern.
        """
        constant = 0.5
        coding_set = self.coding_sets_i[coding_set_id]
        len_old_cs = coding_set.size
        len_new_cs = len_old_cs + 1
        usage_new_cand = self.estimate_max_usage_for_known_cs(
            candidate, coding_set_id)
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

    def get_freq_in_all(self, pattern):
        """Returns frequency of a pattern over all databases,
        sum(log(freq_in_D_cursive(x))).

        Parameters
        ----------
        pattern : Pattern object
            Candidate which frequency we want to know.
        """
        freq = 0.0
        for item in pattern:
            support = 0
            for database in self.databases:
                support += database.get_support(item)
            freq += log2(support / self.all_db_card)
        return freq

    def estimate_max_usage_for_known_cs(self, candidate, cs_id):
        """Returns estimation of candidates usage in a known Ci.
        Union of usages of left and right parent of this pattern.

        Parameters
        ----------
        candidate : Pattern object
            Candidate which estimated usage we want to know.
        cs_id : int
            Id of the coding set in which we want to estimate usage.
        """
        usages_left = \
            self.coding_sets_i[cs_id].gather_usages(candidate.left_is)
        usages_right = \
            self.coding_sets_i[cs_id].gather_usages(candidate.right_is)
        return len(usages_left & usages_right)

    def estimate_max_usage(self, candidate):
        """Returns maximal estimation of candidates usage.
        Calculating the usage in all coding sets and returning the max.

        Parameters
        ----------
        candidate : Pattern object
            Candidate which estimated usage we want to know.
        """
        max_usage = 0
        for cs_left in self.coding_sets_i:
            for cs_right in self.coding_sets_i:
                usages_left = cs_left.gather_usages(candidate.left_is)
                usages_right = cs_right.gather_usages(candidate.right_is)
                usage = len(usages_left & usages_right)
                if usage > max_usage:
                    max_usage = usage
        return max_usage

    def estimate_gain(self, candidate):
        """Returns estimation of candidates Sj gain,
        delta ^L(Sj + X union Y) + sum of estimate_db_gain for all Ci in the Sj.

        Parameters
        ----------
        candidate : Pattern object
            Candidate which estimated gain we want to know.
        """
        total_gain = 0.0
        candidate_len = universal_code_len(len(candidate))
        freq_x_in_all_db = self.get_freq_in_all(candidate)
        estimate_diff_sj = candidate_len + freq_x_in_all_db
        for j in self.u:
            gain_sj = estimate_diff_sj
            for i in j:
                gain_sj += self.estimate_db_gain(candidate, i)
            total_gain += gain_sj
        candidate.set_est_gain(total_gain)

    def reestimate_gain(self):
        for candidate in self.candidates:
            self.estimate_gain(candidate)

    def create_candidate(self, left, right, sj_id):
        """Create and check if the candidate hasn't been already created,
        rejected or accepted, filter low usage candidates and estimate their gain.

        Parameters
        ----------
        left : ItemSet object
            Left parent of candidate to be created.
        right : ItemSet object
            Right parent of candidate to be created.
        sj_id : int
            Sj id, j, from which this candidate comes from.
        """
        new_candidate = Pattern(left, right, sj_id)
        if not (self.already_generated(new_candidate)
                or self.already_rejected(new_candidate)
                or self.already_accepted(new_candidate)):
            if self.estimate_max_usage(new_candidate) > self.min_usage:
                self.estimate_gain(new_candidate)
                self.candidates.append(new_candidate)
            else:
                self.rejected_candidates.append(new_candidate)

    def generate_candidates(self):
        """Candidate generation.
        First step is to generate candidates from alphabet I, since
        the code tables are empty in the begining. For following
        iterations we go through the elements of Sj's and permute them
        with the previously added candidate.
        """
        # At first we generate candidates in I x I,
        # these candidates can be accepted in any Sj.
        if self.num_iterations == 0:
            x_id = 0
            while x_id < len(self.alphabet):
                y_id = x_id + 1
                while y_id < len(self.alphabet):
                    self.create_candidate(self.alphabet[x_id],
                                          self.alphabet[y_id], 0)
                    y_id += 1
                x_id += 1
        else:
            # Then we permute previously added candidate with items of I
            # and the patterns of sj in which it was added
            for j in self.commit_sj_id:
                for y in self.alphabet:
                    if y not in self.current_candidate:
                        self.create_candidate(self.current_candidate,
                                              y, 0)
                for y in self.coding_set_patterns1[j].patterns:
                    if y != self.current_candidate:
                        self.create_candidate(self.current_candidate,
                                              y, 0)
        # In the end we sort the candidates by their estimated gain.
        self.candidates.sort(key=lambda z: z.get_est_gain(), reverse=True)

    def add_candidate_to_all(self):
        """Adds candidate to all coding sets and
        calculates their encoded size.
        """
        for c_i in self.coding_sets_i:
            c_i.try_add(self.current_candidate)
        self.calc_db_sizes_all()

    def add_to_chosen(self, w):
        """Remove candidate from all Sj, where gain is inferior
        to self.min_gain.

        Parameters
        ----------
        w : list of float
            Contains actual gains of the candidate in all Sj"""
        self.candidate_accepted = False
        self.commit_sj_id = []
        w_id = 0
        u_copy = self.u.copy()
        u_copy.sort(
            key=lambda x: (w[self.u.index(x)], len(x), str(x)), reverse=True)
        j = 0
        while j < len(u_copy):
            if w[self.u.index(u_copy[j])] > self.min_gain:
                for i in u_copy[j]:
                    other_j = j + 1
                    while other_j < len(u_copy):
                        if i in u_copy[other_j]:
                            w[self.u.index(u_copy[other_j])] -= \
                                (self.coding_sets_i[i].old_db_size
                                 - self.coding_sets_i[i].encoded_db_size)
                        other_j += 1
            j += 1
        for j in self.u:
            if len(j) > 1:
                if w[w_id] > self.min_gain:
                    better_in_specific_sj = False
                    for i in j:
                        if w[i] > w[w_id]:
                            better_in_specific_sj = True
                    if not better_in_specific_sj:
                        self.accepted_candidates.append(self.current_candidate)
                        self.candidate_accepted = True
                        self.commit_sj_id.append(w_id)
                        self.coding_set_patterns1[w_id].try_add(
                            self.current_candidate)
                    else:
                        deleted = False
                        for i in j:
                            if w[i] < self.min_gain:
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
                    if self.current_candidate not in self.accepted_candidates:
                        self.accepted_candidates.append(self.current_candidate)
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

    def check_gain_in_each(self):
        """Returns list of actual gains of current candidate in all Sj.
        ∆L(D, S ⊕j Z) for all Sj.
        """
        gain = []
        for j in self.coding_set_patterns1:
            gain.append(j.calculate_patternset_diff_encoded_size(
                self.current_candidate))
        return gain

    def prune(self):
        """Prune algorithme.
        Implemented as described in DiffNorm research papers."""
        for ci in self.coding_sets_i:
            candidates = []
            for pattern in ci:
                if pattern.old_usage > pattern.usage and len(pattern) > 1:
                    candidates.append(pattern)
            candidates.sort(key=lambda x: x.old_usage - x.usage, reverse=True)
            while candidates:
                candidate = candidates.pop(0)
                c_i_with_cand = []
                db_split_diff = 0.0
                for c_i in self.coding_sets_i:
                    if candidate in c_i:
                        c_i_with_cand.append(c_i)
                        c_i.try_del(candidate)
                        c_i.set_encoded_db_size(
                            c_i.calculate_db_encoded_size())
                        db_split_diff += c_i.old_db_size - c_i.encoded_db_size
                total_diff = db_split_diff
                for s_j in self.coding_set_patterns1:
                    if candidate in s_j:
                        sub_db_split_diff = 0.0
                        for c_i in s_j.coding_sets:
                            sub_db_split_diff += \
                                c_i.old_db_size - c_i.encoded_db_size
                        total_diff += \
                            universal_code_len(s_j.size) \
                            - universal_code_len(s_j.size - 1) + \
                            universal_code_len(len(candidate)) \
                            - self.get_freq_in_all(candidate) \
                            + sub_db_split_diff
                if total_diff > 0:
                    for s_j in self.coding_set_patterns1:
                        if candidate in s_j:
                            s_j.try_del(candidate)
                    self.reestimate_gain()
                    self.candidates.sort(
                        key=lambda z: z.get_est_gain(), reverse=True)
                else:
                    for c_i in c_i_with_cand:
                        c_i.try_add(candidate)
                        c_i.set_encoded_db_size(
                            c_i.calculate_db_encoded_size())
                for pattern in ci:
                    if pattern.old_usage > pattern.usage and \
                            pattern not in candidates and len(pattern) > 1:
                        candidates.append(pattern)
                candidates.sort(
                        key=lambda x: x.old_usage - x.usage, reverse=True)

    def run(self):
        """DiffNorm run loop.
        Before entering the loop steps:
            1. Initialize alphabet.
            2. Initialize coding sets.
            3. Generate first batch of candidates.
        In loop steps:
            1. Load new candidate.
            2. Add current candidate to all Sj.
            3. Calculate actual gain in all Sj.
            4. Remove candidate from Sj, where gain is low.
            5. If candidate is added - prune and generate new candidates.
        """
        self.init_alphabet()
        self.init_all_ct_i()
        self.generate_candidates()
        while self.candidates:
            self.load_next_candidate()
            print("CANDIDATES LEFT: " + repr(len(self.candidates)))
            self.add_candidate_to_all()
            w = self.check_gain_in_each()
            self.add_to_chosen(w)
            self.num_iterations += 1
            if self.candidate_accepted:
                self.prune()
                self.reestimate_gain()
                self.generate_candidates()
            else:
                self.rejected_candidates.append(self.current_candidate)
        self.set_final_encoded_size()
        self.pp_db()
        self.write_to_disk()

    def pp_db(self):
        """Pretty-printer
        """
        print("<@@@@@@@@ alphabet @@@@@@@@>")
        print(self.alphabet)
        for cs in self.coding_sets_i:
            cs.pp()
        print("<@@@@@@@@ model @@@@@@@@>")
        for sj in self.coding_set_patterns1:
            sj.pp()

    def write_to_disk(self):
        result = open(self.abs_file_path + 'result_' +
                      self.result_name, "w+")
        result.write("<@@@@@@@@ Code Tables @@@@@@@@>" + "\n")
        for cs in self.coding_sets_i:
            result.write(cs.to_string() + "\n")
        result.write("<@@@@@@@@ Pattern Sets @@@@@@@@>" + "\n")
        for sj in self.coding_set_patterns1:
            result.write(sj.to_string() + "\n")
