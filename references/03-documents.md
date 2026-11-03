# 3. Les papiers — extraire des faits, pas recopier des documents

## La règle de base

**Un fait sans source ne rentre pas dans le cerveau.** Chaque ligne extraite porte
d'où elle vient : `Kbis`, `avis SIRENE`, `récap. déclaration 2026-06`,
`facture FAC-2026-014`, `réponse de la personne`. Un fait que personne ne peut
sourcer s'écrit « à confirmer » et va dans `questions-ouvertes.md`.

Sans cette discipline, dans six mois personne ne sait s'il faut corriger le
cerveau ou corriger le document.

## Les champs à extraire

### Kbis / avis SIRENE

| Champ | Ce qu'il décide |
|---|---|
| dénomination, enseigne | en-tête des documents, ce que la Voix a le droit d'écrire |
| forme juridique | mentions obligatoires, mode de signature |
| adresse du siège | mentions, TVA, assurance |
| SIREN / SIRET | identifiant de facturation |
| code NAF et libellé d'activité | contrôle de cohérence — **le champ le plus utile** |
| date d'immatriculation, état | ancienneté, cohérence avec les factures |

**Ne pas recopier** : date et lieu de naissance, nationalité, situation familiale,
mentions de radiation ou de procédure. Présentes sur le document, inutiles à
toute décision.

⚠ Un Kbis de plus de trois mois ne prouve plus l'état actuel : vérifier sur
`recherche-entreprises.api.gouv.fr` avec le SIREN, et citer les deux sources si
elles divergent.

### Récapitulatif de déclaration sociale

| Champ | Ce qu'il décide |
|---|---|
| régime | ce que les agents peuvent calculer |
| catégorie (artisanale, commerciale, libérale) | les taux applicables |
| périodicité | le calendrier des rappels |
| taux réellement appliqués, par nature de CA | toute estimation de cotisation |
| ventilation vente / service | le classement des recettes, donc le taux |
| versement libératoire (oui/non) | ce qui reste à provisionner |

**Jamais un taux de mémoire** : les taux sont datés et changent par décret. Le
cerveau écrit le taux **avec sa date et sa source**, et ajoute « à revérifier
avant toute projection ».

### Factures émises

| Champ | Ce qu'il décide |
|---|---|
| format et continuité de numérotation | si le poste Bureau peut émettre, ou doit d'abord ranger |
| mentions présentes | le modèle à reproduire |
| désignation des lignes | la précision attendue |
| prix constatés | la grille tarifaire du cerveau |
| nature des lignes (bien / service) | le clivage vente/service, donc le taux |
| délai de paiement réel | le calendrier de relance |

**Le contrôle qui compte** : lister les numéros, trier, chercher les trous et les
doublons. Un trou de numérotation ne se répare pas.

### Export de caisse / boutique / tableur

| Champ | Ce qu'il décide |
|---|---|
| CA par mois | saisonnalité, seuils, provision |
| CA par famille | priorités de la Voix et de l'Acquisition |
| panier moyen, nombre de transactions | ce qui est réaliste comme objectif |
| concentration client | risque, urgence des relances |
| canaux de vente | où l'Acquisition a un levier |

Un export incomplet reste incomplet : on note la période couverte et on écrit
« partiel ». On ne complète pas une série par une moyenne.

## Les cinq contrôles de cohérence

Faire dans cet ordre, écrire le résultat **dans un fichier séparé**, jamais en
corrigeant les réponses de la personne.

1. **Activité déclarée ↔ réelle.** Si la vente principale n'est pas au Kbis :
   signaler, avec les trois conséquences (assurance, contrôle social ou fiscal,
   établissement de paiement). Donner les pistes **comme pistes**, jamais comme
   correction : « à faire valider par un professionnel ».
2. **Régime ↔ périodicité ↔ échéances.** Une périodicité sans date de prochaine
   échéance est une bombe à retardement : en tête de `questions-ouvertes.md`.
3. **Nature du CA ↔ taux appliqué.** Une fabrication vendue par celui qui la fait
   relève en principe des ventes de marchandises, pas des prestations. Le rôle de
   l'agent est de **signaler et chiffrer l'écart**, jamais de reclasser.
4. **Cohérence interne des pièces.** Total qui ne fait pas la somme des lignes,
   date d'émission antérieure à la livraison, numéro déjà vu : signaler la pièce
   et la ligne.
5. **Le client récurrent qui ressemble à une structure liée.** Confondre les deux
   fausse le cerveau **et** la Voix (deux marques mélangées dans un contenu).
   Vérifier : qui facture qui, sous quel SIREN.

## Deux fichiers, jamais un seul

- `cerveau/…` : les faits retenus, avec la colonne source.
- `questions-ouvertes.md` : ce qui manque ou se contredit.

**`questions-ouvertes.md` ne quitte jamais la machine.** Il est dans
`.gitignore` : c'est là que vivent les écarts entre le déclaré et le réel, et un
dépôt qui les contient est une pièce à charge. Le dépôt de l'équipe ne contient
que des gabarits — jamais le cerveau d'une personne réelle.

## Minimisation

- Aucune donnée personnelle de client dans le dispositif. Un exemple = un
  identifiant, jamais un nom.
- Aucune coordonnée bancaire, aucun mot de passe, aucune clé. Si le document en
  contient : « présent sur le document, non recopié volontairement ».
- Les montants agrégés sont utiles ; le détail nominatif ne l'est pas.
- Les exemples du dépôt sont une entreprise **fictive**, jamais un cas réel même
  anonymisé : un cas réel garde assez de détails pour être ré-identifié.
