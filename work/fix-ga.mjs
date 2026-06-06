import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const gaMeasurementId = 'G-SYD7WCD35C';
const indexPath = join(process.cwd(), 'outputs', 'deploy', 'index.html');
let html = await readFile(indexPath, 'utf8');

const gtagSnippet = `<script async src="https://www.googletagmanager.com/gtag/js?id=${gaMeasurementId}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '${gaMeasurementId}');
</script>`;

html = html.replace(/<script async src="https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=G-[A-Z0-9]+"><\/script>\s*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*gtag\('js', new Date\(\)\);\s*gtag\('config', 'G-[A-Z0-9]+'\);\s*<\/script>\s*/g, '');

html = html.replace('</head>', `${gtagSnippet}\n</head>`);
html = html.replace("gaMeasurementId: ''", "gaMeasurementId: ''");
await writeFile(indexPath, html, 'utf8');
