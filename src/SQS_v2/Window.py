from src.SQS_v2.Pattern import Pattern


class Window(Pattern):

    cost = 0
    optcost = 0
    optimalwindow = None

    def __init__(self, pattern, first = 0, last = 0, sequence = 0):
        self.pattern = pattern
        self.first = first
        self.last = last
        self.tail = pattern.elements[1:-1]
        self.sequence = sequence

    def __str__(self):
        return str(self.pattern)

    def __repr__(self):
        return str(self.pattern)

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        """Returns iterator over the transactions in the pattern."""
        return iter(self.elements)

    def __next__(self):
        """
            Return the next element of the collection
            :return: A transaction at index-position
            :rtype: Transaction
        """
        try:
            result = self.elements[self.index].upper()
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
