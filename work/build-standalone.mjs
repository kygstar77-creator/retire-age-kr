import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';

const root = process.cwd();
const css = await readFile(join(root, 'src/styles.css'), 'utf8');
const simulator = await readFile(join(root, 'src/utils/retirementSimulator.js'), 'utf8');
const formatters = await readFile(join(root, 'src/utils/formatters.js'), 'utf8');
const shareState = await readFile(join(root, 'src/utils/shareState.js'), 'utf8');
const preview = await readFile(join(root, 'src/preview.js'), 'utf8');
const html = await readFile(join(root, 'local-preview.html'), 'utf8');

const inputFirstUx = `
@media (max-width: 680px) {
  .input-panel.input-open + .results { display: none; }
  body:has(.input-panel.input-open) .mobile-bottom-bar { display: none; }
}
.icon-button,
.mobile-step-actions button,
.mobile-bottom-bar button,
.growth-actions button,
.growth-actions a {
  align-items: center;
  justify-content: center;
  text-align: center;
  line-height: 1.2;
  white-space: nowrap;
}
.mobile-toggle { min-width: 86px; padding: 0 12px; }
.strip-card > span { min-width: 44px; width: auto; padding: 0 8px; text-align: center; word-break: keep-all; white-space: nowrap; font-size: 12px; }
.summary-card .card-top { justify-content: flex-end; }
.summary-card .card-icon { display: none; }
`;

const bundledSimulator = simulator.replaceAll('export ', '');
const bundledFormatters = formatters.replaceAll('export ', '');
const bundledShareState = shareState.replaceAll('export ', '');
const bundledPreview = preview
  .split('\n')
  .filter((line) => !line.trim().startsWith('import '))
  .join('\n');

const standalone = html
  .replace('<link rel="stylesheet" href="/src/styles.css" />', `<style>\n${css}\n${inputFirstUx}\n</style>`)
  .replace('<script type="module" src="/src/preview.js"></script>', `<script type="module">\n${bundledSimulator}\n${bundledFormatters}\n${bundledShareState}\n${bundledPreview}\n</script>`);

await mkdir(join(root, 'outputs'), { recursive: true });
await writeFile(join(root, 'outputs/toesanai-standalone.html'), standalone, 'utf8');
