"""E-Rechnung lesen – ein eigenes Modul des Beleg-Sortierers.

Eine E-Rechnung ist wie ein Formular mit beschrifteten Kästchen (XML).
Dieses Modul liest die Kästchen ab – mit festen Regeln, OHNE KI.

Unterstützt wird hier das vereinfachte XRechnung-Format UBL (Etiketten mit cbc: und cac:).
  cbc: = ein Glas  (ein einzelner Wert, z. B. die Rechnungsnummer)
  cac: = ein Fach  (eine Gruppe, z. B. alles zum Käufer)
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Die Vorsilben cbc: und cac: sind Abkürzungen für diese langen "Adressen" (Namensräume).
# Der Computer braucht die volle Adresse, um die Etiketten sicher zu erkennen.
NAMENSRAUM = {
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
}

# Wo steht was? Der Weg durch die Fächer bis zum Glas – getrennt durch "/".
# Links unser deutscher Name, rechts die englischen Etiketten aus der E-Rechnung.
FELDER = {
    "nummer":     "cbc:ID",
    "datum":      "cbc:IssueDate",
    "verkaeufer": "cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name",
    "kaeufer":    "cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name",
    "netto":      "cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount",
    "steuer":     "cac:TaxTotal/cbc:TaxAmount",
    "brutto":     "cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount",
}


def ist_e_rechnung(datei: Path) -> bool:
    """Eine E-Rechnung erkennen wir (hier) an der Endung .xml."""
    return datei.suffix.lower() == ".xml"


def lese_e_rechnung(datei: Path) -> dict:
    """Liest alle Kästchen aus FELDER ab.
    Fehlt ein Kästchen, steht dort None – es wird nichts erfunden."""
    schrank = ET.parse(datei).getroot()          # die ganze Rechnung = der Schrank
    werte = {}
    for name, weg in FELDER.items():
        glas = schrank.find(weg, NAMENSRAUM)     # dem Weg durch die Fächer folgen
        if glas is not None and glas.text:
            werte[name] = glas.text.strip()      # Inhalt des Glases, ohne Leerzeichen
        else:
            werte[name] = None                   # Kästchen fehlt oder ist leer
    return werte
