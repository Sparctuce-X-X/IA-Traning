"""Génère le fichier de test de l'exercice 2 (flux paresseux).

Usage :  python generer_flux.py [destination] [nb_lignes]
Défauts : corpus_flux/journal.txt, 2 000 000 lignes

Structure entièrement déterministe : un motif de 20 lignes répété,
puis une queue de 4 lignes. Aucun aléatoire, donc la vérité terrain
est calculable à la main (voir VERITE_TERRAIN_EX2.md).

Ce script ne fait qu'écrire des lignes : il ne contient ni générateur,
ni itertools, ni la moindre trace de la solution de l'exercice.
"""

import sys
from pathlib import Path

# Motif de 20 lignes. 10 sont "utiles" selon la règle de l'énoncé
# (non vide après nettoyage, et ne commençant pas par #).
MOTIF: list[str] = [
    "ligne utile 1",
    "",
    "# commentaire en debut de ligne",
    "ligne utile 2",
    "   ",                                  # espaces seulement
    "  # commentaire indente",              # # precede d'espaces
    "cafe elephant naive oeuf",
    "valeur = 3  # note en fin de ligne",   # contient un # mais n'est pas un commentaire
    "",
    "ligne utile 3   ",                     # espaces en fin de ligne
    "#",                                    # commentaire minimal
    "ligne utile 4",
    "",
    "\t",                                   # tabulation seule
    "ligne utile 5",
    "# encore un commentaire",
    "ligne utile 6",
    "",
    "   ligne indentee utile",              # indentee mais utile
    "ligne utile 7",
]

TAILLE_LIGNE_LONGUE = 1_000_000  # caracteres sur une seule ligne


def ecrire(destination: Path, nb_lignes: int) -> int:
    """Ecrit le fichier et retourne le nombre de lignes reellement ecrites."""
    nb_blocs = nb_lignes // len(MOTIF)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8", newline="\n") as f:
        for _ in range(nb_blocs):
            for ligne in MOTIF:
                f.write(ligne + "\n")
        # Queue : une ligne enorme, puis trois lignes courtes.
        # La derniere n'a PAS de retour a la ligne final.
        f.write("x" * TAILLE_LIGNE_LONGUE + "\n")
        f.write("avant derniere ligne\n")
        f.write("# fin du fichier\n")
        f.write("derniere ligne sans retour a la ligne")

    return nb_blocs * len(MOTIF) + 4


def main() -> int:
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else "corpus_flux/journal.txt")
    nb_lignes = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000

    ecrites = ecrire(destination, nb_lignes)
    taille_mo = destination.stat().st_size / 1_000_000
    attendu_utiles = (nb_lignes // len(MOTIF)) * 10 + 3

    print(f"{ecrites:,} lignes ecrites dans {destination} ({taille_mo:.1f} Mo)")
    print(f"lignes utiles attendues : {attendu_utiles:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
