class Alignement:

    index_of_beginning_pattern = 0
    index_of_ending_pattern = 0
    index_of_pattern = 0

    def __init__(self, index_begin, index_ending, pattern):
        self.index_of_beginning_pattern = index_begin
        self.index_of_ending_pattern = index_ending
        self.pattern = pattern
        self.pattern.set_active()
        self.index_of_pattern = pattern.get_index()

    def __repr__(self):
        return str(self.pattern)

    def get_pattern(self):
        return self.pattern

    def copy(self):
        return Alignement(self.index_of_beginning_pattern, self.index_of_ending_pattern, self.pattern)
