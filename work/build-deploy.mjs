import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
async function renderPngFromSvg(svg, outputPath) {
  try {
    const { default: sharp } = await import('sharp');
    await sharp(Buffer.from(svg)).png().toFile(outputPath);
  } catch {
    // The deployed app can still build without the optional local PNG renderer.
  }
}

const root = process.cwd();
const outputs = join(root, 'outputs');
const deploy = join(outputs, 'deploy');
const adsensePublisherId = '3225798545626010';
const adsenseClientId = `ca-pub-${adsensePublisherId}`;

const adsenseHeadScript = `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsenseClientId}"
     crossorigin="anonymous"></script>`;

const productPolishStyle = `<style>
  .hero {
    background:
      radial-gradient(circle at 86% 24%, rgba(18, 96, 68, 0.12), transparent 30%),
      linear-gradient(135deg, #ffffff 0%, #f4f8f7 100%);
  }

  .hero > div:first-child::after {
    content: "서버 저장 없음 · 카톡 공유 최적화 · 3분 계산";
    display: inline-flex;
    width: fit-content;
    margin-top: 18px;
    padding: 9px 12px;
    border: 1px solid rgba(18, 96, 68, 0.16);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.78);
    color: #126044;
    font-size: 0.9rem;
    font-weight: 850;
    line-height: 1.35;
  }

  .input-panel,
  .decision-card,
  .summary-card,
  .scenario-card,
  .report-card,
  .table-card,
  .legal-footer {
    box-shadow: 0 18px 50px rgba(23, 33, 44, 0.06);
  }

  .ops-ad-panel {
    display: none;
    margin: 0 0 20px;
    padding: 14px;
    border: 1px solid #dfe8e5;
    border-radius: 22px;
    background: #ffffff;
  }

  .ops-ad-panel.is-active {
    display: block;
  }

  .ops-ad-label {
    display: block;
    margin-bottom: 8px;
    color: #8a98a4;
    font-size: 0.78rem;
    font-weight: 800;
  }

  @media (max-width: 680px) {
    body {
      background: #eef4f3;
    }

    .app-shell {
      padding-top: 10px;
    }

    .hero {
      margin: 0 12px 12px;
      padding: 22px 18px;
      border-radius: 22px;
    }

    .hero h1 {
      max-width: 14em;
      font-size: 28px;
      line-height: 1.18;
    }

    .hero p {
      margin-top: 12px;
      font-size: 15px;
      line-height: 1.62;
    }

    .hero > div:first-child::after {
      margin-top: 14px;
      white-space: normal;
      font-size: 13px;
      line-height: 1.45;
    }

    .hero-metric {
      margin-top: 18px;
      width: 100%;
      min-height: 82px;
    }

    .layout {
      gap: 12px;
    }

    .input-panel,
    .decision-panel,
    .growth-panel,
    .panel,
    .summary-card,
    .scenario-card {
      border-radius: 22px;
    }

    .section-heading {
      gap: 12px;
      align-items: flex-start;
    }

    .section-heading h2,
    .decision-main h2,
    .insight-title strong {
      word-break: keep-all;
      overflow-wrap: anywhere;
    }

    .decision-main h2 {
      font-size: 26px;
      line-height: 1.24;
    }

    .decision-score {
      min-height: 112px;
    }

    .growth-actions {
      grid-template-columns: 1fr;
    }

    .growth-actions button,
    .mobile-step-actions button,
    .mobile-bottom-bar button {
      min-height: 54px;
      border-radius: 18px;
      font-size: 16px;
    }

    .decision-card,
    .summary-card,
    .scenario-card,
    .report-card,
    .table-card {
      box-shadow: 0 10px 28px rgba(23, 33, 44, 0.05);
    }
  }
</style>`;

