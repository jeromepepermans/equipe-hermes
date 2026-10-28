# Le verrou — trois niveaux, un circuit, une signature

## Les niveaux

| Niveau | Ce qui peut se passer | Exemples |
|---|---|---|
| 🟢 **libre** | rien ne sort de la machine, aucun accord nécessaire | recherche, lecture, calcul, brouillon interne, rangement |
| 🟡 **validation avant sortie** | le livrable est écrit dans `a-valider/`, l'agent **s'arrête** | email, publication, annonce, réponse client, message de prospection |
| 🔴 **signature explicite** | le livrable reste dans `a-valider/` et l'agent rappelle la conséquence exacte | facture définitive, devis engageant, paiement, déclaration fiscale |

Le niveau ne dépend pas du ton du message. « Vas-y, envoie » sur un email 🟡
autorise l'envoi **de ce message précis**, une fois. Sur une facture 🔴, il
n'autorise rien : la signature est le déplacement du fichier.

## Le circuit

```
<racine>/a-valider/   <- l'agent dépose, puis s'arrête
<racine>/livres/      <- l'entrepreneur a validé (il déplace lui-même)
<racine>/archives/    <- refusé, périmé, remplacé
```

**Aucun agent ne déplace un fichier de `a-valider/` vers `livres/`.** Jamais,
même sur instruction orale, même si le fichier est trivial, même pour « ranger ».

Ce déplacement est la seule preuve technique qu'une validation humaine a eu
lieu. Un agent qui le fait supprime la seule trace fiable du dispositif — et le
jour où une facture mal numérotée part, plus personne ne peut dire qui l'a
validée.

Corollaire : **ne jamais vider `a-valider/`**. Un livrable refusé va dans
`archives/`, avec la raison en tête de fichier.

## Ce que l'agent rappelle au niveau 🔴

Le rappel n'est pas une formalité, c'est le contenu de la décision :

- **facture** : le numéro qui sera consommé (une facture annulée ne rend pas son
  numéro), la date d'échéance, le montant, et si la TVA s'applique ;
- **devis** : la durée de validité et ce qui devient engageant ;
- **paiement** : le montant exact et le destinataire ;
- **déclaration** : la période couverte et la date limite légale.

Si l'agent ne peut pas énoncer ces éléments, il ne dépose pas le livrable : il
pose la question. Un 🔴 déposé sans sa conséquence est un piège pour
l'entrepreneur.

## Cas limites, tranchés

| Cas | Niveau | Raison |
|---|---|---|
| Brouillon de facture à relire | 🟡 | rien n'est numéroté tant que l'entrepreneur n'a pas déplacé |
| Facture définitive | 🔴 | numéro consommé, obligation légale |
| Newsletter prête | 🟡 | sort publique, réversible (on peut ne pas envoyer) |
| Message de prospection | 🟡 | engage l'image, pas l'entreprise |
| Réponse à un avis client | 🟢 ou 🟡 selon l'entrepreneur | jamais 🔴 |
| Tarif communiqué à un prospect | 🟡 | devient une promesse commerciale |
| Suppression d'un fichier de `livres/` | 🔴 | perte d'une pièce validée |
| Modification du cerveau | 🟡 | change toutes les productions suivantes |

**Si l'activité n'a aucune obligation engageante**, le niveau 🔴 est déclaré au
paramétrage et laissé vide. Il n'est jamais supprimé : c'est la place de ce qui
engage, et ça arrive vite — une facture au premier client professionnel, un
devis qui devient un engagement. Un dispositif à deux niveaux n'a pas de place
le jour où il en faut trois.

## Le verrou ne se délègue pas

Un chef ne peut pas autoriser un autre chef à sortir un livrable. Seul
l'entrepreneur valide, et sa validation est un **déplacement de fichier**, pas
un message. Un « ok » dans une conversation autorise l'agent à *poursuivre*,
pas à *faire sortir* : le livrable attend toujours dans `a-valider/`.

## Pourquoi c'est la partie non négociable

Un dispositif sans verrou produit du plausible à 9 h du matin : une facture mal
numérotée, un email de prospection parti à un client fâché, un tarif annoncé
trop bas. Aucun de ces trois dégâts ne se répare après coup, et aucun ne vient
d'un agent paresseux : ils viennent tous d'un dispositif qui a laissé une action
irréversible se produire sans témoin.

Le verrou coûte une seconde par livrable. C'est le meilleur rapport de tout le
dispositif.
