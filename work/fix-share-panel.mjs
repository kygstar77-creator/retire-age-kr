import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const indexPath = join(process.cwd(), 'outputs', 'deploy', 'index.html');
let html = await readFile(indexPath, 'utf8');

html = html
  .replaceAll('공유</p><h2>링크 하나로 바로 계산하게 만들기</h2><p>카톡, 커뮤니티, 블로그에서 누르면 앱 설치 없이 모바일 화면에서 바로 열립니다. 입력값도 링크에 담아 비교 시나리오로 공유할 수 있습니다.</p>', '공유</p><h2>깔끔하게 복사해서 공유하기</h2><p>긴 입력값 링크 대신 기본 주소와 읽기 쉬운 결과 요약만 복사합니다. 카톡, 커뮤니티, 블로그에 붙여넣기 좋게 정리했습니다.</p>')
  .replaceAll('퇴사나이는 모든 기능을 한 화면에 밀어 넣지 않고, 사용자가 궁금한 문제별로 바로 들어갈 수 있게 나눴습니다.', '퇴사 판단, 생활비·건보료, 투자·세금, 공유 기능을 목적별로 나눠 필요한 계산기만 바로 사용할 수 있습니다.')
  .replaceAll('계산 링크 복사', '짧은 링크 복사')
  .replaceAll('결과 요약 복사', '요약 문구 복사');

const mobileTopFixStyle = `<style id="mobile-top-fix">
@media (max-width: 680px) {
  .app-shell {
    width: 100%;
    max-width: 100%;
    padding-top: 18px;
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

  .hub-panel,
  .stay-scenario,
  .health-estimator,
  .dividend-calculator,
  .share-community,
  .guide-panel,
  .legal-panel,
  .disclaimer,
  .growth-panel,
  .input-panel,
  .decision-panel,
  .panel {
    width: 100%;
    max-width: 100%;
    border-radius: 22px;
  }

  .hub-panel,
  .stay-scenario,
  .health-estimator,
  .dividend-calculator,
  .share-community,
  .guide-panel,
  .legal-panel,
  .panel {
    padding: 20px;
  }

  .section-heading {
    display: grid;
    grid-template-columns: 1fr;
    align-items: start;
    gap: 12px;
  }

  .section-heading h2 {
    font-size: 25px;
    line-height: 1.28;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  .feature-intro,
  .hub-intro {
    font-size: 15px;
    line-height: 1.68;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  .tax-open-button,
  .tax-copy-button,
  .tax-apply-button,
  .share-actions button,
  .growth-actions button,
  .growth-actions a,
  .section-heading > button {
    width: 100%;
    min-height: 50px;
    padding: 0 14px;
    border-radius: 16px;
    white-space: nowrap;
    word-break: keep-all;
    line-height: 1.15;
  }

  .compact-results,
  .share-actions,
  .tax-grid,
  .feature-grid,
  .mini-grid,
  .tool-grid,
  .trust-grid {
    grid-template-columns: 1fr;
  }

  .tax-result-card,
  .tool-card,
  .trust-grid article,
  .mini-row,
  .share-card,
  .summary-card,
  .scenario-card {
    border-radius: 18px;
  }

  .tax-result-card {
    padding: 18px;
  }

  .tax-result-card strong,
  .mini-row strong {
    font-size: 28px;
    line-height: 1.18;
    word-break: keep-all;
  }
}

@media (max-width: 390px) {
  .app-shell {
    padding-top: 16px;
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

  .hub-panel,
  .stay-scenario,
  .health-estimator,
  .dividend-calculator,
  .share-community,
  .guide-panel,
  .legal-panel,
  .panel {
    padding: 18px;
  }

  .section-heading h2 {
    font-size: 24px;
  }
}
</style>`;

if (!html.includes('id="mobile-top-fix"')) {
  html = html.replace('</head>', `${mobileTopFixStyle}\n</head>`);
}

await writeFile(indexPath, html, 'utf8');
