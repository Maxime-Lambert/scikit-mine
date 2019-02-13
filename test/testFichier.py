from src.File import *
from src.database import *

if __name__ == '__main__':
    monfichier = Fichier("monfichier")
    print("la liste normale")
    print(monfichier.list_string)
    print("")
    print("le dico cree en lien avec le fichier")
    print(monfichier.dico)
    print("")
    print("la liste en int : ")
    print(monfichier.list_int)
    database = Database(monfichier.list_int)
    print("test database ! ")
    print(database)
    monfichier.list_int.append(18)
    print("la liste en int : ")
    print(monfichier.list_int)
    print("test database ! ")
    print(database)
