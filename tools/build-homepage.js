// Builds site/index.html by running the CMS and capturing its export.
// Usage (from repo root):  node tools/build-homepage.js
const { JSDOM } = require('jsdom');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'cms/portico-suites-cms.html'), 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true });
setTimeout(() => {
  const site = dom.window.document.getElementById('previewFrame')?.getAttribute('srcdoc');
  if (!site || site.length < 10000) { console.error('Build FAILED: no site output'); process.exit(1); }
  fs.writeFileSync(path.join(ROOT, 'site/index.html'), site);
  console.log('site/index.html built:', Math.round(site.length / 1024) + ' KB');
  process.exit(0);
}, 1500);
