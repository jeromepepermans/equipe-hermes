# Paramétrage — sept blocs, un fichier

Le paramétrage produit **un seul artefact** : `equipe.json`. Tout le reste en
découle mécaniquement. Une question sans conséquence sur ce fichier ne mérite
pas d'être posée.

Règle de conduite : on pose les blocs par petits groupes, jamais en formulaire
géant. On ne passe au bloc suivant que quand le précédent est exploitable. Une
réponse incertaine se note `a_confirmer`, elle ne s'arrondit pas.

---

## Bloc A — L'entrepreneur

| Question | Champ | Pourquoi |
|---|---|---|
| Comment veux-tu que l'équipe t'appelle ? | `entrepreneur.nom` | apparaît dans les fiches et les rappels |
| Tutoiement ou vouvoiement ? | `langue.tutoiement` | change le ton des quatre fiches |
| Langue de travail ? | `langue.code` | `fr` par défaut |

## Bloc B — L'entreprise

| Question | Champ | Pourquoi |
|---|---|---|
| Nom commercial exact ? | `entreprise.nom` | en-tête des livrables |
| Statut (micro, EI, SASU…) ? | `entreprise.statut` | détermine les mentions et le 🔴 |
| Franchise de TVA ou assujetti ? | `entreprise.tva` | `franchise` → tous les prix TTC, jamais de ligne TVA |
| En une phrase, que vend-elle ? | `entreprise.activite` | sert au troisième poste |

## Bloc C — Où vit le dispositif

| Question | Champ | Défaut |
|---|---|---|
| Dossier de travail ? | `racine` | `~/equipe` |
| Préfixe des skills ? | `prefixe` | `equipe` → `equipe-ceo`, `equipe-bureau`… |
| Profil Hermes hôte ? | `profil` | `default` |

Un préfixe par dispositif permet d'en faire coexister deux sur la même machine
(`equipe-`, `maison-`) sans collision de noms de skills.

## Bloc D — Les trois postes

| Question | Champ | Remarque |
|---|---|---|
| Nom du chef Bureau ? | `postes.bureau.nom` | défaut `Bureau`, mais un prénom rend le poste réel |
| Nom du chef Voix ? | `postes.voix.nom` | idem |
| Libellé du 3ᵉ poste ? | `postes.troisieme.libelle` | `Acquisition` \| `Partenaires` \| `Fidélisation` |
| Nom du chef du 3ᵉ poste ? | `postes.troisieme.nom` | |
| Quelle tâche ne déléguera-t-il jamais ? | `postes.*.ne_fait_jamais` | la ligne la plus utile de la fiche |

Le choix du libellé se déduit de l'activité, il ne se demande pas au hasard :

- plusieurs clients possibles → **Acquisition** ;
- l'activité dépend d'un réseau de distributeurs ou de prescripteurs →
  **Partenaires** ;
- un seul client fait le chiffre d'affaires → **Fidélisation** (le risque est la
  concentration, pas le manque de prospects).

## Bloc E — Le verrou

| Question | Champ | Défaut |
|---|---|---|
| Quels livrables sont 🟡 (validation) ? | `verrou.niveau2` | email, publication, annonce, message client |
| Quels livrables sont 🔴 (signature) ? | `verrou.niveau3` | facture, devis engageant, paiement, déclaration |
| Heures des rappels ? | `verrou.rappel` | `["08:00", "18:00"]` |
| Fuseau ? | `verrou.fuseau` | `Europe/Paris` |

Une facture est 🔴 partout. Une réponse à un avis client ne l'est nulle part.
Ce n'est donc pas universel : on fait confirmer, et on écrit la réponse dans la
fiche du poste concerné.

## Bloc F — Les rappels

| Question | Champ | Défaut |
|---|---|---|
| Rappel du verrou ? | `crons.verrou.actif` | `true` |
| Alerte déclaration URSSAF ? | `crons.urssaf.actif` + `.jour` | `false` |
| Alerte actualisation France Travail ? | `crons.france_travail.actif` + `.jour` | `false` |
| Où livrer les notifications ? | `crons.livraison` | `origin` |

Ne cocher un rappel fiscal que si le régime l'impose réellement. Un rappel qui
tombe à côté est pire que pas de rappel : il décrédibilise les autres.

## Bloc G — Le tableau des tâches

| Question | Champ | Défaut |
|---|---|---|
| Utiliser le kanban Hermes ? | `kanban.actif` | `false` |
| Profil assigné (doit exister) ? | `kanban.assignee` | `default` |

Vérifier l'assignee avant de l'écrire : `hermes kanban assignees`. Un assignee
absent donne des cartes bloquées en `ready`. Le chef se nomme dans le **titre**.

---

## Le fichier produit

`templates/config.example.json` est le squelette commenté. Une version minimale
qui fonctionne :

```json
{
  "version": 1,
  "prefixe": "equipe",
  "profil": "default",
  "racine": "~/equipe",
  "langue": { "code": "fr", "tutoiement": true },
  "entrepreneur": { "nom": "Camille" },
  "entreprise": {
    "nom": "Atelier Camille",
    "statut": "micro-entreprise",
    "tva": "franchise",
    "activite": "restauration de meubles anciens"
  },
  "postes": {
    "bureau":  { "nom": "Jeanne" },
    "voix":    { "nom": "Léa" },
    "troisieme": { "nom": "Marc", "libelle": "Acquisition" }
  },
  "verrou": { "niveau3_actif": true, "rappel": ["08:00", "18:00"], "fuseau": "Europe/Paris" },
  "crons": { "verrou": { "actif": true }, "urssaf": { "actif": false }, "france_travail": { "actif": false }, "livraison": "origin" },
  "kanban": { "actif": false, "assignee": "default" }
}
```

Les blocs absents prennent leur défaut. `racine`, `entrepreneur.nom` et
`entreprise.nom` sont obligatoires : l'installateur refuse de deviner.

## Ce qu'on ne demande pas

- Un tarif exact de mémoire → il vient du cerveau, pas de l'entretien.
- Un mot de passe, une clé, un IBAN → jamais dans le dispositif.
- Le détail des 31 rôles possibles → trois postes, et c'est tout.
- Le nom du client final → donnée personnelle, inutile au démarrage.
