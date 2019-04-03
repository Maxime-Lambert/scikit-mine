from src.SQS_v2.Sequence import Sequence
from src.SQS_v2.CodeTable import CodeTable
from src.SQS_v2.Pattern import Pattern


class Database:

    list_sequence = []

    def __init__(self, list_sequence_int):
        self.index = 0
        for sequence_int in list_sequence_int:
            self.list_sequence.append(Sequence(sequence_int))

    def __iter__(self):
        return iter(self.list_sequence)

    def __next__(self):
        self.index += 1
        try:
            return self.list_sequence[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def make_standard_code_table(self):
        """
            Make the standard code table of the database, i.e. Code table
            composed of singleton item of database

            :return: The Standard code table
            :rtype: CodeTableSQS
        """
        tmp = {}
        # On ajoute les singletons de la base à la SCT
        for sequences in self.list_sequence:
            for item in sequences:
                pattern = Pattern([item])
                if pattern in tmp:
                    tmp[pattern] += 1
                else:
                    tmp[pattern] = 1
        sct = CodeTable(tmp, self)
        return sct
