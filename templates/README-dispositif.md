# {{ENTREPRISE}} — dispositif de travail

{{EFFECTIF_MOT}} et une direction, un verrou de validation. Installé le {{DATE}}
pour {{UTILISATEUR}} ({{ROLE}}).

## Le circuit

1. Un poste produit un livrable et le dépose dans `a-valider/`.
2. **{{UTILISATEUR}} le relit et le déplace lui-même dans `livres/`.**
3. Ce qui est refusé ou périmé va dans `archives/`.

Rien ne sort de la machine sans ce déplacement. Un agent ne déplace jamais un
fichier de `a-valider/` vers `livres/`.

## Les dossiers

| Dossier | Rôle |
|---|---|
| `a-valider/` | produit, en attente de **ta** validation |
| `livres/` | validé (déplacement fait par toi) |
| `archives/` | refusé ou périmé |
| `cerveau/` | les faits stables : identité, offres, fiscal |
| `modeles/` | gabarits de livrables |
| `logs/` | traces locales |
| `organigramme.md` | le récapitulatif validé de l'équipe |

## L'équipe

{{POSTES_TABLE}}

Le découpage et les règles sont dans le skill `{{PREFIXE}}-direction`.
Récapitulatif validé par {{VALIDE_PAR}} le {{VALIDE_LE}} : `organigramme.md`.

## Les niveaux

| Niveau | Ce que ça veut dire |
|---|---|
| 🟢 libre | l'agent travaille, rien ne sort |
| 🟡 validation | le livrable attend dans `a-valider/` |
| 🔴 signature | facture, devis engageant, paiement, déclaration |

## Les rappels

`{{PREFIXE}}-a-valider` liste `a-valider/` deux fois par jour, et se tait quand
le dossier est vide. Voir `crons-a-creer.sh` pour les autres.

## Ce que le dispositif ne fait pas

{{HORS_PERIMETRE}}

- Il n'envoie rien sans ton déplacement de fichier.
- Il ne garantit aucune conformité juridique ou fiscale.
