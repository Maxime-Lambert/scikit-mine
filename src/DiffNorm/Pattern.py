from src.DiffNorm.ItemSet import ItemSet


class Pattern(ItemSet):

    def __init__(self, left_is, right_is, left_cs_id, right_cs_id, sj_id):
        self.max_gain = 0
        self.left_is = left_is
        self.right_is = right_is
        self.left_cs_id = left_cs_id
        self.right_cs_id = right_cs_id
        self.items = left_is | right_is
        self.sj_id = sj_id
        self.max_usage = 0
        """pid = ""
        pid += repr(left_cs_id) + ":"
        for x in left_is:
            pid += repr(x) + ","
        pid = pid[:-1]
        pid += "|"
        pid += repr(left_cs_id) + ":"
        for x in right_is:
            pid += repr(x) + ","
        pid = pid[:-1]
        self.id = pid"""

    def __eq__(self, other):
        if isinstance(other, Pattern):
            if self.items == other.items:
                if (self.left_cs_id == self.right_cs_id == -1) or \
                   (other.left_cs_id == other.right_cs_id == -1) or \
                   (
                           self.sj_id == other.sj_id and
                           self.left_cs_id == other.left_cs_id and
                           self.right_cs_id == other.right_cs_id):
                        return True
            """return \
                self.items == other.items and \
                self.left_cs_id == other.left_cs_id \
                and self.right_cs_id == self.right_cs_id"""
        else:
            return False

    def __repr__(self):
        return \
            repr(self.items) + " | " + repr(self.left_cs_id) \
            + " | " + repr(self.right_cs_id)

    def copy(self):
        copy = Pattern(self.left_is, self.right_is, self.left_cs_id,
                       self.right_cs_id, self.sj_id)
        return copy

    def set_est_gain(self, gain):
        self.max_gain = gain

    def get_est_gain(self):
        return self.max_gain

    def verify_same_ct(self):
        return self.left_cs_id == self.right_cs_id
