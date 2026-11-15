"""Automatische Tests: prüfen, ob das Tool mit den Testdaten das Richtige tut.

Aufruf:  python3 -m unittest -v
"""

import unittest

import beleg_sortierer as bs
import testdaten_erzeugen


class TestBelegSortierer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testdaten_erzeugen.main()
        cls.e = bs.verarbeite("2026-10")
        cls.status = {z["Datei"]: z["Status"] for z in cls.e["protokoll"]}

    def test_alle_belege_verarbeitet(self):
        self.assertEqual(len(self.e["protokoll"]), 13)

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

    def test_kreditkarte_ist_keine_rechnung(self):
        arten = [{"art": "Kreditkartenabrechnung", "stichwoerter": ["Kreditkartenabrechnung"]},
                 {"art": "Eingangsrechnung", "stichwoerter": ["Rechnung"]}]
        art, _ = bs.erkenne_belegart("Kreditkartenabrechnung Oktober", arten)
        self.assertEqual(art, "Kreditkartenabrechnung")


if __name__ == "__main__":
    unittest.main()
