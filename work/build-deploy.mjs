import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const root = process.cwd();
const outputs = join(root, 'outputs');
const deploy = join(outputs, 'deploy');
const adsensePublisherId = '3225798545626010';

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
    adsenseClientId: 'ca-pub-3225798545626010',
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
    return target && target.closest ? target.closest('[data-field]')?.dataset.field : undefined;
  }

  function getResultMeta() {
    var decision = document.getElementById('decisionDashboard');
    var text = decision ? decision.textContent : '';
    var status = text.indexOf('위험') >= 0 ? 'risk' : text.indexOf('주의') >= 0 ? 'caution' : text.indexOf('안정') >= 0 ? 'stable' : 'unknown';
    var targetInput = document.querySelector('[data-field="targetRetirementAge"]');
    var endInput = document.querySelector('[data-field="simulationUntilAge"]');
    return {
      status: status,
      target_age_bucket: targetInput ? Math.round(Number(targetInput.value || 0) / 5) * 5 : undefined,
      end_age_bucket: endInput ? Math.round(Number(endInput.value || 0) / 5) * 5 : undefined
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

  function initAds() {
    if (!config.adsEnabled || !config.adsenseClientId) return;
    loadScript('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(config.adsenseClientId), {
      crossorigin: 'anonymous'
    }, function () {
      insertAdSlot();
    });
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
  initAds();
})();
</script>`;

await import('./build-standalone.mjs');
await mkdir(deploy, { recursive: true });
let indexHtml = await readFile(join(outputs, 'toesanai-standalone.html'), 'utf8');
indexHtml = indexHtml.replaceAll('og-image.png?v=4', 'og-image.png?v=5');
indexHtml = indexHtml.replace('</head>', `${productPolishStyle}\n</head>`);
indexHtml = indexHtml.replace('</body>', `${operationsSnippet}\n</body>`);
await writeFile(join(deploy, 'index.html'), indexHtml, 'utf8');

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
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
