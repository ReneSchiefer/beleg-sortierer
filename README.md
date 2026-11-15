# Beleg-Sortierer

Kleines Werkzeug, das eingegangene Belege **nach Mandant und Belegart sortiert**
und für einen Monat eine **Liste fehlender Belege** erstellt.

> Alle Daten in diesem Projekt sind **fiktive Testdaten**. Es enthält keine echten Mandanten- oder Kundendaten.

## Live-Demo
**Zur Live-Demo: https://reneschiefer.github.io/beleg-sortierer/**

Die Demo läuft im Browser und braucht keine Installation.
Sie liegt im Ordner `docs/`. Nach Änderungen an den Testdaten: `python3 demo_daten_exportieren.py`.

## Problem
In einer Steuerkanzlei kommen Belege ungeordnet an: per Mail, Upload oder Scan, oft mit
Dateinamen wie `scan_0001.pdf`. Jemand muss jeden Beleg öffnen, dem Mandanten zuordnen,
ablegen und am Monatsende abgleichen, was noch fehlt.

## Lösung
1. **Einstellungen** (`einstellungen/*.csv`, in Excel bearbeitbar): Mandanten mit
   Erkennungsmerkmalen und den Belegen, die jeden Monat erwartet werden (Soll).
2. **Erkennen**: Das Tool liest den Inhalt jedes Belegs und sucht Mandant, Belegart und Datum.
3. **Ablegen**: Es kopiert eindeutige Belege nach `ausgabe/sortiert/<Mandant>/<Monat>/<Belegart>/`.
   Unklare Fälle und Duplikate legt es nach `ausgabe/pruefen/`. **Es wird nichts geraten.**
4. **Soll-Ist-Vergleich**: Das Ergebnis ist eine Liste fehlender Belege (CSV für Excel und HTML-Bericht).
5. **Erinnerungs-Entwürfe** pro Mandant: Sie werden **nicht automatisch versendet**. Ein Mensch prüft sie vorher.

## Sicherheitsregeln
- `eingang/` wird nie verändert, das Tool kopiert nur.
- Jede Entscheidung steht mit Begründung im Protokoll und ist dadurch nachvollziehbar.
- Alles läuft lokal. Es werden keine Daten ins Internet oder an eine KI geschickt.

## Benutzung
```bash
python3 testdaten_erzeugen.py              # fiktive Testbelege erzeugen
python3 beleg_sortierer.py --monat 2026-10 # sortieren + Fehlliste
python3 -m unittest -v                     # automatische Tests
```
Du brauchst nur Python 3.10 oder neuer. Weitere Pakete sind nicht nötig.

## Grenzen (ehrlich)
- Die Belege sind hier Textdateien, also so, als wären sie schon per Texterkennung (OCR) gelesen.
  Für echte PDFs oder Scans käme eine Texterkennung davor.
- Die Erkennung arbeitet mit Stichwörtern. Das ist einfach und nachvollziehbar, aber nicht „intelligent“.
  Neue Mandanten oder Belegarten trägt man in den CSV-Dateien nach.
- Eingangs- und Ausgangsrechnungen unterscheidet das Tool noch nicht.
