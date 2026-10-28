---
name: equipe-hermes
description: "Installer CEO + 3 chefs sur une autre instance Hermes."
version: 1.0.0
author: Jérôme PEPERMANS
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [equipe, agents, parametrage, installation, verrou, portabilite]
    related_skills: [equipe-entrepreneur, equipes-delegation, hermes-agent]
---

# Équipe Hermes — installer le dispositif sur une autre instance

## Quand l'utiliser

- Un dispositif « CEO + 3 chefs » existe déjà quelque part et on veut le
  **reproduire sur une autre instance Hermes** (autre machine, autre profil,
  autre client).
- Un entrepreneur a validé son équipe (`equipe-entrepreneur`, lots 1 à 3) et il
  faut maintenant **la poser réellement** : dossiers, skills, rappels, kanban.
- On reprend une instance existante et on veut **vérifier** que le dispositif y
  est complet (les quatre skills, le dossier de travail, le verrou, les crons).

Ne couvre **pas** l'entretien qui décide *qui* fait *quoi* : c'est
`equipe-entrepreneur`. Ici, la décision est déjà prise, on l'installe.

## Ce que le dispositif est — et n'est pas

**Un profil, quatre skills, un dossier, un verrou.** Pas un agent par poste.

| Élément | Rôle |
|---|---|
| **CEO** (`<prefixe>-ceo`) | point d'entrée unique, découpe et dispatche |
| **3 chefs** (`<prefixe>-bureau`, `-voix`, `-<3e>`) | un périmètre chacun, jamais deux sur un livrable |
| **Dossier de travail** | `a-valider/` → `livres/` → `archives/` + `cerveau/` |
| **Verrou** | 🟢 libre / 🟡 validation / 🔴 signature |
| **Rappels** | un cron silencieux qui liste `a-valider/` |

Les chefs ne sont **pas** des profils Hermes. Décision mesurée sur une
installation réelle : trois profils dédiés ont été créés puis supprimés le même
jour — trois mémoires et trois dossiers de skills à tenir pour des postes qui
n'ont aucun outil propre. Un chef = **un skill chargé dans la session en cours**.

Conséquence non évidente, et c'est le piège n°1 : sur le kanban, l'`assignee`
doit être un profil qui **existe** (`hermes kanban assignees`). Un assignee
inconnu laisse la carte en `ready` indéfiniment. Le nom du chef va donc dans le
**titre** : `[Léa] canevas d'atelier`, assignee `default`.

## Procédure — quatre étapes

1. **Auditer la cible** — `references/02-installation.md`, § « avant d'écrire ».
   Version d'Hermes, profil actif, `HERMES_HOME` réel, cron qui tourne, kanban
   qui répond. On ne paramètre pas une instance dont on ne connaît pas les
   chemins.
2. **Paramétrer** — `references/01-parametrage.md`. Sept blocs de questions,
   puis un fichier `equipe.json`. Ce fichier est la seule entrée de
   l'installateur : ce qui n'y est pas ne sera pas installé.
3. **Installer** — `scripts/installer.py --config equipe.json`. Idempotent,
   `--dry-run` disponible, sauvegarde avant écrasement.
4. **Vérifier** — `references/02-installation.md`, § « recette ». Quatre skills
   visibles, dossier complet, rappel muet quand `a-valider/` est vide, une
   mission 🟡 qui s'arrête bien dans `a-valider/`.

## Les quatre skills générés

| Skill | Contenu | Ne fait jamais |
|---|---|---|
| `<prefixe>-ceo` | dispatch, verrou, format de mission, kanban | produire un livrable lui-même |
| `<prefixe>-bureau` | devis, factures, relances, déclarations, CA | publier, prospecter |
| `<prefixe>-voix` | contenu, annonces, fiches, réseaux, SEO | envoyer, signer |
| `<prefixe>-<3e>` | clients, fournisseurs, partenaires **ou** fidélisation | négocier un prix, engager |

