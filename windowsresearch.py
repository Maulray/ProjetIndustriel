import os, re, filecmp

paths=[]

def rechercheFichiersLocaux(fichier, rep):
    # recherche du contenu du répertoire rep (fichiers et sous-répertoires)
    entrees = os.listdir(rep)

    # traitement des fichiers du répertoire
    for entree in entrees:
        if (not os.path.isdir(os.path.join(rep, entree))) and (re.search(fichier.lower(),entree.lower())):
            comp = False
            for p in paths :
                comp = comp or filecmp.cmp(rep+"/"+entree,p,shallow=False)
            if comp==False:
                paths.append(rep+"/"+entree)

    # traitement récursif des sous-répertoires de rep
    for entree in entrees:
        rep2 = os.path.join(rep, entree)
        if os.path.isdir(rep2):
            chemin = rechercheFichiersLocaux(fichier, rep2)
