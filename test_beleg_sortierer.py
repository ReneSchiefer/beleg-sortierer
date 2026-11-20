"""Automatische Tests: prüfen, ob das Tool mit den Testdaten das Richtige tut.

Aufruf:  python3 -m unittest -v
"""

import json
import shutil
import subprocess
import unittest

import beleg_sortierer as bs
import demo_daten_exportieren
import erechnung
import testdaten_erzeugen


def browser_test_moeglich() -> bool:
    """Test 7b braucht Node.js und Playwright (ein Werkzeug, das einen Browser fernsteuert)."""
    if not shutil.which("node"):
        return False
    probe = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True)
    return probe.returncode == 0


class TestBelegSortierer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testdaten_erzeugen.main()
        cls.e = bs.verarbeite("2026-10")
        cls.status = {z["Datei"]: z["Status"] for z in cls.e["protokoll"]}

    def test_alle_belege_verarbeitet(self):
        self.assertEqual(len(self.e["protokoll"]), 17)  # 13 Textbelege + 4 E-Rechnungen

    def test_fehlende_belege_richtig(self):
        fehlend = {(f["Mandant"], f["Fehlender Beleg"]) for f in self.e["fehlend"]}
        self.assertEqual(fehlend, {
            ("Bäckerei Sonnenschein GmbH", "Lohnabrechnung"),
            ("Praxis Dr. Muster", "Kreditkartenabrechnung"),
            ("Café Testlauf UG", "Kassenbericht"),  # September zählt nicht für Oktober
        })

    def test_unklare_faelle_werden_nicht_geraten(self):
        for datei in ["unbekannt_001.txt", "foto_ohne_datum.txt", "sammelbeleg.txt"]:
            self.assertEqual(self.status[datei], "Prüfen", datei)

    def test_duplikat_erkannt(self):
        self.assertEqual(self.status["scan_0001_kopie.txt"], "Duplikat")

    def test_eingang_bleibt_unveraendert(self):
        self.assertEqual(len(list(bs.EINGANG.glob("*.txt"))), 13)
        self.assertEqual(len(list(bs.EINGANG.glob("*.xml"))), 4)

    def test_kreditkarte_ist_keine_rechnung(self):
        arten = [{"art": "Kreditkartenabrechnung", "stichwoerter": ["Kreditkartenabrechnung"]},
                 {"art": "Eingangsrechnung", "stichwoerter": ["Rechnung"]}]
        art, _ = bs.erkenne_belegart("Kreditkartenabrechnung Oktober", arten)
        self.assertEqual(art, "Kreditkartenabrechnung")


    # --- Test 7: Web-Demo und Python-Tool müssen dasselbe Ergebnis liefern ---------------

    def test_7a_demo_hat_aktuelle_daten(self):
        """Die Demo liest docs/daten.js. Diese Datei muss zu einstellungen/ und eingang/ passen.
        Schlägt fehl, wenn jemand vergessen hat: python3 demo_daten_exportieren.py"""
        text = (bs.ORDNER / "docs" / "daten.js").read_text(encoding="utf-8")
        json_teil = text.split("const DATEN = ", 1)[1].rstrip().rstrip(";")
        self.assertEqual(json.loads(json_teil), demo_daten_exportieren.erzeuge_daten())

    @unittest.skipUnless(browser_test_moeglich(), "kein Node.js/Playwright – Browser-Test übersprungen")
    def test_7b_demo_sortiert_wie_python(self):
        """Ein unsichtbarer Browser öffnet die Demo und sortiert. Jede Zeile muss gleich sein."""
        monate = ["2026-10", "2026-09"]
        lauf = subprocess.run(["node", str(bs.ORDNER / "demo_im_browser.js"), *monate],
                              capture_output=True, text=True, check=True)
        demo = json.loads(lauf.stdout)
        self.assertEqual(demo["fehler"], [], "JavaScript-Fehler in der Demo")
        for monat in monate:
            python = [[z["Datei"], z["Mandant"], z["Belegart"], z["Monat"], z["Status"], z["Begründung"]]
                      for z in bs.verarbeite(monat)["protokoll"]]
            self.assertEqual(demo["ergebnis"][monat], python, monat)


    # --- E-Rechnung (Modul erechnung.py) --------------------------------------------------

    def test_erechnung_wird_richtig_gelesen(self):
        """Alle Kästchen der Normalfall-Rechnung werden genau abgelesen."""
        werte = erechnung.lese_e_rechnung(bs.EINGANG / "erechnung_farben.xml")
        self.assertEqual(werte, {
            "nummer": "R-2026-0815", "datum": "2026-10-14",
            "verkaeufer": "Farbenhandel Musterstadt", "kaeufer": "Malerbetrieb Pinselstrich",
            "netto": "500.00", "steuer": "95.00", "brutto": "595.00",
        })

    def test_erechnung_normalfall_wird_sortiert(self):
        zeile = next(z for z in self.e["protokoll"] if z["Datei"] == "erechnung_farben.xml")
        self.assertEqual((zeile["Status"], zeile["Mandant"], zeile["Belegart"], zeile["Monat"]),
                         ("Sortiert", "10002 Malerbetrieb Pinselstrich", "Eingangsrechnung", "2026-10"))

    def test_erechnung_mit_rechenfehler_geht_zum_menschen(self):
        self.assertEqual(self.status["erechnung_kaffee.xml"], "Prüfen")

    def test_erechnung_unbekannter_kaeufer_wird_nicht_geraten(self):
        self.assertEqual(self.status["erechnung_unbekannt.xml"], "Prüfen")

    def test_erechnung_gleiche_rechnungsnummer_ist_duplikat(self):
        self.assertEqual(self.status["erechnung_farben_nochmal.xml"], "Duplikat")

    def test_pruefung_findet_fehlende_angabe(self):
        werte = {"nummer": None, "datum": "2026-10-01", "verkaeufer": "A", "kaeufer": "B",
                 "netto": "10.00", "steuer": "1.90", "brutto": "11.90"}
        self.assertIn("Angabe fehlt (nummer)", erechnung.pruefe_e_rechnung(werte))
        werte["nummer"] = "X-1"
        self.assertIsNone(erechnung.pruefe_e_rechnung(werte))   # jetzt ist alles in Ordnung

    def test_erechnung_erkannt_textbeleg_nicht(self):
        self.assertTrue(erechnung.ist_e_rechnung(bs.EINGANG / "erechnung_farben.xml"))
        self.assertFalse(erechnung.ist_e_rechnung(bs.EINGANG / "scan_0001.txt"))


if __name__ == "__main__":
    unittest.main()