const operationsSnippet = `<script>
(function () {
  var config = {
    gaMeasurementId: '',
    cloudflareAnalyticsToken: '',
    adsenseClientId: '${adsenseClientId}',
    adsenseSlotId: '',
    adsenseAutoAds: true,
    adsEnabled: true
  };

  window.toesanaiOps = window.toesanaiOps || {};
  window.toesanaiOps.config = config;

  var state = {
    inputStarted: false,
    resultTracked: false,
    adInserted: false
  };

  function loadScript(src, attrs, onload) {
    if (!src || document.querySelector('script[src="' + src + '"]')) return;
    var script = document.createElement('script');
    script.async = true;
    script.src = src;
    Object.keys(attrs || {}).forEach(function (key) {
      script.setAttribute(key, attrs[key]);
    });
    if (onload) script.onload = onload;
    document.head.appendChild(script);
  }

  function initAnalytics() {
    if (!config.gaMeasurementId) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', config.gaMeasurementId, { send_page_view: true });
    loadScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(config.gaMeasurementId));
  }

  function initCloudflareAnalytics() {
    if (!config.cloudflareAnalyticsToken) return;
    loadScript('https://static.cloudflareinsights.com/beacon.min.js', {
      'data-cf-beacon': JSON.stringify({ token: config.cloudflareAnalyticsToken })
    });
  }

  function trackEvent(name, params) {
    if (!window.gtag) return;
    window.gtag('event', name, Object.assign({ app_name: 'toesanai' }, params || {}));
  }

  function getFieldName(target) {
    return target && target.closest ? target.closest('[data-field]')?.dataset.field : null;
  }

  function getResultMeta() {
    var decision = document.getElementById('decisionDashboard');
    var text = decision ? decision.textContent : '';
    var status = text.indexOf('위험') >= 0 ? 'risk' : text.indexOf('주의') >= 0 ? 'caution' : text.indexOf('안정') >= 0 ? 'stable' : 'unknown';
    var targetInput = document.querySelector('[data-field="targetRetirementAge"]');
    var endInput = document.querySelector('[data-field="simulationUntilAge"]');
    return {
      status: status,
      target_age_bucket: targetInput ? Math.round(Number(targetInput.value || 0) / 5) * 5 : null,
      end_age_bucket: endInput ? Math.round(Number(endInput.value || 0) / 5) * 5 : null
    };
  }

  function maybeTrackResult() {
    var decision = document.getElementById('decisionDashboard');
    if (!decision || state.resultTracked) return;
    if (decision.textContent && decision.textContent.trim().length > 20) {
      state.resultTracked = true;
      trackEvent('result_view', getResultMeta());
      insertAdSlot();
    }
  }

  function insertAdSlot() {
    if (!config.adsEnabled || !config.adsenseClientId || !config.adsenseSlotId || state.adInserted) return;
    var anchor = document.getElementById('growthPanel') || document.querySelector('.results');
    if (!anchor || !anchor.parentNode) return;
    state.adInserted = true;
    var panel = document.createElement('section');
    panel.className = 'ops-ad-panel is-active';
    panel.setAttribute('aria-label', '광고');
    panel.innerHTML = '<span class="ops-ad-label">광고</span><ins class="adsbygoogle" style="display:block" data-ad-client="' + config.adsenseClientId + '" data-ad-slot="' + config.adsenseSlotId + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
    anchor.parentNode.insertBefore(panel, anchor.nextSibling);
    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (error) {}
  }

  document.addEventListener('input', function (event) {
    var field = getFieldName(event.target);
    if (!field) return;
    if (!state.inputStarted) {
      state.inputStarted = true;
      trackEvent('input_started');
    }
    trackEvent('input_change', { field_name: field });
  }, { passive: true });

  document.addEventListener('click', function (event) {
    var target = event.target.closest('button, a');
    if (!target) return;
    if (target.dataset.copy === 'link' || target.id === 'bottomShareButton') trackEvent('share_link_copy', getResultMeta());
    if (target.dataset.copy === 'summary') trackEvent('share_summary_copy', getResultMeta());
    if (target.id === 'resetButton') trackEvent('inputs_reset');
    if (target.id === 'mobileInputToggle' || target.id === 'bottomEditButton') trackEvent('input_panel_open');
    if (target.closest('.legal-footer')) trackEvent('legal_link_click', { link_text: target.textContent.trim().slice(0, 30) });
  }, { passive: true });

  var observer = new MutationObserver(maybeTrackResult);
  document.addEventListener('DOMContentLoaded', function () {
    var decision = document.getElementById('decisionDashboard');
    if (decision) observer.observe(decision, { childList: true, subtree: true, characterData: true });
    maybeTrackResult();
  });

  initAnalytics();
  initCloudflareAnalytics();
})();
</script>`;

