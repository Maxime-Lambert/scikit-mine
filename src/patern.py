from src.Transaction import *


class Pattern:
    """docstring for Pattern"""

    def __init__(self, transaction):
        self.usage = 0
        self.support = 0
        self.elements = transaction

    def __repr__(self):
        res = "["
        res += self.elements.toString()
        res += "]"
        return res

    def __eq__(self, pattern):
        return self.elements.__eq__(pattern.elements)

    def __hash__(self):
        i = 0
        for t in self.elements:
            i += t
        return i
        
    def union(self, pattern2):
        res = self.elements + pattern2.elements
        trans = Transaction(sorted(list(set(res))))
        return Pattern(trans)


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