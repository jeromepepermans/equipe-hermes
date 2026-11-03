#!/usr/bin/env python3
"""Tests réels de l'installateur — aucun mock, HOME et HERMES_HOME temporaires.

    python3 tests/test_installer.py

Couvre ce qui compte pour la v2 : nombre de postes variable, verrou de
validation, validation périmée, poste sans livrable ou sans justification,
récapitulatif, idempotence, --force, --dry-run, rappel muet.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALLER = ROOT / "scripts" / "installer.py"


def poste(nom, libelle, modele, pourquoi="une tache recurrente sans livrable produit"):
    return {"nom": nom, "libelle": libelle, "modele": modele, "pourquoi": pourquoi}


def config(postes, prefixe="essai"):
    return {
        "version": 2,
        "prefixe": prefixe,
        "racine": "~/dispositif",
        "langue": {"code": "fr", "tutoiement": True},
        "utilisateur": {"nom": "Camille", "role": "indépendante"},
        "entreprise": {
            "nom": "Atelier Roux",
            "statut": "micro-entreprise",
            "tva": "franchise",
            "activite": "restauration de meubles anciens",
        },
        "inventaire": {
            "date": "2026-10-29",
            "profils_hermes": ["boutique"],
            "personnes": [{"nom": "Camille", "role": "fabrication et vente"}],
            "outils": ["boutique en ligne"],
            "deja_couvert": ["le site et la boutique (profil boutique)"],
            "constat": "deux domaines tenus, trois jamais faits",
        },
        "postes": postes,
        "hors_perimetre": ["la fabrication"],
        "ecarte": [{"sujet": "un poste Logistique", "raison": "3 expéditions par mois"}],
        "verrou": {"rappel": ["08:00", "18:00"], "fuseau": "Europe/Paris"},
        "crons": {"verrou": {"actif": True}, "urssaf": {"actif": True, "jour": "26"}},
        "kanban": {"actif": True, "assignee": "default"},
    }


TROIS = config([
    poste("Jeanne", "Bureau", "bureau", "les factures partent en retard"),
    poste("Léa", "Voix", "voix", "les fiches produit sont vides"),
    poste("Marc", "Fidélisation", "fidelisation", "le client principal n'est jamais relancé"),
])


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="equipe-hermes-test-"))
        self.home = self.tmp / "hermes"
        self.home.mkdir()
        self.ws = self.tmp / "workspace"
        self.ws.mkdir()
        self.userhome = self.tmp / "userhome"
        self.userhome.mkdir()
        self.env = dict(os.environ, HERMES_HOME=str(self.home), HOME=str(self.userhome))
        self.cfg = self.write_config(TROIS)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- utilitaires ----------------------------------------------------

    def write_config(self, data, name="equipe.json"):
        path = self.tmp / name
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def run_installer(self, *extra, cfg=None):
        cmd = [sys.executable, str(INSTALLER), "--config", str(cfg or self.cfg)] + list(extra)
        return subprocess.run(cmd, capture_output=True, text=True, env=self.env,
                              cwd=str(self.ws), timeout=120)

    def racine(self):
        return self.userhome / "dispositif"

    def valider(self, nom="Camille Roux", cfg=None):
        res = self.run_installer("--valider", nom, cfg=cfg)
        self.assertEqual(res.returncode, 0, res.stderr)
        return res

    def installer(self, *extra):
        self.valider()
        return self.run_installer(*extra)

    def skills(self):
        return self.home / "skills" / "essai"

    # -- verrou de validation -------------------------------------------

    def test_installation_refusee_sans_validation(self):
        res = self.run_installer()
        self.assertEqual(res.returncode, 3, "code de sortie attendu : 3 (refus)")
        self.assertIn("refusée", res.stderr)
        self.assertIn("--valider", res.stderr)
        self.assertFalse(self.racine().exists(), "aucune écriture ne doit avoir lieu")
        self.assertFalse((self.home / "skills").exists())

    def test_force_ne_leve_pas_le_verrou(self):
        res = self.run_installer("--force")
        self.assertEqual(res.returncode, 3)
        self.assertFalse((self.home / "skills").exists())

    def test_recapitulatif_seul(self):
        res = self.run_installer("--recapitulatif")
        self.assertEqual(res.returncode, 0, res.stderr)
        recap = self.racine() / "organigramme.md"
        self.assertTrue(recap.exists())
        texte = recap.read_text(encoding="utf-8")
        self.assertIn("NON VALIDÉ", texte)
        self.assertIn("3 postes", texte)
        self.assertIn("un poste Logistique", texte)          # section « écarté »
        self.assertFalse((self.home / "skills").exists(), "le récapitulatif n'installe rien")

    def test_validation_puis_installation(self):
        self.valider("Camille Roux")
        cfg = json.loads(self.cfg.read_text(encoding="utf-8"))
        self.assertTrue(cfg["validation"]["valide"])
        self.assertEqual(cfg["validation"]["par"], "Camille Roux")
        self.assertEqual(cfg["validation"]["postes_valides"], 3)

        res = self.run_installer()
        self.assertEqual(res.returncode, 0, res.stderr)
        texte = (self.racine() / "organigramme.md").read_text(encoding="utf-8")
        self.assertIn("VALIDÉ", texte)
        self.assertIn("Camille Roux", texte)

    def test_validation_perimee_refusee(self):
        self.valider()
        quatre = json.loads(self.cfg.read_text(encoding="utf-8"))
        quatre["postes"].append(poste("Sam", "Production", "production", "ruptures de matière"))
        path = self.write_config(quatre, "equipe-4.json")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("revalider", res.stderr)
        self.assertFalse((self.home / "skills").exists())

    # -- nombre de postes variable --------------------------------------

    def test_un_seul_poste(self):
        cfg = config([poste("Jeanne", "Bureau", "bureau", "les factures ne sont jamais faites")])
        path = self.write_config(cfg, "un.json")
        self.valider(cfg=path)
        res = self.run_installer(cfg=path)
        self.assertEqual(res.returncode, 0, res.stderr)
        found = sorted(p.parent.name for p in self.skills().glob("*/SKILL.md"))
        self.assertEqual(found, ["essai-bureau", "essai-direction"])
        direction = (self.skills() / "essai-direction" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("un poste", direction)
        self.assertNotIn("Léa", direction)

    def test_cinq_postes(self):
        cfg = config([
            poste("Jeanne", "Bureau", "bureau", "factures"),
            poste("Léa", "Voix", "voix", "fiches produit"),
            poste("Marc", "Acquisition", "acquisition", "aucun prospect"),
            poste("Sam", "Production", "production", "réassort"),
            poste("Nino", "Logistique", "logistique", "expéditions"),
        ])
        path = self.write_config(cfg, "cinq.json")
        self.valider(cfg=path)
        res = self.run_installer(cfg=path)
        self.assertEqual(res.returncode, 0, res.stderr)
        found = sorted(p.parent.name for p in self.skills().glob("*/SKILL.md"))
        self.assertEqual(found, ["essai-acquisition", "essai-bureau", "essai-direction",
                                 "essai-logistique", "essai-production", "essai-voix"])
        direction = (self.skills() / "essai-direction" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("5 postes", direction)
        for nom in ("Jeanne", "Léa", "Marc", "Sam", "Nino"):
            self.assertIn(nom, direction)

    def test_poste_libre(self):
        cfg = config([{
            "nom": "Yann", "libelle": "Réserve", "modele": "libre",
            "pourquoi": "les invendus ne sont jamais suivis",
            "perimetre": ["suivre les invendus"],
            "livrables": ["`AAAA-MM-JJ__invendus.md`"],
        }])
        path = self.write_config(cfg, "libre.json")
        self.valider(cfg=path)
        res = self.run_installer(cfg=path)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue((self.skills() / "essai-reserve" / "SKILL.md").exists())

    # -- refus de configuration -----------------------------------------

    def test_poste_sans_livrable_refuse(self):
        cfg = json.loads(json.dumps(TROIS))
        cfg["postes"][1] = {"nom": "Léa", "libelle": "Voix", "modele": "libre",
                            "pourquoi": "des contenus à écrire",
                            "perimetre": ["rédiger des contenus"]}
        path = self.write_config(cfg, "sans-livrable.json")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("aucun livrable", res.stderr)

    def test_poste_sans_pourquoi_refuse(self):
        cfg = json.loads(json.dumps(TROIS))
        del cfg["postes"][0]["pourquoi"]
        path = self.write_config(cfg, "sans-pourquoi.json")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("pourquoi", res.stderr)

    def test_slug_en_double_refuse(self):
        cfg = json.loads(json.dumps(TROIS))
        cfg["postes"].append(dict(cfg["postes"][0], nom="Jeanne 2"))
        path = self.write_config(cfg, "doublon.json")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("déjà utilisé", res.stderr)

    def test_config_incomplete(self):
        cfg = json.loads(json.dumps(TROIS))
        cfg["utilisateur"]["nom"] = ""
        path = self.write_config(cfg, "incomplet.json")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("utilisateur.nom", res.stderr)

    def test_aucun_poste_refuse(self):
        cfg = json.loads(json.dumps(TROIS))
        cfg["postes"] = []
        path = self.write_config(cfg, "vide.json")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("postes", res.stderr)

    # -- installation ----------------------------------------------------

    def test_structure_et_skills(self):
        res = self.installer()
        self.assertEqual(res.returncode, 0, res.stderr)

        found = sorted(p.parent.name for p in self.skills().glob("*/SKILL.md"))
        self.assertEqual(found, ["essai-bureau", "essai-direction",
                                 "essai-fidelisation", "essai-voix"])

        for skill in self.skills().glob("*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("{{", text, "placeholder non résolu dans %s" % skill)
            desc = re.search(r"^description:\s*\"(.*)\"$", text, re.M)
            if desc is None:
                self.fail("description absente dans %s" % skill)
            self.assertLessEqual(len(desc.group(1)), 60,
                                 "description trop longue (%d) dans %s"
                                 % (len(desc.group(1)), skill))

        racine = self.racine()
        for sub in ("a-valider", "livres", "archives", "cerveau", "modeles", "logs"):
            self.assertTrue((racine / sub).is_dir(), "dossier manquant : %s" % sub)
        for name in ("README.md", "config.json", "crons-a-creer.sh", "organigramme.md"):
            self.assertTrue((racine / name).exists(), "fichier manquant : %s" % name)

        json.loads((racine / "cerveau" / "entreprise.json").read_text(encoding="utf-8"))

        direction = (self.skills() / "essai-direction" / "SKILL.md").read_text(encoding="utf-8")
        for attendu in ("Jeanne", "Léa", "Marc", "Fidélisation", "Camille",
                        "Atelier Roux", "boutique"):
            self.assertIn(attendu, direction)

        # le poste doit porter sa justification
        bureau = (self.skills() / "essai-bureau" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("les factures partent en retard", bureau)

        script = self.home / "scripts" / "essai-a-valider.sh"
        self.assertTrue(script.exists())
        self.assertTrue(os.access(script, os.X_OK))
        self.assertNotIn("__RACINE__", script.read_text(encoding="utf-8"))

    def test_idempotence(self):
        self.assertEqual(self.installer().returncode, 0)
        res = self.run_installer()
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertNotIn("écrasé", res.stdout)
        self.assertIn("inchangé", res.stdout)

    def test_non_destructif_puis_force(self):
        self.assertEqual(self.installer().returncode, 0)
        skill = self.skills() / "essai-voix" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n<!-- retouche -->\n",
                         encoding="utf-8")

        res = self.run_installer()
        self.assertEqual(res.returncode, 0)
        self.assertIn("conservé", res.stdout)
        self.assertIn("retouche", skill.read_text(encoding="utf-8"))

        res = self.run_installer("--force")
        self.assertEqual(res.returncode, 0)
        self.assertIn("écrasé", res.stdout)
        self.assertNotIn("retouche", skill.read_text(encoding="utf-8"))
        self.assertEqual(len(list(skill.parent.glob("SKILL.md.bak-*"))), 1,
                         "sauvegarde --force absente")

    def test_dry_run_n_ecrit_rien(self):
        self.valider()
        res = self.run_installer("--dry-run")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertFalse((self.racine() / "a-valider").exists())
        self.assertFalse((self.home / "skills").exists())
        self.assertIn("créé", res.stdout)

    def test_rappel_muet_puis_bavard(self):
        self.assertEqual(self.installer().returncode, 0)
        script = self.home / "scripts" / "essai-a-valider.sh"
        vide = subprocess.run(["bash", str(script)], capture_output=True, text=True)
        self.assertEqual(vide.returncode, 0)
        self.assertEqual(vide.stdout.strip(), "",
                         "le rappel doit être muet quand a-valider/ est vide")

        (self.racine() / "a-valider" / "2026-11-04__relance.md").write_text("x", encoding="utf-8")
        plein = subprocess.run(["bash", str(script)], capture_output=True, text=True)
        self.assertIn("À valider (1)", plein.stdout)
        self.assertIn("relance", plein.stdout)

    def test_profil_dedie(self):
        self.valider()
        res = self.run_installer("--profile", "devops")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue((self.home / "profiles" / "devops" / "skills" / "essai"
                         / "essai-direction" / "SKILL.md").exists())
        self.assertFalse((self.home / "skills" / "essai").exists())

    def test_cron_urssaf_utilise_le_poste_bureau(self):
        self.assertEqual(self.installer().returncode, 0)
        crons = (self.racine() / "crons-a-creer.sh").read_text(encoding="utf-8")
        # le skill de rappel n'est attaché que si un poste « bureau » existe
        self.assertIn("essai-bureau", crons)
        self.assertIn("déclaration", crons)


if __name__ == "__main__":
    unittest.main(verbosity=2)
