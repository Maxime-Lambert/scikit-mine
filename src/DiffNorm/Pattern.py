from src.DiffNorm.ItemSet import *


class Pattern(ItemSet):

    def __init__(self, left_is, right_is, left_cs_id, right_cs_id):
        self.max_gain = 0
        self.left_is = left_is
        self.right_is = right_is
        self.left_cs_id = left_cs_id
        self.right_cs_id = right_cs_id
        print(repr(left_is) + "  " + repr(type(left_is)) + "  " + repr(right_is) + "  " + repr(type(right_is)))
        self.items = ItemSet(left_is | right_is)

    def __eq__(self, other):
        if isinstance(other, Pattern):
            return self.items == other.items and self.left_cs_id == other.left_cs_id and \
                   self.right_cs_id == other.right_cs_id
        else:
            return False

    def __repr__(self):
        return repr(self.left_is) + " | " + repr(self.right_is) + ", " + repr(self.left_cs_id) + " | " + \
               repr(self.right_cs_id) + ", " + repr(self.max_gain)

    def set_est_gain(self, gain):
        self.max_gain = gain

    def get_est_gain(self):
        return self.max_gain

    def verify_same_ct(self):
        return self.left_cs_id == self.right_cs_id
