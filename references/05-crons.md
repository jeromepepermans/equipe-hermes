# Les rappels — silencieux, sans LLM, vérifiables

## Le principe

Un rappel est un `ls` formaté, pas un tour de langage. Trois conséquences :

1. **`--no-agent`** : aucun modèle n'est appelé. Coût nul, latence nulle, aucune
   possibilité d'inventer un fichier qui n'existe pas.
2. **Sortie vide = silence.** Dossier vide → le job n'envoie rien. C'est ce qui
   le rend supportable : un rappel qui notifie « rien à valider » est ignoré au
   bout de trois jours, et le vrai jour passe inaperçu.
3. **Vérifiable à la main.** On peut lancer le script soi-même, sans le
   planificateur, et comparer.

## Le script

`scripts/a-valider.sh` est installé sous
`<HERMES_HOME>/scripts/<prefixe>-a-valider.sh`, avec la racine substituée.

```bash
RACINE="${1:-__RACINE__}"
[ -d "$RACINE/a-valider" ] || exit 0
n=0
for f in "$RACINE"/a-valider/*; do
  [ -e "$f" ] || continue
  n=$((n+1))
done
[ "$n" -eq 0 ] && exit 0
echo "À valider ($n) — $RACINE/a-valider"
ls -1t "$RACINE/a-valider" | head -10 | sed 's/^/  · /'
```

Points de conception :

- `exit 0` sans sortie quand le dossier est vide ou absent ;
- un plafond à 10 lignes : au-delà, l'entrepreneur ne lit plus ;
- tri par date décroissante : le plus récent d'abord ;
- aucun `cd`, aucun chemin relatif : il doit tourner depuis n'importe où.

## Création du cron

L'installateur écrit `<racine>/crons-a-creer.sh` avec les commandes exactes.
Création manuelle du rappel principal :

```bash
hermes cron create "0 8,18 * * *" \
  --name "Rappel — éléments à valider" \
  --script "<prefixe>-a-valider.sh" \
  --no-agent \
  --deliver origin
```

Vérifications :

```bash
hermes cron status          # le planificateur tourne
hermes cron list            # le job existe, enabled=true
bash "<HERMES_HOME>/scripts/<prefixe>-a-valider.sh"   # muet si vide
```

## `--deliver` : le point qui casse en silence

`--deliver origin` suppose une origine (une conversation d'où le job a été
créé). Créé depuis un terminal, il n'y a pas d'origine : le job tourne et ne
livre nulle part.

| Situation | `--deliver` |
|---|---|
| job créé depuis une session existante (Telegram, desktop) | `origin` |
| job créé en ligne de commande, livraison Telegram | `telegram` (canal configuré) |
| job créé en ligne de commande, aucune notification voulue | `local` |

Toujours vérifier après création : `hermes cron runs <id>` doit montrer une
exécution `ok` et une livraison sans erreur. Un `last_delivery_error` non nul
signifie que le rappel existe mais ne parle à personne.

## Rappels fiscaux — prudence

Les alertes URSSAF et France Travail ne sont créées que si le régime les impose.
Elles ne remplacent jamais l'obligation elle-même : elles rappellent une
échéance, elles ne calculent rien.

| Rappel | Quand | Contenu attendu |
|---|---|---|
| URSSAF | le jour déclaré par le paramétrage (souvent 26) | période, date limite, « à faire sur le site » |
| France Travail | le 2 et le 10 (si concerné) | actualisation à faire avant le 15 |

Ces deux-là sont des jobs **avec agent** (ils rédigent un rappel lisible), pas
des scripts : ils ont besoin de la date et du régime. Ils restent désactivés par
défaut dans le paramétrage.

## Ce qu'un rappel ne fait jamais

- Déplacer un fichier de `a-valider/` vers `livres/` — jamais, à aucun niveau.
- Envoyer un email au nom de l'entrepreneur.
- Résumer le contenu des livrables (il liste des noms de fichiers, rien de plus).
- Répéter une alerte déjà envoyée le même jour.

## Budget

Trois jobs qui tournent deux fois par jour en mode `--no-agent` coûtent zéro
appel de modèle. Le seul coût réel du dispositif vient des missions, pas des
rappels : ne pas économiser sur les rappels, ne pas en ajouter non plus.
