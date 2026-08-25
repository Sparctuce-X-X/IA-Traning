# Corpus de test — exercice 1

12 fichiers, 4 extensions, 2 groupes de doublons, un quasi-doublon piégeux.

```
corpus_test/
├── .cache/temporaire.txt          ← dossier caché
├── README.md
├── rapport.md
├── data.csv
├── notes.txt                      ┐
├── notes_copie.txt                ├ contenu identique (3 fichiers)
├── vide.txt                       ┐
├── vide2.log                      ├ tous deux vides → doublons eux aussi
├── archive/
│   ├── notes.txt                  ┘ même nom qu'à la racine, même contenu
│   ├── notes_v2.txt               ← contenu de notes.txt + UN espace final
│   └── journal.log
└── sous/dossier/profond/accents.txt   ← UTF-8 (café, éléphant, naïve, œuf)
```

## Résultats attendus

**Fichiers par extension** (les 12 fichiers) : `.txt` 7 · `.md` 2 · `.log` 2 · `.csv` 1
Si tu décides d'ignorer les dossiers cachés : `.txt` 6, le reste inchangé.

**Doublons** (2 groupes) :
- `notes.txt` + `notes_copie.txt` + `archive/notes.txt`
- `vide.txt` + `vide2.log`

`archive/notes_v2.txt` **n'est pas** un doublon.

**Top mots** — dépend de ta règle de découpage. Référence : passage en minuscules,
mots = suites de lettres uniquement (`[^\W\d_]+`), tous les fichiers inclus.

| mot | n | | mot | n |
|---|---|---|---|---|
| le | 30 | | est | 6 |
| chat | 10 | | et | 5 |
| chien | 9 | | sur | 4 |
| dort | 8 | | toit | 4 |
| un | 6 | | aussi | 4 |

Si tu exclus `.cache/`, `le` tombe à 29 et `un` à 5 — le classement bouge légèrement.
Un écart ici n'est pas forcément un bug : c'est une règle de découpage différente.
Mais tu dois pouvoir dire **laquelle**.

## Les pièges, et ce qu'ils te demandent de trancher

1. **`vide.txt` et `vide2.log` sont des doublons.** Empreinte identique (le sha256
   de la chaîne vide), extensions différentes. Volontaire ou aberration ? Décide, et
   écris ta décision en commentaire.
2. **`archive/notes_v2.txt`** diffère d'un seul espace en fin de fichier. Si ton script
   le déclare doublon, tu ne hashes pas ce que tu crois — ou tu as `strip()` quelque part.
3. **Deux `notes.txt`** à des chemins différents : ta clé de regroupement doit être
   l'empreinte du contenu, jamais le nom.
4. **`.cache/`** : `rglob("*")` le parcourt. Le filtrer ou non est un choix, pas un oubli.
5. **`accents.txt`** : sans `encoding="utf-8"` explicite, ça marche chez toi et casse
   dans le conteneur du bloc 6. Le hash doit porter sur des `bytes`, le comptage de mots
   sur du `str` décodé — c'est le point B.9 du mémo, en situation réelle.
6. **`.csv` et `.md`** contiennent de la structure (en-têtes, titres). Tu les comptes
   comme du texte brut ? Encore un choix à assumer.

## Vérifier sans Python

```bash
find corpus_test -type f | wc -l                    # 12
find corpus_test -type f | sed 's/.*\.//' | sort | uniq -c
find corpus_test -type f -exec sha256sum {} + | sort | awk '{print $1}' | uniq -d
```

Le troisième pipeline te donne les empreintes en double : c'est ton oracle indépendant,
et c'est exactement le modèle Unix du mémo 7 (A.2).

## Régénérer / durcir

`python generer_corpus.py [destination]` réécrit le dossier de zéro.

Une fois ton script vert, ajoute toi-même : un fichier de 50 Mo (ta boucle tient-elle
en mémoire constante ?), un fichier binaire `.pdf` bidon (que fait `read_text` dessus ?),
et un lien symbolique circulaire (que fait `rglob` ?).
