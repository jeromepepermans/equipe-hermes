# equipe-hermes

Un skill Hermes qui **installe et paramètre** un dispositif de travail
« CEO + 3 chefs » sur n'importe quelle instance Hermes : quatre skills, un
dossier de travail, un verrou de validation, des rappels silencieux.

C'est la partie **exécution** d'une idée qui existe déjà en deux morceaux :

| Dépôt | Ce qu'il fait | Quand |
|---|---|---|
| [`equipe-entrepreneur`](https://github.com/jeromepepermans/equipe-entrepreneur) | l'entretien : statut, activité, documents, 3 fiches de poste, cerveau | avant, pour décider |
| **`equipe-hermes`** (ici) | le paramétrage réel : dossiers, skills, verrou, rappels, kanban | après, pour installer |

## Le problème que ça résout

Un dispositif d'agents se rate rarement au moment de l'idée. Il se rate à
l'installation : les skills sont écrits à la main dans un coin, le dossier de
validation n'existe pas, l'agent « envoie » un email qu'il n'aurait jamais dû
envoyer, et deux semaines plus tard plus personne ne sait quel poste a produit
quoi.

Ici, l'installation est **un fichier de paramétrage** et **une commande**. Le
résultat est vérifiable en six contrôles, et rejouable sur une autre machine
sans copier quoi que ce soit à la main.

## Démarrage rapide

```bash
git clone https://github.com/jeromepepermans/equipe-hermes
cp -r equipe-hermes ~/.hermes/skills/equipe-hermes

cp equipe-hermes/templates/config.example.json ./equipe.json
# remplir : entrepreneur, entreprise, trois postes, racine

python3 equipe-hermes/scripts/installer.py --config equipe.json --dry-run
python3 equipe-hermes/scripts/installer.py --config equipe.json
```

Puis, dans une session Hermes :

```
charge equipe-hermes et termine l'installation — voici equipe.json
```

Sortie réelle (exemple fictif) :

```
  Équipe Atelier Roux — installation réelle
  racine      : /home/camille/dispositif
  skills      : /home/camille/.hermes/skills/atelier

  dossier  /home/camille/dispositif/a-valider
  créé     /home/camille/dispositif/README.md
  créé     /home/camille/dispositif/cerveau/entreprise.json
  créé     /home/camille/.hermes/skills/atelier/atelier-ceo/SKILL.md
  créé     /home/camille/.hermes/skills/atelier/atelier-bureau/SKILL.md
  créé     /home/camille/.hermes/skills/atelier/atelier-voix/SKILL.md
  créé     /home/camille/.hermes/skills/atelier/atelier-fidelisation/SKILL.md
  créé     /home/camille/.hermes/scripts/atelier-a-valider.sh
  créé     /home/camille/dispositif/crons-a-creer.sh
```

## Ce que l'installation crée

```
<racine>/
├── README.md              le circuit en cinq lignes
├── config.json            le paramétrage appliqué (sans secret)
├── crons-a-creer.sh       les rappels, prêts à coller
├── a-valider/             l'agent dépose ici, puis s'arrête
├── livres/                validé (déplacement par l'entrepreneur)
├── archives/              refusé ou périmé
├── cerveau/               entreprise.json, offres.md, fiscal.md
├── modeles/  logs/
```

```
<HERMES_HOME>/skills/<prefixe>/
├── <prefixe>-ceo/           dispatch, verrou, format de mission
├── <prefixe>-bureau/        devis, factures, relances, déclarations
├── <prefixe>-voix/          contenu, annonces, réseaux, SEO
└── <prefixe>-<3e>/          acquisition | partenaires | fidélisation
<HERMES_HOME>/scripts/<prefixe>-a-valider.sh
```

## Les trois choses qui rendent le dispositif tenable

1. **Trois postes, pas trente.** Bureau, Voix, et un troisième poste dont le
   libellé dépend de l'activité (Acquisition, Partenaires ou Fidélisation). Les
   spécialistes n'existent pas en permanence : un spécialiste = un skill chargé
   au moment où le chef en a besoin.
2. **Un verrou à trois niveaux.** 🟢 libre, 🟡 validation avant sortie,
   🔴 signature. **Aucun agent ne déplace un fichier de `a-valider/` vers
   `livres/`** : ce déplacement est la signature de l'entrepreneur, et la seule
   preuve technique qu'une validation a eu lieu.
3. **Des rappels muets.** Un cron `--no-agent` liste `a-valider/` deux fois par
   jour et **ne dit rien quand le dossier est vide**. Coût zéro, aucune
   invention possible, rien à ignorer.

## Ce que l'installateur garantit

| Garantie | Comment c'est tenu |
|---|---|
| Idempotent | relancé sans changement, il n'écrit rien et l'affiche |
| Non destructif | un fichier différent n'est pas écrasé sans `--force` |
| `--force` sauvegarde | copie `.bak-<horodatage>` avant chaque écrasement |
| `--dry-run` | plan complet, zéro écriture (vérifié par les tests) |
| Aucun secret | ne lit ni n'écrit de variable sensible, ne crée aucun `.env` |
| Testé | 8 tests réels, sans mock, sur un `HOME` temporaire |

```bash
python3 tests/test_installer.py     # 8 tests, aucun mock
```

## Le dépôt

```
SKILL.md                        le skill (à charger dans Hermes)
references/01-parametrage.md    les 7 blocs de questions → equipe.json
references/02-installation.md   audit de la cible, pose, recette en 6 contrôles
references/03-postes.md         gabarit des fiches, règles de dispatch
references/04-verrou.md         les 3 niveaux, le circuit, les cas limites
references/05-crons.md          rappels silencieux, --no-agent, --deliver
references/06-autre-instance.md ce qui voyage et ce qui ne voyage pas
references/07-exemple.md        exemple complet — entreprise fictive
templates/                      gabarits (config, 2 skills, cerveau, README)
scripts/installer.py            l'installateur
scripts/a-valider.sh            le rappel
tests/test_installer.py         les tests
```

## Ce que ce dépôt n'est pas

- Pas un générateur d'agents à la chaîne : trois postes, et le quatrième exige
  une décision écrite.
- Pas un cabinet comptable ni juridique : il prépare, signale, et renvoie vers
  un professionnel.
- Pas une équipe de développement : c'est `equipes-delegation` et les profils
  techniques qui s'en chargent.
- Pas un endroit où mettre vos données : les exemples sont **fictifs**, et le
  dossier de travail généré n'est jamais versionné.

## Licence

MIT — voir `LICENCE`. Les exemples d'entreprise sont inventés ; n'y mettez
jamais de données réelles.
