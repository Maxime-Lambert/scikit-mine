from src.DiffNorm.ItemSet import ItemSet
from src.DiffNorm.DiffNormUtils import log_gamma, calc_log_double_factorial


class CodeTable:
    """Code table/ coding set/ Ci.

    Structure assigned to each individual database Di. Stores items
    from the alphabet I and all the patterns related to Di,
    i.e. all x, who are in Sj and i in j.

    todo:
        Make this class inherit from list and get rid of useless
        built-in functions.

    Parameters
    ----------
    database : DataBase object
        Database to which this code table will be associated.

    Attributes
    ----------
    index : int
        Iterator over the contents of this table.
    usage : int
        Usage of a code table is sum of usages of its' elements.
    size : int
        Number of elements in this code table.
    patterns : list of ItemSet objects
        List of items of the alphabet I and all the patterns related to
        the database associated to this code table.
    i : int
        Index of this code table, i like in Ci or Di.
    t_data : dict
        Cover of all transactions of Di. To each key = tid (transaction index)
        we associate its' cover (patterns and items of this code table used to
        describe this transaction).
    initial_encoded_size : float
        Size of the description of database Di (Di | Ci) in the beginning
        of the execution, in bits.
    final_encoded_size : float
        Size of the description of database Di (Di | Ci) in the end, in bits.
    encoded_db_size : float
        Size of the description of database Di (Di | Ci) at one step of
        the algorithme, in bits.
    old_db_size : float
        Size of the description of database Di (Di | Ci), after adding
        or deleting a pattern to/from this code table, in bits.
    """

    def __init__(self, database):
        self.index = 0
        self.usage = 0
        self.size = 0
        self.patterns = []
        self.database = database
        self.i = self.database.id
        self.t_data = {}
        self.initial_encoded_size = 0.0
        self.final_encoded_size = 0.0
        self.encoded_db_size = 0.0
        self.old_db_size = 0.0

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

    def update_t_data(self):
        """Recalculate cover of all transactions of Di.
        Used in initializing of a code table and after adding or deleting
        a pattern.

        todo:
            Recalculate cover only of those transactions, who used the
            modified pattern and not of all transactions.
        """
        tid = 0
        for transaction in self.database:
            self.t_data[int(str(self.database.id) + str(tid))] = \
                self.calculate_cover(transaction)
            tid += 1

    def set_encoded_db_size(self, size):
        """Setter for encoded_db_size.

        Parameters
        ----------
        size : float
            New size of the database, in bits.
        """
        self.encoded_db_size = size

    def update_usage(self):
        """Update self.usage.
        """
        self.usage = self.calculate_usage()

    def calculate_usage(self):
        """Sum the usages of all patterns of this code table
        (= self.usage).
        """
        usage = 0
        for pattern in self.patterns:
            usage += pattern.usage
        return usage

    def update_usages(self):
        """Update usages of all patterns of this code table.
        todo:
            Implement it in a more intellegent way, don't recalculate
            usage of all patterns each time, but only of those patterns,
            who've changed.
        """
        for pattern in self.patterns:
            pattern.old_usage = pattern.usage
            pattern.usage = len(self.gather_usages(pattern))

    def rollback_usages(self):
        """Rollback pattern usages, called when an action (add a pattern or delete a pattern)
         was rejected.
        """
        for pattern in self.patterns:
            pattern.usage = pattern.old_usage

    def calculate_db_encoded_size(self):
        """Returns database Di size described with this code table (D|C).
        """
        constant = 0.5
        x = log_gamma(self.usage + constant * self.size)
        y = log_gamma(constant * self.size)
        t = 0.0
        for pattern in self.patterns:
            usage = pattern.usage
            t += calc_log_double_factorial(2 * usage - 1) - usage
        return x - y - t

    def gather_usages(self, pattern):
        """Returns usage of a pattern.

        Parameters
        ----------
        pattern : Pattern object
            Pattern, which usage we want to extract.
        """
        usages = set()
        for tid in self.t_data:
            if pattern in self.t_data[tid]:
                usages.add(tid)
        return usages

    def calculate_cover(self, transaction):
        """Returns cover (set of patterns, which cover it)
         of a transaction. Recursive.

        Parameters
        ----------
        transaction : ItemSet object
            Transaction, which cover we want to calculate.
        """
        for pattern in self.patterns:
            if transaction >= pattern:
                return pattern.fuse(self.calculate_cover(ItemSet(transaction)
                                                         - ItemSet(pattern)))
        return ItemSet([])

    def try_add(self, candidate):
        """Adds a pattern to this code table and:
            1. Saves old database description size self.encoded_db_size.
            2. Sorts patterns in SCO.
            3. Updates cover of all transaction.
            4. Updates usages of patterns in this code table.
            5. Updates total usage of this code table.

        Parameters
        ----------
        candidate : Pattern object
            Pattern to add.
        """
        self.old_db_size = self.encoded_db_size
        self.add(candidate.copy())
        self.sort_in_sco()
        self.update_t_data()
        self.update_usages()
        self.update_usage()

    def try_del(self, candidate):
        """Deletes a pattern from this code table and:
            1. Saves old database description size self.encoded_db_size.
            2. Sorts patterns in SCO.
            3. Updates cover of all transaction.
            4. Updates usages of patterns in this code table.
            5. Updates total usage of this code table.

        Parameters
        ----------
        candidate : Pattern object
            Pattern to delete.
        """

        self.old_db_size = self.encoded_db_size
        self.delete_pattern(candidate)
        self.sort_in_sco()
        self.update_t_data()
        self.update_usages()
        self.update_usage()

    def delete_pattern(self, pattern):
        """Action of deleting a pattern. Also updates this code tables'
        size self.size.

        Parameters
        ----------
        pattern : Pattern object
            Pattern to delete.
        """
        self.patterns.remove(pattern)
        self.size -= 1

    def rollback(self):
        """Rollbacks previous action (delete or add).
        todo:
            Optimize this fucntion. Instead of recalculating attributes each time
            save their values and just reassign them back.
        """
        self.encoded_db_size = self.old_db_size
        self.sort_in_sco()
        self.update_t_data()
        self.rollback_usages()
        self.update_usage()

    def sort_in_sco(self):
        """Sort this code tables' patterns in SCO (standard cover order),
        i.e. descending on:
            1. Patterns' size.
            2. Patterns' support in the database Di.
            3. Lexicographical order.
        """
        self.patterns.sort(key=lambda x: (len(x), self.database.get_support(x),
                                          str(x)), reverse=True)

    def add(self, pattern):
        """Action of adding a pattern. Also updates this code tables'
        size self.size.

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
        print("NИNИNИNИNИNИN ct de " + self.database.name + " NИNИNИNИNИNИNИ")
        print()
        print("Initial encoded size")
        print(self.initial_encoded_size)
        print("Final encoded size")
        print(self.final_encoded_size)
        print()
        for x in self.patterns:
            print(repr(x) + " " + repr(len(self.gather_usages(x))))
        print()
