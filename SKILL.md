---
name: equipe-hermes
description: "Construire et installer une équipe d'agents sur mesure."
version: 2.0.0
author: Jérôme PEPERMANS
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [equipe, agents, entretien, diagnostic, installation, verrou]
    related_skills: [equipes-delegation, hermes-agent]
---

# Équipe sur mesure — de l'inventaire à l'installation

## Quand l'utiliser

- Une personne veut « des agents » et ne sait pas quoi leur confier.
- Elle a déjà une équipe, et il faut la compléter, la refaire ou la porter ailleurs.
- Il faut **installer** une équipe décidée : dossiers, skills, verrou, rappels.

Le skill va de l'inventaire à l'installation. Il ne part d'aucun modèle d'équipe :
**le nombre de postes est un résultat**, pas une entrée.

## Le principe

> **Un poste existe si, et seulement si, il porte une tâche récurrente qui a un
> livrable nommé.**

Aucun plafond. Un dispositif à 1 poste est légitime ; un à 6 aussi. Ce qui tue un
dispositif, ce n'est pas le nombre, c'est le poste sans livrable — celui qu'on ne
charge jamais et qui donne à la personne l'impression que l'équipe ne sert à rien.

Trois mots du principe sont opposables :

| Mot | Ce qu'il élimine |
|---|---|
| **récurrente** (≥ 1×/mois) | les tâches annuelles, qui sont des notes d'agenda |
| **que personne ne fait** | les doublons d'un profil, d'un outil ou d'un prestataire existant |
| **livrable nommé** | « suivre la stratégie », « être présent », « réfléchir » |

## Le parcours — six étapes

| # | Étape | Sortie | Document |
|---|---|---|---|
| 1 | **Inventaire** — ce qui existe déjà | constat en trois lignes | `references/01-inventaire.md` |
| 2 | **Entretien** — qui est la personne, statut, activités, papiers | réponses + documents | `references/02-entretien.md` |
| 3 | **Documents** — extraire des faits sourcés | `cerveau/`, `questions-ouvertes.md` | `references/03-documents.md` |
| 4 | **Diagnostic** — des besoins aux postes | liste justifiée | `references/04-diagnostic.md` |
| 5 | **Récapitulatif validé** | `organigramme.md` + validation | `references/05-organigramme.md` |
| 6 | **Installation** | dossiers, skills, verrou, rappels | `references/06-installation.md` |

**L'étape 1 se refait à chaque entretien.** Trois mois plus tard, un profil est
apparu, une prestataire a été recrutée, un poste a fusionné. Un diagnostic posé
sur un inventaire périmé produit des doublons — l'erreur la plus coûteuse, parce
qu'elle est invisible : le poste existe, personne ne l'appelle.

## Ce que l'entretien doit savoir

1. **Qui** — rôle exact (entrepreneur, indépendant, dirigeant, salarié,
   association), forme juridique, activités multiples éventuelles.
2. **Ce qui se vend vraiment** — pas ce que le Kbis déclare.
3. **L'argent** — ordres de grandeur seulement, jamais un montant de mémoire.
4. **Le temps** — cinq tâches, ce qui est détesté, ce qui n'est jamais fait,
   « deux heures par semaine, tu donnerais quoi ? ».
5. **Les outils et les accès** — la liste, jamais un mot de passe.
6. **Les papiers** — Kbis, SIRENE, récapitulatifs de déclaration, factures,
   exports de caisse. Chaque fait entre avec **sa source**.

Le rôle n'est pas décoratif : il décide de ce qui est engageant, donc du niveau
🔴. Un salarié qui n'engage pas l'entreprise et un dirigeant de société n'ont pas
le même verrou.

## Le récapitulatif est un verrou technique

```bash
python3 scripts/installer.py --config equipe.json --recapitulatif   # montrer
python3 scripts/installer.py --config equipe.json --valider "<nom>" # approuver
python3 scripts/installer.py --config equipe.json                   # installer
```

