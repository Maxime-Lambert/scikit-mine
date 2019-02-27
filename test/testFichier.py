from src.Files import *
from src.database import *

if __name__ == '__main__':
    monfichier = Files("fichier2")
    print("la liste normale")
    print(monfichier.list_string)
    print("")
    print("le dico cree en lien avec le fichier")
    print(monfichier.dico)
    print("")
    print("la liste en int : ")
    print(monfichier.list_int)

