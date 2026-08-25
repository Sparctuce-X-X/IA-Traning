# Exercice 2 — le flux paresseux

## Ce que tu as

- `generer_flux.py` — écrit le fichier de test. `python generer_flux.py [destination] [nb_lignes]`
- `corpus_flux/echantillon.txt` — 204 lignes, 1 Mo. Pour itérer vite et vérifier à l'œil.
- Le gros fichier n'est pas fourni (29 Mo) : génère-le toi-même.

```bash
python generer_flux.py corpus_flux/journal.txt 2000000
```

Le fichier est **déterministe** : un motif de 20 lignes répété, puis une queue de 4 lignes.
Aucun aléatoire, donc les comptes ci-dessous sont exacts et reproductibles.

## Résultats attendus

Règle de référence : une ligne est **utile** si, après `strip()`, elle n'est pas vide
et ne commence pas par `#`.

| fichier | lignes | utiles | paquets de 50 | dernier paquet |
|---|---|---|---|---|
| `echantillon.txt` | 204 | 103 | 3 | 3 |
| `journal.txt` (2 M) | 2 000 004 | 1 000 003 | 20 001 | 3 |

Formule générale : `utiles = (nb_lignes // 20) * 10 + 3`

**Si tu trouves 133 au lieu de 103** (ou 1 300 003 au lieu de 1 000 003), tu ne fais pas
de `strip()` : tu comptes comme utiles les lignes ne contenant que des espaces ou une
tabulation, et les commentaires précédés d'espaces. Ce n'est pas forcément faux — mais
c'est une règle différente, et tu dois savoir laquelle tu appliques.

## Les pièges, et ce qu'ils te demandent de trancher

Le motif contient exprès :

1. `"   "` et `"\t"` — vides à l'œil, non vides pour Python. `if ligne:` ne suffit pas.
2. `"  # commentaire indente"` — `startswith("#")` répond **False** sans `strip()` préalable.
3. `"valeur = 3  # note en fin de ligne"` — contient un `#` mais **n'est pas** un commentaire.
   Si tu filtres avec `"#" in ligne`, tu la perds.
4. `"ligne utile 3   "` — espaces en fin. Utile, mais ta sortie doit-elle les conserver ?
5. `"derniere ligne sans retour a la ligne"` — le fichier ne se termine pas par `\n`.
   Beaucoup de découpages maison perdent cette ligne. Le `for ligne in f` de Python, non.
6. **Une ligne de 1 000 000 de caractères** juste avant la queue. C'est le piège
   intéressant : ta mémoire est constante *par rapport au nombre de lignes*, pas dans
   l'absolu. Cette seule ligne fait un pic de ~1 Mo. Constate-le, c'est la limite réelle
   du modèle « ligne par ligne ».

## Mesurer la mémoire — c'est le critère de réussite

Sans mesure, tu ne sais pas si ton générateur est paresseux : un script qui fait
`f.readlines()` produit exactement la même sortie, en avalant 29 Mo.

**Méthode 1 — `tracemalloc`**, dans ton script, autour de la consommation :

```python
import tracemalloc
tracemalloc.start()
...          # ta boucle de consommation
courant, pic = tracemalloc.get_traced_memory()
print(f"pic : {pic / 1_000_000:.1f} Mo")
```

**Méthode 2 — depuis le shell**, sans toucher au code :

```bash
/usr/bin/time -v python3 ex02_flux_paresseux.py 2>&1 | grep "Maximum resident"
```

Ce que tu dois observer : un pic de quelques Mo (dominé par la ligne longue),
et surtout **le même pic sur 200 lignes et sur 2 000 000 de lignes**. C'est ça,
la mémoire constante — pas un petit chiffre, un chiffre qui ne bouge pas avec l'entrée.

Fais la contre-épreuve : écris la version `readlines()`, mesure, compare. Sans le
point de comparaison, le chiffre ne veut rien dire.

## Vérifier sans Python

```bash
wc -l corpus_flux/journal.txt        # 2000003 — pourquoi pas 2000004 ? (indice : dernière ligne)
grep -cvE '^\s*(#|$)' corpus_flux/journal.txt   # 1000003 : ton oracle indépendant
```

Le premier écart est instructif : `wc -l` compte les `\n`, pas les lignes.

## Rappel de l'énoncé

1. Générateur qui rend les lignes utiles.
2. Consommation par paquets de 50 via `itertools.batched`, en n'affichant que le
   numéro de paquet et sa taille.
3. La mémoire ne croît pas avec la taille du fichier — **prouvé par une mesure**.
4. Ajoute volontairement un second `for` sur le même générateur, observe, explique.
5. Bonus : les 10 premières lignes utiles via `islice`, **sans** dérouler le reste.
   Pour le prouver : compte les lignes réellement lues.
