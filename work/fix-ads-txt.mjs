import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const deploy = join(process.cwd(), 'outputs', 'deploy');
await mkdir(deploy, { recursive: true });
await writeFile(
  join(deploy, 'ads.txt'),
  'google.com, pub-3225798545626010, DIRECT, f08c47fec0942fa0\n',
  'utf8'
);
