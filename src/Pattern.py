import transaction as Transaction


class Pattern:
    """docstring for Pattern"""

    def __init__(self, transaction):
        self.usage = 0
        self.support = 0
        self.elements = transaction

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.text[self.index].upper()
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __repr__(self):
        res = "["
        res += self.elements.toString()
        res += "]"
        return res

    def __eq__(self, pattern):
        return self.elements.__eq__(pattern.elements)

    def __str__(self):
        res = ""
        for transaction in self.elements:
            res += str(transaction)
        return res

    def __hash__(self):
        return hash(self.usage)

    def union(self, pattern2):
        res = self.elements + pattern2.elements
        trans = Transaction(sorted(list(set(res))))
        return Pattern(trans)

    def add_usage(self):
        self.usage += 1


if __name__ == '__main__':
    trans = Transaction(['A', 'B'])
    pattern = Pattern(trans)
    trans2 = Transaction(['B', 'C'])
    pattern2 = Pattern(trans2)
    trans3 = Transaction(['C'])
    pattern3 = Pattern(trans3)
    print("pattern : ")
    print(pattern)
    print("pattern2 : ")
    print(pattern2)
    print("pattern3 : ")
    print(pattern3)
    pattern4 = pattern.union(pattern2)
    print("pattern4 (pattern + pattern2) : ")
    print(pattern4)
    pattern5 = pattern.union(pattern3)
    print("pattern5 (pattern + pattern3) : ")
    print(pattern5)
