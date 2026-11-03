# equipe-hermes

Un skill Hermes qui **construit une équipe d'agents sur mesure** — inventaire,
entretien, diagnostic, organigramme validé — puis l'**installe** sur une instance
Hermes : dossier de travail, skills des postes, verrou de validation, rappels
silencieux.

Le nombre de postes n'est pas fixé : il est **la conséquence** de ce que la
personne fait, de ce qui lui prend son temps, et de ce qui existe déjà chez elle.
Un utilisateur qui a déjà deux agents n'a pas besoin des mêmes postes que
quelqu'un qui part de zéro.

> Ce dépôt remplace et absorbe `equipe-entrepreneur` (privé) : l'entretien, le
> diagnostic et l'installation sont désormais dans un seul skill, pour qu'il n'y
> ait plus de trou entre « on décide l'équipe » et « on l'installe ».

## Le parcours

| # | Étape | Ce qui sort |
|---|---|---|
| 1 | **Inventaire** (toujours en premier) | ce qui existe déjà : profils, personnes, outils, ce qui marche mal |
| 2 | **Entretien** | rôle, statut, activités, argent, temps, outils, papiers |
| 3 | **Documents** | le cerveau, avec un fait par source |
| 4 | **Diagnostic** | la liste justifiée des postes — 1, 2, 4, 6… |
| 5 | **Récapitulatif validé** | `organigramme.md`, approuvé nommément |
| 6 | **Installation** | dossiers, skills, verrou, rappels |

L'inventaire se refait **à chaque entretien** : une équipe de trois mois a changé.

## La règle, une seule

> **Un poste existe si, et seulement si, il porte une tâche récurrente qui a un
> livrable nommé.**

Pas de plafond. « Suivre la stratégie » ou « être présent » n'est pas un
livrable ; « facture PDF », « liste de prospects », « planning de production » le
sont. Ce qui tue un dispositif, ce n'est pas le nombre de postes, c'est le poste
que personne ne charge.

## Démarrage rapide

```bash
git clone https://github.com/jeromepepermans/equipe-hermes
cp -r equipe-hermes ~/.hermes/skills/equipe-hermes

cp equipe-hermes/templates/config.example.json ./equipe.json
# remplir : utilisateur, entreprise, inventaire, postes (la liste a la taille du diagnostic)

python3 equipe-hermes/scripts/installer.py --config equipe.json --recapitulatif
python3 equipe-hermes/scripts/installer.py --config equipe.json --valider "Camille Roux"
python3 equipe-hermes/scripts/installer.py --config equipe.json
```

Sans l'étape `--valider`, l'installation **refuse de tourner** (code de sortie 3,
aucune écriture). C'est voulu : le récapitulatif est le seul moment où l'équipe se
discute à froid.

Puis, dans une session Hermes :

```
charge equipe-hermes, commence par l'inventaire
```

## Le récapitulatif, en clair

```markdown
# Organigramme — Atelier Roux

## 1. Ce qui existait déjà (inventaire du 2026-10-29)
| Ce qui existe déjà | Détail |
|---|---|
| Profil Hermes | `boutique` |
| experte-comptable | comptes annuels |

**Déjà couvert, donc non recréé :** site et boutique, comptabilité

## 2. L'équipe proposée — 4 postes
| # | Poste | Nom | Pourquoi il existe | Livrable principal | Niveau |
|---|---|---|---|---|---|
| 1 | Bureau | Jeanne | factures en retard, relances jamais faites | facture PDF | 🔴 |
| 2 | Voix | Léa | fiches produit vides, pas de newsletter | fiche produit | 🟡 |
| 3 | Acquisition | Marc | aucun prospect contacté depuis 8 mois | liste de prospects | 🟡 |
| 4 | Production | Sam | ruptures de matière | liste de réassort | 🟡 |

## 5. Écarté, et pourquoi
- un poste Logistique — 3 expéditions par mois, pas récurrent
- un poste « Direction » — ne produit aucun livrable
```

## Ce que l'installation crée

```
<racine>/
├── organigramme.md        le récapitulatif validé (dérivé, régénéré)
├── a-valider/ livres/ archives/
├── cerveau/               entreprise.json, offres.md, fiscal.md
├── README.md  config.json  crons-a-creer.sh
└── modeles/  logs/

<HERMES_HOME>/skills/<prefixe>/
├── <prefixe>-direction/   dispatch, verrou, format de mission
└── <prefixe>-<slug>/      un par poste (autant que le diagnostic en a trouvé)
<HERMES_HOME>/scripts/<prefixe>-a-valider.sh
```

Huit modèles de postes (`bureau`, `voix`, `acquisition`, `partenaires`,
`fidelisation`, `production`, `logistique`, `sav`) sont des points de départ, ou
`libre` pour un poste décrit entièrement par l'utilisateur.

## Ce que l'installateur garantit

| Garantie | Comment c'est tenu |
|---|---|
| Pas d'installation sans validation | `validation.valide` + nom + date, sinon sortie 3 et zéro écriture |
| Pas de validation périmée | si le nombre de postes a changé, l'installation refuse |
| `--force` ne contourne pas le verrou | seul `--valider` le lève |
| Un poste sans livrable est refusé | contrôle à la lecture de la configuration |
| Un poste sans justification est refusé | champ `pourquoi` obligatoire |
| Idempotent | relancé sans changement, il n'écrit rien et l'affiche |
| Non destructif | un fichier différent n'est pas écrasé sans `--force` |
| `--force` sauvegarde | copie `.bak-<horodatage>` avant chaque écrasement |
| `--dry-run` | plan complet, zéro écriture |
| Aucun secret | ne lit ni n'écrit de variable sensible, ne crée aucun `.env` |

```bash
python3 tests/test_installer.py     # tests réels, aucun mock
```

## Le dépôt

```
SKILL.md                        le skill (à charger dans Hermes)
references/01-inventaire.md     ce qui existe déjà — toujours en premier
references/02-entretien.md      rôle, statut, activités, temps ; ce que ça décide
references/03-documents.md      extraction des papiers, contrôles, minimisation
references/04-diagnostic.md     comment N postes se déduisent des besoins
references/05-organigramme.md   le récapitulatif et le verrou de validation
references/06-installation.md   audit de la cible, pose, recette en 7 contrôles
references/07-verrou.md         les 3 niveaux, le circuit, les cas limites
references/08-crons.md          rappels silencieux, --no-agent, --deliver
references/09-portabilite.md    ce qui voyage et ce qui ne voyage pas
references/10-exemple.md        deux cas complets — 4 postes et 1 poste, fictifs
templates/                      config, organigramme, questions, 2 gabarits de skills, cerveau
scripts/installer.py            l'installateur
scripts/a-valider.sh            le rappel
tests/test_installer.py         les tests
```

## Ce que ce dépôt n'est pas

- Pas un générateur d'agents à la chaîne : chaque poste doit porter un livrable
  récurrent, et le récapitulatif doit être validé.
- Pas un cabinet comptable ni juridique : il prépare, signale, renvoie vers un
  professionnel.
- Pas une équipe de développement : c'est `equipes-delegation` et les profils
  techniques qui s'en chargent.
- Pas un endroit où mettre vos données : les exemples sont **fictifs**, et le
  dossier de travail généré n'est jamais versionné.

## Licence

MIT — voir `LICENCE`.
