# 6. L'installation — audit de la cible, pose, recette

## 1. Avant d'écrire — audit de la cible

Cinq vérifications, dans cet ordre. Sans elles, on écrit des chemins qui
n'existent pas.

```bash
hermes --version                    # version et mode d'installation
echo "${HERMES_HOME:-~/.hermes}"    # racine réelle (profil actif)
hermes cron status                  # le planificateur tourne ?
hermes kanban assignees             # profils réellement assignables
ls "$HERMES_HOME/skills"            # skills déjà présents (collisions de préfixe)
```

| Point | Pourquoi ça compte |
|---|---|
| `HERMES_HOME` | un profil actif déplace tout sous `profiles/<nom>/` |
| version | les options de `hermes cron create` changent selon les versions |
| kanban | sans assignee valide, les cartes restent en `ready` |
| préfixe | `equipe-` déjà pris → choisir `maison-`, `atelier-`… |
| planificateur arrêté | les crons seront créés mais ne partiront jamais |

**Aucun chemin absolu en dur** dans un skill généré : l'équipe doit fonctionner
pour une autre personne, sur une autre machine, avec un autre `HERMES_HOME`.

## 2. Poser

```bash
python3 scripts/installer.py --config equipe.json --dry-run    # plan, rien d'écrit
python3 scripts/installer.py --config equipe.json              # écrit
```

L'installation est **refusée** tant que l'organigramme n'est pas validé
(`05-organigramme.md`). C'est le seul prérequis.

| Option | Effet |
|---|---|
| `--dry-run` | affiche chaque fichier et son état | 
| `--force` | écrase un fichier existant, après sauvegarde `.bak-<horodatage>` |
| `--profile devops` | installe dans `$HERMES_HOME/profiles/devops` |
| `--hermes-home /chemin` | force la racine Hermes |
| `--with-crons` | crée le rappel du verrou après installation |

Trois garanties :

1. **Idempotent** — relancé sans changement, il n'écrit rien et le dit.
2. **Non destructif** — un fichier différent n'est pas écrasé sans `--force`.
3. **Sans secret** — ne lit ni n'écrit aucune variable sensible, aucun `.env`.

## 3. Ce qui est créé

```
<racine>/
├── organigramme.md        le récapitulatif validé (dérivé, régénéré)
├── README.md              le circuit en cinq lignes
├── config.json            la configuration appliquée (sans secret)
├── crons-a-creer.sh       les rappels, prêts à coller
├── a-valider/  livres/  archives/
├── cerveau/               entreprise.json, offres.md, fiscal.md
├── modeles/  logs/

<HERMES_HOME>/skills/<prefixe>/
├── <prefixe>-direction/SKILL.md        dispatch, verrou, format de mission
└── <prefixe>-<slug>/SKILL.md           un par poste, autant que le diagnostic en a trouvé

<HERMES_HOME>/scripts/<prefixe>-a-valider.sh
```

Le cerveau est écrit **vide de faits** : trois fichiers structurés avec leurs
sources à remplir. L'installateur ne recopie jamais un SIRET, un tarif ou une
mention.

## 4. Recette — sept contrôles

Un seul échec = installation incomplète. Ne pas annoncer « c'est prêt ».

| # | Contrôle | Commande / geste | Attendu |
|---|---|---|---|
| 1 | les skills sont là | `ls <HERMES_HOME>/skills/<prefixe>/*/SKILL.md \| wc -l` | **N + 1** (N postes + direction) |
| 2 | aucun gabarit non résolu | `grep -c "{{" …/*/SKILL.md` | `0` partout |
| 3 | le récapitulatif est validé | `grep "VALIDÉ" <racine>/organigramme.md` | une ligne avec le nom |
| 4 | le rappel est muet à vide | `bash <HERMES_HOME>/scripts/<prefixe>-a-valider.sh` | **aucune sortie** |
| 5 | il parle quand il y a un fichier | poser un `.md` dans `a-valider/`, relancer | une ligne, avec le nom |
| 6 | la direction se charge | « charge `<prefixe>-direction` » | la table des postes s'affiche |
| 7 | le verrou tient | mission 🟡 de test | livrable dans `a-valider/`, l'agent s'arrête |

Contrôle 6 en ligne de commande si besoin :

```bash
hermes -z "charge <prefixe>-direction et liste mes postes en 3 lignes"
```

## 5. Après la pose

1. Créer les rappels : `bash <racine>/crons-a-creer.sh` (ou `--with-crons`).
2. Vérifier : `hermes cron list`.
3. Remplir le cerveau depuis les papiers (`03-documents.md`), chaque fait sourcé.
4. Lancer **une** vraie mission 🟡 courte, et laisser la personne déplacer le
   fichier elle-même. C'est la seule preuve que le circuit est compris.
5. Consigner dans `livres/` ce qui a coincé au premier passage.

## 6. Désinstallation

L'installateur ne supprime rien : il n'a pas à décider ce qui appartient à la
personne.

```bash
rm -rf "<HERMES_HOME>/skills/<prefixe>"
rm -f  "<HERMES_HOME>/scripts/<prefixe>-a-valider.sh"
hermes cron remove <id>          # un par rappel (hermes cron list)
```

Le dossier de travail n'est **jamais** supprimé par un script : il peut contenir
des factures.
