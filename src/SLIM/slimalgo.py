#import numpy as np
#import scipy.sparse as sp
#from .Transaction import Transaction 
#from .codeTable import CodeTable
#from .database import Database

#v0 : helloworld?
#v1 : Pour une premiere version on peut zapper la comparaison des usages
#et tester toutes les combinaisons de candidats


def _slim(d):
    """
    Parameters
    ----------
    
    """
    standard_code_table = d.standard_code_table()
    code_table = standard_code_table
    ct_has_improved = True
    #ct_pattern_set = code_table.get_pattern_list
    
    while ct_has_improved != False:
        #tri par usage de CT + liste de candidat
        candidates_list = [] #pattern list
        best_usage = 0
        ct_has_improved = False
        indice_pattern_x = 0
        x_current = code_table.get_pattern(indice_pattern_x) #attention si viiiiiide
	#------------- Mine candidates -------------#
        while indice_pattern_x < code_table.size-1 & code_table.get(indice_pattern_x).usage>= best_usage:
            indice_pattern_y = indice_pattern_x + 1 #on ne prend que les patterns juste après x
            y_current = code_table.get_pattern(indice_pattern_y)
            while indice_pattern_y < code_table.size & y_current.usage <= best_usage: # ??
                y_current = code_table.get(indice_pattern_y) #indice dans un set?
                while best_usage < y_current.usage :
                    x_y_current = x_current.union(y_current)
                    if best_usage < x_y_current.usage: #si bon usage on le garde et maj best_usage
                        candidates_list.append(x_y_current)
                        best_usage = x_y_current.usage
                y_current = code_table.get_pattern(++indice_pattern_y)
            x_current = code_table.get_pattern(++indice_pattern_x) #on prend le premier pattern
	#------------- Improve CT -------------#
        indice_candidat = 0
            # on parcours la liste de candidats tant que l'on a pas améliorer CT ou qu'il reste des candidats non testés
        while indice_candidat <= len(candidates_list) & ct_has_improved==False:
            candidate = candidates_list[indice_candidat] 
            code_table_temp = code_table.add_pattern(candidate)
            if code_table_temp.taille <= code_table.taille:
                code_table = code_table_temp.post_prune
                ct_has_improved = True
            else:
                indice_candidat = indice_candidat+1 #remove plutot que compteur
print('Hello world!')