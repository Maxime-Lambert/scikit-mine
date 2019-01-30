import sys
import os
# jenkins exposes the workspace directory through env.
sys.path.append(os.environ['WORKSPACE'])
from src.fichier import *



if __name__ == '__main__':
    monfichier = Fichier("monfichier")
    monfichier.miseEnPlace()
    print("la liste normale")
    print(monfichier.liste)
    print("")
    print("le dico cree en lien avec le fichier")
    print(monfichier.dico)
    print("")
    print("la liste en int : ")
    print(monfichier.listeInt)