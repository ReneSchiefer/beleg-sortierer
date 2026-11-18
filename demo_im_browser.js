// Hilfsprogramm für Test 7b: öffnet die Web-Demo in einem unsichtbaren Browser,
// klickt für jeden Monat auf "Belege sortieren" und gibt das Protokoll als JSON aus.
// Läuft nur, wo Node.js und Playwright installiert sind. Sonst überspringt Python den Test.
// Aufruf: node demo_im_browser.js 2026-10 2026-09
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const browser = await chromium.launch();
  const seite = await browser.newPage();
  const fehler = [];
  seite.on("pageerror", (e) => fehler.push(e.message)); // JavaScript-Fehler mitschreiben

  await seite.goto("file://" + path.join(__dirname, "docs", "index.html"));
  const ergebnis = {};
  for (const monat of process.argv.slice(2)) {
    await seite.selectOption("#monat", monat); // Monat wählen
    await seite.click("#los");                 // "Belege sortieren" klicken
    // Jede Tabellenzeile im Protokoll als Liste ihrer Zellen auslesen
    ergebnis[monat] = await seite.$$eval("#protokoll tr", (zeilen) =>
      zeilen
        .map((z) => [...z.querySelectorAll("td")].map((td) => td.innerText.trim()))
        .filter((zellen) => zellen.length > 0)
    );
  }
  console.log(JSON.stringify({ ergebnis, fehler }));
  await browser.close();
})();