await import('./build-standalone.mjs');
await mkdir(deploy, { recursive: true });
let indexHtml = await readFile(join(outputs, 'toesanai-standalone.html'), 'utf8');
indexHtml = indexHtml.replaceAll('og-image.png?v=4', 'og-image.png?v=5');
indexHtml = polishPublicCopy(indexHtml);
indexHtml = indexHtml.replace('</head>', `${adsenseHeadScript}\n${productPolishStyle}\n</head>`);
indexHtml = indexHtml.replace('</body>', `${operationsSnippet}\n</body>`);
await writeFile(join(deploy, 'index.html'), indexHtml, 'utf8');

function polishPublicCopy(html) {
  const replacements = [
    ['금융자산, 생활비, 국민연금, 부업 소득을 입력해 퇴사 가능 나이와 자산 고갈 시점을 확인하세요.', '생활비 재원, 국민연금, 퇴사 후 소득을 입력해 퇴사 가능 나이와 자금 유지 기간을 확인하세요.'],
    ['금융자산, 생활비, 투자수익률, 국민연금을 넣고 퇴사 가능 나이와 자산 고갈 시점을 계산해보세요.', '생활비 재원, 투자수익률, 국민연금을 넣고 퇴사 가능 나이와 자금 유지 기간을 계산해보세요.'],
    ['금융자산, 생활비, 투자수익률, 국민연금을 입력해 퇴사 가능 나이와 자산 고갈 시점을 계산합니다.', '생활비 재원, 생활비, 투자수익률, 국민연금을 입력해 퇴사 가능 나이와 자금 유지 기간을 계산합니다.'],
    ['돈이 바닥날 수 있어요', '자금이 부족할 수 있어요'],
    ['돈이 바닥나지 않는지', '생활비 재원이 유지되는지'],
    ['돈이 바닥나지 않으면', '생활비 재원이 마이너스가 되지 않으면'],
    ['돈이 바닥나는지', '생활비 재원이 부족해지는지'],
    ['자산 고갈', '자금 부족'],
    ['고갈 나이', '자금 부족 시점'],
    ['고갈 예상', '자금 부족 가능'],
    ['고갈 기준', '자금 부족 기준'],
    ['고갈되지', '부족해지지'],
    ['고갈될', '부족해질'],
    ['고갈은', '자금 부족은'],
    ['고갈', '자금 부족'],
    ['바닥', '자금 부족'],
    ['잔여 금융자산', '생활비 재원'],
    ['금융자산 유지', '생활비 재원 유지'],
    ['금융자산은', '생활비 재원은'],
    ['금융자산이', '생활비 재원이'],
    ['금융자산을', '생활비 재원을'],
    ['금융자산으로', '생활비 재원으로'],
    ['금융자산과', '생활비 재원과'],
    ['금융자산', '생활비 재원'],
    ['인출해야 하는 돈', '준비한 돈에서 써야 하는 생활비'],
    ['예상 인출률', '첫해 필요 생활비 비율'],
    ['인출률', '필요 생활비 비율'],
    ['인출액', '사용액'],
    ['퇴사 첫해 꺼내 쓰는 비율', '첫해 필요 생활비 비율'],
    ['첫해에 쓸 돈 ÷ 퇴사 시점 생활비 재원', '퇴사 시점에 준비한 돈 대비 첫해에 필요한 생활비'],
    ['FIRE 갭', '보수 기준 차이'],
    ['브릿지', '국민연금 받기 전 기간'],
    ['추가 여력', '더 모아야 할 돈']
  ];

  return replacements.reduce((current, [from, to]) => current.replaceAll(from, to), html);
}

const readme = `# 퇴사나이 배포본

이 폴더는 정적 호스팅에 바로 올릴 수 있는 배포용 파일입니다.

## 파일

- index.html
- robots.txt
- sitemap.xml
- ads.txt
- og-image.png
- og-image.svg

이 버전은 서버, 로그인, DB 없이 브라우저 안에서 계산하고 localStorage에 입력값을 저장합니다.
`;

const robots = `User-agent: *
Allow: /

Sitemap: https://retire-age-kr.pages.dev/sitemap.xml
`;

const adsTxt = `google.com, pub-${adsensePublisherId}, DIRECT, f08c47fec0942fa
`;

