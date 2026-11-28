# Beleg-Sortierer

Kleines Werkzeug, das eingegangene Belege **nach Mandant und Belegart sortiert**
und für einen Monat eine **Liste fehlender Belege** erstellt.
Es liest auch **E-Rechnungen** (XML) – genau statt geraten – und **rechnet sie nach**.

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

## E-Rechnungen (Modul `erechnung.py`)
Eine E-Rechnung ist wie ein Formular mit beschrifteten Kästchen (XML). Das Modul liest die Kästchen ab –
mit festen Regeln, **ohne KI** – und prüft jede E-Rechnung in dieser Reihenfolge:
1. **Lesbar?** Ist es gültiges XML?
2. **Vollständig und richtig?** Alle Angaben da, Beträge sind Zahlen, **Netto + Steuer = Brutto** (gerechnet in Cent).
3. **Für wen?** Der Mandant wird **nur beim Käufer** gesucht – der Verkäufer ist der Lieferant.
4. **Schon da?** Gleiche Rechnungsnummer vom gleichen Lieferanten → Duplikat.

Fällt eine Rechnung durch, kommt sie nach `ausgabe/pruefen/`. Alle lesbaren E-Rechnungen stehen zusätzlich
mit Lieferant, Nummer, Datum und Beträgen in der **Rechnungsliste** (`rechnungsliste_<Monat>.csv`, Beträge mit Komma für Excel).
Die vier Test-E-Rechnungen zeigen je einen Fall: Normalfall, Rechenfehler, unbekannter Käufer, Duplikat.

## Sicherheitsregeln
- `eingang/` wird nie verändert, das Tool kopiert nur.
- Jede Entscheidung steht mit Begründung im Protokoll und ist dadurch nachvollziehbar.
- Alles läuft lokal. Es werden keine Daten ins Internet oder an eine KI geschickt.

## Benutzung
```bash
python3 testdaten_erzeugen.py              # fiktive Testbelege erzeugen
python3 beleg_sortierer.py --monat 2026-10 # sortieren + Fehlliste
python3 -m unittest -v                     # automatische Tests (16)
```
Die Tests prüfen auch, ob die **Web-Demo dasselbe Ergebnis liefert wie das Python-Tool**:
- Test 7a: `docs/daten.js` passt zu `einstellungen/` und `eingang/` (läuft immer).
- Test 7b: Ein unsichtbarer Browser öffnet die Demo, sortiert und vergleicht jede Zeile mit Python
  (Protokoll und Rechnungsliste).
  Braucht Node.js und Playwright – fehlen sie, wird dieser eine Test übersprungen.
Du brauchst nur Python 3.10 oder neuer. Weitere Pakete sind nicht nötig.

## Grenzen (ehrlich)
- Die meisten Belege sind hier Textdateien, also so, als wären sie schon per Texterkennung (OCR) gelesen.
  Für echte PDFs oder Scans käme eine Texterkennung davor.
- Die E-Rechnungen sind **vereinfacht**: Aufbau einer XRechnung im Format UBL, aber nicht alle Pflichtfelder.
  Das zweite Format (CII, z. B. in ZUGFeRD-PDFs) wird noch nicht gelesen. Eine E-Rechnung wird an der Endung `.xml` erkannt.
- Bei E-Rechnungen wird der Mandant nur als Käufer gesucht. Ausgangsrechnungen eines Mandanten landen deshalb bei „prüfen“.
- Die Erkennung arbeitet mit Stichwörtern. Das ist einfach und nachvollziehbar, aber nicht „intelligent“.
  Neue Mandanten oder Belegarten trägt man in den CSV-Dateien nach.
- Bei Textbelegen unterscheidet das Tool Eingangs- und Ausgangsrechnungen noch nicht.

## Rechte
© 2026 René Schiefer – **alle Rechte vorbehalten.**
Ansehen und Ausprobieren der Demo sind erlaubt. Kopieren, Weitergeben oder Nutzen des Codes – auch in Teilen
oder abgewandelt – nur mit meiner vorherigen schriftlichen Erlaubnis.
Dieses Projekt steht ausdrücklich **nicht** unter einer Open-Source-Lizenz.
