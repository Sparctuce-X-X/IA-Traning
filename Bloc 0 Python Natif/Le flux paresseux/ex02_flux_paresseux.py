from pathlib import Path
from itertools import batched  , islice
import tracemalloc

tracemalloc.start()
def lignes_utiles(chemin , lues=None):
    with Path(chemin).open(encoding='utf-8') as f:
        for ligne in f:
            if lues is not None:
                lues[0] += 1 
            ligne = ligne.strip()
            if ligne and not ligne.startswith('#'):
                yield ligne

document = lignes_utiles("./corpus_flux/journal.txt")

for i , lot in enumerate(batched(document,50), start=0):
    print(f" lot numéro {i} = {len(lot)} paquet{"s" if len(lot) > 1 else ""}")

actuel, pic = tracemalloc.get_traced_memory()
print(f"Actuel: {actuel / 1024:.1f} KiB, Pic: {pic / 1024:.1f} KiB\n")
tracemalloc.stop()



tracemalloc.start()
echantillon = lignes_utiles("./corpus_flux/echantillon.txt")

for i , lot in enumerate(batched(echantillon,50), start=1):
    print(f" lot numéro {i} = {len(lot)} paquet{"s" if len(lot) > 1 else ""}")

actuel, pic = tracemalloc.get_traced_memory()
print(f"Actuel: {actuel / 1024:.1f} KiB, Pic: {pic / 1024:.1f} KiB\n")
tracemalloc.stop()

lues = [0]
apercu = list(islice(lignes_utiles("./corpus_flux/journal.txt", lues), 10))

print(f"{len(apercu)} lignes rendues, {lues[0]} lues sur 2 000 004")
for ligne in apercu:
    print(" -", ligne)