Le troisième poste est le seul dont le **libellé** change selon l'activité
(`Acquisition`, `Partenaires`, `Fidélisation`) ; son **nom** se choisit avec
l'entrepreneur. Bureau et Voix ne changent jamais : ce sont les deux manques de
temps qui existent dans tous les métiers.

Gabarits : `templates/skills/ceo.SKILL.md`, `templates/skills/chef.SKILL.md`.
Règles de rédaction et de dispatch : `references/03-postes.md`.

## Le verrou — non négociable

- 🟢 **libre** : recherche, lecture, calcul, brouillon interne.
- 🟡 **validation avant sortie** : email, publication, annonce, message client.
  Le livrable est écrit dans `a-valider/` et l'agent **s'arrête**.
- 🔴 **signature explicite** : facture, devis engageant, paiement, déclaration.
  Le livrable reste dans `a-valider/`, l'agent rappelle la conséquence exacte
  (numéro consommé, engagement, échéance légale).

**Aucun agent ne déplace un fichier de `a-valider/` vers `livres/`.** Le
déplacement est la signature de l'entrepreneur — c'est aussi la seule preuve
technique qu'une validation a eu lieu. Détail et cas limites :
`references/04-verrou.md`.

Si l'activité n'a aucune obligation engageante, 🔴 est **déclaré et laissé
vide** : il n'est jamais supprimé. Une facture au premier client professionnel
arrive vite.

## Rappels automatiques

`references/05-crons.md`. Deux règles apprises sur une instance réelle :

1. **Sortie vide = silence.** Un rappel qui notifie « rien à valider » finit
   ignoré en trois jours.
2. **`--no-agent`.** Un rappel est un `ls` formaté, pas un tour de LLM : zéro
   coût, zéro latence, zéro risque d'invention.

L'installateur écrit le script de rappel et la commande exacte ; la création du
cron reste une décision explicite (`--with-crons` ou commande affichée).

## Règles transverses

1. **Langue et ton de l'entrepreneur**, fixés au paramétrage (tutoiement ou
   vouvoiement). Ils s'appliquent aux quatre fiches, pas seulement au CEO.
2. **Zéro invention** : un chiffre, un taux, une date non vérifié se marque
   « à confirmer ».
3. **Aucun secret, aucune donnée personnelle** dans le dossier du dispositif ni
   dans ce dépôt : pas de mot de passe, de clé, d'IBAN, de coordonnée client.
   Les exemples de `references/07-exemple.md` sont **fictifs**.
4. **Ne jamais garantir la conformité** juridique ou fiscale : « à faire
   valider par un professionnel ».
5. **Ne pas rouvrir** la question « un profil par chef ». Elle a été tranchée
   par la mesure, pas par le goût.

## Pièges

- **Écrire les skills avant d'avoir le `equipe.json`.** On produit alors quatre
  fiches à réécrire, avec des noms de postes qui changent en cours de route.
- **Créer un profil Hermes par chef.** Voir plus haut : trois mémoires à tenir
  pour rien, et des cartes kanban orphelines.
- **Confondre « l'agent a fini » et « c'est validé ».** Tant que le fichier est
  dans `a-valider/`, la mission n'est pas terminée.
- **Laisser un rappel bavard.** Le verrou meurt de bruit, pas d'oubli.
- **Recopier un vrai dossier client en exemple.** Le dépôt est public : les
  exemples sont inventés, et le restent.
- **Écraser un dispositif existant.** `installer.py` sauvegarde avant
  d'écraser ; ne jamais contourner avec un `--force` réflexe.

## Installation de ce skill

```bash
git clone https://github.com/jeromepepermans/equipe-hermes
cp -r equipe-hermes ~/.hermes/skills/equipe-hermes
```

Puis, dans une session : « charge `equipe-hermes` et installe le dispositif —
voici `equipe.json` ».