const today = new Date().toISOString().slice(0, 10);
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://retire-age-kr.pages.dev/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://retire-age-kr.pages.dev/privacy/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://retire-age-kr.pages.dev/terms/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://retire-age-kr.pages.dev/contact/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
`;

const headers = `/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://pagead2.googlesyndication.com https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://www.google-analytics.com https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net; connect-src 'self' https://www.google-analytics.com https://analytics.google.com https://region1.google-analytics.com https://pagead2.googlesyndication.com https://cloudflareinsights.com; frame-src https://googleads.g.doubleclick.net https://tpc.googlesyndication.com; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
`;

const ogImage = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#17212c"/>
  <rect x="72" y="72" width="1056" height="486" rx="28" fill="#f8fafb"/>
  <text x="120" y="190" fill="#126044" font-family="Arial, sans-serif" font-size="44" font-weight="700">퇴사나이</text>
  <text x="120" y="288" fill="#17212c" font-family="Arial, sans-serif" font-size="66" font-weight="800">내 자산으로 몇 살에</text>
  <text x="120" y="370" fill="#17212c" font-family="Arial, sans-serif" font-size="66" font-weight="800">퇴사할 수 있을까?</text>
  <text x="120" y="462" fill="#53616c" font-family="Arial, sans-serif" font-size="32">한국형 조기은퇴·반퇴 시뮬레이터</text>
  <rect x="790" y="142" width="270" height="204" rx="22" fill="#dff3e9"/>
  <text x="925" y="207" text-anchor="middle" fill="#126044" font-family="Arial, sans-serif" font-size="28" font-weight="700">목표 퇴사</text>
  <text x="925" y="292" text-anchor="middle" fill="#126044" font-family="Arial, sans-serif" font-size="82" font-weight="800">39세</text>
</svg>`;

await writeFile(join(deploy, 'README.md'), readme, 'utf8');
await writeFile(join(deploy, 'robots.txt'), robots, 'utf8');
await writeFile(join(deploy, 'ads.txt'), adsTxt, 'utf8');
await writeFile(join(deploy, 'sitemap.xml'), sitemap, 'utf8');
await writeFile(join(deploy, '_headers'), headers, 'utf8');
await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await renderPngFromSvg(ogImage, join(deploy, 'og-image.png'));

async function writeInfoPage(slug, title, lead, sections) {
  const pageDir = join(deploy, slug);
  await mkdir(pageDir, { recursive: true });
  const body = sections.map((section) => `
        <section class="info-card">
          <h2>${section.title}</h2>
          ${section.paragraphs.map((paragraph) => `<p>${paragraph}</p>`).join('\n          ')}
        </section>`).join('\n');
  const html = `<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="robots" content="index, follow" />
    <title>${title} - 퇴사나이</title>
    <meta name="description" content="${lead}" />
    <link rel="canonical" href="https://retire-age-kr.pages.dev/${slug}/" />
    ${adsenseHeadScript}
    <style>
      :root { color: #17212c; background: #eef4f3; font-family: Inter, Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
      body { margin: 0; }
      .info-shell { width: min(920px, calc(100% - 32px)); margin: 0 auto; padding: 44px 0 72px; }
      .top-link { display: inline-flex; margin-bottom: 24px; color: #126044; font-weight: 800; text-decoration: none; }
      .info-hero, .info-card { background: #fff; border: 1px solid #dfe8e5; border-radius: 22px; box-shadow: 0 18px 50px rgba(23, 33, 44, 0.06); }
      .info-hero { padding: 34px; margin-bottom: 16px; }
      .brand { color: #126044; font-weight: 900; margin: 0 0 12px; }
      h1 { margin: 0; font-size: clamp(30px, 5vw, 48px); letter-spacing: 0; line-height: 1.15; }
      .lead { color: #53616c; font-size: 18px; line-height: 1.7; margin: 18px 0 0; }
      .info-card { padding: 28px; margin-top: 14px; }
      h2 { margin: 0 0 12px; font-size: 22px; }
      p { color: #53616c; line-height: 1.75; margin: 10px 0 0; }
      .info-footer { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 28px; color: #53616c; }
      .info-footer a { color: #53616c; text-decoration: none; font-weight: 800; }
      @media (max-width: 680px) {
        .info-shell { width: min(100% - 24px, 920px); padding-top: 18px; }
        .info-hero, .info-card { border-radius: 20px; padding: 22px; }
        .lead { font-size: 15px; }
      }
    </style>
  </head>
  <body>
    <main class="info-shell">
      <a class="top-link" href="/">← 계산기로 돌아가기</a>
      <section class="info-hero">
        <p class="brand">퇴사나이</p>
        <h1>${title}</h1>
        <p class="lead">${lead}</p>
      </section>
      ${body}
      <nav class="info-footer">
        <a href="/">계산기</a>
        <a href="/privacy/">개인정보</a>
        <a href="/terms/">이용약관</a>
        <a href="/contact/">문의</a>
      </nav>
    </main>
  </body>
</html>`;
  await writeFile(join(pageDir, 'index.html'), html, 'utf8');
}

