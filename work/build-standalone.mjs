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
/* Keep the Codex input-first UX on every viewport in the deployed build. */
.input-panel.input-open + .results { display: none; }
body:has(.input-panel.input-open) .mobile-bottom-bar { display: none; }
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
await writeFile(join(root, 'outputs', 'toesanai-standalone.html'), standalone, 'utf8');
