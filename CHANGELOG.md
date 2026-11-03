# Journal des versions

## 2.0.0 — 2026-10-29

**Le nombre de postes devient un résultat, et l'installation attend une
validation.**

- Fusion d'`equipe-entrepreneur` (entretien) dans ce dépôt : un seul skill va de
  l'inventaire à l'installation.
- **Inventaire obligatoire et rejoué à chaque entretien** : `postes` n'est créé
  que pour ce que personne ne fait déjà (`references/01-inventaire.md`).
- **`postes` devient une liste de taille libre** (1, 2, 4, 6…). Plus de clés
  fixes `bureau` / `voix` / `troisieme`.
- **Règle unique** : un poste existe s'il porte une tâche récurrente avec un
  livrable nommé. Aucun plafond.
- **Chaque poste doit porter un `pourquoi`** : la tâche récurrente qu'il couvre.
  Un poste sans justification, sans livrable ou au slug en double est refusé à la
  lecture de la configuration.
- **Récapitulatif obligatoire + verrou de validation** : `--recapitulatif`,
  `--valider "<nom>"`, puis installation. Sans validation, sortie 3 et aucune
  écriture ; si le nombre de postes change après validation, l'installation
  refuse à nouveau.
- **Huit modèles de postes** (bureau, voix, acquisition, partenaires,
  fidelisation, production, logistique, sav) ou `libre`. Ce sont des points de
  départ, pas des cases à cocher.
- Entretien enrichi : **rôle** (entrepreneur, dirigeant, salarié, association),
  **activités multiples**, et le rôle qui décide du niveau 🔴.
- Le skill de direction s'appelle `<prefixe>-direction` (et non plus `-ceo`).
- `references/` réorganisé en dix documents ; `01-parametrage.md`,
  `02-installation.md`, `03-postes.md`, `04-verrou.md`, `05-crons.md`,
  `06-autre-instance.md`, `07-exemple.md` remplacés.
- Tests étendus : nombre de postes variable, verrou de validation, validation
  périmée, poste sans livrable, slug en double, récapitulatif.

### Décisions de conception

| Point | Décision | Raison |
|---|---|---|
| Nombre de postes | déduit du diagnostic, aucun plafond | un dispositif à 1 poste est valide ; le danger est le poste sans livrable, pas le nombre |
| Inventaire | toujours en premier, rejoué à chaque entretien | un poste en doublon ne sera jamais chargé, et personne ne s'en aperçoit |
| Validation | technique, pas procédurale | une règle de politesse se contourne en trois semaines |
| Validation périmée | refusée | une validation qui ne correspond plus au contenu ne vaut rien |
| Modèles de postes | bibliothèque de départs, pas de rôles imposés | un gabarit n'est pas un diagnostic |
| Un profil, pas un par poste | les postes sont des skills | trois profils = trois mémoires pour des postes sans outil propre |
| `description` des skills | ≤ 60 caractères | une description trop longue empêche l'enregistrement du skill |
| Crons | générés, création explicite | `--deliver origin` n'a pas de sens sur un job créé en terminal |
| Exemples | fictifs | le dépôt est public |

## 1.0.0 — 2026-10-28

Première version publiable.

- Skill `equipe-hermes` : procédure en quatre étapes (audit de la cible,
  paramétrage, installation, recette).
- `scripts/installer.py` : installateur idempotent, non destructif, `--dry-run`,
  `--force` avec sauvegarde, `--profile`, `--with-crons`. Python 3.9+,
  bibliothèque standard uniquement.
- Quatre skills générés : CEO, Bureau, Voix, troisième poste
  (`Acquisition` / `Partenaires` / `Fidélisation`) — **nombre fixe, remplacé en
  2.0.0**.
- Dossier de travail complet : `a-valider/`, `livres/`, `archives/`, `cerveau/`,
  `modeles/`, `logs/`, README du circuit, `config.json`, `crons-a-creer.sh`.
- Rappel du verrou en `--no-agent`, muet quand `a-valider/` est vide.
- Huit tests réels, sans mock, sur un `HOME` temporaire.
