# Exemple complet — entièrement fictif

> **Entreprise inventée.** Les noms, montants, adresses et chiffres de ce
> document sont faux et ne doivent jamais être recopiés dans un vrai dossier.
> Il ne sert qu'à montrer la forme d'un paramétrage et d'une installation
> réussie.

## L'entrepreneur (fictif)

Camille Roux, micro-entrepreneure, restauration de meubles anciens, franchise de
TVA, travaille seule, tutoiement. Un client régulier (un hôtel) fait 40 % du
chiffre d'affaires ; le reste vient de particuliers et d'un dépôt-vente.

## Le paramétrage

```json
{
  "version": 1,
  "prefixe": "atelier",
  "profil": "default",
  "racine": "~/atelier-camille",
  "langue": { "code": "fr", "tutoiement": true },
  "entrepreneur": { "nom": "Camille" },
  "entreprise": {
    "nom": "Atelier Roux",
    "statut": "micro-entreprise",
    "tva": "franchise",
    "activite": "restauration de meubles anciens"
  },
  "postes": {
    "bureau": { "nom": "Jeanne" },
    "voix": { "nom": "Léa" },
    "troisieme": { "nom": "Marc", "libelle": "Fidélisation" }
  },
  "verrou": {
    "niveau3_actif": true,
    "rappel": ["08:00", "18:00"],
    "fuseau": "Europe/Paris"
  },
  "crons": {
    "verrou": { "actif": true },
    "urssaf": { "actif": true, "jour": "26" },
    "france_travail": { "actif": false },
    "livraison": "telegram"
  },
  "kanban": { "actif": true, "assignee": "default" }
}
```

Le troisième poste est **Fidélisation** et non Acquisition, parce que l'hôtel
fait 40 % du chiffre d'affaires : le risque est la concentration, pas le manque
de prospects. C'est exactement le raisonnement du bloc D, et il change le
travail du chef — relancer, élargir la gamme vendue à ce client, éviter la
dépendance, au lieu de chercher des inconnus.

## Ce que l'installation produit

```
~/atelier-camille/
├── a-valider/            (vide)
├── livres/               (vide)
├── archives/             (vide)
├── cerveau/
│   ├── entreprise.json   identité de facturation, à remplir
│   ├── offres.md         ce qui se vend, à quel prix, à confirmer
│   └── fiscal.md         régime, échéances, source
├── modeles/
├── logs/
├── README.md
├── config.json
└── crons-a-creer.sh

~/.hermes/skills/atelier/
├── atelier-ceo/SKILL.md
├── atelier-bureau/SKILL.md
├── atelier-voix/SKILL.md
└── atelier-fidelisation/SKILL.md

~/.hermes/scripts/atelier-a-valider.sh
```

## La recette, telle qu'elle a été passée

| # | Contrôle | Résultat |
|---|---|---|
| 1 | 4 skills | `4` |
| 2 | aucun `{{` résiduel | `0` dans les quatre fichiers |
| 3 | rappel sur dossier vide | aucune sortie |
| 4 | rappel avec un fichier | `À valider (1) — …/a-valider` + le nom |
| 5 | chargement du CEO | règle de dispatch rendue en trois lignes |
| 6 | mission 🟡 | livrable dans `a-valider/`, agent arrêté |

## La première mission 🟡

Demande de Camille : « prépare la relance du dépôt-vente, ça fait deux mois ».

Le CEO produit :

```
Mission    : relance du dépôt-vente (2 mois sans nouvelle pièce)
Département: Marc (Fidélisation)
Livrable   : ~/atelier-camille/a-valider/2026-11-04__relance-depot-vente.md
Niveau     : 🟡 validation
Échéance   : pas d'échéance
```

Marc lit `cerveau/offres.md`, constate que le tarif du dépôt-vente n'y est pas
sourcé, écrit « à confirmer » au lieu d'inventer une commission, dépose le
brouillon de message dans `a-valider/` et s'arrête.

Camille corrige la commission, déplace le fichier dans `livres/`. Le lendemain,
elle copie le message dans son courriel elle-même : l'agent n'a jamais eu accès
à sa boîte.

## Ce que cet exemple montre

- Le **troisième poste** se déduit de l'activité, il ne se choisit pas par goût.
- Le **cerveau vide** n'empêche pas de travailler : il oblige à marquer
  « à confirmer » au lieu d'inventer. C'est le comportement attendu.
- Le **verrou 🟡** ne bloque pas la production, il bloque la sortie.
- L'agent n'a **pas** envoyé le message : c'est Camille qui l'a fait, depuis son
  propre outil. Le dispositif n'a jamais eu ses identifiants.

## Ce qu'il ne faut pas imiter

- Recopier ce paramétrage tel quel : le troisième poste serait faux pour une
  autre activité.
- Activer l'alerte URSSAF sans vérifier le régime réel.
- Mettre `"livraison": "telegram"` sans avoir testé que le canal répond.
- Utiliser un vrai nom d'entreprise dans un exemple de dépôt public.
