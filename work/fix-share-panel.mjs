import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const indexPath = join(process.cwd(), 'outputs', 'deploy', 'index.html');
let html = await readFile(indexPath, 'utf8');

html = html
  .replaceAll('공유</p><h2>링크 하나로 바로 계산하게 만들기</h2><p>카톡, 커뮤니티, 블로그에서 누르면 앱 설치 없이 모바일 화면에서 바로 열립니다. 입력값도 링크에 담아 비교 시나리오로 공유할 수 있습니다.</p>', '공유</p><h2>깔끔하게 복사해서 공유하기</h2><p>긴 입력값 링크 대신 기본 주소와 읽기 쉬운 결과 요약만 복사합니다. 카톡, 커뮤니티, 블로그에 붙여넣기 좋게 정리했습니다.</p>')
  .replaceAll('계산 링크 복사', '짧은 링크 복사')
  .replaceAll('결과 요약 복사', '요약 문구 복사');

const mobileTopFixStyle = `<style id="mobile-top-fix">
@media (max-width: 680px) {
  .app-shell {
    width: 100%;
    max-width: 100%;
    padding-left: 12px;
    padding-right: 12px;
  }

  .site-nav,
  .site-nav div {
    width: 100%;
    min-width: 0;
  }

  .site-nav {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .site-nav strong {
    display: block;
    width: 100%;
    white-space: nowrap;
  }

  .site-nav div {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
  }

  .site-nav button,
  .site-footer button {
    width: 100%;
    min-width: 0;
    padding: 0 8px;
    white-space: nowrap;
  }

  .main-tabs {
    width: 100%;
    max-width: 100%;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 4px;
    padding: 6px;
    overflow: visible;
    border-radius: 12px;
  }

  .main-tabs button {
    min-width: 0;
    min-height: 42px;
    padding: 0 4px;
    font-size: 12px;
    line-height: 1.15;
    white-space: normal;
    word-break: keep-all;
  }
}

@media (max-width: 390px) {
  .app-shell {
    padding-left: 10px;
    padding-right: 10px;
  }

  .main-tabs {
    gap: 3px;
    padding: 5px;
  }

  .main-tabs button {
    min-height: 40px;
    padding: 0 2px;
    font-size: 11px;
  }
}
</style>`;

if (!html.includes('id="mobile-top-fix"')) {
  html = html.replace('</head>', `${mobileTopFixStyle}\n</head>`);
}

await writeFile(indexPath, html, 'utf8');
