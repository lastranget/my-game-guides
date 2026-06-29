// Render-check a guide on the AYN Thor's narrow screen.
// Reports horizontal overflow at 411px and the height of every `section.screenfit`
// vs the ~418px one-screen budget (viewport 472 − 54px scroll-padding).
//
// Setup:  cd tools && npm i puppeteer-core
// Usage:  node tools/fitcheck.js guides/kofxi/kofxi-terry.html [more.html ...]
// Note: snap-confined Chromium can't read /tmp or hidden dirs — pass files under $HOME,
//       or copy them there first (this script copies into $HOME automatically).
const puppeteer = require('puppeteer-core');
const fs = require('fs'), os = require('os'), path = require('path');

const CHROME = process.env.CHROME || '/usr/bin/chromium-browser';
const files = process.argv.slice(2);
if (!files.length) { console.error('usage: node fitcheck.js <file.html> ...'); process.exit(1); }

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
    userDataDir: path.join(os.homedir(), '_fitcheck_profile'),
  });
  const page = await browser.newPage();
  for (const f of files) {
    const tmp = path.join(os.homedir(), '_fitcheck_' + path.basename(f));
    fs.copyFileSync(f, tmp);
    await page.setViewport({ width: 411, height: 472, deviceScaleFactor: 1 });
    await page.goto('file://' + tmp, { waitUntil: 'networkidle0' });
    const ov = await page.evaluate(() => {
      const d = document.documentElement;
      return { sw: d.scrollWidth, cw: d.clientWidth };
    });
    const secs = await page.evaluate(() => {
      const budget = 472 - 54;
      return [...document.querySelectorAll('section.screenfit')].map(s => {
        const h2 = s.querySelector('h2');
        const h = Math.round(s.getBoundingClientRect().bottom - h2.getBoundingClientRect().top);
        return { t: h2.textContent.replace('contents ↑', '').trim(), h, over: h > budget };
      });
    });
    const over = secs.filter(s => s.over);
    console.log(`\n## ${f}`);
    console.log(`   overflow: ${ov.sw === ov.cw ? 'OK' : 'BAD (' + ov.sw + '>' + ov.cw + ')'}`);
    console.log(`   screenfit: ${secs.length} sections, ${over.length} over ${472 - 54}px budget`);
    over.forEach(s => console.log(`     ⚠️ ${s.h}px  ${s.t}`));
    fs.unlinkSync(tmp);
  }
  await browser.close();
})();
