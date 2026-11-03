# Inventaire — ce qui existe déjà (toujours en premier)

On ne construit pas une équipe dans le vide. Avant toute question sur l'activité,
on demande **ce qui tourne déjà** : profils Hermes, agents, personnes, outils,
prestataires. Un poste créé en doublon d'un existant ne sera jamais utilisé — et
il coûtera une fiche à tenir.

**Cet inventaire se refait à chaque entretien**, pas seulement au premier. Trois
mois plus tard, un profil est apparu, un poste a fusionné, une prestataire a été
recrutée. Un diagnostic posé sur un inventaire périmé produit des doublons.

## Les quatre questions

### 1. Quels agents / profils Hermes existent déjà ?

```bash
hermes profile list 2>/dev/null || ls ~/.hermes/profiles
ls ~/.hermes/skills | head -40
hermes cron list
```

À noter : le nom du profil, son périmètre réel, ce qu'il fait bien, ce qu'il ne
fait pas. Ne pas se contenter de la liste : demander « à quoi il te sert
vraiment ».

### 2. Qui travaille déjà avec toi, humainement ?

- conjoint, associé, salarié, apprenti ;
- comptable, expert-comptable, avocat ;
- graphiste, photographe, imprimeur ;
- prestataire qui tient les réseaux, le site, la boutique.

Pour chacun : **ce qu'il fait**, ce qu'il ne fait pas, et à quel rythme.

### 3. Quels outils produisent déjà du travail ?

Boutique en ligne, caisse, banque, logiciel de compta, outil de facturation,
boîte mail, réseaux, fichiers partagés, CRM, tableur. On note **où vit la
donnée**, jamais un mot de passe.

### 4. Qu'est-ce qui marche déjà, et qu'est-ce qui ne marche pas ?

C'est la question la plus utile de l'inventaire. Un agent qui rate systématiquement
quelque chose indique un besoin réel ; un agent que personne n'ouvre n'indique
rien du tout — il sera remplacé, pas dupliqué.

## Le constat d'inventaire

Trois lignes, écrites avec la personne :

```
Ce qui est couvert     : <ce qui se fait déjà, par qui>
Ce qui est mal couvert : <ce qui se fait, mais mal ou en retard>
Ce qui n'est pas fait  : <ce que personne ne fait, et qui coûte>
```

**Seule la troisième colonne produit des postes.** La deuxième produit d'abord
une correction de l'existant ; créer un poste pour masquer un dysfonctionnement
connu ne fait que déplacer le problème.

## Ce que l'inventaire décide

| Constat | Conséquence sur l'équipe |
|---|---|
| un domaine déjà tenu par un profil Hermes qui fonctionne | aucun poste créé, il est cité comme « déjà couvert » |
| un domaine tenu par un humain, mais saturé | un poste qui prépare le travail de cet humain, sans le remplacer |
| un domaine tenu, mais mal | d'abord un correctif ; un poste seulement si le problème est le temps |
| un domaine que personne ne touche | candidat à un poste — s'il y a un livrable nommé |
| un outil qui fait déjà le travail (compta externalisée) | aucun poste ; le poste se limite à préparer les pièces |

## Le piège à éviter

Créer un poste « Direction » ou « Stratégie » parce que l'inventaire est vide.
Un poste sans livrable nommé ne se crée pas, même quand le domaine paraît
important. « Réfléchir à la stratégie » n'est pas un livrable : c'est le travail
de la personne elle-même.

## Exemple d'inventaire réel (fictif)

```
Ce qui est couvert     : site et boutique (profil devops), comptabilité (experte-comptable)
Ce qui est mal couvert : factures (irrégulières), fiches produit (vides)
Ce qui n'est pas fait  : relances d'impayés, newsletter, prospection
```

→ trois postes : Bureau (factures + relances), Voix (fiches + newsletter),
Acquisition. Pas quatre : la logistique n'existe pas, il expédie 3 colis par mois.
