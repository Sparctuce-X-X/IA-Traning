from pathlib import Path
from collections import Counter
import re
import hashlib

def recuperer_fichiers(chemin): 
    dossier = Path(chemin)
    fichiers = [f for f in dossier.rglob("*") if f.is_file()]
    return fichiers

def fichiers_par_extension(fichiers):
    compteur = []
    for f in fichiers:
        compteur.append(f.suffix)

    fichiers_avec_suffix = Counter(compteur)

    return fichiers_avec_suffix


def mots_les_plus_frequent(fichiers):
    motif = r'[^\W\d_]+'
    compteur = Counter() 

    for f in fichiers:
        texte = f.read_text(encoding="utf-8")
        mots = re.findall(motif,texte.lower())
        compteur.update(mots)
    top_10_mots = compteur.most_common(10)

    return top_10_mots
    

def liste_des_fichiers_en_doublon(fichiers):
    empreintes =  {}
    for f in fichiers:
        texte = f.read_bytes()
        empreinte = hashlib.sha256(texte).hexdigest()

        if empreinte  in empreintes:
            empreintes[empreinte].append(f)
        else:
            empreintes[empreinte] = [f]  
    return empreintes
             

fichiers= recuperer_fichiers("./corpus_test")

fichiers_avec_suffix = fichiers_par_extension(fichiers)

for cle , valeur  in fichiers_avec_suffix.items():
        print(f"il y a {valeur} fichier{"s" if valeur > 1  else ""} {cle}")

print("\n")

top_10_mots = mots_les_plus_frequent(fichiers)
i = 1

for cle , valeur in top_10_mots:
        print(f"le top {i} est : '{cle}'")
        i+=1

print("\n")

fichiers_en_doublons = liste_des_fichiers_en_doublon(fichiers)

for empreinte , noms in fichiers_en_doublons.items():
     if len(noms) > 1:
        print(f"{noms} ont un contenue identique\n")

