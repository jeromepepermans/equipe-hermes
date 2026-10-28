#!/usr/bin/env python3
"""Installe le dispositif « CEO + 3 chefs » dans une instance Hermes.

Entrée  : un fichier de paramétrage (equipe.json) + les gabarits du dépôt.
Sortie  : dossier de travail, 4 skills, script de rappel, commandes de cron.

Idempotent et non destructif :
  - relancé sans changement, il n'écrit rien ;
  - un fichier existant différent n'est jamais écrasé sans --force ;
  - --force sauvegarde avant d'écrire (.bak-<horodatage>).

Python 3.9+, bibliothèque standard uniquement.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates"

SLUGS = {"bureau": "bureau", "voix": "voix"}

DEFAULTS = {
    "bureau": {
        "quand": [
            "Une facture, un devis, une relance ou une déclaration à produire.",
            "Une question sur le chiffre d'affaires, les échéances ou un impayé.",
        ],
        "perimetre": [
            "Devis : chiffrage, conditions, envoi préparé.",
            "Factures : brouillon, numérotation, enregistrement dans `livres/`.",
            "Relances : impayés, échéances dépassées.",
            "Déclarations : préparation du chiffre à déclarer, jamais l'envoi.",
            "Suivi du chiffre d'affaires, par période et par client.",
        ],
        "livrables": [
            "Facture / devis : PDF déposé dans `a-valider/`, nommé `AAAA-MM-JJ__facture-<client>.pdf`.",
            "Relance : `AAAA-MM-JJ__relance-<client>.md`.",
            "Récapitulatif : `AAAA-MM-JJ__ca-<periode>.md`.",
        ],
        "interdits": [
            "Publier, prospecter, répondre à un avis.",
            "Négocier un prix ou consentir une remise.",
            "Envoyer une facture au client : l'envoi est une commande distincte.",
        ],
    },
    "voix": {
        "quand": [
            "Un contenu à écrire ou réécrire : newsletter, annonce, fiche produit, page.",
            "Une demande de calendrier éditorial ou de cohérence de ton.",
        ],
        "perimetre": [
            "Newsletter et emails d'audience.",
            "Annonces et descriptions de produits.",
            "Réseaux sociaux : rédaction seulement.",
            "SEO : titres, méta, structure, contenu de page.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__newsletter-<sujet>.md`.",
            "`AAAA-MM-JJ__fiche-<produit>.md`.",
            "`AAAA-MM-JJ__calendrier-<mois>.md`.",
        ],
        "interdits": [
            "Envoyer un email, publier, programmer une publication.",
            "Signer un document.",
            "Fixer un prix.",
        ],
    },
}

TROISIEME = {
    "acquisition": {
        "quand": [
            "Chercher de nouveaux clients ou de nouveaux canaux.",
            "Préparer un premier contact ou une relance de prospection.",
        ],
        "perimetre": [
            "Identifier des prospects qualifiés, avec preuve (URL, page, tarif constaté).",
            "Préparer des messages de premier contact.",
            "Tenir la liste des prospects et des relances.",
        ],
        "courte": "trouver des clients, qualifier, préparer le premier contact",
        "interdits": [
            "Négocier un prix, une remise, un délai.",
            "Engager l'entreprise par écrit.",
            "Contacter qui que ce soit sans validation.",
        ],
    },
    "partenaires": {
        "quand": [
            "Chercher des distributeurs, revendeurs ou prescripteurs.",
            "Préparer les éléments d'un partenariat.",
        ],
        "perimetre": [
            "Identifier et qualifier des distributeurs ou prescripteurs, avec preuve.",
            "Préparer les éléments de présentation d'un partenariat.",
            "Suivre les échanges, sans négocier.",
        ],
        "courte": "trouver et qualifier des distributeurs et prescripteurs",
        "interdits": [
            "Négocier un contrat ou une commission.",
            "Signer ou engager l'entreprise.",
            "Communiquer un tarif non validé.",
        ],
    },
    "fidelisation": {
        "quand": [
            "Le client principal donne des signes de distance ou de mécontentement.",
            "Préparer une relance ou une offre complémentaire.",
        ],
        "perimetre": [
            "Suivre le client principal : fréquence, satisfaction, signaux de départ.",
            "Préparer des relances et des offres complémentaires.",
            "Réduire la dépendance : pistes de diversification.",
        ],
        "courte": "garder le client principal et réduire la dépendance",
        "interdits": [
            "Négocier un prix ou une condition.",
            "Engager l'entreprise par écrit.",
            "Contacter le client sans validation.",
        ],
    },
}


# --------------------------------------------------------------------------
# utilitaires
# --------------------------------------------------------------------------

def now_stamp():
    return datetime.now().astimezone().strftime("%Y-%m-%d")


def norm(value):
    """minuscules sans accents — pour comparer des libellés saisis."""
    value = (value or "").strip().lower()
    for src, dst in (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("â", "a"),
                     ("î", "i"), ("ï", "i"), ("ô", "o"), ("û", "u"), ("ù", "u"), ("ç", "c")):
        value = value.replace(src, dst)
    return value


def slugify(value):
    value = (value or "").strip().lower()
    value = (value.replace("é", "e").replace("è", "e").replace("ê", "e")
             .replace("à", "a").replace("â", "a").replace("î", "i")
             .replace("ô", "o").replace("û", "u").replace("ç", "c"))
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "poste"


def expand(path):
    return Path(os.path.expandvars(os.path.expanduser(str(path))))


def hermes_home(explicit=None, profile=None):
    if explicit:
        base = expand(explicit)
    else:
        base = expand(os.environ.get("HERMES_HOME") or "~/.hermes")
    if profile and profile != "default":
        return base / "profiles" / profile
    return base


def read_template(rel):
    path = TPL / rel
    if not path.exists():
        raise SystemExit("gabarit manquant : %s" % path)
    return path.read_text(encoding="utf-8")


def render(text, values):
    out = text
    for key, val in values.items():
        out = out.replace("{{%s}}" % key, str(val))
    left = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", out)))
    if left:
        raise SystemExit("placeholders non résolus : %s" % ", ".join(left))
    return out


def bullets(lines):
    return "\n".join("- " + l for l in lines)


def deep_merge(base, override):
    out = dict(base)
    for key, val in (override or {}).items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], val)
        else:
            out[key] = val
    return out


# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------

def load_config(path):
    cfg_path = expand(path)
    if not cfg_path.exists():
        raise SystemExit("paramétrage introuvable : %s" % cfg_path)
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    raw.pop("_commentaire", None)

    cfg = deep_merge({
        "version": 1,
        "prefixe": "equipe",
        "profil": "default",
        "hermes_home": None,
        "racine": "~/equipe",
        "langue": {"code": "fr", "tutoiement": True, "ton": "direct et concret"},
        "entrepreneur": {"nom": ""},
        "entreprise": {"nom": "", "statut": "à confirmer", "tva": "franchise", "activite": ""},
        "postes": {"bureau": {"nom": "Bureau"}, "voix": {"nom": "Voix"},
                   "troisieme": {"nom": "Troisième", "libelle": "Acquisition"}},
        "verrou": {"niveau3_actif": True, "rappel": ["08:00", "18:00"], "fuseau": "Europe/Paris"},
        "crons": {"verrou": {"actif": True}, "urssaf": {"actif": False, "jour": "26"},
                  "france_travail": {"actif": False, "jour": "2"}, "livraison": "origin"},
        "kanban": {"actif": False, "assignee": "default"},
    }, raw)

    missing = []
    if not cfg["entrepreneur"].get("nom"):
        missing.append("entrepreneur.nom")
    if not cfg["entreprise"].get("nom"):
        missing.append("entreprise.nom")
    if not cfg.get("racine"):
        missing.append("racine")
    if missing:
        raise SystemExit("paramétrage incomplet — manque : %s" % ", ".join(missing))

    libelle = cfg["postes"]["troisieme"].get("libelle", "Acquisition").strip()
    if norm(libelle) not in TROISIEME:
        raise SystemExit(
            "postes.troisieme.libelle doit être Acquisition, Partenaires ou Fidélisation (reçu : %r)" % libelle
        )
    cfg["postes"]["troisieme"]["libelle"] = libelle.capitalize()
    return cfg


# --------------------------------------------------------------------------
# écriture
# --------------------------------------------------------------------------

class Writer:
    def __init__(self, dry_run=False, force=False):
        self.dry_run = dry_run
        self.force = force
        self.rows = []
        self.backups = []

    def write(self, path, content, mode=None):
        path = expand(path)
        state = "créé"
        if path.exists():
            old = path.read_text(encoding="utf-8", errors="replace")
            if old == content:
                state = "inchangé"
                self.rows.append((state, path))
                return state
            if not self.force:
                state = "conservé (existe, différent — --force pour écraser)"
                self.rows.append((state, path))
                return state
            if not self.dry_run:
                bak = path.with_suffix(path.suffix + ".bak-" + datetime.now().strftime("%Y%m%d%H%M%S"))
                shutil.copy2(path, bak)
                self.backups.append(bak)
            state = "écrasé (sauvegarde)"
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            if mode:
                os.chmod(path, mode)
        self.rows.append((state, path))
        return state

    def mkdir(self, path):
        path = expand(path)
        if not path.exists() and not self.dry_run:
            path.mkdir(parents=True, exist_ok=True)
        self.rows.append(("dossier", path))


# --------------------------------------------------------------------------
# rendu des pièces
# --------------------------------------------------------------------------

def tva_phrase(mode):
    mode = (mode or "").lower()
    if mode.startswith("franchise"):
        return "Tous les prix sont **TTC**, jamais de ligne de TVA."
    if mode.startswith("assujetti"):
        return "Prix HT + TVA, avec le taux sourcé dans `cerveau/fiscal.md`."
    return "Régime de TVA **à confirmer** dans `cerveau/fiscal.md` avant toute facture."


def tva_note(mode):
    mode = (mode or "").lower()
    if mode.startswith("franchise"):
        return "TTC (franchise de TVA) : aucune ligne de TVA sur les documents."
    if mode.startswith("assujetti"):
        return "HT, TVA ajoutée au taux figurant dans `fiscal.md`."
    return "à confirmer (régime de TVA non renseigné)."


def kanban_bloc(cfg, prefixe, racine):
    if not cfg["kanban"].get("actif"):
        return ("Kanban **désactivé** au paramétrage : une mission = un livrable = une\n"
                "conversation avec le CEO. Pour l'activer plus tard, voir\n"
                "`references/02-installation.md` du skill `equipe-hermes`.")
    assignee = cfg["kanban"].get("assignee") or "default"
    return (
        "Kanban Hermes (`kanban_create` / `kanban_list`), une carte par livrable.\n\n"
        "**Le nom du chef va dans le TITRE de la carte, jamais dans l'assignee.**\n"
        "Assigné `%s` (seul profil vérifié comme existant) ; un assignee inconnu est\n"
        "marqué `skipped_nonspawnable` et la carte reste en `ready` indéfiniment.\n"
        "Exemple : `[%s] canevas d'atelier`, assignee `%s`.\n\n"
        "Statuts utiles : `todo` (découpé), `running` (le chef travaille), `blocked`\n"
        "(attend %s — avec `kind: needs_input`), `done` (validé)."
        % (assignee, cfg["postes"]["voix"]["nom"], assignee, cfg["entrepreneur"]["nom"])
    )


def base_values(cfg, prefixe, racine):
    tutoie = bool(cfg["langue"].get("tutoiement", True))
    code = cfg["langue"].get("code", "fr")
    langue_ton = ("Français, tutoiement" if tutoie else "Français, vouvoiement") \
        if code == "fr" else "Langue de travail : %s" % code
    return {
        "PREFIXE": prefixe,
        "RACINE": str(racine),
        "ENTREPRENEUR": cfg["entrepreneur"]["nom"],
        "ENTREPRISE": cfg["entreprise"]["nom"],
        "STATUT": cfg["entreprise"].get("statut", "à confirmer"),
        "TVA_MODE": cfg["entreprise"].get("tva", "à confirmer"),
        "TVA_PHRASE": tva_phrase(cfg["entreprise"].get("tva")),
        "TVA_NOTE": tva_note(cfg["entreprise"].get("tva")),
        "ACTIVITE": cfg["entreprise"].get("activite") or "l'activité",
        "LANGUE_TON": langue_ton,
        "TON": cfg["langue"].get("ton", "direct et concret"),
        "DATE": now_stamp(),
        "BUREAU_NOM": cfg["postes"]["bureau"]["nom"],
        "VOIX_NOM": cfg["postes"]["voix"]["nom"],
        "TROISIEME_NOM": cfg["postes"]["troisieme"]["nom"],
        "TROISIEME_LIBELLE": cfg["postes"]["troisieme"]["libelle"],
        "TROISIEME_SLUG": slugify(cfg["postes"]["troisieme"]["libelle"]),
        "KANBAN_BLOC": kanban_bloc(cfg, prefixe, racine),
    }


def chef_values(cfg, prefixe, racine, key):
    poste = cfg["postes"][key]
    if key == "troisieme":
        lib = poste["libelle"].capitalize()
        src = TROISIEME[norm(lib)]
        slug = slugify(lib)
        nom = poste["nom"]
    else:
        src = DEFAULTS[key]
        slug = SLUGS[key]
        nom = poste["nom"]
        lib = "Bureau" if key == "bureau" else "Voix"

    perimetre = poste.get("perimetre") or src["perimetre"]
    livrables = poste.get("livrables") or src.get("livrables") or [
        "`AAAA-MM-JJ__<sujet>.md` dans `a-valider/`.",
        "En tête : destinataire, niveau, conséquence si 🔴.",
    ]
    interdits = poste.get("ne_fait_jamais") or src["interdits"]
    quand = poste.get("quand") or src["quand"]

    vals = base_values(cfg, prefixe, racine)
    vals.update({
        "POSTE_SLUG": slug,
        "POSTE_NOM": nom,
        "POSTE_LIBELLE": lib,
        "POSTE_LIBELLE_LOWER": lib.lower(),
        "POSTE_QUAND": bullets(quand),
        "POSTE_PERIMETRE": bullets(perimetre),
        "POSTE_LIVRABLES": bullets(livrables),
        "POSTE_INTERDITS": bullets(interdits),
        "TROISIEME_PERIMETRE_COURT": TROISIEME[norm(cfg["postes"]["troisieme"]["libelle"])]["courte"],
    })
    return vals, slug, nom


def cron_script(cfg, prefixe, racine):
    txt = (ROOT / "scripts" / "a-valider.sh").read_text(encoding="utf-8")
    txt = txt.replace("__RACINE__", str(racine))
    if "__RACINE__" in txt:
        raise SystemExit("substitution de racine incomplète")
    return txt


def cron_deliver(cfg):
    return cfg["crons"].get("livraison") or "origin"


def crons_file(cfg, prefixe, racine, script_name):
    hours = cfg["verrou"].get("rappel") or ["08:00", "18:00"]
    hh = sorted({int(str(h).split(":")[0]) for h in hours})
    expr = "0 %s * * *" % ",".join(str(h) for h in hh)
    deliver = cron_deliver(cfg)
    lines = [
        "#!/usr/bin/env bash",
        "# Rappels du dispositif %s — créés une fois, à la main." % cfg["entreprise"]["nom"],
        "# Vérifier avant : hermes cron status && hermes cron list",
        "",
        "# 1. Rappel du verrou (script, sans LLM, muet si a-valider/ est vide)",
        'hermes cron create "%s" \\' % expr,
        '  --name "%s — éléments à valider" \\' % prefixe,
        '  --script "%s" \\' % script_name,
        "  --no-agent \\",
        '  --deliver %s' % deliver,
        "",
    ]
    if cfg["crons"].get("urssaf", {}).get("actif"):
        jour = str(cfg["crons"]["urssaf"].get("jour", "26"))
        lines += [
            "# 2. Alerte déclaration URSSAF (avec agent : rédige un rappel lisible)",
            'hermes cron create "0 9 %s * *" \\' % jour,
            '  --name "%s — déclaration URSSAF" \\' % prefixe,
            '  --skill "%s-bureau" \\' % prefixe,
            '  --deliver %s \\' % deliver,
            '  "Rappel : la déclaration de chiffre d\'affaires (%s) est à faire. '
            'Rappelle la période et la date limite, sans calculer de montant. '
            'Si une date est incertaine, dis-le."' % cfg["entreprise"]["nom"],
            "",
        ]
    if cfg["crons"].get("france_travail", {}).get("actif"):
        jour = str(cfg["crons"]["france_travail"].get("jour", "2"))
        lines += [
            "# 3. Alerte actualisation France Travail",
            'hermes cron create "0 9 %s * *" \\' % jour,
            '  --name "%s — actualisation France Travail" \\' % prefixe,
            '  --deliver %s \\' % deliver,
            '  "Rappel : actualisation France Travail à faire avant le 15. '
            'Un message court suffit, sans descriptif."',
            "",
        ]
    lines += [
        "# Contrôle après création :",
        "#   hermes cron list",
        "#   hermes cron runs <id>      -> statut ok, pas de last_delivery_error",
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# installation
# --------------------------------------------------------------------------

def install(cfg, args):
    prefixe = cfg["prefixe"].strip()
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", prefixe):
        raise SystemExit("prefixe invalide (minuscules, chiffres, tirets) : %r" % prefixe)
    racine = expand(cfg["racine"])
    home = hermes_home(cfg.get("hermes_home") or args.hermes_home, args.profile or cfg.get("profil"))
    skills_dir = home / "skills" / prefixe
    scripts_dir = home / "scripts"

    w = Writer(dry_run=args.dry_run, force=args.force)

    for sub in ("a-valider", "livres", "archives", "cerveau", "modeles", "logs"):
        w.mkdir(racine / sub)

    base = base_values(cfg, prefixe, racine)
    w.write(racine / "README.md", render(read_template("README-dispositif.md"), base))
    w.write(racine / "config.json", json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    for name in ("entreprise.json", "offres.md", "fiscal.md"):
        content = render(read_template("cerveau/%s" % name), base)
        w.write(racine / "cerveau" / name, content)

    # CEO
    ceo_vals = dict(base)
    ceo_vals["TROISIEME_PERIMETRE_COURT"] = TROISIEME[
        norm(cfg["postes"]["troisieme"]["libelle"])]["courte"]
    w.write(skills_dir / ("%s-ceo" % prefixe) / "SKILL.md",
            render(read_template("skills/ceo.SKILL.md"), ceo_vals))

    # 3 chefs
    rendered = []
    for key in ("bureau", "voix", "troisieme"):
        vals, slug, nom = chef_values(cfg, prefixe, racine, key)
        path = skills_dir / ("%s-%s" % (prefixe, slug)) / "SKILL.md"
        w.write(path, render(read_template("skills/chef.SKILL.md"), vals))
        rendered.append((nom, slug))

    # rappel
    script_name = "%s-a-valider.sh" % prefixe
    w.write(scripts_dir / script_name, cron_script(cfg, prefixe, racine), mode=0o755)

    # commandes de cron
    w.write(racine / "crons-a-creer.sh", crons_file(cfg, prefixe, racine, script_name), mode=0o755)

    # affichage
    print("")
    print("  Équipe %s — installation %s" % (cfg["entreprise"]["nom"], "à blanc" if args.dry_run else "réelle"))
    print("  racine      : %s" % racine)
    print("  skills      : %s" % skills_dir)
    print("  script      : %s" % (scripts_dir / script_name))
    print("  profil      : %s" % (args.profile or cfg.get("profil") or "default"))
    print("")
    width = max(len(s) for s, _ in w.rows)
    for state, path in w.rows:
        print("  %-*s  %s" % (width, state, path))
    if w.backups:
        print("")
        print("  sauvegardes :")
        for b in w.backups:
            print("    %s" % b)
    print("")

    if not args.dry_run:
        print("  Charge les skills dans une session : « charge %s-ceo »." % prefixe)
        if cfg["crons"].get("verrou", {}).get("actif"):
            print("  Rappels : bash %s" % (racine / "crons-a-creer.sh"))

        if args.with_crons:
            create_cron(cfg, prefixe, script_name, home, racine)

    return 0


def create_cron(cfg, prefixe, script_name, home, racine):
    hours = cfg["verrou"].get("rappel") or ["08:00", "18:00"]
    hh = sorted({int(str(h).split(":")[0]) for h in hours})
    expr = "0 %s * * *" % ",".join(str(h) for h in hh)
    name = "%s — éléments à valider" % prefixe
    env = dict(os.environ)
    env["HERMES_HOME"] = str(home)

    try:
        listing = subprocess.run(["hermes", "cron", "list"], capture_output=True,
                                 text=True, env=env, timeout=60)
        if name in (listing.stdout or ""):
            print("  cron : « %s » existe déjà — rien à créer" % name)
            return
    except Exception:
        pass

    cmd = ["hermes", "cron", "create", expr, "--name", name,
           "--script", script_name, "--no-agent", "--deliver", cron_deliver(cfg)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=90)
        if res.returncode == 0:
            print("  cron créé : %s (%s)" % (name, expr))
            print("  vérifier  : hermes cron list && hermes cron status")
        else:
            print("  cron NON créé (%s) — créer à la main :" % (res.stderr or res.stdout).strip()[:200])
            print("    " + " ".join(cmd))
    except FileNotFoundError:
        print("  cron NON créé : commande `hermes` introuvable — voir %s" % (racine / "crons-a-creer.sh"))


def main(argv=None):
    p = argparse.ArgumentParser(description="Installe le dispositif CEO + 3 chefs dans une instance Hermes.")
    p.add_argument("--config", required=True, help="fichier de paramétrage JSON")
    p.add_argument("--profile", help="profil Hermes cible (défaut : celui du paramétrage)")
    p.add_argument("--hermes-home", help="racine Hermes (défaut : $HERMES_HOME ou ~/.hermes)")
    p.add_argument("--dry-run", action="store_true", help="affiche le plan, n'écrit rien")
    p.add_argument("--force", action="store_true", help="écrase les fichiers existants (avec sauvegarde)")
    p.add_argument("--with-crons", action="store_true", help="crée le rappel du verrou après installation")
    p.add_argument("--version", action="version", version="equipe-hermes %s" % VERSION)
    args = p.parse_args(argv)

    cfg = load_config(args.config)
    return install(cfg, args)


if __name__ == "__main__":
    sys.exit(main())
