# 7. Le verrou — trois niveaux, un circuit, une signature

## Les niveaux

| Niveau | Ce qui peut se passer | Exemples |
|---|---|---|
| 🟢 **libre** | rien ne sort, aucun accord nécessaire | recherche, lecture, calcul, brouillon interne, rangement |
| 🟡 **validation avant sortie** | le livrable est écrit dans `a-valider/`, l'agent **s'arrête** | email, publication, annonce, réponse client, prospection |
| 🔴 **signature explicite** | le livrable reste dans `a-valider/` et l'agent rappelle la conséquence | facture définitive, devis engageant, paiement, déclaration |

Le niveau dépend du **rôle** de la personne (bloc A de l'entretien), pas de son
humeur ni du ton du message. Un salarié qui n'engage pas l'entreprise aura
souvent un 🔴 vide ; un dirigeant de société l'aura plein.

« Vas-y, envoie » sur un email 🟡 autorise l'envoi **de ce message précis**, une
fois. Sur une facture 🔴, ça n'autorise rien : la signature est le déplacement du
fichier.

## Le circuit

```
<racine>/a-valider/   <- un poste dépose, puis s'arrête
<racine>/livres/      <- la personne a validé (elle déplace elle-même)
<racine>/archives/    <- refusé, périmé, remplacé
```

**Aucun agent ne déplace un fichier de `a-valider/` vers `livres/`.** Jamais,
même sur instruction orale, même pour « ranger ».

Ce déplacement est la seule preuve technique qu'une validation humaine a eu lieu.
Un agent qui le fait supprime la seule trace fiable du dispositif — et le jour
où une facture mal numérotée part, plus personne ne peut dire qui l'a validée.

Corollaire : **ne jamais vider `a-valider/`**. Un livrable refusé va dans
`archives/`, avec la raison en tête de fichier.

## L'en-tête obligatoire

Tout livrable de `a-valider/` commence par :

```
Niveau      : 🟡 validation | 🔴 signature
Sujet       : <une phrase>
Conséquence : <ce qui devient vrai si je déplace ce fichier>
```

Exemples de conséquence utile :

- `numéro FAC-2026-014 consommé dès émission, aucun retour arrière`
- `engagement de prix valable 30 jours à compter de la date du devis`
- `message publié au nom de la marque, non supprimable après envoi`

Si l'agent ne peut pas écrire la conséquence, le livrable n'est pas prêt.

## Nommage et numérotation

`AAAA-MM-JJ__<type>__<slug>.md` — la date trie, le type filtre, le slug dit de
quoi il s'agit.

Pour les documents engageants : `<TYPE>-AAAA-NNN>`, compteur continu sur l'année
civile. **Avant d'émettre, on liste** :

```bash
ls <dossier>/ | grep -oE 'FAC-[0-9]{4}-[0-9]{3}' | sort | tail -1
```

Le prochain numéro est le dernier + 1. **Si le dossier est vide ou ambigu,
l'agent demande — il ne devine pas.** Un trou de numérotation est plus grave
qu'un retard de facturation.

## Ce que l'agent rappelle au niveau 🔴

- **facture** : le numéro consommé, l'échéance, le montant, et si la TVA s'applique ;
- **devis** : la durée de validité et ce qui devient engageant ;
- **paiement** : le montant exact et le destinataire ;
- **déclaration** : la période et la date limite légale.

S'il ne peut pas énoncer ces éléments, il ne dépose pas le livrable : il pose la
question.

## Cas limites, tranchés

| Cas | Niveau | Raison |
|---|---|---|
| brouillon de facture à relire | 🟡 | rien n'est numéroté avant le déplacement |
| facture définitive | 🔴 | numéro consommé, obligation légale |
| newsletter prête | 🟡 | sort publique, réversible |
| message de prospection | 🟡 | engage l'image, pas l'entreprise |
| réponse à un avis client | 🟢 ou 🟡 | jamais 🔴 |
| tarif communiqué à un prospect | 🟡 | devient une promesse commerciale |
| suppression dans `livres/` | 🔴 | perte d'une pièce validée |
| modification du cerveau | 🟡 | change toutes les productions suivantes |

**Si l'activité n'a aucune obligation engageante**, 🔴 est déclaré et laissé vide.
Il n'est jamais supprimé : une facture au premier client professionnel arrive
vite. Un dispositif à deux niveaux n'a pas de place le jour où il en faut trois.

## Le verrou ne se délègue pas

Un poste ne peut pas autoriser un autre poste à sortir un livrable. Seule la
personne valide, et sa validation est un **déplacement de fichier**, pas un
message.

## Vérification au bout d'une semaine

1. Un fichier est-il apparu dans `livres/` sans avoir été déplacé ?
   → un agent a signé à sa place : défaut grave.
2. La personne a-t-elle envoyé quelque chose alors que le livrable attendait ?
   → le circuit est en double, il faut en choisir un.
3. `a-valider/` est-il vide en permanence ?
   → soit les postes ne produisent rien, soit quelqu'un les a désactivés.
