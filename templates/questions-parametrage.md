# Questionnaire de paramétrage — à poser par petits groupes

Sept blocs, chacun avec une conséquence visible sur l'installation. On ne pose
pas tout d'un coup. Une réponse incertaine se note `a_confirmer`.

---

**Bloc A — toi**
1. Comment veux-tu que l'équipe t'appelle ?
2. On se tutoie ou on se vouvoie ?
3. Langue de travail ?

**Bloc B — l'entreprise**
4. Nom commercial exact ?
5. Statut (micro, EI, SASU, autre) ?
6. Franchise de TVA, ou assujetti ?
7. En une phrase : que vends-tu réellement ?

**Bloc C — où on installe**
8. Dossier de travail (défaut `~/equipe`) ?
9. Préfixe des skills (défaut `equipe`) ?
10. Profil Hermes hôte (défaut `default`) ?

**Bloc D — les trois postes**
11. Nom du chef Bureau (défaut `Bureau`) ?
12. Nom du chef Voix (défaut `Voix`) ?
13. Le troisième poste : plutôt trouver des clients (**Acquisition**), tenir un
    réseau de distributeurs (**Partenaires**), ou garder ton client principal
    (**Fidélisation**) ?
14. Son nom ?
15. Pour chacun des trois : quelle tâche ne délégueras-tu **jamais** ?

**Bloc E — le verrou**
16. Quels livrables doivent attendre ta validation (🟡) ?
17. Quels livrables engagent (🔴) — facture, devis, paiement, déclaration ?
18. À quelles heures veux-tu le rappel (défaut 8 h et 18 h) ?
19. Fuseau horaire (défaut Europe/Paris) ?

**Bloc F — les rappels**
20. Rappel URSSAF : ton régime impose-t-il une déclaration mensuelle ou
    trimestrielle ? Quel jour ?
21. France Travail : concerné ? Quel jour d'actualisation ?
22. Où livrer les notifications (Telegram, desktop, aucune) ?

**Bloc G — le tableau des tâches**
23. Utiliser le kanban Hermes ?
24. Quel profil assigné (`hermes kanban assignees` pour la liste) ?

---

## Ce qu'on ne demande pas ici

- Un montant exact de mémoire → il vient du cerveau.
- Un numéro d'immatriculation → il vient du Kbis, pas de la mémoire.
- Un mot de passe, un jeton, un IBAN.
- Le nom d'un client final.

## Ce qu'on fait des réponses

Elles remplissent `equipe.json`, puis :

```bash
python3 scripts/installer.py --config equipe.json --dry-run
```

Le plan affiché est la dernière occasion de corriger avant d'écrire.
