// Automatisch erzeugt von demo_daten_exportieren.py – FIKTIVE TESTDATEN
const DATEN = {
 "mandanten": [
  {
   "nr": "10001",
   "name": "Bäckerei Sonnenschein GmbH",
   "merkmale": [
    "Bäckerei Sonnenschein",
    "Sonnenschein GmbH",
    "Mandant 10001"
   ],
   "soll": [
    "Kontoauszug",
    "Kassenbericht",
    "Lohnabrechnung"
   ]
  },
  {
   "nr": "10002",
   "name": "Malerbetrieb Pinselstrich",
   "merkmale": [
    "Pinselstrich",
    "Mandant 10002"
   ],
   "soll": [
    "Kontoauszug",
    "Eingangsrechnung",
    "Lohnabrechnung"
   ]
  },
  {
   "nr": "10003",
   "name": "Praxis Dr. Muster",
   "merkmale": [
    "Dr. Muster",
    "Praxis Muster",
    "Mandant 10003"
   ],
   "soll": [
    "Kontoauszug",
    "Kreditkartenabrechnung"
   ]
  },
  {
   "nr": "10004",
   "name": "Café Testlauf UG",
   "merkmale": [
    "Café Testlauf",
    "Testlauf UG",
    "Mandant 10004"
   ],
   "soll": [
    "Kontoauszug",
    "Kassenbericht",
    "Eingangsrechnung"
   ]
  }
 ],
 "belegarten": [
  {
   "art": "Kontoauszug",
   "stichwoerter": [
    "Kontoauszug"
   ]
  },
  {
   "art": "Kreditkartenabrechnung",
   "stichwoerter": [
    "Kreditkartenabrechnung"
   ]
  },
  {
   "art": "Lohnabrechnung",
   "stichwoerter": [
    "Lohnabrechnung",
    "Entgeltabrechnung",
    "Verdienstabrechnung"
   ]
  },
  {
   "art": "Kassenbericht",
   "stichwoerter": [
    "Kassenbericht",
    "Kassenbuch"
   ]
  },
  {
   "art": "Eingangsrechnung",
   "stichwoerter": [
    "Rechnung"
   ]
  }
 ],
 "belege": [
  {
   "name": "Dokument.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nKontoauszug Nr. 10\nPraxis Dr. Muster\nDatum: 31.10.2026\n"
  },
  {
   "name": "IMG_2041.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nVolksbank Beispielland\nKontoauszug 10/2026\nKunde: Malerbetrieb Pinselstrich\nDatum: 30.10.2026\n"
  },
  {
   "name": "Rechnung(2).txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nFarbengroßhandel Muster KG\nRECHNUNG Nr. 2026-4471\nan: Malerbetrieb Pinselstrich\nRechnungsdatum: 14.10.2026\n20 Eimer Wandfarbe weiß  –  1.180,00 EUR netto\n"
  },
  {
   "name": "erechnung_farben.xml",
   "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- FIKTIVE TESTDATEN – KEINE ECHTE RECHNUNG (Normalfall) -->\n<Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\"\n         xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\"\n         xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\">\n  <cbc:ID>R-2026-0815</cbc:ID>\n  <cbc:IssueDate>2026-10-14</cbc:IssueDate>\n  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>\n  <cac:AccountingSupplierParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Farbenhandel Musterstadt</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingSupplierParty>\n  <cac:AccountingCustomerParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Malerbetrieb Pinselstrich</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingCustomerParty>\n  <cac:TaxTotal>\n    <cbc:TaxAmount currencyID=\"EUR\">95.00</cbc:TaxAmount>\n  </cac:TaxTotal>\n  <cac:LegalMonetaryTotal>\n    <cbc:TaxExclusiveAmount currencyID=\"EUR\">500.00</cbc:TaxExclusiveAmount>\n    <cbc:TaxInclusiveAmount currencyID=\"EUR\">595.00</cbc:TaxInclusiveAmount>\n  </cac:LegalMonetaryTotal>\n</Invoice>\n"
  },
  {
   "name": "erechnung_farben_nochmal.xml",
   "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- FIKTIVE TESTDATEN – KEINE ECHTE RECHNUNG (erneut geschickt) -->\n<Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\"\n         xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\"\n         xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\">\n  <cbc:ID>R-2026-0815</cbc:ID>\n  <cbc:IssueDate>2026-10-14</cbc:IssueDate>\n  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>\n  <cac:AccountingSupplierParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Farbenhandel Musterstadt</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingSupplierParty>\n  <cac:AccountingCustomerParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Malerbetrieb Pinselstrich</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingCustomerParty>\n  <cac:TaxTotal>\n    <cbc:TaxAmount currencyID=\"EUR\">95.00</cbc:TaxAmount>\n  </cac:TaxTotal>\n  <cac:LegalMonetaryTotal>\n    <cbc:TaxExclusiveAmount currencyID=\"EUR\">500.00</cbc:TaxExclusiveAmount>\n    <cbc:TaxInclusiveAmount currencyID=\"EUR\">595.00</cbc:TaxInclusiveAmount>\n  </cac:LegalMonetaryTotal>\n</Invoice>\n"
  },
  {
   "name": "erechnung_kaffee.xml",
   "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- FIKTIVE TESTDATEN – KEINE ECHTE RECHNUNG (Rechenfehler) -->\n<Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\"\n         xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\"\n         xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\">\n  <cbc:ID>KR-2026-77</cbc:ID>\n  <cbc:IssueDate>2026-10-20</cbc:IssueDate>\n  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>\n  <cac:AccountingSupplierParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Kaffeerösterei Beispiel</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingSupplierParty>\n  <cac:AccountingCustomerParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Café Testlauf UG</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingCustomerParty>\n  <cac:TaxTotal>\n    <cbc:TaxAmount currencyID=\"EUR\">14.00</cbc:TaxAmount>\n  </cac:TaxTotal>\n  <cac:LegalMonetaryTotal>\n    <cbc:TaxExclusiveAmount currencyID=\"EUR\">200.00</cbc:TaxExclusiveAmount>\n    <cbc:TaxInclusiveAmount currencyID=\"EUR\">241.00</cbc:TaxInclusiveAmount>\n  </cac:LegalMonetaryTotal>\n</Invoice>\n"
  },
  {
   "name": "erechnung_unbekannt.xml",
   "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- FIKTIVE TESTDATEN – KEINE ECHTE RECHNUNG (unbekannter Käufer) -->\n<Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\"\n         xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\"\n         xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\">\n  <cbc:ID>2026-1001</cbc:ID>\n  <cbc:IssueDate>2026-10-05</cbc:IssueDate>\n  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>\n  <cac:AccountingSupplierParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Bürobedarf Muster</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingSupplierParty>\n  <cac:AccountingCustomerParty>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Firma Irgendwer GmbH</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:AccountingCustomerParty>\n  <cac:TaxTotal>\n    <cbc:TaxAmount currencyID=\"EUR\">15.20</cbc:TaxAmount>\n  </cac:TaxTotal>\n  <cac:LegalMonetaryTotal>\n    <cbc:TaxExclusiveAmount currencyID=\"EUR\">80.00</cbc:TaxExclusiveAmount>\n    <cbc:TaxInclusiveAmount currencyID=\"EUR\">95.20</cbc:TaxInclusiveAmount>\n  </cac:LegalMonetaryTotal>\n</Invoice>\n"
  },
  {
   "name": "foto_ohne_datum.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nKassenbericht\nBäckerei Sonnenschein GmbH\n(Datum unleserlich)\n"
  },
  {
   "name": "kasse_sept.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nKassenbuch September 2026\nCafé Testlauf UG\nDatum: 30.09.2026\n"
  },
  {
   "name": "lohn_okt.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nLohnabrechnung Oktober 2026\nArbeitgeber: Malerbetrieb Pinselstrich\nDatum: 28.10.2026\nMitarbeiter: Max Beispiel (fiktiv)\n"
  },
  {
   "name": "sammelbeleg.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nRechnung Nr. 77\nan: Malerbetrieb Pinselstrich\nKopie an: Café Testlauf UG\nDatum: 20.10.2026\n"
  },
  {
   "name": "scan_0001.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nSparkasse Musterstadt\nKontoauszug Nr. 10/2026\nKontoinhaber: Bäckerei Sonnenschein GmbH\nDatum: 31.10.2026\nEndsaldo: 12.430,17 EUR\n"
  },
  {
   "name": "scan_0001_kopie.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nSparkasse Musterstadt\nKontoauszug Nr. 10/2026\nKontoinhaber: Bäckerei Sonnenschein GmbH\nDatum: 31.10.2026\nEndsaldo: 12.430,17 EUR\n"
  },
  {
   "name": "scan_0002.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nKassenbericht Oktober 2026\nBäckerei Sonnenschein GmbH, Filiale Hauptstraße\nDatum: 31.10.2026\nTageseinnahmen gesamt: 18.920,40 EUR\n"
  },
  {
   "name": "scan_0007.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nKontoauszug 10/2026\nCafé Testlauf UG (haftungsbeschränkt)\nDatum: 31.10.2026\n"
  },
  {
   "name": "scan_0008.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nKaffeerösterei Bohne GmbH\nRechnung Nr. 889\nLieferung an: Café Testlauf UG\nDatum: 07.10.2026\nKaffeebohnen 30 kg – 540,00 EUR netto\n"
  },
  {
   "name": "unbekannt_001.txt",
   "text": "*** FIKTIVE TESTDATEN – KEIN ECHTER BELEG ***\nRechnung Nr. 55\nan: Firma Irgendwer\nDatum: 12.10.2026\n"
  }
 ]
};
