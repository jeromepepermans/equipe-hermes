# Installation sur une instance — audit, pose, recette

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

À noter avant de continuer :

| Point | Pourquoi ça compte |
|---|---|
| `HERMES_HOME` | un profil actif déplace tout sous `profiles/<nom>/` |
| version | les options `hermes cron create` varient selon les versions |
| kanban | sans assignee valide, les cartes restent en `ready` |
| préfixe | `equipe-` déjà pris → choisir `maison-`, `atelier-`… |
| planificateur arrêté | les crons seront créés mais ne partiront jamais |

**Ne jamais coder de chemin absolu en dur** dans un skill généré : le dispositif
doit fonctionner pour un autre utilisateur, sur une autre machine, avec un autre
`HERMES_HOME`. La racine est écrite dans le `equipe.json` et substituée.

## 2. Poser

```bash
python3 scripts/installer.py --config equipe.json --dry-run   # le plan, rien d'écrit
python3 scripts/installer.py --config equipe.json             # écrit
```

Options :

| Option | Effet |
|---|---|
| `--dry-run` | affiche chaque fichier et son état (`créé`, `inchangé`, `écrasé`) |
| `--force` | écrase un fichier existant, après sauvegarde `.bak-<horodatage>` |
| `--profile devops` | installe dans `$HERMES_HOME/profiles/devops` |
| `--hermes-home /chemin` | force la racine Hermes |
| `--with-crons` | crée le rappel du verrou après installation |

Trois garanties de l'installateur :

1. **Idempotent** — relancé sans changement, il n'écrit rien et le dit.
2. **Non destructif** — un fichier existant différent n'est pas écrasé sans
   `--force`, et `--force` sauvegarde d'abord.
3. **Sans secret** — il ne lit ni n'écrit aucune variable d'environnement
   sensible ; aucun `.env` n'est créé.

## 3. Ce qui est créé

```
<racine>/
├── README.md              le circuit en cinq lignes, lisible par l'humain
├── config.json            la copie du paramétrage (sans secret)
├── crons-a-creer.sh       les commandes de rappel, prêtes à coller
├── a-valider/             l'agent dépose ici, puis s'arrête
├── livres/                validé (déplacement par l'entrepreneur)
├── archives/              refusé ou périmé
├── cerveau/               entreprise.json, offres.md, fiscal.md
├── modeles/               gabarits de livrables
└── logs/                  traces locales

<HERMES_HOME>/skills/<prefixe>/
├── <prefixe>-ceo/SKILL.md
├── <prefixe>-bureau/SKILL.md
├── <prefixe>-voix/SKILL.md
└── <prefixe>-<3e>/SKILL.md

<HERMES_HOME>/scripts/<prefixe>-a-valider.sh     rappel silencieux
```

Le cerveau est écrit **vide de faits** : trois fichiers structurés avec leurs
sources à remplir. L'installateur ne recopie jamais un SIRET, un tarif ou une
mention : ces valeurs viennent du lot 1 d'`equipe-entrepreneur` ou des documents
de l'entrepreneur.

## 4. Recette — six contrôles

À exécuter après installation, dans cet ordre. Un seul échec = installation
incomplète, ne pas annoncer « c'est prêt ».

| # | Contrôle | Commande / geste | Attendu |
|---|---|---|---|
| 1 | Les 4 skills sont lisibles | `ls <HERMES_HOME>/skills/<prefixe>/*/SKILL.md \| wc -l` | `4` |
| 2 | Les noms sont substitués | `grep -c "{{" <HERMES_HOME>/skills/<prefixe>/*/SKILL.md` | `0` partout |
| 3 | Le rappel est muet à vide | `bash <HERMES_HOME>/scripts/<prefixe>-a-valider.sh` | **aucune sortie** |
| 4 | Il parle quand il y a un fichier | poser un `.md` dans `a-valider/`, relancer | une ligne, avec le nom du fichier |
| 5 | Le skill se charge dans une session | « charge `<prefixe>-ceo` » | la session répond avec la règle de dispatch |
| 6 | Le verrou tient | mission 🟡 de test | le livrable est dans `a-valider/`, l'agent s'arrête |

Contrôle 5 en ligne de commande si besoin :

```bash
hermes -z "charge <prefixe>-ceo et donne-moi la règle de dispatch en 3 lignes"
```

## 5. Après la pose

1. Créer les rappels : `bash <racine>/crons-a-creer.sh` (ou `--with-crons`).
2. Vérifier : `hermes cron list` — un job par rappel, nom explicite.
3. Démarrer une **vraie** mission 🟡 courte, et laisser l'entrepreneur déplacer
   lui-même le fichier. C'est la seule preuve que le circuit est compris.
4. Consigner dans `<racine>/livres/` ce qui a coincé au premier passage : c'est
   le meilleur retour pour ajuster les fiches.

## 6. Désinstallation

L'installateur ne supprime rien : il n'a pas à décider ce qui est à l'utilisateur.

```bash
rm -rf "<HERMES_HOME>/skills/<prefixe>"          # les 4 skills
rm -f  "<HERMES_HOME>/scripts/<prefixe>-a-valider.sh"
hermes cron remove <id>                          # un par rappel (hermes cron list)
# le dossier <racine> reste : il contient le travail de l'entrepreneur
```

Le dossier `a-valider/`, `livres/` et `archives/` n'est **jamais** supprimé par
un script : il peut contenir des factures.