L'installateur **refuse** de tourner si l'organigramme n'est pas validé : code de
sortie 3, aucune écriture. Il refuse aussi si le nombre de postes a changé depuis
la validation — une validation qui ne correspond plus au contenu ne vaut rien.
`--force` ne lève pas ce verrou ; seul `--valider` le fait.

Le récapitulatif contient toujours : ce qui existait déjà, les N postes avec leur
**justification**, ce qui n'est pas couvert, et **ce qui a été écarté avec la
raison**.

## Ce que l'installation crée

```
<racine>/
├── organigramme.md        le récapitulatif validé (dérivé)
├── a-valider/ livres/ archives/
├── cerveau/               entreprise.json, offres.md, fiscal.md
├── README.md  config.json  crons-a-creer.sh
└── modeles/  logs/

<HERMES_HOME>/skills/<prefixe>/
├── <prefixe>-direction/   dispatch, verrou, format de mission
└── <prefixe>-<slug>/      un par poste, autant que le diagnostic en a trouvé

<HERMES_HOME>/scripts/<prefixe>-a-valider.sh
```

Huit modèles de postes servent de **points de départ** (`bureau`, `voix`,
`acquisition`, `partenaires`, `fidelisation`, `production`, `logistique`, `sav`),
ou `libre` pour un poste entièrement décrit par l'utilisateur. Choisir un modèle
ne justifie pas le poste : la phrase « pourquoi il existe » reste obligatoire.

## Le verrou — non négociable

- 🟢 **libre** : recherche, lecture, calcul, brouillon interne.
- 🟡 **validation avant sortie** : email, publication, annonce, message client.
  Le livrable est écrit dans `a-valider/` et l'agent **s'arrête**.
- 🔴 **signature explicite** : facture, devis engageant, paiement, déclaration.
  Le livrable reste dans `a-valider/`, l'agent rappelle la conséquence exacte.

**Aucun agent ne déplace un fichier de `a-valider/` vers `livres/`.** Le
déplacement est la signature, et la seule preuve technique qu'une validation a eu
lieu. Détail : `references/07-verrou.md`.

## Portabilité

Une équipe finalisée voyage sous forme de **paramétrage + skills régénérés**,
jamais d'un `rsync` : le cerveau, `livres/` et `questions-ouvertes.md` restent
chez la personne. Détail : `references/09-portabilite.md`.

## Règles transverses

1. **Langue et ton de la personne**, fixés à l'entretien, appliqués partout.
2. **Zéro invention** : un chiffre, un taux, une date non vérifié se marque
   « à confirmer ».
3. **Aucun secret, aucune donnée personnelle** dans le dispositif : pas de mot de
   passe, de clé, d'IBAN, de coordonnée client. `questions-ouvertes.md` ne quitte
   jamais la machine.
4. **Les exemples du dépôt sont fictifs** — jamais un cas réel, même anonymisé.
5. **Ne jamais garantir la conformité** juridique ou fiscale.
6. **Le rôle décide du verrou**, pas le ton du message.

## Pièges

- **Sauter l'inventaire.** Le doublon est l'erreur la plus coûteuse et la plus
  discrète.
- **Partir du gabarit « Bureau / Voix / Acquisition ».** C'est un modèle, pas un
  diagnostic.
- **Compter les tâches.** Cinq tâches ne font pas cinq postes.
- **Créer un poste « Direction ».** La direction est le skill de dispatch ; elle
  ne produit aucun livrable.
- **Installer sans récapitulatif validé.** L'installateur le refuse — ne pas
  contourner en éditant `validation.valide` à la main : c'est le seul endroit du
  dispositif où la personne est vraiment consultée.
- **Confondre « l'agent a fini » et « c'est validé ».**

## Installation de ce skill

```bash
git clone https://github.com/jeromepepermans/equipe-hermes
cp -r equipe-hermes ~/.hermes/skills/equipe-hermes
```

Puis, dans une session : « charge `equipe-hermes`, commence par l'inventaire ».
