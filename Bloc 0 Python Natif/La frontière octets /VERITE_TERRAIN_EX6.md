# Exercice 6 — Vérité terrain

Fichier : `corpus_json/appels.json`, **1647 octets pour 1601 caractères**.
L'écart de 46 est le nombre d'octets supplémentaires consommés par les accents en
UTF-8 : c'est la première chose à vérifier, et elle démontre à elle seule que
`len(bytes) != len(str)`.

Régénère avec `python generer_journal_json.py`.

## Résultats attendus

| grandeur | valeur |
|---|---|
| nombre d'appels | 6 |
| somme des coûts en `Decimal` | **0.71** |
| somme des coûts en `float` | **0.7100000000000001** |
| total `tokens_entrée` | 29 250 |
| appels sans fuseau horaire | `a3` |
| appels avec un champ manquant | `a4` (pas de `tokens_sortie`) |

**La ligne à retenir est la deuxième contre la troisième.** Les coûts sont
`0.1, 0.1, 0.2, 0.2, 0, 0.11`. En `Decimal` la somme est exacte ; en `float` tu
récoltes un `...0001` parasite. Calcule les deux, affiche les deux, et garde la
comparaison dans ta sortie : c'est la démonstration de l'exercice.

## Les pièges, et ce qu'ils te demandent de trancher

1. **Les clés du JSON ont des accents** (`coût`, `modèle`, `tokens_entrée`,
   `généré_le`). Volontaire : tu ne peux pas y accéder par attribut, et tu dois
   penser à l'encodage jusque dans les noms de champs.

2. **`a3` a un horodatage sans fuseau** : `"2026-08-28T14:02:00"`. `fromisoformat`
   l'accepte et rend un objet dont `tzinfo` vaut `None`. Le comparer aux autres
   lève `TypeError: can't compare offset-naive and offset-aware datetimes`.
   Décide : tu rejettes, ou tu supposes UTC ? Écris ta décision en commentaire.

3. **`a2` est en `+02:00`**, pas en UTC. Si tu ne normalises pas, ton tri
   chronologique est faux. Deux instants identiques peuvent s'écrire différemment.

4. **`a4` n'a pas de `tokens_sortie`.** `a["tokens_sortie"]` lève `KeyError`.
   `a.get("tokens_sortie", 0)` te donne zéro — mais zéro est-il la vérité, ou un
   mensonge commode ? Encore un arbitrage.

5. **`a5` a un coût de `"0"`.** Vérifie qu'il ne casse rien et qu'il n'est pas
   confondu avec une valeur absente. `if not cout:` serait un bug ici.

6. **Les coûts sont des chaînes**, pas des nombres JSON. C'est exprès :
   `Decimal("0.1")` est exact, `Decimal(0.1)` reprend le flottant approximatif et
   te rend `0.1000000000000000055511151231257827`. Essaie les deux une fois.

7. **`json.dumps` refuse les `Decimal`** : `TypeError: Object of type Decimal is
   not JSON serializable`. Tu dois choisir comment le sérialiser — en chaîne
   (exact, mais plus un nombre pour le consommateur), en `float` (nombre, mais tu
   perds ce que tu venais de gagner), ou en entier de centièmes. Le bon choix
   dépend de l'usage, et tu dois savoir le justifier.

## Vérifier sans Python

```bash
wc -c corpus_json/appels.json    # 1647 octets
wc -m corpus_json/appels.json    # 1601 caractères
file corpus_json/appels.json     # doit annoncer UTF-8
python3 -c "import json,sys;print(len(json.load(open('corpus_json/appels.json',encoding='utf-8'))['appels']))"
```

Les deux premières commandes sont ton oracle sur l'encodage : `wc -c` compte les
octets, `wc -m` les caractères. Si les deux nombres sont égaux, ton fichier a
perdu ses accents en route.

## Critères de réussite

- « café » et « œuf » survivent à l'aller-retour sans devenir `caf\u00e9`
  (`ensure_ascii=False`). Affiche la sortie avec **et** sans, pour voir la différence.
- La somme en `Decimal` vaut exactement `0.71`, et tu peux montrer le
  `0.7100000000000001` du `float` à côté.
- Tous tes horodatages normalisés ont un `tzinfo` non nul, et sont triables entre eux.
- Tu peux dire, pour chaque variable de ton script, si elle contient des `bytes`
  ou un `str`.
