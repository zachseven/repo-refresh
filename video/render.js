const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const FPS = 30;
  const OUT = process.env.FRAMES_DIR;
  const onlyList = process.env.ONLY ? process.env.ONLY.split(',').map(Number) : null;
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--force-color-profile=srgb', '--disable-gpu']
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'scene.html'));
  const dur = await page.evaluate(() => window.DURATION);
  const total = Math.round(dur * FPS);
  const frames = onlyList || Array.from({length: total}, (_, i) => i);
  let done = 0;
  for (const f of frames) {
    const t = f / FPS;
    await page.evaluate((tt) => window.seekTo(tt), t);
    const name = String(f).padStart(5, '0') + '.png';
    await page.screenshot({ path: path.join(OUT, name) });
    done++;
    if (done % 60 === 0) console.log(`  ${done}/${frames.length} (t=${t.toFixed(1)}s)`);
  }
  console.log(`done ${done} frames`);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
