from pathlib import Path
from collections import Counter
import re 
import logging
import statistics as st
import hashlib
import argparse
import csv 
from collections import defaultdict

logger = logging.getLogger(__name__)

class ErreurIngestion(Exception):
    pass

class DocumentIllisible(ErreurIngestion):
    def __init__(self, chemin: str, motif: str):
        super().__init__(f"document {chemin} : Illisible car {motif}")
        self.chemin = chemin
        self.motif = motif

def parse_args():
    parser = argparse.ArgumentParser(description="Mon script")
    parser.add_argument("-c" , type=str , required=True , help = "Chemin vers le dossier")
    parser.add_argument("--top" , type=int , required=True , help="Top des mots les plus fréquent")
    parser.add_argument("--seuil" , type=int , required=True , help="le seuil minimal pour les mots les plus fréquents")
    parser.add_argument("--verbeux" ,action='store_true')
    return parser.parse_args()


def recuperer_fichiers(chemin:str) -> list[Path]:
    dossier = Path(chemin)
    fichiers = [f for f in dossier.rglob("*") if f.is_file()]
    return fichiers

def trier_lisibles(fichiers):
    lisibles = []
    rejetes = []
    for f in fichiers:
        try:
            f.read_text(encoding="utf-8")    
        except UnicodeDecodeError:
            logger.warning("écarté : %s", f)
            rejetes.append(f)
        else:
            lisibles.append(f)
    return lisibles, rejetes

def mots_les_plus_frequent(fichiers:Path , top:str ) -> list[tuple[str, int]]:
    motif = r'[^\W\d_]+'
    compteur = Counter() 

    for f in fichiers:
        texte = f.read_text(encoding="utf-8")
        mots = re.finditer(motif,texte.lower())
        compteur.update(mots)

    top_mots = compteur.most_common(top)

    return top_mots


def fichier_par_extension(fichiers:Path) -> list:
    return [f.suffix for f in fichiers]

def fichiers_avec_taille(fichiers:Path) -> list:
    return [f.stat().st_size for f in fichiers]

def stats_par_extension(fichiers):
    stats = defaultdict(lambda: {"nombre" : 0 ,"taille_totale" : 0})
    for f in fichiers:
        stats[f.suffix]["nombre"] += 1
        stats[f.suffix]["taille_totale"] += f.stat().st_size
    return dict(stats)

def doublons_par_empreinte(fichiers):
    empreintes = {}

    for f in fichiers:
        bytes = f.read_bytes()
        empreinte = hashlib.sha256(bytes).hexdigest()

        if empreinte in empreintes:
            empreintes[empreinte].append(f.resolve())
        else:
            empreintes[empreinte] = [f.resolve()]
    return empreintes 
def main():
    args = parse_args()
    dossier = Path(args.c)
    if not dossier.is_dir():
        logger.error("dossier introuvable : %s", dossier)
        return 2

    niveau = logging.DEBUG if args.verbeux else logging.INFO
    logging.basicConfig(level=niveau)   
    

    fichiers = recuperer_fichiers(args.c)
    lisisibles , rejetes = trier_lisibles(fichiers)
    top = mots_les_plus_frequent(lisisibles,args.top)
    seuil = args.seuil
    logger.info("-------- LES %d MOTS LES PLUS FRÉQUENTS --------", args.top)

    for mot , recurrence in top:
        if recurrence > seuil:
            logger.info(" le mot '%s' : présent %s fois" , mot , recurrence)

    logger.info("--------LE NOMBRE DE FICHE PAR EXTENSION-------")
    fichiersExtension = Counter(fichier_par_extension(fichiers))

    for extension , nombre in fichiersExtension.items():
        logger.info(f" il y'a {nombre} fichier {extension}")

    logger.info("-----STATISTIQUE DE TAILLE------")
    fichiersTaille = fichiers_avec_taille(fichiers)
    moyenneTailleFichiers = st.mean(fichiersTaille)
    medianeTailleFichiers = st.median(fichiersTaille)
    maxTailleFichiers = max(fichiersTaille)
    logger.info("La moyenne  de la taille des fichiers est %s",moyenneTailleFichiers)
    logger.info("La médiane  de la taille des fichiers est %s",medianeTailleFichiers)
    logger.info("Le max de la taille des fichiers est %s",maxTailleFichiers)

    logger.info("-----Les FICHIERS DOUBLONS------")
    doublonsFichiers = doublons_par_empreinte(fichiers)
    for noms in doublonsFichiers.values():
        if len(noms) > 1:
            logger.info("%s ont la même empreinte", noms)


    with open("stats.csv", "w", encoding="utf-8", newline="") as f:
        stats = stats_par_extension(fichiers)
        writer = csv.writer(f)
        writer.writerow(["extension", "nombre", "taille_totale"])  
        for extension , valeurs in stats.items():
            writer.writerow([extension,valeurs["nombre"],valeurs["taille_totale"]])

    return 1 if rejetes else 0
if __name__ == "__main__":
    raise SystemExit(main())