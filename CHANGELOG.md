# Journal des versions

## 1.0.0 — 2026-10-28

Première version publiable.

- Skill `equipe-hermes` : procédure en quatre étapes (audit de la cible,
  paramétrage, installation, recette).
- `scripts/installer.py` : installateur idempotent, non destructif, `--dry-run`,
  `--force` avec sauvegarde, `--profile`, `--with-crons`. Python 3.9+,
  bibliothèque standard uniquement.
- Quatre skills générés par paramétrage : CEO, Bureau, Voix, troisième poste
  (`Acquisition` / `Partenaires` / `Fidélisation`).
- Dossier de travail complet : `a-valider/`, `livres/`, `archives/`, `cerveau/`,
  `modeles/`, `logs/`, README du circuit, `config.json`, `crons-a-creer.sh`.
- Rappel du verrou en `--no-agent`, muet quand `a-valider/` est vide.
- Sept blocs de paramétrage documentés, avec la raison de chaque question.
- Huit tests réels, sans mock, sur un `HOME` temporaire : structure, idempotence,
  non-destructif puis `--force`, `--dry-run`, rappel muet puis bavard, config
  incomplète, libellé invalide, profil dédié.
- Exemple complet **fictif** de bout en bout.

### Décisions de conception

| Point | Décision | Raison |
|---|---|---|
| Un profil, pas un par chef | les chefs sont des skills | trois profils = trois mémoires et trois dossiers de skills à tenir, pour des postes sans outil propre |
| Assignee kanban | `default`, nom du chef dans le titre | un assignee inexistant laisse la carte en `ready` pour toujours |
| `description` des skills générés | ≤ 60 caractères | une description trop longue empêche l'enregistrement du skill |
| Le cerveau n'est jamais écrasé sans `--force` | il contient les vrais faits | un `--force` réflexe détruirait le travail du lot 1 |
| Crons créés à la main | `crons-a-creer.sh` | `--deliver origin` n'a aucun sens sur un job créé en terminal |
| Exemples fictifs | entreprise inventée | le dépôt est public |
