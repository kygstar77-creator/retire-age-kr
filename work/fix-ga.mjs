import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const gaMeasurementId = 'G-0NB0Z9WHH0';
const indexPath = join(process.cwd(), 'outputs', 'deploy', 'index.html');
let html = await readFile(indexPath, 'utf8');
html = html.replace("gaMeasurementId: ''", `gaMeasurementId: '${gaMeasurementId}'`);
await writeFile(indexPath, html, 'utf8');
