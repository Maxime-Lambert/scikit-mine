from src.DiffNorm.ItemSet import ItemSet


class Pattern(ItemSet):
    """Pattern.

    Pattern herits from ItemSet, making it more suitable
    to represent candidate pattern (a candidate is a structure
    that we consider to add to a code table).

    todo:
        Make smarter inheritance from ItemSet.

    Parameters
    ----------
    left_is : ItemSet object
        List of items of this pattern/transaction.
    right_is : ItemSet object
        List of items of this pattern/transaction.
    sj_id : int
        List of items of this pattern/transaction.

    Attributes
    ----------
    max_gain : int
        Maximal estimated gain of this candidate.
    left_is : ItemSet
        Left parent of this itemset, X in X | Y.
    right_is : ItemSet
        Right parent of this itemset, Y in X | Y.
    items : set of int
        List of items of this pattern.
    max_usage: int
        Maximal estimated usage of this candidate.
    """

    def __init__(self, left_is, right_is, sj_id):
        self.max_gain = 0
        self.left_is = left_is
        self.right_is = right_is
        self.items = left_is | right_is
        self.sj_id = sj_id
        self.max_usage = 0

    def __eq__(self, other):
        if isinstance(other, Pattern):
            if self.items == other.items and \
               self.sj_id == other.sj_id:
                    return True
        else:
            return False

    def __repr__(self):
        return repr(self.items)

    def copy(self):
        """Returns a clone of self
        """
        copy = Pattern(self.left_is, self.right_is, self.sj_id)
        return copy

    def set_est_gain(self, gain):
        """Setter for gain.

        Parameters
        ----------
        gain : float
            New gain of this pattern.
        """
        self.max_gain = gain

    def get_est_gain(self):
        """Returns gain of this pattern.
        Getter.
        """
        return self.max_gain
