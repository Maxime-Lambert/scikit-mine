# -*- coding: utf-8 -*-

from src.Pattern import Pattern
from src.CodeTable import CodeTable


class Convert:

    def to_code_table_slim(filename, sct):
        entree = open(filename+".txt", "r")
        sortie = open(filename+"slim.txt", "w")
        lignes = entree.readlines()
        counter = 0
        conversion = {}
        first = True
        it = sorted(sct.patternMap.keys(), key=lambda p: p.support,
                    reverse=True)
        for pattern in it:
            for y in pattern.elements:
                conversion[str(y)] = counter
                counter += 1
        for ligne in lignes:
            curr = ligne.split()
            res = ""
            for x in curr:
                if not x[0] == "(":
                    res += str(conversion[x]) + " "
                else:
                    res += x
            if first:
                sortie.write(res)
                first = False
            else:
                sortie.write("\n"+res)
