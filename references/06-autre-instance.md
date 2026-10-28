# Porter le dispositif sur une autre instance

Un dispositif n'est pas un dossier qu'on copie : c'est **quatre skills, un
fichier de paramétrage et des rappels**. Ce qui voyage et ce qui ne voyage pas
n'est pas symétrique — c'est la source des moitiés d'installation.

## Ce qui voyage

| Élément | Comment |
|---|---|
| `equipe.json` | le paramétrage, à la main (il contient des noms, pas de secret) |
| Les quatre skills | régénérés par l'installateur, jamais copiés à la main |
| Les gabarits du cerveau | régénérés vides, puis remplis avec les vrais faits |
| `scripts/a-valider.sh` | régénéré avec la racine de la cible |
| Les specs de rappels | recréées (les identifiants de cron diffèrent) |

## Ce qui ne voyage pas

| Élément | Pourquoi |
|---|---|
| Le contenu de `cerveau/` | il contient des faits d'entreprise, parfois des données personnelles |
| `livres/` et `a-valider/` | ce sont des documents de travail, souvent sensibles |
| Les identifiants de cron | propres à l'instance (`hermes cron list` les donne) |
| Les sessions Hermes | elles ne sont pas des données du dispositif |
| La mémoire et les profils | chaque instance a les siens, et c'est voulu |
| `.env`, clés, jetons | jamais, sous aucun prétexte |

Conséquence : **une migration n'est jamais un `rsync`.** On transporte le
paramétrage, on régénère le reste, on re-remplit le cerveau depuis les
documents de l'entrepreneur.

## Trois cas concrets

### 1. Même machine, deuxième dispositif

Préfixe différent obligatoire, sinon les skills s'écrasent.

```bash
python3 scripts/installer.py --config equipe-atelier.json   # prefixe: "atelier"
```

Deux dispositifs = deux dossiers, deux jeux de skills, deux rappels.
L'entrepreneur ne mélange pas les deux : un dossier = une activité.

### 2. Autre machine, même entrepreneur

```bash
# sur la cible
git clone https://github.com/jeromepepermans/equipe-hermes
cp -r equipe-hermes ~/.hermes/skills/equipe-hermes
python3 ~/.hermes/skills/equipe-hermes/scripts/installer.py --config equipe.json --dry-run
```

Adapter `racine` au système de fichiers de la cible (`~/equipe` convient aux
deux, mais pas `C:\`), puis relancer sans `--dry-run`.

### 3. Autre entrepreneur

C'est un nouveau paramétrage, pas une copie : noms, activité, troisième poste,
verrou peuvent tous changer. On repart du questionnaire
(`references/01-parametrage.md`) et on ne réutilise **que** la structure.

## Différences entre instances à vérifier avant de promettre

| Point | Où le voir | Effet si négligé |
|---|---|---|
| version d'Hermes | `hermes --version` | options de `cron create` différentes |
| profil actif | `echo $HERMES_HOME` | skills installés dans le mauvais dossier |
| planificateur | `hermes cron status` | crons créés, jamais exécutés |
| kanban | `hermes kanban assignees` | cartes en `ready` sans worker |
| canal de notification | `hermes gateway status` | rappels muets |
| fuseau horaire | `date` | rappels à 3 h du matin |

Sur une instance fraîchement installée, le cas le plus fréquent n'est pas un
skill manquant : c'est un **planificateur arrêté** et un **canal non configuré**.
Les deux se voient en une commande, et les deux rendent le verrou inopérant.

## Le dossier de travail peut vivre ailleurs

Rien n'oblige `<racine>` à être sous le `HOME` de l'utilisateur Hermes — un
dossier synchronisé (Nextcloud, iCloud, drive monté) fonctionne, à condition
que :

- le chemin soit **stable** (pas de chemin monté qui change de nom) ;
- l'agent y ait accès en écriture ;
- il ne soit pas dans un dossier synchronisé **et** chiffré côté client, où le
  script de rappel ne verrait rien.

Un dossier synchronisé est même souhaitable : `livres/` contient des pièces
comptables que l'entrepreneur doit pouvoir ouvrir depuis son téléphone.

## Après la migration — la seule preuve qui compte

Une mission 🟡 réelle, courte, sur la nouvelle instance, qui s'arrête dans
`a-valider/`, puis un déplacement fait **par l'entrepreneur**. Tant que ce
geste n'a pas eu lieu, la migration n'est pas terminée : elle est seulement
écrite.
