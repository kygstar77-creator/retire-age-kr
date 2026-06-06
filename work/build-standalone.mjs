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

/* Polished button and compact metric label alignment. */
.icon-button,
.mobile-step-actions button,
.mobile-bottom-bar button,
.growth-actions button,
.growth-actions a {
  align-items: center;
  justify-content: center;
  text-align: center;
  line-height: 1.2;
  white-space: nowrap;
}

.mobile-toggle {
  min-width: 86px;
  padding: 0 12px;
}

.strip-card > span {
  min-width: 44px;
  width: auto;
  padding: 0 8px;
  text-align: center;
  word-break: keep-all;
  white-space: nowrap;
  font-size: 12px;
}

.card-icon {
  min-width: 50px;
  width: auto;
  padding: 0 8px;
  white-space: nowrap;
  text-align: center;
  font-size: 12px;
  font-weight: 850;
}

.legal-footer {
  max-width: 1180px;
  margin: 28px auto 96px;
  padding: 0 20px;
  color: #6f7e89;
  font-size: 14px;
  text-align: center;
}

.legal-footer nav {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.legal-footer a {
  color: #32414d;
  font-weight: 800;
  text-decoration: none;
}

.legal-footer a:hover {
  color: #126044;
}

@media (max-width: 680px) {
  .legal-footer {
    margin: 24px auto 108px;
    padding: 0 16px;
    font-size: 13px;
  }
}
`;

const legalFooter = `
<footer class="legal-footer" aria-label="서비스 운영 정보">
  <nav>
    <a href="/privacy">개인정보처리방침</a>
    <span>·</span>
    <a href="/terms">이용약관</a>
    <span>·</span>
    <a href="/contact">문의</a>
  </nav>
  <p>퇴사나이는 입력값과 가정에 따른 참고용 시뮬레이션이며, 투자 권유나 재무 자문이 아닙니다.</p>
</footer>`;

const bundledSimulator = simulator.replaceAll('export ', '');
const bundledFormatters = formatters.replaceAll('export ', '');
const bundledShareState = shareState.replaceAll('export ', '');
const patchedPreview = preview
  .replace("['목표까지 필요한 월 투자액', requiredMonthlyValue, requiredMonthlyDetail,", "['월투자', '목표까지 필요한 월 투자액', requiredMonthlyValue, requiredMonthlyDetail,")
  .replace("['목표 퇴사 판정', survives ?", "['판정', '목표 퇴사 판정', survives ?")
  .replace("['가장 빠른 퇴사 가능 나이', formatAge(earliestRetirementAge),", "['나이', '가장 빠른 퇴사 가능 나이', formatAge(earliestRetirementAge),")
  .replace("['퇴사 첫해 인출률', formatPercent(safeWithdrawalRate),", "['인출률', '퇴사 첫해 인출률', formatPercent(safeWithdrawalRate),")
  .replace("[`${data.simulationUntilAge}세 잔여 금융자산`, formatEok(finalFinancialAsset),", "['잔액', `${data.simulationUntilAge}세 잔여 금융자산`, formatEok(finalFinancialAsset),")
  .replace("['퇴사 시점 금융자산', formatEok(retirementFinancialAsset),", "['자산', '퇴사 시점 금융자산', formatEok(retirementFinancialAsset),")
  .replace('cards.map(([label, value, detail, tone, badge]) => `', 'cards.map(([icon, label, value, detail, tone, badge]) => `')
  .replace('<span class="card-icon">원</span>', '<span class="card-icon">${icon}</span>');
const bundledPreview = patchedPreview
  .split('\n')
  .filter((line) => !line.trim().startsWith('import '))
  .join('\n');

const standalone = html
  .replace('<link rel="stylesheet" href="/src/styles.css" />', `<style>\n${css}\n${inputFirstUx}\n</style>`)
  .replace('</main>', `</main>\n${legalFooter}`)
  .replace('<script type="module" src="/src/preview.js"></script>', `<script type="module">\n${bundledSimulator}\n${bundledFormatters}\n${bundledShareState}\n${bundledPreview}\n</script>`);

await mkdir(join(root, 'outputs'), { recursive: true });
await writeFile(join(root, 'outputs', 'toesanai-standalone.html'), standalone, 'utf8');
