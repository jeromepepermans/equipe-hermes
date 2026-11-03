# 5. Le récapitulatif — et le verrou de validation

## Pourquoi un récapitulatif, et pas directement l'installation

Un organigramme proposé puis installé dans la même respiration n'est jamais
discuté. La personne découvre son équipe en même temps que ses skills, corrige
après coup, et l'écart entre ce qu'elle voulait et ce qui existe se paie en
fiches périmées.

Le récapitulatif est le seul moment où l'équipe se discute **à froid** : ce qui
est créé, pourquoi, ce qui ne l'est pas, et ce qui a été écarté.

## Le format

`organigramme.md` est écrit à la racine du dossier de travail. Il est **dérivé**
de `equipe.json` : il se régénère, il ne s'édite jamais à la main.

Il contient six sections :

1. **Ce qui existait déjà** — l'inventaire, avec sa date, et la ligne « déjà
   couvert, donc non recréé ».
2. **L'équipe proposée** — un tableau : numéro, libellé, nom, *pourquoi il
   existe*, livrable principal, niveau.
3. **Le détail par poste** — périmètre, livrables, ce qu'il ne fait jamais,
   niveau maximum.
4. **Ce que l'équipe ne couvre pas** — le cœur de métier, la décision, la
   conformité.
5. **Écarté, et pourquoi** — un poste envisagé puis refusé, avec sa raison. Cette
   section évite de rediscuter la même idée trois fois.
6. **La validation** — l'état, et la commande exacte pour valider.

## Le verrou technique

```bash
# 1. écrire le récapitulatif, sans rien installer
python3 scripts/installer.py --config equipe.json --recapitulatif

# 2. le montrer, le discuter, puis valider
python3 scripts/installer.py --config equipe.json --valider "Camille Roux"

# 3. installer — refuse si l'étape 2 n'a pas eu lieu
python3 scripts/installer.py --config equipe.json
```

Trois garanties, vérifiées par les tests :

| Garantie | Comment |
|---|---|
| pas d'installation sans validation | `validation.valide` doit être `true` avec nom et date ; sinon code de sortie 3 et **aucune écriture** |
| pas de validation périmée | si le nombre de postes a changé depuis la validation, l'installation refuse et demande de revalider |
| pas de triche silencieuse | `--force` n'ignore pas le verrou ; seul `--valider` le lève |

La validation s'écrit aussi dans la configuration (`par`, `le`, `postes_valides`)
et dans le récapitulatif : la personne voit son nom sur le document qu'elle a
approuvé.

## Ce qu'on montre, dans cet ordre

1. **D'abord « ce qui existait déjà ».** C'est ce qui prouve que l'équipe ne
   recrée pas ce qui marche.
2. **La liste des postes, avec le « pourquoi ».** Pas le détail technique.
3. **Ce qui est écarté, et pourquoi.** C'est la section qui fait naître les
   objections utiles.
4. **Ce qui n'est pas couvert.** Pour que personne n'attende d'un agent qu'il
   fabrique, répare ou signe.
5. Le détail par poste, seulement si la personne le demande.

## Comment conduire la discussion

| Ce que dit la personne | Ce qui change |
|---|---|
| « ça, je ne le déléguerai jamais » | la ligne sort de la fiche et va dans « ce qui n'est pas couvert » |
| « ça ne me prend pas de temps » | le poste correspondant est retiré ou fusionné |
| « il manque quelqu'un pour X » | X passe le test du diagnostic ; s'il a un livrable récurrent, il devient un poste |
| « pourquoi pas un poste pour Y ? » | la réponse est dans « écarté, et pourquoi » ; sinon on l'ajoute après diagnostic |
| « je veux deux personnes sur le même sujet » | refuser : deux postes sur un livrable se neutralisent |

Après une modification, on **régénère le récapitulatif** et on le revalide. Une
validation qui ne correspond plus au contenu ne vaut rien — c'est exactement ce
que le contrôle `postes_valides` empêche.

## Les erreurs classiques

- **Valider en disant « oui oui » sans lire.** Le récapitulatif existe pour être
  lu : il tient sur deux écrans et il est daté.
- **Valider puis changer la config à la main.** L'installation refusera : le
  nombre de postes ne correspondra plus à la validation. C'est voulu.
- **Sauter le récapitulatif parce que « c'est évident ».** C'est précisément le
  cas où l'inventaire avait été oublié.
- **Faire valider par une autre personne que l'intéressée.** Le nom porté dans la
  validation est celui qui engage.
