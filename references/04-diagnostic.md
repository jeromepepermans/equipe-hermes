# 4. Le diagnostic — des besoins aux postes

C'est l'étape qui a remplacé « on crée trois postes ». Elle produit un **nombre**
qui n'est ni fixé d'avance ni arbitraire.

## La seule règle

> **Un poste existe si, et seulement si, il porte une tâche récurrente qui a un
> livrable nommé.**

Trois mots comptent :

- **récurrente** — au moins une fois par mois. Une tâche annuelle n'est pas un
  poste, c'est une note dans l'agenda.
- **qui n'est faite par personne** — sinon, c'est un correctif de l'existant,
  pas un poste (voir l'inventaire).
- **livrable nommé** — un fichier, un document, une liste, un message, avec un
  chemin et un format. « Suivre la stratégie » n'est pas un livrable.

Aucune limite de nombre. Un dispositif à 1 poste est légitime ; un dispositif à 6
aussi, si chacun passe le test. Ce qui tue un dispositif, ce n'est pas le nombre,
c'est le poste sans livrable.

## La procédure, en quatre passes

### Passe 1 — la liste brute

Reprendre **mot pour mot** les réponses du bloc D (les cinq tâches, ce qui est
détesté, ce qui n'est jamais fait, « 2 h par semaine »). Ne rien reformuler.

### Passe 2 — éliminer

| À éliminer | Pourquoi |
|---|---|
| ce qui est déjà couvert par un profil, une personne, un outil | inventaire, ligne « déjà couvert » |
| ce qui est fait une fois par an | pas récurrent |
| ce qui n'a pas de livrable nommé | impossible à valider, donc impossible à tenir |
| ce qui est le cœur de métier | ne se délègue pas : fabriquer, réparer, coder, soigner |
| ce qui est une décision | prix, client, partenariat : reste à la personne |

Ce qui reste est candidat.

### Passe 3 — regrouper

Regrouper les candidats par **livrable**, pas par thème. Deux tâches qui
produisent le même type de document vont dans le même poste, même si les mots
sont différents.

Test de regroupement : « si je confie A et B au même poste, la fiche reste-t-elle
lisible en une page ? » Si non, ce sont deux postes.

Test inverse : « si je sépare A et B, est-ce que deux postes produisent des
livrables distincts ? » Si non, c'est un seul poste.

### Passe 4 — nommer et justifier

Chaque poste reçoit : un **nom** (prénom), un **libellé** (Bureau, Voix,
Acquisition, Production, Logistique, Relation client, ou un libellé propre), et
surtout une **justification en une phrase** : *quelle tâche récurrente il porte*.

Cette phrase est obligatoire dans la configuration. Un poste sans justification
est refusé par l'installateur — c'est le garde-fou contre le poste décoratif.

## La bibliothèque de modèles

Sept modèles existent (`scripts/installer.py`, dictionnaire `MODELES`) : `bureau`,
`voix`, `acquisition`, `partenaires`, `fidelisation`, `production`, `logistique`,
`sav`. Ce sont des **points de départ**, pas des cases à cocher :

- un poste `modele` hérite d'un périmètre, de livrables et d'interdits par défaut ;
- un poste `libre` doit fournir lui-même son périmètre, ses livrables, ses
  interdits ;
- dans les deux cas, un modèle peut être corrigé poste par poste.

Choisir un modèle ne justifie pas le poste. La justification reste la phrase
« pourquoi il existe ».

## Quatre diagnostics réels, quatre résultats différents

| Situation | Postes | Pourquoi ce nombre |
|---|---|---|
| **Le fabricant seul** — il produit, vend sur les marchés, n'a jamais facturé un professionnel | **1** (Bureau) | sa seule tâche récurrente non faite est la facturation ; le reste, il le fait et l'aime |
| **L'artisane qui vend en boutique et sur les marchés** | **2** (Bureau, Voix) | fiches produit et annonces jamais faites ; la prospection ne concerne pas son métier |
| **Le dispositif déjà outillé** — un profil gère le site et la boutique, un comptable tient les comptes | **3** (Bureau, Voix, Acquisition) | trois manques restants, deux domaines déjà couverts par l'inventaire |
| **L'atelier avec stock, expéditions et SAV** | **4 à 5** (Bureau, Voix, Production, Logistique, parfois Relation client) | quatre tâches récurrentes distinctes, chacune avec ses livrables |

Le troisième cas est celui qui a produit la règle « 3 postes » : elle était vraie
**pour cette personne**, à ce moment-là, avec son inventaire. Elle n'est pas
transposable.

## Les pièges du diagnostic

- **Partir du modèle.** « Bureau, Voix, Acquisition » n'est pas un diagnostic,
  c'est un gabarit. Si la personne n'a pas de clients à chercher, Acquisition
  n'existe pas.
- **Compter les tâches.** Cinq tâches ne font pas cinq postes : elles font un ou
  deux postes qui les portent.
- **Créer un poste pour ce que la personne n'aime pas mais fait très bien.**
  L'aversion n'est pas un besoin : le temps, oui.
- **Oublier l'inventaire.** Le doublon est l'erreur la plus coûteuse, parce
  qu'elle est invisible : le poste existe, personne ne l'appelle.
- **Un poste « Direction ».** La direction, c'est le skill de dispatch, pas un
  poste. Elle ne produit aucun livrable.

## Ce que le diagnostic écrit

Il ne produit pas encore les fiches : il produit la **liste justifiée**, qui
devient la section `postes` de `equipe.json`, puis le récapitulatif
(`05-organigramme.md`), qui doit être validé avant toute installation.
