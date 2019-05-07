from src.Pattern import Pattern


class Pattern(Pattern):

    active = False
    index = 0
    usage = 0
    gain = 0.0
    elements = []

    def __init__(self, elements):
        self.elements = elements
        self.support = 1

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return str(self.elements)

    def __str__(self):
        return str(self.elements)


    def __eq__(self, other):
        if not isinstance(other, Pattern):
            return False
        return self.elements == other.elements

    def __hash__(self):
        """
            Return the hash value of the usage
            :return: An hash value
            :rtype: Integer
        """
        return hash(self.usage)

    def is_active(self):
        return self.active

    def set_active(self):
        self.active = True

    def add(self, window):
        res = []
        for symbol in self.elements:
            res.append(symbol)
        res.append(window)
        self.elements = res

    def get_index(self):
        return self.index

    def set_usage(self, usage):
        self.usage = usage

    def union(self, pattern):
        res = []
        res.extend(self.elements)
        res.extend(pattern.elements)
        return Pattern(res)

    def contains(self, list_include):
        if self.elements == list_include.elements:
            return False
        res = True
        for i in range(len(self.elements)):
            if self.elements[i] == list_include.elements[0]:
                if len(self.elements) - i < i + len(list_include.elements):
                    return False
                for j in range(len(list_include.elements)):
                    if self.elements[i+j] != list_include.elements[j]:
                        return False
            return True
        return False

    def is_sub_list(self, other):
        if self.elements == other.elements:
            return False
        return set.issubset(set(other.elements), set(self.elements))
