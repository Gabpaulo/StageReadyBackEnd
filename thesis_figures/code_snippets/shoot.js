// Screenshot each html/listing_*.html card to a PNG at 2x.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const pg = await b.newPage({ deviceScaleFactor: 2, viewport: { width: 1400, height: 800 } });
  for (const f of fs.readdirSync(path.join(out, 'html')).filter(f => f.endsWith('.html'))) {
    await pg.setContent(fs.readFileSync(path.join(out, 'html', f), 'utf8'));
    await pg.evaluate(() => document.fonts.ready);
    await pg.locator('#card').screenshot({ path: path.join(out, f.replace('.html', '.png')) });
  }
  await b.close();
})();
