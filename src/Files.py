class Files:
    """docstring for Fichier"""
    list_string = []
    list_int = []
    dico = {}

    def __init__(self, nom):
        file = open(nom + ".txt", "r")
        lignes = file.readlines()
        tmp = []
        tab = []

        for ligne in lignes:
            tmp = []
            tmp = ligne.split(" ")
            tab.append(tmp)

        for trans in tab:
            tmp = []
            for trans2 in trans:
                tmp.append(trans2.replace("\n", ""))
            self.list_string.append(tmp)
        self.start()

    def start(self):
        i = 1
        key = 0
        for trans in self.list_string:
            res = []
            for val in trans:
                key = self.key_exist(val)
                if key != 0:
                    res.append(key)
                else:
                    self.dico[i] = val
                    res.append(i)
                    i += 1
            self.list_int.append(res)

    def key_exist(self, val):
        for key, value in self.dico.items():
            if val == value:
                return key
        return 0

    def to_file(ct, filename):
        first = True
        f = open(filename+".txt", "w")
        for k in ct.order_by_standard_cover_order():
            if first:
                f.write(repr(k))
                first = False
            else:
                f.write("\n"+repr(k))

def print_toto():
    print('Toto')
