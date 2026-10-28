#!/usr/bin/env python3
"""Tests réels de l'installateur — aucun mock, un HOME temporaire.

    python3 tests/test_installer.py
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

CONFIG = {
    "version": 1,
    "prefixe": "essai",
    "racine": "~/dispositif",
    "langue": {"code": "fr", "tutoiement": True},
    "entrepreneur": {"nom": "Camille"},
    "entreprise": {
        "nom": "Atelier Roux",
        "statut": "micro-entreprise",
        "tva": "franchise",
        "activite": "restauration de meubles anciens",
    },
    "postes": {
        "bureau": {"nom": "Jeanne"},
        "voix": {"nom": "Léa"},
        "troisieme": {"nom": "Marc", "libelle": "Fidélisation"},
    },
    "verrou": {"rappel": ["08:00", "18:00"], "fuseau": "Europe/Paris"},
    "crons": {"verrou": {"actif": True}, "urssaf": {"actif": True, "jour": "26"}},
    "kanban": {"actif": True, "assignee": "default"},
}


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="equipe-hermes-test-"))
        self.home = self.tmp / "hermes"
        self.home.mkdir()
        self.ws = self.tmp / "workspace"
        self.ws.mkdir()
        self.cfg = self.tmp / "equipe.json"
        self.cfg.write_text(json.dumps(CONFIG, ensure_ascii=False), encoding="utf-8")
        self.userhome = self.tmp / "userhome"
        self.userhome.mkdir()
        self.env = dict(os.environ, HERMES_HOME=str(self.home), HOME=str(self.userhome))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_installer(self, *extra, cfg=None):
        cmd = [sys.executable, str(INSTALLER), "--config", str(cfg or self.cfg)] + list(extra)
        return subprocess.run(cmd, capture_output=True, text=True, env=self.env,
                              cwd=str(self.ws), timeout=120)

    def racine(self):
        # l'installateur développe ~ avec $HOME, isolé sur le dossier du test
        return self.userhome / "dispositif"

    # ------------------------------------------------------------------

    def test_structure_et_skills(self):
        res = self.run_installer()
        self.assertEqual(res.returncode, 0, res.stderr)

        skills = self.home / "skills" / "essai"
        found = sorted(p.parent.name for p in skills.glob("*/SKILL.md"))
        self.assertEqual(found, ["essai-bureau", "essai-ceo", "essai-fidelisation", "essai-voix"])

        for skill in skills.glob("*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("{{", text, "placeholder non résolu dans %s" % skill)
            desc = re.search(r"^description:\s*\"(.*)\"$", text, re.M)
            if desc is None:
                self.fail("description absente dans %s" % skill)
            self.assertLessEqual(
                len(desc.group(1)), 60,
                "description trop longue (%d) dans %s" % (len(desc.group(1)), skill),
            )

        racine = self.racine()
        for sub in ("a-valider", "livres", "archives", "cerveau", "modeles", "logs"):
            self.assertTrue((racine / sub).is_dir(), "dossier manquant : %s" % sub)
        for name in ("README.md", "config.json", "crons-a-creer.sh"):
            self.assertTrue((racine / name).exists(), "fichier manquant : %s" % name)

        # le cerveau doit être du JSON valide
        json.loads((racine / "cerveau" / "entreprise.json").read_text(encoding="utf-8"))

        # noms substitués partout
        ceo = (skills / "essai-ceo" / "SKILL.md").read_text(encoding="utf-8")
        for attendu in ("Jeanne", "Léa", "Marc", "Fidélisation", "Camille", "Atelier Roux"):
            self.assertIn(attendu, ceo)

        # script de rappel exécutable et racine substituée
        script = self.home / "scripts" / "essai-a-valider.sh"
        self.assertTrue(script.exists())
        self.assertTrue(os.access(script, os.X_OK))
        self.assertNotIn("__RACINE__", script.read_text(encoding="utf-8"))

    def test_idempotence(self):
        self.assertEqual(self.run_installer().returncode, 0)
        res = self.run_installer()
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertNotIn("écrasé", res.stdout)
        self.assertNotIn("créé", res.stdout.replace("créés", ""))
        self.assertIn("inchangé", res.stdout)

    def test_non_destructif_puis_force(self):
        self.assertEqual(self.run_installer().returncode, 0)
        skill = self.home / "skills" / "essai" / "essai-voix" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n<!-- retouche -->\n", encoding="utf-8")

        res = self.run_installer()
        self.assertEqual(res.returncode, 0)
        self.assertIn("conservé", res.stdout)
        self.assertIn("retouche", skill.read_text(encoding="utf-8"))

        res = self.run_installer("--force")
        self.assertEqual(res.returncode, 0)
        self.assertIn("écrasé", res.stdout)
        self.assertNotIn("retouche", skill.read_text(encoding="utf-8"))
        backups = list(skill.parent.glob("SKILL.md.bak-*"))
        self.assertEqual(len(backups), 1, "sauvegarde --force absente")

    def test_dry_run_n_ecrit_rien(self):
        res = self.run_installer("--dry-run")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertFalse((self.racine() / "a-valider").exists())
        self.assertFalse((self.home / "skills").exists())
        self.assertIn("créé", res.stdout)

    def test_rappel_muet_puis_bavard(self):
        self.assertEqual(self.run_installer().returncode, 0)
        script = self.home / "scripts" / "essai-a-valider.sh"
        vide = subprocess.run(["bash", str(script)], capture_output=True, text=True)
        self.assertEqual(vide.returncode, 0)
        self.assertEqual(vide.stdout.strip(), "", "le rappel doit être muet quand a-valider/ est vide")

        (self.racine() / "a-valider" / "2026-11-04__relance.md").write_text("x", encoding="utf-8")
        plein = subprocess.run(["bash", str(script)], capture_output=True, text=True)
        self.assertIn("À valider (1)", plein.stdout)
        self.assertIn("relance", plein.stdout)

    def test_config_incomplete(self):
        bad = dict(CONFIG)
        bad["entrepreneur"] = {"nom": ""}
        path = self.tmp / "bad.json"
        path.write_text(json.dumps(bad), encoding="utf-8")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("entrepreneur.nom", res.stderr)

    def test_libelle_invalide(self):
        bad = json.loads(json.dumps(CONFIG))
        bad["postes"]["troisieme"]["libelle"] = "Commercial"
        path = self.tmp / "bad2.json"
        path.write_text(json.dumps(bad), encoding="utf-8")
        res = self.run_installer(cfg=path)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Acquisition", res.stderr)

    def test_profil_dedie(self):
        res = self.run_installer("--profile", "devops")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue((self.home / "profiles" / "devops" / "skills" / "essai" / "essai-ceo" / "SKILL.md").exists())
        self.assertFalse((self.home / "skills" / "essai").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
