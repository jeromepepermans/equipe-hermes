# 9. Porter une équipe sur une autre instance

Une équipe n'est pas un dossier qu'on copie : c'est **un organigramme validé,
N+1 skills, un fichier de configuration et des rappels**. Ce qui voyage et ce qui
ne voyage pas n'est pas symétrique.

## Ce qui voyage

| Élément | Comment |
|---|---|
| `equipe.json` | à la main : il contient des noms et des choix, aucun secret |
| `organigramme.md` | régénéré à partir du même `equipe.json` |
| Les skills | **régénérés** par l'installateur, jamais copiés à la main |
| Le cerveau | régénéré vide, puis rempli avec les vrais faits |
| `a-valider.sh` | régénéré avec la racine de la cible |
| Les specs de rappels | recréées (les identifiants de cron diffèrent) |

## Ce qui ne voyage pas

| Élément | Pourquoi |
|---|---|
| le contenu de `cerveau/` | faits d'entreprise, parfois données personnelles |
| `livres/`, `a-valider/`, `archives/` | documents de travail, souvent sensibles |
| `questions-ouvertes.md` | écarts entre déclaré et réel — reste chez la personne |
| les identifiants de cron | propres à l'instance |
| la mémoire et les profils Hermes | chaque instance a les siens |
| `.env`, clés, jetons | jamais |

**Une migration n'est jamais un `rsync`.** On transporte le paramétrage, on
régénère le reste, on re-remplit le cerveau depuis les papiers.

## Trois cas

### 1. Même machine, deuxième équipe

Préfixe différent obligatoire, sinon les skills s'écrasent.

```bash
python3 scripts/installer.py --config equipe-atelier.json   # prefixe: "atelier"
```

Deux équipes = deux dossiers, deux jeux de skills, deux rappels. Un dossier =
une activité ; l'utilisateur ne mélange pas les deux.

### 2. Autre machine, même personne

```bash
git clone https://github.com/jeromepepermans/equipe-hermes
cp -r equipe-hermes ~/.hermes/skills/equipe-hermes
python3 ~/.hermes/skills/equipe-hermes/scripts/installer.py --config equipe.json --dry-run
```

Adapter `racine` au système de fichiers de la cible, puis relancer sans
`--dry-run`. **Refaire l'inventaire** (`01-inventaire.md`) : la nouvelle machine
a peut-être déjà des profils et des crons qui couvrent des domaines.

### 3. Autre personne

C'est un **nouveau diagnostic**, pas une copie. L'inventaire, le rôle, les
activités, le nombre de postes peuvent tous changer. On ne réutilise que la
structure et les gabarits.

## Vérifier avant de promettre

| Point | Où le voir | Effet si négligé |
|---|---|---|
| version d'Hermes | `hermes --version` | options `cron create` différentes |
| profil actif | `echo $HERMES_HOME` | skills dans le mauvais dossier |
| planificateur | `hermes cron status` | crons créés, jamais exécutés |
| kanban | `hermes kanban assignees` | cartes en `ready` sans worker |
| canal de notification | `hermes gateway status` | rappels muets |
| fuseau horaire | `date` | rappels à 3 h du matin |

Sur une instance fraîche, le cas le plus fréquent n'est pas un skill manquant :
c'est un **planificateur arrêté** et un **canal non configuré**. Les deux rendent
le verrou inopérant.

## Le dossier de travail peut vivre ailleurs

Rien n'oblige la racine à être sous le `HOME` de l'utilisateur Hermes. Un dossier
synchronisé (Nextcloud, drive monté) fonctionne si le chemin est **stable**, si
l'agent y a accès en écriture, et s'il n'est pas chiffré côté client — le script
de rappel ne verrait rien.

Un dossier synchronisé est même souhaitable : `livres/` contient des pièces que
la personne doit pouvoir ouvrir depuis son téléphone.

## Après la migration — la seule preuve

Une mission 🟡 réelle, courte, sur la nouvelle instance, qui s'arrête dans
`a-valider/`, puis un déplacement fait **par la personne**. Tant que ce geste n'a
pas eu lieu, la migration est écrite, pas terminée.
