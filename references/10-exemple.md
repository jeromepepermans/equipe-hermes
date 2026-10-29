# 10. Deux exemples complets — entièrement fictifs

> Noms, montants et situations **inventés**. Ne rien recopier dans un vrai
> dossier. Ces exemples existent pour montrer la **forme** du raisonnement, pas
> un modèle d'équipe à réutiliser.

---

## Exemple A — l'atelier (4 postes)

### 1. Inventaire (avant toute question)

```
Profils Hermes : "boutique" — site, catalogue, paiements. Fonctionne.
Personnes      : Camille (fabrication et vente), experte-comptable (comptes).
Outils         : boutique en ligne, tableur de CA, caisse, boîte mail.
Constat        : ce qui est couvert → site et comptabilité.
                 mal couvert → fiches produit vides, factures irrégulières.
                 jamais fait → relances d'impayés, newsletter, prospection.
```

### 2. Entretien — les réponses qui comptent

- Rôle : **entrepreneuse individuelle**, micro-entreprise, franchise de TVA.
- Activité : restauration de meubles anciens (vente), quelques prestations de
  conseil (service) — part service environ un quart du CA.
- Bloc D : les cinq tâches chronophages sont fabrication, réponses aux clients,
  factures, photos et fiches produit, achats de matières. Ce qu'elle déteste :
  les relances. Ce qu'elle ne fait jamais : la newsletter, la prospection.
  « Deux heures par semaine ? Les factures et les relances. »

### 3. Diagnostic

| Candidat (bloc D) | Verdict | Pourquoi |
|---|---|---|
| fabrication | écarté | cœur de métier |
| factures + relances | **poste 1 — Bureau** | récurrent, livrable (PDF, relance), non couvert |
| photos et fiches produit | **poste 2 — Voix** | récurrent, livrable (fiche), non couvert |
| newsletter | fusionné dans Voix | même livrable (contenu) |
| prospection | **poste 3 — Acquisition** | récurrent, livrable (liste + message), non couvert |
| achats de matières | **poste 4 — Production** | récurrent (hebdomadaire), livrable (liste de réassort) |
| site et paiements | écarté | déjà couvert par le profil `boutique` |
| comptabilité | écarté | déjà couvert par l'experte-comptable |

**4 postes**, pas 3 : l'inventaire en couvrait deux domaines, et le quatrième
poste sort du bloc D (les achats), pas d'un gabarit.

### 4. Récapitulatif (extrait)

```markdown
## 2. L'équipe proposée — 4 postes

| # | Poste | Nom | Pourquoi il existe | Livrable principal | Niveau |
|---|---|---|---|---|---|
| 1 | Bureau | Jeanne | les factures partent en retard, les relances ne sont jamais faites | facture PDF | 🔴 signature |
| 2 | Voix | Léa | les fiches produit sont vides, la newsletter n'existe pas | fiche produit | 🟡 validation |
| 3 | Acquisition | Marc | aucun prospect contacté depuis 8 mois | liste de prospects | 🟡 validation |
| 4 | Production | Sam | les ruptures de matière bloquent l'atelier | liste de réassort | 🟡 validation |

## 5. Écarté, et pourquoi
- un poste Logistique — 3 expéditions par mois, tâche non récurrente
- un poste « Direction » — ne produit aucun livrable

## 6. Validation
Pour valider : python3 scripts/installer.py --config equipe.json --valider "<votre nom>"
```

Camille valide. L'installation écrit **5 skills** (direction + 4 postes).

### 5. Première mission

```
Mission    : préparer les relances des deux factures impayées
Poste      : Jeanne — Bureau
Livrable   : ~/atelier/a-valider/2026-11-05__relance__client-b.md
Niveau     : 🟡 validation
Échéance   : pas d'échéance
```

Jeanne lit `cerveau/offres.md`, constate que le délai de paiement n'y est pas
sourcé, écrit « à confirmer » au lieu d'inventer 30 jours, dépose le brouillon
et s'arrête. Camille corrige, déplace le fichier dans `livres/`, envoie le
message elle-même depuis sa boîte.

---

## Exemple B — le fabricant seul (1 poste)

Même méthode, résultat différent.

### Inventaire

```
Profils Hermes : aucun.
Personnes      : Théo, seul. Sa compagne tient un tableur de caisse.
Outils         : caisse, banque, téléphone, Instagram (rarement).
Constat        : couvert → rien vraiment. mal couvert → caisse (tableur).
                 jamais fait → facture aux professionnels, relances.
```

### Entretien (extrait)

- Rôle : **indépendant**, micro-entreprise, franchise de TVA.
- Activité : vente de pièces en bois tourné, marchés et quelques commandes.
- Bloc D : il aime tout ce qu'il fait sauf… les papiers. « Deux heures par
  semaine ? Les factures et les relances, je ne les fais jamais. »
- Il ne veut pas de newsletter (« je n'ai rien à raconter »), pas de prospection
  (« les marchés me suffisent »).

### Diagnostic

| Candidat | Verdict |
|---|---|
| factures, relances, déclarations | **poste 1 — Bureau** |
| photos et contenu | refusé par la personne, pas de livrable attendu |
| prospection | pas de besoin : les marchés couvrent la demande |
| production | c'est son métier, il le fait |

**1 poste.** C'est un dispositif valide : il règle le seul manque de temps réel.
Lui proposer trois postes aurait produit deux skills jamais chargés — et, à la
première facture ratée, la conclusion « l'équipe ne sert à rien ».

### Ce que ça donne installé

```
~/.hermes/skills/atelier/
├── atelier-direction/SKILL.md
└── atelier-bureau/SKILL.md
```

Le récapitulatif porte explicitement, en section 5 : « poste Voix — écarté :
la personne ne veut pas produire de contenu, aucun livrable attendu » et « poste
Acquisition — écarté : les marchés fournissent la demande ». Ces deux lignes
empêchent de rediscuter la question tous les trois mois.

---

## Ce que les deux exemples démontrent

1. **Le nombre de postes change avec la personne**, pas avec une doctrine : 4
   dans un cas, 1 dans l'autre.
2. **L'inventaire change le résultat** : chez Camille, deux domaines étaient
   déjà tenus — sans inventaire, le diagnostic aurait proposé 6 postes.
3. **Ce qui est écarté est écrit.** C'est ce qui rend le récapitulatif crédible :
   il ne prétend pas tout couvrir.
4. **Le verrou est identique** dans les deux cas, y compris à 1 poste : la
   facture attend dans `a-valider/`, la personne déplace.
