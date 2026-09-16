"""Génère le dossier de test de l'exercice 1 (inventaire de corpus).

Usage :  python generer_corpus.py [destination]
Par défaut : ./corpus_test  (le dossier est écrasé s'il existe déjà)

Ce script ne fait qu'écrire des fichiers : il ne contient aucune trace
de la solution de l'exercice (ni Counter, ni hashlib, ni parcours récursif).
"""

import shutil
import sys
from pathlib import Path

A = """Le chat dort sur le toit.
Le chien dort aussi.

# ceci est un commentaire
Le chat et le chien dorment.
"""

B = """# Projet corpus

Le projet contient des documents de test.
Le format est libre.
"""

C = """# Rapport

Le rapport decrit le projet et le format des documents.
Le chat n'y figure pas.
"""

D = """id,titre,langue
1,Le chat,fr
2,The cat,en
3,Le chien,fr
"""

E = """2026-08-20 INFO demarrage
2026-08-20 ERROR fichier illisible
2026-08-20 INFO fin
"""

F = """Un fichier avec des accents : café, éléphant, naïve, œuf.
Le café est chaud.
"""

G = """Fichier temporaire dans un dossier cache.
Le cache ne devrait peut-etre pas etre parcouru.
"""

FICHIERS: dict[str, str] = {
    "notes.txt": A,
    "notes_copie.txt": A,                    # doublon exact de notes.txt
    "README.md": B,
    "rapport.md": C,
    "data.csv": D,
    "vide.txt": "",
    "vide2.log": "",                         # doublon exact de vide.txt
    "archive/notes.txt": A,                  # meme nom qu'a la racine + doublon
    "archive/notes_v2.txt": A + " ",         # quasi-doublon : un espace en plus
    "archive/journal.log": E,
    "sous/dossier/profond/accents.txt": F,
    ".cache/temporaire.txt": G,              # dossier cache
}


def main() -> int:
    racine = Path(sys.argv[1] if len(sys.argv) > 1 else "corpus_test")
    if racine.exists():
        shutil.rmtree(racine)
    for chemin_relatif, contenu in FICHIERS.items():
        cible = racine / chemin_relatif
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(contenu, encoding="utf-8")
    print(f"{len(FICHIERS)} fichiers ecrits dans {racine}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
