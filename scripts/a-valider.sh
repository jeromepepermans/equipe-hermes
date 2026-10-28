#!/usr/bin/env bash
# Rappel du verrou : liste a-valider/ et se tait quand c'est vide.
# Installé par equipe-hermes. La racine est substituée à l'installation ;
# on peut aussi la passer en argument : a-valider.sh /chemin/du/dispositif
RACINE="${1:-__RACINE__}"

[ -d "$RACINE/a-valider" ] || exit 0

n=0
for f in "$RACINE"/a-valider/*; do
  [ -e "$f" ] || continue
  n=$((n + 1))
done

[ "$n" -eq 0 ] && exit 0

echo "À valider ($n) — $RACINE/a-valider"
ls -1t "$RACINE/a-valider" | head -10 | sed 's/^/  · /'
if [ "$n" -gt 10 ]; then
  echo "  … et $((n - 10)) autre(s)"
fi
