# 1. L'inventaire — ce qui existe déjà, toujours en premier

## Pourquoi il passe avant tout

Un poste créé en doublon ne sera jamais utilisé. Il coûtera une fiche à tenir, un
skill à charger, et il donnera à la personne l'impression que l'équipe ne sert à
rien — parce que dans son domaine, elle avait déjà quelqu'un.

L'inventaire répond à une seule question : **qu'est-ce qui est déjà fait, et par
qui ?** Le diagnostic ne crée ensuite des postes que pour ce qui reste.

## L'ordre, non négociable

```
1. inventaire  →  2. entretien  →  3. diagnostic  →  4. récapitulatif validé
```

Et l'inventaire **se refait à chaque entretien** : nouvelle machine, nouveau
profil, prestataire recruté, poste fusionné. Un inventaire de six mois n'est plus
un inventaire.

## Ce qu'on inventorie

| Catégorie | Comment | À noter |
|---|---|---|
| profils Hermes | `ls ~/.hermes/profiles`, `hermes cron list` | périmètre réel, ce qui marche, ce qui ne marche pas |
| skills installés | `ls ~/.hermes/skills` | un skill déjà là rend un poste inutile |
| personnes | questions | conjoint, associé, salarié, comptable, prestataires |
| outils | questions | boutique, caisse, compta, banque, mail, réseaux, CRM |
| ce qui rate | questions | ce qui est fait mais mal, ou jamais |

Aucun mot de passe, aucun jeton : **la liste des outils suffit**.

## Le constat en trois lignes

```
Ce qui est couvert     : <fait, par qui>
Ce qui est mal couvert : <fait, mais mal ou en retard>
Ce qui n'est pas fait  : <personne ne le fait, et ça coûte>
```

**Seule la troisième ligne produit des postes.** La deuxième produit d'abord un
correctif : créer un poste pour masquer un dysfonctionnement connu déplace le
problème sans le résoudre.

## Ce que ça change dans la configuration

```json
"inventaire": {
  "date": "2026-10-29",
  "profils_hermes": ["devops"],
  "personnes": [{"nom": "Camille", "role": "production et vente"}],
  "outils": ["boutique en ligne", "compta externalisée"],
  "deja_couvert": ["site et boutique (devops)", "comptabilité (experte-comptable)"],
  "constat": "deux domaines tenus, trois jamais faits"
}
```

Ces champs apparaissent **dans le récapitulatif validé** : la personne doit voir,
noir sur blanc, ce qu'on ne lui recrée pas. C'est ce qui l'autorise à croire le
reste.

## Les pièges

- **Inventorier les outils au lieu des tâches.** « J'ai un Shopify » ne dit pas
  qui met les fiches produit à jour.
- **Prendre la liste des profils pour un inventaire.** Un profil installé et
  jamais utilisé n'est pas une couverture.
- **Sauter l'inventaire sur une réinstallation.** C'est exactement le cas où il
  change le plus : la machine a peut-être déjà des profils et des crons.
