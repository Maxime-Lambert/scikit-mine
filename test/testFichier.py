from src.fichier import *
from src.database import *

if __name__ == '__main__':
    monfichier = Fichier("monfichier")
    monfichier.mise_en_place()
    print("la liste normale")
    print(monfichier.liste)
    print("")
    print("le dico cree en lien avec le fichier")
    print(monfichier.dico)
    print("")
    print("la liste en int : ")
    print(monfichier.liste_int)
    database = Database(monfichier.liste_int)
    print("test database ! ")
    print(database)
