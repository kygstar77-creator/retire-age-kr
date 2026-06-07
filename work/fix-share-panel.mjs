import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const indexPath = join(process.cwd(), 'outputs', 'deploy', 'index.html');
let html = await readFile(indexPath, 'utf8');

html = html
  .replaceAll('공유</p><h2>링크 하나로 바로 계산하게 만들기</h2><p>카톡, 커뮤니티, 블로그에서 누르면 앱 설치 없이 모바일 화면에서 바로 열립니다. 입력값도 링크에 담아 비교 시나리오로 공유할 수 있습니다.</p>', '공유</p><h2>깔끔하게 복사해서 공유하기</h2><p>긴 입력값 링크 대신 기본 주소와 읽기 쉬운 결과 요약만 복사합니다. 카톡, 커뮤니티, 블로그에 붙여넣기 좋게 정리했습니다.</p>')
  .replaceAll('계산 링크 복사', '짧은 링크 복사')
  .replaceAll('결과 요약 복사', '요약 문구 복사');

await writeFile(indexPath, html, 'utf8');
