// 계산기 결과 아래 쿠팡 관련 상품 1칸(10/1 결승선 F1). 규칙: work/research/coupang-policy.md 6장 체크리스트 2·3·4·12.
// - 링크 바로 위에 대가성 문구(권장 문구 그대로, 조건부 표현 금지, 본문과 다른 색) · 발급받은 link.coupang.com 주소 그대로(리다이렉트·단축기 금지)
// - 플로팅·자동 이동 없음, 계산기 화면 맨 끝(계산 방법 뒤)에만 둔다(본문보다 광고가 커지지 않게) · 금융상품은 넣지 않는다
// - 가격은 싣지 않는다(실시간 가격과 달라질 수 있어서). 링크가 없는 계산기는 아무것도 그리지 않는다.
// - 디자인 관문(design/f1-coupang/spec.md): 문구와 상품을 한 카드로, 주황·아이콘·› 없음(내부 링크처럼 보이지 않게), 라벨 '광고'.
import { ListRow } from '../../ui/index.js';
import { COUPANG_PICKS } from '../../firemap-v2/coupangPicks.js';
import { logEvent } from '../../utils/live.js';

export const COUPANG_DISCLOSURE = '이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.';
const isIssuedLink = (u) => /^https:\/\/link\.coupang\.com\/a\/[A-Za-z0-9]+$/.test(String(u || ''));

export default function CoupangPick({ from }) {
  const pick = COUPANG_PICKS[from];
  if (!pick || !isIssuedLink(pick.url) || !pick.title) return null;
  const onClick = () => { try { logEvent('coupang_click', { from, id: pick.id }); } catch { /* ignore */ } };
  return (
    <div className="fm-coupang-pick ds-listgroup ds-mt-4">
      <p className="ds-list__label">광고 · 쿠팡 파트너스</p>
      <div className="ds-list">
        <p className="fm-coupang-pick__disclosure ds-mt-0 ds-mb-0">{COUPANG_DISCLOSURE}</p>
        <ListRow title={pick.title} desc={pick.desc} size="S" chevron={false}
          trail={<span className="ds-caption fm-coupang-pick__trail">쿠팡 ↗</span>}
          href={pick.url} target="_blank" rel="sponsored nofollow noopener noreferrer" onClick={onClick} />
      </div>
    </div>
  );
}
