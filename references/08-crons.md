# 8. Les rappels — silencieux, sans LLM, vérifiables

## Le principe

Un rappel est un `ls` formaté, pas un tour de langage. Trois conséquences :

1. **`--no-agent`** : aucun modèle appelé. Coût nul, latence nulle, aucune
   possibilité d'inventer un fichier qui n'existe pas.
2. **Sortie vide = silence.** Dossier vide → rien n'est envoyé. Un rappel qui
   notifie « rien à valider » est ignoré au bout de trois jours, et le vrai jour
   passe inaperçu.
3. **Vérifiable à la main.** On peut lancer le script soi-même, sans le
   planificateur, et comparer.

## Le script

`scripts/a-valider.sh` est installé sous
`<HERMES_HOME>/scripts/<prefixe>-a-valider.sh`, racine substituée.

```bash
RACINE="${1:-__RACINE__}"
[ -d "$RACINE/a-valider" ] || exit 0
n=0
for f in "$RACINE"/a-valider/*; do [ -e "$f" ] || continue; n=$((n+1)); done
[ "$n" -eq 0 ] && exit 0
echo "À valider ($n) — $RACINE/a-valider"
ls -1t "$RACINE/a-valider" | head -10 | sed 's/^/  · /'
```

Points de conception : sortie vide si le dossier est vide ou absent, plafond à
10 lignes, tri du plus récent, aucun `cd`.

## Création du cron

```bash
hermes cron create "0 8,18 * * *" \
  --name "<prefixe> — éléments à valider" \
  --script "<prefixe>-a-valider.sh" \
  --no-agent \
  --deliver origin
```

Vérifications :

```bash
hermes cron status                                      # planificateur vivant
hermes cron list                                        # job présent, enabled
bash "<HERMES_HOME>/scripts/<prefixe>-a-valider.sh"     # muet si vide
```

## `--deliver` : le point qui casse en silence

`--deliver origin` suppose une origine (la conversation d'où le job a été créé).
Créé depuis un terminal, il n'y a pas d'origine : le job tourne et ne livre
nulle part.

| Situation | `--deliver` |
|---|---|
| job créé depuis une session existante (Telegram, desktop) | `origin` |
| job créé en ligne de commande, notification Telegram | `telegram` |
| job créé en ligne de commande, aucune notification | `local` |

Vérifier après création : `hermes cron runs <id>` doit montrer une exécution `ok`
sans `last_delivery_error`.

## Rappels fiscaux — prudence

Créés **seulement** si le régime les impose, et seulement après lecture d'un
papier (`03-documents.md`). Ils rappellent une échéance ; ils ne calculent rien.

| Rappel | Quand | Contenu |
|---|---|---|
| URSSAF | le jour déclaré (souvent le 26) | période, date limite, « à faire sur le site » |
| France Travail | le 2 et le 10 si concerné | actualisation avant le 15 |

Ces deux-là sont des jobs **avec agent** (ils rédigent un rappel lisible à partir
du régime). Ils restent désactivés par défaut : une alerte qui tombe à côté
détrône les autres.

## Ce qu'un rappel ne fait jamais

- Déplacer un fichier de `a-valider/` vers `livres/`.
- Envoyer un email au nom de la personne.
- Résumer le contenu des livrables (il liste des noms de fichiers).
- Répéter la même alerte dans la même journée.

## Budget

Trois jobs `--no-agent` deux fois par jour = zéro appel de modèle. Le coût réel
d'un dispositif vient des missions, pas des rappels : ne pas économiser sur les
rappels, ne pas en ajouter non plus.
