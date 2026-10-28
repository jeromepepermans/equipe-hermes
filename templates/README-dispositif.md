# {{ENTREPRISE}} — dispositif de travail

Un CEO, trois départements, un verrou de validation. Installé le {{DATE}} pour
{{ENTREPRENEUR}}.

## Le circuit

1. Un chef produit un livrable et le dépose dans `a-valider/`.
2. **{{ENTREPRENEUR}} le relit et le déplace lui-même dans `livres/`.**
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

## Les trois postes

| Département | Chef | Skill |
|---|---|---|
| 📋 Bureau | **{{BUREAU_NOM}}** | `{{PREFIXE}}-bureau` |
| 📣 Voix | **{{VOIX_NOM}}** | `{{PREFIXE}}-voix` |
| 🎯 {{TROISIEME_LIBELLE}} | **{{TROISIEME_NOM}}** | `{{PREFIXE}}-{{TROISIEME_SLUG}}` |

Le découpage et les règles sont dans le skill `{{PREFIXE}}-ceo`.

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

- Il ne connaît pas ton cœur de métier : {{ACTIVITE}} reste ton travail.
- Il n'envoie rien sans ton déplacement de fichier.
- Il ne garantit aucune conformité juridique ou fiscale.
