"""Beleg-Sortierer – sortiert eingegangene Belege nach Mandant und Belegart
und erstellt eine Liste der fehlenden Belege für einen Monat.

Aufruf:   python3 beleg_sortierer.py --monat 2026-10

Ablauf in 5 Schritten:
  1. Einstellungen lesen   (welche Mandanten, welche Belegarten, was wird erwartet)
  2. Jeden Beleg erkennen  (Mandant, Belegart, Datum – anhand des Inhalts;
                           E-Rechnungen: Kästchen ablesen und nachrechnen, Modul erechnung.py)
  3. Kopieren              (in ausgabe/sortiert/... oder ausgabe/pruefen/...)
  4. Soll mit Ist vergleichen -> Liste fehlender Belege
  5. Berichte schreiben    (CSV für Excel + HTML-Übersicht + Erinnerungs-ENTWÜRFE)

Sicherheitsregeln im Code:
  - Der Ordner 'eingang/' wird nie verändert. Das Tool KOPIERT nur.
  - Unklare Fälle werden nicht geraten, sondern landen in 'pruefen/'.
  - Erinnerungen an Mandanten sind nur Entwürfe. Ein Mensch prüft und versendet.
  - Es wird nichts ins Internet geschickt. Alles läuft lokal.
"""

import argparse
import csv
import hashlib
import html
import re
import shutil
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

import erechnung

ORDNER = Path(__file__).parent
EINGANG = ORDNER / "eingang"
AUSGABE = ORDNER / "ausgabe"
EINSTELLUNGEN = ORDNER / "einstellungen"


