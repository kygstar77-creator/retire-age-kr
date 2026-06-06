import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const gaMeasurementId = 'G-0NB0Z9WHH0';
const indexPath = join(process.cwd(), 'outputs', 'deploy', 'index.html');
let html = await readFile(indexPath, 'utf8');

const gtagSnippet = `<script async src="https://www.googletagmanager.com/gtag/js?id=${gaMeasurementId}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '${gaMeasurementId}');
</script>`;

if (!html.includes(`gtag/js?id=${gaMeasurementId}`)) {
  html = html.replace('</head>', `${gtagSnippet}\n</head>`);
}

html = html.replace("gaMeasurementId: ''", "gaMeasurementId: ''");
await writeFile(indexPath, html, 'utf8');