await writeInfoPage('privacy', '개인정보처리방침', '퇴사나이는 사용자가 입력한 자산 정보를 서버에 저장하지 않는 브라우저 기반 계산기입니다.', [
  {
    title: '수집하는 정보',
    paragraphs: [
      '퇴사나이는 회원가입, 로그인, 데이터베이스를 사용하지 않습니다. 사용자가 입력한 나이, 생활비, 자산, 연금 정보는 계산을 위해 브라우저 안에서만 처리됩니다.',
      '입력값 저장 기능은 사용자의 브라우저 localStorage를 사용합니다. 운영자는 개별 사용자가 입력한 금액이나 결과를 볼 수 없습니다.'
    ]
  },
  {
    title: '분석과 광고',
    paragraphs: [
      '서비스 품질 개선을 위해 Cloudflare Web Analytics, Google Analytics 같은 방문 통계 도구를 사용할 수 있습니다. 이 도구들은 페이지뷰, 유입 경로, 기기 환경 같은 서비스 이용 통계를 확인하기 위한 목적입니다.',
      'Google AdSense가 적용되는 경우 광고 제공 과정에서 쿠키 또는 유사 기술이 사용될 수 있습니다. 광고 관련 데이터 처리는 Google의 정책을 따릅니다.'
    ]
  },
  {
    title: '문의',
    paragraphs: [
      '개인정보, 서비스 개선 제안, 오류 제보, 협업 문의는 문의 페이지를 통해 안내된 이메일로 연락할 수 있습니다.'
    ]
  }
]);

await writeInfoPage('terms', '이용약관', '퇴사나이는 조기은퇴와 반퇴 가능성을 이해하기 위한 참고용 시뮬레이션 서비스입니다.', [
  {
    title: '서비스의 성격',
    paragraphs: [
      '퇴사나이는 사용자가 입력한 값과 가정을 바탕으로 계산 결과를 보여주는 참고용 도구입니다. 투자 권유, 금융상품 추천, 세무·법률·재무 자문을 제공하지 않습니다.',
      '실제 퇴사, 투자, 대출 상환, 연금 수령과 관련된 의사결정 전에는 공식 자료와 전문가 상담을 함께 확인해야 합니다.'
    ]
  },
  {
    title: '계산 결과의 한계',
    paragraphs: [
      '투자수익률, 물가상승률, 생활비, 국민연금, 퇴사 후 소득은 실제 상황에 따라 달라질 수 있습니다. 계산 결과는 미래를 보장하지 않습니다.',
      '시장 변동, 세금, 건강보험료, 주거비 변화, 가족 상황, 제도 변경 등은 별도로 검토해야 합니다.'
    ]
  },
  {
    title: '사용자의 책임',
    paragraphs: [
      '사용자는 본인의 판단과 책임으로 계산 결과를 활용합니다. 서비스 이용 과정에서 입력값을 정확하게 검토하고, 필요하면 여러 시나리오를 비교해보는 것을 권장합니다.'
    ]
  }
]);

await writeInfoPage('contact', '문의', '서비스 개선 제안, 오류 제보, 제휴와 협업 문의를 받을 수 있는 공식 연락 창구입니다.', [
  {
    title: '문의 이메일',
    paragraphs: [
      '개선사항, 오류 제보, 제휴 및 협업 문의는 <a href="mailto:retireage.kr@gmail.com">retireage.kr@gmail.com</a> 로 보내주세요.',
      '입력한 개인 자산 정보는 서버에 저장되지 않으므로, 문의할 때는 필요한 화면 설명이나 공개 가능한 정보만 함께 보내주세요.'
    ]
  },
  {
    title: '좋은 제안 예시',
    paragraphs: [
      '입력 단계에서 헷갈린 문구, 모바일에서 불편한 흐름, 계산 결과에서 이해하기 어려운 표현, 추가로 보고 싶은 지표를 알려주시면 우선순위에 반영하겠습니다.',
      '금융기관, 커뮤니티, 콘텐츠 파트너십 제안도 이 이메일로 보내면 됩니다.'
    ]
  }
]);
