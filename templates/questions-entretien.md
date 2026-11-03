# L'entretien — six blocs, après l'inventaire

> L'inventaire (`questions-inventaire.md`) se fait **avant**. Sans lui, on
> propose des postes qui font déjà le travail ailleurs.

## Comment poser les questions

- **Par blocs, pas en formulaire.** Un bloc à la fois, en annonçant combien il en
  reste.
- **Une question = une conséquence.** Si aucune décision de l'équipe n'en dépend,
  la question ne se pose pas.
- **Ne jamais corriger la réponse en la notant.** Un chiffre approximatif se note
  « (approx.) » : c'est un fait utile, il indique où l'agent devra demander.
- **« Je ne sais pas » est une réponse valide.** Elle va dans
  `questions-ouvertes.md` et devient une tâche.
- **Tutoiement ou vouvoiement** : demandé au tout début, tenu pour tout le
  dispositif.

---

## Bloc A — Qui est la personne (4 questions)

Le rôle change ce qui est engageant, donc ce qui passe par le verrou.

1. **Quel est ton rôle exactement ?** entrepreneur / indépendant / micro-entrepreneur
   / dirigeant de société / salarié qui veut déléguer / association / autre.
   *Ce que ça décide :* un salarié ne signe pas au nom de l'entreprise ; un
   dirigeant engage la société ; un indépendant engage sa personne.
2. **Sous quelle forme juridique exerces-tu, et depuis quand ?**
   *Ce que ça décide :* mentions obligatoires, mode de signature, niveau 🔴.
3. **As-tu plusieurs activités ?** Les lister, même celles qui ne sont pas
   déclarées ensemble.
   *Ce que ça décide :* une équipe peut devoir couvrir deux métiers — ou une
   seule des deux, si l'autre est déjà tenue.
4. **Comment veux-tu que l'équipe t'appelle, et on se tutoie ?**

## Bloc B — Ce qui se vend réellement (4 questions)

C'est le bloc où l'écart entre l'administratif et le réel apparaît. Toutes les
fiches en dépendent.

5. **Qu'est-ce que tu vends exactement, à qui, à quel prix constaté ?**
6. **Comment une vente se passe-t-elle, du premier contact au paiement ?**
7. **Quelle est ton activité déclarée** (libellé et code NAF) ? Noter tel quel.
8. **Le contrôle de cohérence, posé une seule fois** : « ton Kbis dit X, tu me
   décris Y — écart, ou activité exercée sous une autre casquette ? »
   Trois garde-fous : posée une fois, jamais relancée ; la réponse ne va **jamais**
   dans un fichier versionné ; formulée à partir de la pièce, pas de la personne.

## Bloc C — L'argent (5 questions)

9. **Ordre de grandeur du chiffre d'affaires des 12 derniers mois** (moins de
   10 k€ / 10-50 k€ / plus de 50 k€), et **part vente / part service**.
   *Ordres de grandeur, jamais un montant exact de mémoire : les montants exacts
   viennent des documents.*
10. **Panier moyen**, et **part du plus gros client** dans le CA.
11. **Saisonnalité ?** (marchés, fêtes, rentrée, saison touristique)
12. **Comment encaisses-tu, et qui gère les impayés aujourd'hui ?**
13. **Plus gros poste de dépense, et justificatifs rangés quelque part ?**

## Bloc D — Le temps (4 questions) — le bloc qui produit les postes

14. **Les cinq tâches qui te prennent le plus de temps** dans une semaine
    ordinaire. Les lister sans hiérarchiser.
15. **Lesquelles détestes-tu** au point de les repousser ?
16. **Lesquelles ne fais-tu jamais** alors que tu sais qu'elles comptent ?
17. **Si tu avais quelqu'un deux heures par semaine, tu lui donnerais quoi ?**
    C'est la question qui vaut toutes les autres.

## Bloc E — Les outils et les accès (3 questions)

18. **Où vit ton activité ?** (boutique, caisse, banque, compta, mail, réseaux,
    fichiers partagés)
19. **Quels accès existent, et lesquels sont partagés ?** Jamais un mot de passe :
    seulement la liste des outils.
20. **Où sont les fichiers que tu produis**, et dans quel format ?

**Lecture seule tant que le cerveau n'est pas validé.** L'écriture n'arrive
qu'ensuite, et seulement par les scripts d'un poste nommé.

## Bloc F — Les papiers (liste, pas question)

Demander les pièces en disant à quoi chacune sert. Un document manquant n'est
jamais un blocage : il devient une ligne dans `questions-ouvertes.md`.

| Pièce | À quoi elle sert | Si absente |
|---|---|---|
| Kbis ou avis SIRENE | identité de facturation, activité déclarée, NAF | interroger `recherche-entreprises.api.gouv.fr` avec le SIREN |
| Récapitulatif de déclaration sociale | régime, périodicité, taux réellement appliqués | demander la périodicité, marquer les taux « à confirmer » |
| 5 à 10 dernières factures | numérotation, mentions, désignation, prix | sans exemple, le poste Bureau ne produit rien |
| Export de CA (caisse, boutique, tableur) | clivage vente/service, saisonnalité, panier | reconstituer depuis les factures, marquer « partiel » |
| Devis / conditions de vente | délais, validité, pénalités | proposer un gabarit, à valider |
| Contrat avec un client récurrent | distinguer un client d'une structure liée | demander, c'est une confusion fréquente |

**Aucun document n'est recopié tel quel** : on en extrait des champs, avec la
source (`references/03-documents.md`).

## Ce que l'entretien ne demande jamais

- Un mot de passe, une clé, un IBAN, un numéro de carte.
- Le détail d'un compte bancaire.
- Des données personnelles de clients.
- Un avis juridique ou fiscal.

## À la fin de l'entretien

On ne propose **pas** encore l'équipe. On passe au diagnostic
(`references/04-diagnostic.md`), qui confronte les réponses du bloc D à
l'inventaire — puis on présente le récapitulatif (`references/05-organigramme.md`).
