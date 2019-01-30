from src.fichier import *



if __name__ == '__main__':
    monfichier = Fichier("scikit_learn.pattern_mining/test/monfichier")
    monfichier.miseEnPlace()
    print("la liste normale")
    print(monfichier.liste)
    print("")
    print("le dico cree en lien avec le fichier")
    print(monfichier.dico)
    print("")
    print("la liste en int : ")
    print(monfichier.listeInt)