#!/usr/bin/env python3
"""Construit et installe une équipe d'agents sur mesure dans une instance Hermes.

Entrée  : un organigramme validé (equipe.json), produit par l'inventaire puis
          l'entretien.
Sortie  : dossier de travail, un skill de direction, N skills de postes,
          script de rappel, récapitulatif de l'équipe.

Trois commandes, dans cet ordre imposé :
  --recapitulatif        écrit le récapitulatif de l'équipe, n'installe rien
  --valider "<nom>"      marque l'organigramme validé par cette personne
  (défaut)               installe — REFUSE tant que l'organigramme n'est pas validé

Idempotent et non destructif : un fichier existant différent n'est jamais écrasé
sans --force, et --force sauvegarde avant d'écrire.

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

VERSION = "2.0.0"
ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates"

# ---------------------------------------------------------------------------
# Bibliothèque de modèles de postes.
# Ce ne sont PAS des postes imposés : seulement des points de départ pour un
# poste que l'utilisateur a déjà décidé de créer. Un poste « libre » fournit
# lui-même son périmètre et ses livrables.
# ---------------------------------------------------------------------------

MODELES = {
    "bureau": {
        "libelle": "Bureau",
        "quand": [
            "Une facture, un devis, une relance ou une déclaration à produire.",
            "Une question sur le chiffre d'affaires, les échéances ou un impayé.",
        ],
        "perimetre": [
            "Devis : chiffrage, conditions, préparation de l'envoi.",
            "Factures : brouillon, numérotation, enregistrement.",
            "Relances : impayés, échéances dépassées.",
            "Déclarations : préparation du chiffre à déclarer, jamais l'envoi.",
            "Suivi du chiffre d'affaires, par période et par client.",
        ],
        "livrables": [
            "Facture / devis : PDF dans `a-valider/`, `AAAA-MM-JJ__facture-<client>.pdf`.",
            "Relance : `AAAA-MM-JJ__relance-<client>.md`.",
            "Récapitulatif : `AAAA-MM-JJ__ca-<periode>.md`.",
        ],
        "interdits": [
            "Publier, prospecter, répondre à un avis.",
            "Négocier un prix ou consentir une remise.",
            "Envoyer une facture au client : l'envoi est une commande distincte.",
        ],
        "niveau": "signature",
    },
    "voix": {
        "libelle": "Voix",
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
        "niveau": "validation",
    },
    "acquisition": {
        "libelle": "Acquisition",
        "quand": [
            "Chercher de nouveaux clients ou de nouveaux canaux.",
            "Préparer un premier contact ou une relance de prospection.",
        ],
        "perimetre": [
            "Identifier des prospects qualifiés, avec preuve (URL, page, tarif constaté).",
            "Préparer des messages de premier contact.",
            "Tenir la liste des prospects et des relances.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__prospects-<sujet>.md` : nom, ville, URL, preuve, contact.",
            "`AAAA-MM-JJ__message-<destinataire>.md`.",
        ],
        "interdits": [
            "Négocier un prix, une remise, un délai.",
            "Engager l'entreprise par écrit.",
            "Contacter qui que ce soit sans validation.",
        ],
        "niveau": "validation",
    },
    "partenaires": {
        "libelle": "Partenaires",
        "quand": [
            "Chercher des distributeurs, revendeurs ou prescripteurs.",
            "Préparer les éléments d'un partenariat.",
        ],
        "perimetre": [
            "Identifier et qualifier des distributeurs ou prescripteurs, avec preuve.",
            "Préparer les éléments de présentation d'un partenariat.",
            "Suivre les échanges, sans négocier.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__partenaires-<sujet>.md` : nom, preuve, contact, angle.",
            "`AAAA-MM-JJ__dossier-<partenaire>.md`.",
        ],
        "interdits": [
            "Négocier un contrat ou une commission.",
            "Signer ou engager l'entreprise.",
            "Communiquer un tarif non validé.",
        ],
        "niveau": "validation",
    },
    "fidelisation": {
        "libelle": "Fidélisation",
        "quand": [
            "Le client principal donne des signes de distance ou de mécontentement.",
            "Préparer une relance ou une offre complémentaire.",
        ],
        "perimetre": [
            "Suivre le client principal : fréquence, satisfaction, signaux de départ.",
            "Préparer des relances et des offres complémentaires.",
            "Réduire la dépendance : pistes de diversification.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__suivi-client-<sujet>.md`.",
            "`AAAA-MM-JJ__relance-<client>.md`.",
        ],
        "interdits": [
            "Négocier un prix ou une condition.",
            "Engager l'entreprise par écrit.",
            "Contacter le client sans validation.",
        ],
        "niveau": "validation",
    },
    "production": {
        "libelle": "Production",
        "quand": [
            "Le planning de fabrication ou de prestation doit être tenu à jour.",
            "Un réassort de matières ou de pièces approche.",
        ],
        "perimetre": [
            "Tenir le planning de production et les commandes en cours.",
            "Signaler les ruptures de matière avant qu'elles bloquent.",
            "Préparer les listes de réassort, sans commander.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__planning-production.md`.",
            "`AAAA-MM-JJ__reassort-<matiere>.md`.",
        ],
        "interdits": [
            "Passer une commande fournisseur.",
            "Négocier un prix d'achat.",
            "Promettre une date de livraison au client.",
        ],
        "niveau": "validation",
    },
    "logistique": {
        "libelle": "Logistique",
        "quand": [
            "Une expédition ou un retour doit être préparé.",
            "Un envoi est en retard ou bloqué chez le transporteur.",
        ],
        "perimetre": [
            "Préparer les bordereaux et les étiquettes, sans expédier.",
            "Suivre les envois et signaler les anomalies.",
            "Tenir la liste des retours et des remboursements à traiter.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__expeditions.md`.",
            "`AAAA-MM-JJ__anomalie-<suivi>.md`.",
        ],
        "interdits": [
            "Choisir un transporteur sans validation.",
            "Promettre une date au client.",
            "Traiter un remboursement.",
        ],
        "niveau": "validation",
    },
    "sav": {
        "libelle": "Relation client",
        "quand": [
            "Une demande SAV, une réclamation ou un avis client arrive.",
            "Un client demande un geste commercial ou une garantie.",
        ],
        "perimetre": [
            "Préparer les réponses SAV et les réponses aux avis.",
            "Tenir l'historique des incidents et des promesses faites.",
            "Signaler les défauts récurrents qui coûtent.",
        ],
        "livrables": [
            "`AAAA-MM-JJ__reponse-<client-id>.md`.",
            "`AAAA-MM-JJ__incidents-<periode>.md`.",
        ],
        "interdits": [
            "Accorder un remboursement ou un avoir.",
            "Promettre un remplacement ou un délai.",
            "Contacter le client sans validation.",
        ],
        "niveau": "validation",
    },
}

NIVEAUX = {"libre": "🟢 libre", "validation": "🟡 validation", "signature": "🔴 signature"}


# ---------------------------------------------------------------------------
# utilitaires
# ---------------------------------------------------------------------------

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
    value = norm(value)
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
    return "\n".join("- " + str(l) for l in lines)


def deep_merge(base, override):
    out = dict(base)
    for key, val in (override or {}).items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], val)
        else:
            out[key] = val
    return out


# ---------------------------------------------------------------------------
# configuration — et contrôle de l'organigramme
# ---------------------------------------------------------------------------

DEFAULTS = {
    "version": 2,
    "prefixe": "equipe",
    "profil": "default",
    "hermes_home": None,
    "racine": "~/equipe",
    "langue": {"code": "fr", "tutoiement": True, "ton": "direct et concret"},
    "utilisateur": {"nom": "", "role": "entrepreneur"},
    "entreprise": {"nom": "", "statut": "à confirmer", "tva": "franchise", "activite": ""},
    "inventaire": {"date": None, "profils_hermes": [], "personnes": [], "outils": [],
                   "deja_couvert": [], "constat": ""},
    "postes": [],
    "hors_perimetre": [],
    "ecarte": [],
    "verrou": {"rappel": ["08:00", "18:00"], "fuseau": "Europe/Paris"},
    "crons": {"verrou": {"actif": True}, "urssaf": {"actif": False, "jour": "26"},
              "france_travail": {"actif": False, "jour": "2"}, "livraison": "origin"},
    "kanban": {"actif": False, "assignee": "default"},
    "validation": {"valide": False, "par": None, "le": None, "postes_valides": None},
}


def load_config(path):
    cfg_path = expand(path)
    if not cfg_path.exists():
        raise SystemExit("organigramme introuvable : %s" % cfg_path)
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    raw.pop("_commentaire", None)
    cfg = deep_merge(DEFAULTS, raw)

    missing = []
    if not cfg["utilisateur"].get("nom"):
        missing.append("utilisateur.nom")
    if not cfg["entreprise"].get("nom"):
        missing.append("entreprise.nom")
    if not cfg.get("racine"):
        missing.append("racine")
    if not cfg.get("postes"):
        missing.append("postes (au moins un)")
    if missing:
        raise SystemExit("organigramme incomplet — manque : %s" % ", ".join(missing))

    if not re.match(r"^[a-z0-9][a-z0-9-]*$", cfg["prefixe"]):
        raise SystemExit("prefixe invalide (minuscules, chiffres, tirets) : %r" % cfg["prefixe"])

    seen = {}
    for i, poste in enumerate(cfg["postes"], start=1):
        where = "postes[%d]" % (i - 1)
        if not poste.get("nom"):
            raise SystemExit("%s : nom manquant (le poste doit porter un nom)" % where)
        if not poste.get("libelle"):
            raise SystemExit("%s : libelle manquant (Bureau, Voix, Production…)" % where)
        modele = norm(poste.get("modele") or "")
        if modele == "libre":
            modele = ""
        if modele and modele not in MODELES:
            raise SystemExit("%s : modele inconnu %r — possibles : %s (ou \"libre\")"
                             % (where, poste.get("modele"), ", ".join(sorted(MODELES))))
        poste["modele"] = modele or None

        # un poste qui déclare un modèle hérite de son périmètre, de ses livrables,
        # de ses déclencheurs et de ses interdits ; la config peut tout surcharger.
        modele_def = MODELES.get(modele or "", {})
        if not poste.get("perimetre"):
            poste["perimetre"] = list(modele_def.get("perimetre", []))
        if not poste.get("livrables"):
            poste["livrables"] = list(modele_def.get("livrables", []))
        if not poste.get("quand"):
            poste["quand"] = list(modele_def.get("quand", []))
        if not poste.get("ne_fait_jamais"):
            poste["ne_fait_jamais"] = list(modele_def.get("interdits", []))

        slug = poste.get("slug") or slugify(poste.get("libelle") or poste["nom"])
        poste["slug"] = slugify(slug)
        if poste["slug"] in seen:
            raise SystemExit("%s : slug « %s » déjà utilisé par un autre poste"
                             % (where, poste["slug"]))
        seen[poste["slug"]] = True
        if not poste.get("livrables"):
            raise SystemExit("%s (%s) : aucun livrable — un poste sans livrable nommé "
                             "ne se crée pas" % (where, poste["nom"]))
        if not poste.get("perimetre"):
            raise SystemExit("%s (%s) : périmètre vide" % (where, poste["nom"]))
        if not poste.get("pourquoi"):
            raise SystemExit("%s (%s) : « pourquoi » manquant — chaque poste doit dire "
                             "quelle tâche récurrente il porte" % (where, poste["nom"]))
        niveau = norm(poste.get("niveau") or MODELES.get(poste["modele"] or "", {}).get("niveau", "validation"))
        if niveau not in NIVEAUX:
            raise SystemExit("%s : niveau inconnu %r (libre, validation, signature)"
                             % (where, poste.get("niveau")))
        poste["niveau"] = niveau

    v = cfg["validation"]
    if v.get("valide"):
        if not v.get("par") or not v.get("le"):
            raise SystemExit("validation incomplète : nom du validateur et date obligatoires")
        if v.get("postes_valides") != len(cfg["postes"]):
            raise SystemExit(
                "l'organigramme a changé depuis la validation (%s poste(s) validé(s), %d "
                "aujourd'hui) — revalider avant d'installer"
                % (v.get("postes_valides"), len(cfg["postes"])))
    return cfg


def poste_data(poste):
    modele = MODELES.get(poste.get("modele") or "", {})
    return {
        "nom": poste["nom"],
        "libelle": poste["libelle"],
        "slug": poste["slug"],
        "pourquoi": poste["pourquoi"],
        "quand": poste.get("quand") or modele.get("quand", ["Une demande entre dans son périmètre."]),
        "perimetre": poste["perimetre"],
        "livrables": poste["livrables"],
        "interdits": poste.get("ne_fait_jamais") or modele.get("interdits", []),
        "niveau": poste["niveau"],
    }


# ---------------------------------------------------------------------------
# rendu
# ---------------------------------------------------------------------------

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


def kanban_bloc(cfg):
    if not cfg["kanban"].get("actif"):
        return ("Kanban **désactivé** à l'installation : une mission = un livrable = une\n"
                "conversation avec la direction. Pour l'activer plus tard, voir\n"
                "`references/06-installation.md`.")
    assignee = cfg["kanban"].get("assignee") or "default"
    exemple = cfg["postes"][0]["nom"]
    return (
        "Kanban Hermes (`kanban_create` / `kanban_list`), une carte par livrable.\n\n"
        "**Le nom du poste va dans le TITRE de la carte, jamais dans l'assignee.**\n"
        "Assigné `%s` (profil vérifié comme existant) ; un assignee inconnu est marqué\n"
        "`skipped_nonspawnable` et la carte reste en `ready` indéfiniment.\n"
        "Exemple : `[%s] canevas d'atelier`, assignee `%s`.\n\n"
        "Statuts : `todo` (découpé), `running` (le poste travaille), `blocked` (attend\n"
        "%s — avec `kind: needs_input`), `done` (validé)."
        % (assignee, exemple, assignee, cfg["utilisateur"]["nom"]))


def postes_table(cfg, with_why=False):
    if with_why:
        head = ("| # | Poste | Nom | Pourquoi il existe | Livrable principal | Niveau |\n"
                "|---|---|---|---|---|---|\n")
        rows = []
        for i, p in enumerate(cfg["postes"], start=1):
            d = poste_data(p)
            rows.append("| %d | **%s** | %s | %s | %s | %s |" % (
                i, d["libelle"], d["nom"], d["pourquoi"], d["livrables"][0], NIVEAUX[d["niveau"]]))
        return head + "\n".join(rows)
    head = ("| # | Poste | Nom | Skill | Périmètre |\n|---|---|---|---|---|\n")
    rows = []
    for i, p in enumerate(cfg["postes"], start=1):
        d = poste_data(p)
        rows.append("| %d | %s | **%s** | `%s-%s` | %s |" % (
            i, d["libelle"], d["nom"], cfg["prefixe"], d["slug"],
            d["perimetre"][0].rstrip(".")))
    return head + "\n".join(rows)


def inventaire_table(cfg):
    inv = cfg.get("inventaire") or {}
    lines = []
    for p in inv.get("profils_hermes") or []:
        lines.append("| Profil Hermes | `%s` |" % p)
    for p in inv.get("personnes") or []:
        if isinstance(p, dict):
            lines.append("| %s | %s |" % (p.get("nom", "?"), p.get("role", "")))
        else:
            lines.append("| personne | %s |" % p)
    for o in inv.get("outils") or []:
        lines.append("| outil | %s |" % o)
    if not lines:
        lines.append("| — | **aucun existant déclaré** |")
    return "| Ce qui existe déjà | Détail |\n|---|---|\n" + "\n".join(lines)


def base_values(cfg, racine):
    tutoie = bool(cfg["langue"].get("tutoiement", True))
    code = cfg["langue"].get("code", "fr")
    langue_ton = ("Français, tutoiement" if tutoie else "Français, vouvoiement") \
        if code == "fr" else "Langue de travail : %s" % code
    n = len(cfg["postes"])
    return {
        "PREFIXE": cfg["prefixe"],
        "RACINE": str(racine),
        "UTILISATEUR": cfg["utilisateur"]["nom"],
        "ROLE": cfg["utilisateur"].get("role", "entrepreneur"),
        "ENTREPRISE": cfg["entreprise"]["nom"],
        "STATUT": cfg["entreprise"].get("statut", "à confirmer"),
        "EFFECTIF": str(n),
        "EFFECTIF_MOT": "un poste" if n == 1 else "%d postes" % n,
        "TVA_MODE": cfg["entreprise"].get("tva", "à confirmer"),
        "TVA_PHRASE": tva_phrase(cfg["entreprise"].get("tva")),
        "TVA_NOTE": tva_note(cfg["entreprise"].get("tva")),
        "ACTIVITE": cfg["entreprise"].get("activite") or "l'activité",
        "LANGUE_TON": langue_ton,
        "TON": cfg["langue"].get("ton", "direct et concret"),
        "DATE": now_stamp(),
        "POSTES_TABLE": postes_table(cfg),
        "POSTES_TABLE_WHY": postes_table(cfg, with_why=True),
        "POSTES_NOMS": ", ".join(p["nom"] for p in cfg["postes"]),
        "INVENTAIRE_TABLE": inventaire_table(cfg),
        "DEJA_COUVERT": bullets((cfg.get("inventaire") or {}).get("deja_couvert")
                                or ["rien de déclaré"]),
        "HORS_PERIMETRE": bullets(cfg.get("hors_perimetre")
                                  or ["le cœur de métier de l'activité"]),
        "ECARTE": bullets(ecarte_lines(cfg)),
        "KANBAN_BLOC": kanban_bloc(cfg),
        "VALIDE_PAR": cfg["validation"].get("par") or "non validé",
        "VALIDE_LE": cfg["validation"].get("le") or "—",
    }


def ecarte_lines(cfg):
    out = []
    for e in cfg.get("ecarte") or []:
        if isinstance(e, dict):
            out.append("%s — %s" % (e.get("sujet", "?"), e.get("raison", "")))
        else:
            out.append(str(e))
    return out or ["rien d'écarté"]


def chef_values(cfg, racine, poste):
    d = poste_data(poste)
    vals = base_values(cfg, racine)
    vals.update({
        "POSTE_SLUG": d["slug"],
        "POSTE_NOM": d["nom"],
        "POSTE_LIBELLE": d["libelle"],
        "POSTE_LIBELLE_LOWER": d["libelle"].lower(),
        "POSTE_POURQUOI": d["pourquoi"],
        "POSTE_QUAND": bullets(d["quand"]),
        "POSTE_PERIMETRE": bullets(d["perimetre"]),
        "POSTE_LIVRABLES": bullets(d["livrables"]),
        "POSTE_INTERDITS": bullets(d["interdits"]),
        "POSTE_NIVEAU": NIVEAUX[d["niveau"]],
        "POSTE_TAGS": ", ".join(dict.fromkeys([cfg["prefixe"], d["slug"], d["libelle"].lower()])),
    })
    return vals


def organigramme_md(cfg, racine):
    """Récapitulatif soumis à validation — dérivé de la config, jamais édité à la main."""
    v = cfg["validation"]
    etat = ("**VALIDÉ** par %s le %s (%s poste(s))" % (v["par"], v["le"], v["postes_valides"])
            if v.get("valide") else
            "**NON VALIDÉ** — l'installation refuse de tourner en l'état.")
    n = len(cfg["postes"])
    lignes = [
        "# Organigramme — %s" % cfg["entreprise"]["nom"],
        "",
        "Récapitulatif de l'équipe proposée à **%s** (%s). Fichier **dérivé** de "
        "`equipe.json` : il se régénère, ne pas l'éditer à la main."
        % (cfg["utilisateur"]["nom"], cfg["utilisateur"].get("role", "entrepreneur")),
        "",
        "> État de la validation : %s" % etat,
        "",
        "## 1. Ce qui existait déjà (inventaire du %s)"
        % ((cfg.get("inventaire") or {}).get("date") or now_stamp()),
        "",
        inventaire_table(cfg),
        "",
    ]
    constat = (cfg.get("inventaire") or {}).get("constat")
    if constat:
        lignes += ["**Constat :** %s" % constat, ""]
    lignes += ["**Déjà couvert, donc non recréé :**", "",
               bullets((cfg.get("inventaire") or {}).get("deja_couvert") or ["rien de déclaré"]), ""]
    lignes += ["## 2. L'équipe proposée — %s" % ("un poste" if n == 1 else "%d postes" % n), "",
               postes_table(cfg, with_why=True), ""]
    lignes += ["## 3. Détail des postes", ""]
    for i, p in enumerate(cfg["postes"], start=1):
        d = poste_data(p)
        lignes += ["### %d. %s — %s" % (i, d["nom"], d["libelle"]), "",
                   "**Pourquoi il existe :** %s" % d["pourquoi"], "",
                   "**Périmètre :**", "", bullets(d["perimetre"]), "",
                   "**Livrables :**", "", bullets(d["livrables"]), "",
                   "**Ne fait jamais :**", "", bullets(d["interdits"]), "",
                   "**Niveau maximum :** %s" % NIVEAUX[d["niveau"]], ""]
    lignes += ["## 4. Ce que l'équipe ne couvre pas", "",
               bullets(cfg.get("hors_perimetre") or ["le cœur de métier"]), ""]
    lignes += ["## 5. Écarté, et pourquoi", "", bullets(ecarte_lines(cfg)), ""]
    lignes += ["## 6. Validation", "",
               "Pour valider : `python3 scripts/installer.py --config equipe.json "
               "--valider \"<votre nom>\"`",
               "Tant que ce fichier n'est pas validé, **rien ne s'installe**.", ""]
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# écriture
# ---------------------------------------------------------------------------

class Writer:
    def __init__(self, dry_run=False, force=False):
        self.dry_run = dry_run
        self.force = force
        self.rows = []
        self.backups = []

    def write(self, path, content, mode=None, derived=False):
        path = expand(path)
        state = "créé"
        if path.exists():
            old = path.read_text(encoding="utf-8", errors="replace")
            if old == content:
                state = "inchangé"
                self.rows.append((state, path))
                return state
            if not (self.force or derived):
                state = "conservé (existe, différent — --force pour écraser)"
                self.rows.append((state, path))
                return state
            if not self.dry_run and not derived:
                bak = path.with_suffix(path.suffix + ".bak-" + datetime.now().strftime("%Y%m%d%H%M%S"))
                shutil.copy2(path, bak)
                self.backups.append(bak)
            state = "régénéré" if derived else "écrasé (sauvegarde)"
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


# ---------------------------------------------------------------------------
# cron
# ---------------------------------------------------------------------------

def cron_script(racine):
    txt = (ROOT / "scripts" / "a-valider.sh").read_text(encoding="utf-8")
    txt = txt.replace("__RACINE__", str(racine))
    if "__RACINE__" in txt:
        raise SystemExit("substitution de racine incomplète")
    return txt


def cron_deliver(cfg):
    return cfg["crons"].get("livraison") or "origin"


def crons_file(cfg, racine, script_name):
    hours = cfg["verrou"].get("rappel") or ["08:00", "18:00"]
    hh = sorted({int(str(h).split(":")[0]) for h in hours})
    expr = "0 %s * * *" % ",".join(str(h) for h in hh)
    deliver = cron_deliver(cfg)
    prefixe = cfg["prefixe"]
    lignes = [
        "#!/usr/bin/env bash",
        "# Rappels du dispositif %s — à créer une fois." % cfg["entreprise"]["nom"],
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
        bureau = next((p for p in cfg["postes"] if p.get("modele") == "bureau"), None)
        lignes += [
            "# 2. Alerte déclaration URSSAF (avec agent : rédige un rappel lisible)",
            'hermes cron create "0 9 %s * *" \\' % jour,
            '  --name "%s — déclaration URSSAF" \\' % prefixe,
        ]
        if bureau:
            lignes.append('  --skill "%s-%s" \\' % (prefixe, bureau["slug"]))
        lignes += [
            '  --deliver %s \\' % deliver,
            '  "Rappel : la déclaration de chiffre d\'affaires (%s) est à faire. '
            'Rappelle la période et la date limite, sans calculer de montant. '
            'Si une date est incertaine, dis-le."' % cfg["entreprise"]["nom"],
            "",
        ]
    if cfg["crons"].get("france_travail", {}).get("actif"):
        jour = str(cfg["crons"]["france_travail"].get("jour", "2"))
        lignes += [
            "# 3. Alerte actualisation France Travail",
            'hermes cron create "0 9 %s * *" \\' % jour,
            '  --name "%s — actualisation France Travail" \\' % prefixe,
            '  --deliver %s \\' % deliver,
            '  "Rappel : actualisation France Travail à faire avant le 15. '
            'Un message court suffit, sans descriptif."',
            "",
        ]
    lignes += ["# Contrôle après création :",
               "#   hermes cron list",
               "#   hermes cron runs <id>      -> statut ok, pas de last_delivery_error"]
    return "\n".join(lignes) + "\n"


# ---------------------------------------------------------------------------
# commandes
# ---------------------------------------------------------------------------

def cmd_recapitulatif(cfg, args):
    racine = expand(cfg["racine"])
    w = Writer(dry_run=args.dry_run)
    w.mkdir(racine)
    w.write(racine / "organigramme.md", organigramme_md(cfg, racine), derived=True)
    print("")
    print("  Récapitulatif — %s — %s" % (cfg["entreprise"]["nom"],
          "un poste" if len(cfg["postes"]) == 1 else "%d postes" % len(cfg["postes"])))
    for state, path in w.rows:
        print("  %-12s %s" % (state, path))
    if not cfg["validation"].get("valide"):
        print("")
        print("  ⛔ non validé — rien ne s'installera avant :")
        print("     python3 scripts/installer.py --config %s --valider \"<nom>\"" % args.config)
    print("")


def cmd_valider(cfg, args, config_path):
    cfg["validation"] = {"valide": True, "par": args.valider, "le": now_stamp(),
                         "postes_valides": len(cfg["postes"])}
    path = expand(config_path)
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    racine = expand(cfg["racine"])
    w = Writer()
    w.write(racine / "organigramme.md", organigramme_md(cfg, racine), derived=True)
    print("")
    print("  ✅ organigramme validé par %s le %s — %s"
          % (args.valider, cfg["validation"]["le"],
             "un poste" if len(cfg["postes"]) == 1 else "%d postes" % len(cfg["postes"])))
    print("  %s" % path)
    print("  installer : python3 scripts/installer.py --config %s" % config_path)
    print("")


def cmd_install(cfg, args):
    if not cfg["validation"].get("valide"):
        print("", file=sys.stderr)
        print("  ⛔ installation refusée : l'organigramme n'est pas validé.", file=sys.stderr)
        print("     1. récapitulatif : --recapitulatif", file=sys.stderr)
        print("     2. validation    : --valider \"<nom de la personne>\"", file=sys.stderr)
        print("", file=sys.stderr)
        return 3

    racine = expand(cfg["racine"])
    home = hermes_home(cfg.get("hermes_home") or args.hermes_home, args.profile or cfg.get("profil"))
    prefixe = cfg["prefixe"]
    skills_dir = home / "skills" / prefixe
    scripts_dir = home / "scripts"

    w = Writer(dry_run=args.dry_run, force=args.force)
    for sub in ("a-valider", "livres", "archives", "cerveau", "modeles", "logs"):
        w.mkdir(racine / sub)

    base = base_values(cfg, racine)
    w.write(racine / "organigramme.md", organigramme_md(cfg, racine), derived=True)
    w.write(racine / "README.md", render(read_template("README-dispositif.md"), base))
    w.write(racine / "config.json", json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    for name in ("entreprise.json", "offres.md", "fiscal.md"):
        w.write(racine / "cerveau" / name, render(read_template("cerveau/%s" % name), base))

    w.write(skills_dir / ("%s-direction" % prefixe) / "SKILL.md",
            render(read_template("skills/ceo.SKILL.md"), base))

    for poste in cfg["postes"]:
        w.write(skills_dir / ("%s-%s" % (prefixe, poste["slug"])) / "SKILL.md",
                render(read_template("skills/chef.SKILL.md"), chef_values(cfg, racine, poste)))

    script_name = "%s-a-valider.sh" % prefixe
    w.write(scripts_dir / script_name, cron_script(racine), mode=0o755)
    w.write(racine / "crons-a-creer.sh", crons_file(cfg, racine, script_name), mode=0o755)

    print("")
    print("  Équipe %s — %s — installation %s"
          % (cfg["entreprise"]["nom"],
             "un poste" if len(cfg["postes"]) == 1 else "%d postes" % len(cfg["postes"]),
             "à blanc" if args.dry_run else "réelle"))
    print("  racine      : %s" % racine)
    print("  skills      : %s" % skills_dir)
    print("  validé par  : %s le %s" % (cfg["validation"]["par"], cfg["validation"]["le"]))
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
        print("  Charge la direction dans une session : « charge %s-direction »." % prefixe)
        if cfg["crons"].get("verrou", {}).get("actif"):
            print("  Rappels : bash %s" % (racine / "crons-a-creer.sh"))
        if args.with_crons:
            create_cron(cfg, script_name, home, racine)
    return 0


def create_cron(cfg, script_name, home, racine):
    hours = cfg["verrou"].get("rappel") or ["08:00", "18:00"]
    hh = sorted({int(str(h).split(":")[0]) for h in hours})
    expr = "0 %s * * *" % ",".join(str(h) for h in hh)
    name = "%s — éléments à valider" % cfg["prefixe"]
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
    p = argparse.ArgumentParser(
        description="Construit et installe une équipe d'agents sur mesure "
                    "(N postes, organigramme validé).")
    p.add_argument("--config", required=True, help="organigramme / paramétrage JSON")
    p.add_argument("--recapitulatif", action="store_true",
                   help="écrit le récapitulatif de l'équipe, n'installe rien")
    p.add_argument("--valider", metavar="NOM",
                   help="marque l'organigramme comme validé par cette personne")
    p.add_argument("--profile", help="profil Hermes cible (défaut : celui du paramétrage)")
    p.add_argument("--hermes-home", help="racine Hermes (défaut : $HERMES_HOME ou ~/.hermes)")
    p.add_argument("--dry-run", action="store_true", help="affiche le plan, n'écrit rien")
    p.add_argument("--force", action="store_true", help="écrase les fichiers existants (avec sauvegarde)")
    p.add_argument("--with-crons", action="store_true", help="crée le rappel du verrou après installation")
    p.add_argument("--version", action="version", version="equipe-hermes %s" % VERSION)
    args = p.parse_args(argv)

    cfg = load_config(args.config)

    if args.valider:
        cmd_valider(cfg, args, args.config)
        return 0
    if args.recapitulatif:
        cmd_recapitulatif(cfg, args)
        return 0
    return cmd_install(cfg, args)


if __name__ == "__main__":
    sys.exit(main())
