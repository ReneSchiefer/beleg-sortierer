"""Überträgt Einstellungen und Testbelege in die Web-Demo (docs/daten.js).

So nutzen Python-Tool und Web-Demo immer dieselben Testdaten.
Aufruf:  python3 demo_daten_exportieren.py
"""

import json

import beleg_sortierer as bs


def erzeuge_daten() -> dict:
    """Sammelt Einstellungen und Testbelege – genau das, was die Demo braucht.
    Der Test 7 nutzt diese Funktion, um zu prüfen, ob docs/daten.js aktuell ist."""
    return {
        "mandanten": bs.lade_mandanten(),
        "belegarten": bs.lade_belegarten(),
        "belege": [
            {"name": d.name, "text": d.read_text(encoding="utf-8")}
            for d in sorted(bs.EINGANG.glob("*.txt"))
        ],
    }


def main() -> None:
    daten = erzeuge_daten()
    ziel = bs.ORDNER / "docs" / "daten.js"
    ziel.parent.mkdir(exist_ok=True)
    ziel.write_text(
        "// Automatisch erzeugt von demo_daten_exportieren.py – FIKTIVE TESTDATEN\n"
        "const DATEN = " + json.dumps(daten, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    print(f"{len(daten['belege'])} Testbelege nach {ziel} exportiert.")


if __name__ == "__main__":
    main()
