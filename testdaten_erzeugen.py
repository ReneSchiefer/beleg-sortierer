"""Erzeugt FIKTIVE Testbelege im Ordner 'eingang/'.

Alle Namen, Nummern und Beträge sind erfunden. Es gibt hier keine echten
Kunden- oder Mandantendaten.

Die Belege sind einfache Textdateien. Sie stehen für Belege, die schon
eingescannt und per Texterkennung (OCR) gelesen wurden.
Die Dateinamen sind absichtlich unordentlich (scan_0003.txt, IMG_2041.txt ...),
so wie sie in der Praxis per Mail oder Scanner ankommen. Das Tool erkennt
Mandant und Belegart deshalb am INHALT, nicht am Dateinamen.
"""

from pathlib import Path
import shutil

HINWEIS = "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***"

BELEGE = {
    # --- Bäckerei Sonnenschein (10001): Lohnabrechnung FEHLT ---
    "scan_0001.txt": """Sparkasse Musterstadt
Kontoauszug Nr. 10/2026
Kontoinhaber: Bäckerei Sonnenschein GmbH
Datum: 31.10.2026
Endsaldo: 12.430,17 EUR""",
    "scan_0002.txt": """Kassenbericht Oktober 2026
Bäckerei Sonnenschein GmbH, Filiale Hauptstraße
Datum: 31.10.2026
Tageseinnahmen gesamt: 18.920,40 EUR""",

    # --- Malerbetrieb Pinselstrich (10002): alles da ---
    "IMG_2041.txt": """Volksbank Beispielland
Kontoauszug 10/2026
Kunde: Malerbetrieb Pinselstrich
Datum: 30.10.2026""",
    "Rechnung(2).txt": """Farbengroßhandel Muster KG
RECHNUNG Nr. 2026-4471
an: Malerbetrieb Pinselstrich
Rechnungsdatum: 14.10.2026
20 Eimer Wandfarbe weiß  –  1.180,00 EUR netto""",
    "lohn_okt.txt": """Lohnabrechnung Oktober 2026
Arbeitgeber: Malerbetrieb Pinselstrich
Datum: 28.10.2026
Mitarbeiter: Max Beispiel (fiktiv)""",

    # --- Praxis Dr. Muster (10003): Kreditkartenabrechnung FEHLT ---
    "Dokument.txt": """Kontoauszug Nr. 10
Praxis Dr. Muster
Datum: 31.10.2026""",

    # --- Café Testlauf (10004): Kassenbericht FEHLT, ---
    # --- dafür liegt ein Kassenbericht aus SEPTEMBER vor (falscher Monat) ---
    "scan_0007.txt": """Kontoauszug 10/2026
Café Testlauf UG (haftungsbeschränkt)
Datum: 31.10.2026""",
    "scan_0008.txt": """Kaffeerösterei Bohne GmbH
Rechnung Nr. 889
Lieferung an: Café Testlauf UG
Datum: 07.10.2026
Kaffeebohnen 30 kg – 540,00 EUR netto""",
    "kasse_sept.txt": """Kassenbuch September 2026
Café Testlauf UG
Datum: 30.09.2026""",

    # --- Problemfälle, die ein Mensch prüfen muss ---
    # 1) Absender unbekannt -> kein Mandant erkennbar
    "unbekannt_001.txt": """Rechnung Nr. 55
an: Firma Irgendwer
Datum: 12.10.2026""",
    # 2) Kein Datum erkennbar
    "foto_ohne_datum.txt": """Kassenbericht
Bäckerei Sonnenschein GmbH
(Datum unleserlich)""",
    # 3) Zwei Mandanten in einem Beleg -> unklar
    "sammelbeleg.txt": """Rechnung Nr. 77
an: Malerbetrieb Pinselstrich
Kopie an: Café Testlauf UG
Datum: 20.10.2026""",
}

# Eine Datei kommt doppelt an (z. B. per Mail UND per Upload)
DUPLIKATE = {"scan_0001_kopie.txt": "scan_0001.txt"}


def main() -> None:
    eingang = Path(__file__).parent / "eingang"
    if eingang.exists():
        shutil.rmtree(eingang)
    eingang.mkdir()

    for name, text in BELEGE.items():
        (eingang / name).write_text(f"{HINWEIS}\n{text}\n", encoding="utf-8")
    for kopie, original in DUPLIKATE.items():
        shutil.copy(eingang / original, eingang / kopie)

    print(f"{len(BELEGE) + len(DUPLIKATE)} fiktive Testbelege in {eingang} erzeugt.")


if __name__ == "__main__":
    main()
