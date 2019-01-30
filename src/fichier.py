class Fichier:
	"""docstring for Fichier"""
	liste = []
	listeInt = []
	dico = {}


	def __init__(self, nom):
		fichier = open(nom + ".txt","r")
		lignes = fichier.readlines();
		tmp = []
		tab = []

		for ligne in lignes :
			tmp = []
			tmp = ligne.split(" ")
			tab.append(tmp)

		for trans in tab:
			tmp = []
			for trans2 in trans:
				tmp.append(trans2.replace("\n",""))
			self.liste.append(tmp)

	def miseEnPlace(self):
		i = 1
		cle = 0
		for trans in self.liste:
			res = []
			for val in trans :
				cle = self.valeurExist(val)
				if(cle != 0):
					res.append(cle)
				else :
					self.dico[i] = val
					res.append(i)
					i += 1
			self.listeInt.append(res)

	def valeurExist(self, val): 
		for cle,valeur in self.dico.items() :
			if(val == valeur):
				return cle
		return 0
