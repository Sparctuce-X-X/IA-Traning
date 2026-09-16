import hashlib
import logging
import re
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)


@contextmanager
def chrono(nom: str):
    debut = time.perf_counter()
    try:
        yield
    finally:
        logger.info("%s: %.2fs", nom, time.perf_counter() - debut)


def recuperer_fichiers(chemin):
    dossier = Path(chemin)
    return [f for f in dossier.rglob("*") if f.is_file()]


def fichiers_par_extension(fichiers):
    compteur = []
    for f in fichiers:
        compteur.append(f.suffix)
    return Counter(compteur)


def mots_les_plus_frequent(fichiers):
    motif = r"[^\W\d_]+"
    compteur = Counter()
    for f in fichiers:
        texte = f.read_text(encoding="utf-8")
        compteur.update(re.findall(motif, texte.lower()))
    return compteur.most_common(10)


def liste_des_fichiers_en_doublon(fichiers):
    empreintes = {}
    for f in fichiers:
        empreinte = hashlib.sha256(f.read_bytes()).hexdigest()
        if empreinte in empreintes:
            empreintes[empreinte].append(f)
        else:
            empreintes[empreinte] = [f]
    return empreintes


def main() -> int:
    logging.basicConfig(level=logging.INFO)

    fichiers = recuperer_fichiers("./corpus_test")

    with chrono("récupération des fichiers par extension"):
        for cle, valeur in fichiers_par_extension(fichiers).items():
            logger.info("extension %s : %s fichiers", cle, valeur)

    with chrono("récupération des mots les plus fréquents"):
        for i, (mot, n) in enumerate(mots_les_plus_frequent(fichiers), start=1):
            logger.info("le top %s est : '%s'", i, mot)

    with chrono("récupération de la liste des fichiers en double"):
        for noms in liste_des_fichiers_en_doublon(fichiers).values():
            if len(noms) > 1:
                logger.info(" %s ont un contenu identique", noms)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
