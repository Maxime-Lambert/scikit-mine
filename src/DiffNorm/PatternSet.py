from src.DiffNorm.ItemSet import ItemSet
from src.DiffNorm.DiffNormUtils import universal_code_len
from math import log2


class PatternSet:
    """Part of coding set/ Sj.

    Structure representing Sj in the research papers. Stores items
    all the patterns related to the group j (group of Databases that
    the user wish to study).

    todo:
        Make this class inherit from something and get rid of useless
        built-in functions.

    Parameters
    ----------
    coding_sets : list of CodeTable objects
        Coding sets that contain the patterns of this PatternSet.
    all_databases : list of DataBase objects
        List of ALL databases.
    j : int
        id of self, mostly used for PrettyPrinter.

    Attributes
    ----------
    index : int
        Iterator over the contents of this table.
    j : int
        Index of this pattern set, j like in Sj.
    size : int
        Number of elements in this pattern set.
    patterns : list of ItemSet objects
        List of items of all the patterns related to all
        the databases associated to this pattern set.
    coding_sets : list of CodeTable objects
        List of Ci, that i in j and self is Sj.
    all_databases : list of DataBase objects
        List of ALL Di, not only those who are related to this Sj.
    all_db_card : int
        Sum of cardinals of all Di in self.all_databases
    databases : list of DataBase objects
        List of Di, that i in j and self is Sj, only databases that are
        related to this pattern set.
    """

    def __init__(self, coding_sets, all_databases, j):
        self.index = 0
        self.j = j
        self.size = 0
        self.patterns = []
        self.coding_sets = coding_sets
        self.all_databases = all_databases
        self.all_db_card = 0
        for database in self.all_databases:
            self.all_db_card += database.db_card
        self.databases = []
        for cs in coding_sets:
            self.databases.append(cs.database)

    def __repr__(self):
        return repr(self.patterns)

    def __iter__(self):
        return iter(self.patterns)

    def __next__(self):
        self.index += 1
        try:
            return self.patterns[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def __contains__(self, element):
        return element in self.patterns

    def __len__(self):
        return len(self.patterns)

    def __getitem__(self, item):
        return self.patterns[item]

    def get_cs_ids(self):
        """Return list of int, CodeTable.i of coding sets
        in self.coding_sets.
        """
        ids = []
        for cs in self.coding_sets:
            ids.append(cs.i)
        return ids

    def get_support(self, pattern):
        """Return support of a pattern (number of transaction
        this pattern appears in).

        Parameters
        ----------
        pattern : Pattern object
            Pattern which support we want to calculate.
        """
        support = 0
        for database in self.databases:
            support += database.get_support(pattern)
        return support

        #  Calculate sum(log(freq_in_D_cursive(x)))
    def get_freq_in_all(self, pattern):
        """Return frequency of a pattern.

        Parameters
        ----------
        pattern : Pattern object
            Pattern which frequency we want to calculate.
        """
        freq = 0.0
        for item in pattern:
            support = 0
            for database in self.all_databases:
                support += database.get_support(item)
            freq += log2(support / self.all_db_card)
        return freq

    def calculate_patternset_diff_encoded_size(self, pattern):
        """Returns encoded size of Sj after performing an action
        on a pattern (deleting or adding).

        Parameters
        ----------
        pattern : Pattern object
            Pattern which size will be considered in the calculation.
        """
        old_sj_card_size = universal_code_len(self.size)
        new_sj_card_size = universal_code_len(self.size + 1)
        pattern_size = universal_code_len(len(pattern))
        freq = self.get_freq_in_all(pattern)
        cs_sum_of_diff = 0.0
        for cs in self.coding_sets:
            cs_sum_of_diff += cs.old_db_size - cs.encoded_db_size
        return \
            old_sj_card_size - new_sj_card_size - pattern_size \
            + freq + cs_sum_of_diff

    def try_add(self, candidate):
        """Adds a pattern to this code table and sorts patterns in SCO.

        Parameters
        ----------
        candidate : Pattern object
            Pattern to add.
        """
        self.add(candidate.copy())
        self.sort_in_sco()

    def try_del(self, candidate):
        """Deletes a pattern from self and sorts patterns in SCO.

        Parameters
        ----------
        candidate : Pattern object
            Pattern to delete.
        """
        self.delete_pattern(candidate)
        self.sort_in_sco()

    def delete_pattern(self, pattern):
        """Action of deleting a pattern. Also updates self.size.

        Parameters
        ----------
        pattern : Pattern object
            Pattern to delete.
        """
        self.patterns.remove(pattern)
        self.size -= 1

    def sort_in_sco(self):
        """Sort self' patterns in SCO (standard cover order),
        i.e. descending on:
            1. Patterns' size.
            2. Patterns' support fromm all Di in self.databases.
            3. Lexicographical order.
        """
        self.patterns.sort(
            key=lambda x: (len(x), self.get_support(x), str(x)), reverse=True)

    def add(self, pattern):
        """Action of adding a pattern. Also updates self.size.

        Parameters
        ----------
        pattern : Pattern object
            Pattern to add.
        """
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            self.size += 1

    def pp(self):
        """Pretty-printer
        """
        print("NИNИNИNИNИNИN S" + repr(self.j) + " NИNИNИNИNИNИNИ")
        for x in self.patterns:
            print(x)
        print()

    def to_string(self):
        string = "NИNИNИNИNИNИN S" + repr(self.j) + " NИNИNИNИNИNИNИ" + "\n"
        for x in self.patterns:
            string += repr(x) + "\n"
        return string
