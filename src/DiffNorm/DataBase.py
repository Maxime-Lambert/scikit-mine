from src.DiffNorm.ItemSet import ItemSet
from os import path


class DataBase:
    """Database / Di.

    Structure which represents individual database Di.
    Stores transactions.

    todo:
        Make this class inherit from list and get rid of useless
        built-in functions.

    Parameters
    ----------
    name : str
        Name of the file containing transactions for this database.
    db_id : int
        Index of this database, i from Di.

    Attributes
    ----------
    index : int
        Iterator over the contents of this database.
    id : int
        Index of this database, i from Di.
    db_card : int
        Cardinal, number of elements in this database.
    transactions : list of ItemSet objects
        List of transactions.
    """

    def __init__(self, name, db_id):
        data_directory_path = "../../test/data/DiffNorm/"
        dn_dir = path.dirname(__file__)
        abs_file_path = path.join(dn_dir, data_directory_path)
        self.id = db_id
        self.index = 0
        self.transactions = []
        self.name = name
        file = open(abs_file_path + name, "r")
        lines = file.readlines()
        for line in lines:
            transacations = line.split(" ")
            self.transactions.append(ItemSet([int(item)
                                              for item in transacations]))
        self.db_card = len(self.transactions)

    def __repr__(self):
        return repr(self.transactions)

    def __iter__(self):
        return iter(self.transactions)

    def __next__(self):
        self.index += 1
        try:
            return self.transactions[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def __len__(self):
        return len(self.transactions)

    def __getitem__(self, transaction):
        return self.transactions[transaction]

    def get_support(self, pattern):
        """Return support of a pattern (number of transaction
        this pattern appears in.

        Parameters
        ----------
        pattern : Pattern object
            Pattern which support we want to calculate.
        """
        support = 0
        for transaction in self.transactions:
            if transaction >= pattern:
                support += 1
        return support

    def pp(self):
        """Pretty-printer
        """
        print("NИNИNИNИNИNИNИNИ " + self.name + " NИNИNИNИNИNИNИNИ")
        for transaction in self.transactions:
            print(repr(transaction))
        print()