# ---------------------------------------------------------------------------
# Schritt 1: Einstellungen lesen
# ---------------------------------------------------------------------------
def lese_csv(datei: Path) -> list[dict]:
    with open(datei, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def lade_mandanten() -> list[dict]:
    mandanten = []
    for zeile in lese_csv(EINSTELLUNGEN / "mandanten.csv"):
        mandanten.append({
            "nr": zeile["Mandantennummer"],
            "name": zeile["Name"],
            "merkmale": zeile["Erkennungsmerkmale"].split("|"),
            "soll": zeile["Soll-Belege pro Monat"].split("|"),
        })
    return mandanten


def lade_belegarten() -> list[dict]:
    # Reihenfolge = Priorität: Die erste passende Belegart gewinnt.
    # Deshalb steht "Rechnung" (sehr allgemein) ganz unten, sonst würde
    # z. B. eine "Kreditkartenabrechnung" fälschlich als Rechnung erkannt.
    return [
        {"art": z["Belegart"], "stichwoerter": z["Stichwörter"].split("|")}
        for z in lese_csv(EINSTELLUNGEN / "belegarten.csv")
    ]


# ---------------------------------------------------------------------------
# Schritt 2: Einen Beleg erkennen
# ---------------------------------------------------------------------------
def erkenne_mandant(text: str, mandanten: list[dict]):
    """Gibt (mandant, begruendung) zurück. mandant ist None, wenn unklar."""
    treffer = []
    for m in mandanten:
        gefunden = [w for w in m["merkmale"] if w.lower() in text.lower()]
        if gefunden:
            treffer.append((m, gefunden[0]))
    if len(treffer) == 1:
        m, wort = treffer[0]
        return m, f"Mandant über '{wort}' erkannt"
    if not treffer:
        return None, "kein Mandant erkannt"
    namen = ", ".join(m["name"] for m, _ in treffer)
    return None, f"mehrere Mandanten möglich ({namen})"


def erkenne_belegart(text: str, belegarten: list[dict]):
    for b in belegarten:
        for wort in b["stichwoerter"]:
            if wort.lower() in text.lower():
                return b["art"], f"Belegart über '{wort}' erkannt"
    return None, "keine Belegart erkannt"


DATUM_MUSTER = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")


def erkenne_monat(text: str):
    """Sucht das erste Datum im Format TT.MM.JJJJ und gibt 'JJJJ-MM' zurück."""
    treffer = DATUM_MUSTER.search(text)
    if not treffer:
        return None, "kein Datum erkannt"
    tag, monat, jahr = treffer.groups()
    return f"{jahr}-{monat}", f"Datum {tag}.{monat}.{jahr}"


def pruefsumme(datei: Path) -> str:
    """Fingerabdruck des Inhalts. Gleicher Inhalt = gleiche Prüfsumme = Duplikat."""
    return hashlib.sha256(datei.read_bytes()).hexdigest()


def entscheide_textbeleg(datei: Path, mandanten, belegarten):
    """Textbeleg: Mandant, Belegart und Monat über Stichwörter suchen (wie bisher)."""
    text = datei.read_text(encoding="utf-8")
    mandant, grund_m = erkenne_mandant(text, mandanten)
    art, grund_a = erkenne_belegart(text, belegarten)
    beleg_monat, grund_d = erkenne_monat(text)
    if mandant is None:
        status, grund = "Prüfen", grund_m
    elif art is None:
        status, grund = "Prüfen", grund_a
    elif beleg_monat is None:
        status, grund = "Prüfen", grund_d
    else:
        status, grund = "Sortiert", f"{grund_m}; {grund_a}; {grund_d}"
    return mandant, art, beleg_monat, status, grund


def entscheide_e_rechnung(datei: Path, mandanten, rechnungen: dict):
    """E-Rechnung: Kästchen ablesen statt suchen – dann prüfen und zuordnen.
    Reihenfolge: lesbar? → vollständig und richtig gerechnet? → Mandant (= Käufer)? → doppelt?"""
    art = "Eingangsrechnung"   # Käufer ist unser Mandant → er hat eingekauft
    try:
        werte = erechnung.lese_e_rechnung(datei)
    except ET.ParseError:
        return None, art, None, "Prüfen", "E-Rechnung nicht lesbar (kein gültiges XML)"
    beleg_monat = erechnung.monat_aus_datum(werte["datum"])

    fehler = erechnung.pruefe_e_rechnung(werte)
    if fehler:
        return None, art, beleg_monat, "Prüfen", fehler

    # Nur im Fach "Käufer" nach dem Mandanten suchen – der Verkäufer ist der Lieferant
    mandant, grund_m = erkenne_mandant(werte["kaeufer"], mandanten)
    if mandant is None:
        return None, art, beleg_monat, "Prüfen", f"E-Rechnung: Käufer '{werte['kaeufer']}' – {grund_m}"

    schluessel = (werte["verkaeufer"], werte["nummer"])
    if schluessel in rechnungen:
        return (mandant, art, beleg_monat, "Duplikat",
                f"gleiche Rechnungsnummer {werte['nummer']} von {werte['verkaeufer']} wie {rechnungen[schluessel]}")
    rechnungen[schluessel] = datei.name

    grund = (f"E-Rechnung: {grund_m} (Käufer); Rechnung {werte['nummer']} rechnet "
             f"({werte['netto']} + {werte['steuer']} = {werte['brutto']}); Datum {werte['datum']}")
    return mandant, art, beleg_monat, "Sortiert", grund


# ---------------------------------------------------------------------------
# Hauptablauf
# ---------------------------------------------------------------------------
def verarbeite(monat: str) -> dict:
    mandanten = lade_mandanten()
    belegarten = lade_belegarten()

    # Ausgabe-Ordner bei jedem Lauf neu anlegen (eingang/ bleibt unberührt)
    if AUSGABE.exists():
        shutil.rmtree(AUSGABE)
    (AUSGABE / "sortiert").mkdir(parents=True)
    (AUSGABE / "pruefen").mkdir()

    protokoll = []      # eine Zeile pro Beleg: was wurde erkannt und warum
    gesehen = {}        # Prüfsumme -> Dateiname (für Duplikate)
    rechnungen = {}     # (Lieferant, Rechnungsnummer) -> Dateiname (Duplikate bei E-Rechnungen)
    eingegangen = set() # (Mandantennummer, Belegart) im gewählten Monat

    # Textbelege (.txt) und E-Rechnungen (.xml), sortiert nach Dateiname
    alle = list(EINGANG.glob("*.txt")) + list(EINGANG.glob("*.xml"))
    for datei in sorted(alle, key=lambda d: d.name):
        # Schritt 2 + 3: erkennen und entscheiden – E-Rechnung oder Textbeleg?
        if erechnung.ist_e_rechnung(datei):
            mandant, art, beleg_monat, status, grund = entscheide_e_rechnung(datei, mandanten, rechnungen)
        else:
            mandant, art, beleg_monat, status, grund = entscheide_textbeleg(datei, mandanten, belegarten)

        # Genau gleicher Inhalt wie ein früherer Beleg (Fingerabdruck)? → Duplikat
        summe = pruefsumme(datei)
        if summe in gesehen:
            status, grund = "Duplikat", f"gleicher Inhalt wie {gesehen[summe]}"
        gesehen.setdefault(summe, datei.name)

        if status == "Sortiert":
            ziel = (AUSGABE / "sortiert" / f"{mandant['nr']}_{mandant['name']}"
                    / beleg_monat / art)
            if beleg_monat == monat:
                eingegangen.add((mandant["nr"], art))
        else:
            ziel = AUSGABE / "pruefen" / ("duplikate" if status == "Duplikat" else "unklar")
        ziel.mkdir(parents=True, exist_ok=True)
        shutil.copy2(datei, ziel / datei.name)

        protokoll.append({
            "Datei": datei.name,
            "Mandant": f"{mandant['nr']} {mandant['name']}" if mandant else "",
            "Belegart": art or "",
            "Monat": beleg_monat or "",
            "Status": status,
            "Begründung": grund,
        })

    # Schritt 4: Soll-Ist-Vergleich
    fehlend = []
    for m in mandanten:
        for soll_art in m["soll"]:
            if (m["nr"], soll_art) not in eingegangen:
                fehlend.append({"Mandantennummer": m["nr"], "Mandant": m["name"],
                                "Monat": monat, "Fehlender Beleg": soll_art})

    return {"monat": monat, "mandanten": mandanten,
            "protokoll": protokoll, "fehlend": fehlend}


# ---------------------------------------------------------------------------
# Schritt 5: Berichte schreiben
# ---------------------------------------------------------------------------
def schreibe_csv(datei: Path, zeilen: list[dict]) -> None:
    if not zeilen:
        datei.write_text("Keine Einträge\n", encoding="utf-8-sig")
        return
    # utf-8-sig + Semikolon: so öffnet deutsches Excel die Datei korrekt
    with open(datei, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=zeilen[0].keys(), delimiter=";")
        w.writeheader()
        w.writerows(zeilen)


def tabelle_html(zeilen: list[dict]) -> str:
    if not zeilen:
        return "<p>Keine Einträge.</p>"
    kopf = "".join(f"<th>{html.escape(k)}</th>" for k in zeilen[0])
    rumpf = ""
    for z in zeilen:
        klasse = z.get("Status", "").lower()
        zellen = "".join(f"<td>{html.escape(str(v))}</td>" for v in z.values())
        rumpf += f'<tr class="{klasse}">{zellen}</tr>'
    return f"<table><tr>{kopf}</tr>{rumpf}</table>"


def schreibe_berichte(e: dict) -> None:
    monat, protokoll, fehlend = e["monat"], e["protokoll"], e["fehlend"]
    schreibe_csv(AUSGABE / f"protokoll_{monat}.csv", protokoll)
    schreibe_csv(AUSGABE / f"fehlende_belege_{monat}.csv", fehlend)

    # Erinnerungs-Entwürfe pro Mandant (werden NICHT automatisch versendet)
    entwuerfe = AUSGABE / "erinnerungs_entwuerfe"
    entwuerfe.mkdir()
    for m in e["mandanten"]:
        offen = [f["Fehlender Beleg"] for f in fehlend if f["Mandantennummer"] == m["nr"]]
        if not offen:
            continue
        liste = "\n".join(f"  - {a}" for a in offen)
        (entwuerfe / f"{m['nr']}_{monat}.txt").write_text(
            "ENTWURF – vor dem Versand von einem Menschen prüfen!\n\n"
            f"Betreff: Fehlende Unterlagen {monat}\n\n"
            f"Guten Tag,\n\nfür {m['name']} fehlen uns für {monat} noch:\n{liste}\n\n"
            "Bitte reichen Sie diese Unterlagen nach. Vielen Dank!\n",
            encoding="utf-8")

    zaehler = {}
    for z in protokoll:
        zaehler[z["Status"]] = zaehler.get(z["Status"], 0) + 1
    kacheln = "".join(f"<div class='kachel'><b>{n}</b><br>{s}</div>"
                      for s, n in zaehler.items())
    kacheln += f"<div class='kachel fehlt'><b>{len(fehlend)}</b><br>fehlende Belege</div>"

    seite = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Belegübersicht {monat}</title><style>
body{{font-family:system-ui,sans-serif;margin:2rem;color:#222;background:#fff}}
table{{border-collapse:collapse;width:100%;margin-bottom:2rem;font-size:.9rem}}
th,td{{border:1px solid #ccc;padding:.4rem .6rem;text-align:left}}
th{{background:#f0f0f0}} tr.prüfen td{{background:#fff4d6}}
tr.duplikat td{{background:#eee;color:#666}}
.kachel{{display:inline-block;border:1px solid #ccc;border-radius:8px;padding:.6rem 1rem;margin:0 .5rem 1rem 0;text-align:center}}
.kachel b{{font-size:1.6rem}} .fehlt{{border-color:#c33;color:#c33}}
.hinweis{{color:#666;font-size:.85rem}}
</style></head><body>
<h1>Belegübersicht {monat}</h1>
<p class="hinweis">Fiktive Testdaten · erstellt {datetime.now():%d.%m.%Y %H:%M}</p>
{kacheln}
<h2>Fehlende Belege</h2>{tabelle_html(fehlend)}
<h2>Alle eingegangenen Belege</h2>{tabelle_html(protokoll)}
</body></html>"""
    (AUSGABE / f"bericht_{monat}.html").write_text(seite, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Belege sortieren und fehlende Belege finden")
    parser.add_argument("--monat", required=True, help="Abrechnungsmonat im Format JJJJ-MM, z. B. 2026-10")
    args = parser.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}", args.monat):
        parser.error("Monat bitte im Format JJJJ-MM angeben, z. B. 2026-10")

    ergebnis = verarbeite(args.monat)
    schreibe_berichte(ergebnis)

    print(f"\nBelege verarbeitet: {len(ergebnis['protokoll'])}")
    for z in ergebnis["protokoll"]:
        print(f"  {z['Status']:9} {z['Datei']:24} {z['Begründung']}")
    print(f"\nFehlende Belege für {args.monat}: {len(ergebnis['fehlend'])}")
    for f in ergebnis["fehlend"]:
        print(f"  {f['Mandant']:28} {f['Fehlender Beleg']}")
    print(f"\nBericht: {AUSGABE / ('bericht_' + args.monat + '.html')}")


if __name__ == "__main__":
    main()
