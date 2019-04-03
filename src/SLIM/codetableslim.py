# -*- coding: utf-8 -*-

from src.Pattern import Pattern
from src.CodeTable import CodeTable


class Convert:

    def to_code_table_slim(filename, sct):
        entree = open(filename+".txt", "r")
        sortie = open(filename+"_slim.txt", "w")
        lignes = entree.readlines()
        counter = 0
        conversion = {}
        first = True
        it = sct.order_by_standard_cover_order()
        for pattern in it:
            for y in pattern.elements:
                if counter == 4:
                    conversion[str(y)] = 5
                elif counter == 5:
                    conversion[str(y)] = 6
                elif counter == 6:
                    conversion[str(y)] = 7
                elif counter == 7:
                    conversion[str(y)] = 8
                elif counter == 8:
                    conversion[str(y)] = 4
                else:
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
