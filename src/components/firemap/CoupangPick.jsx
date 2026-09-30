// 계산기 결과 아래 쿠팡 관련 상품 1칸(10/1 결승선 F1). 규칙: work/research/coupang-policy.md 6장 체크리스트 2·3·4·12.
// - 링크 바로 위에 대가성 문구(권장 문구 그대로, 조건부 표현 금지, 본문과 다른 색) · 발급받은 link.coupang.com 주소 그대로(리다이렉트·단축기 금지)
// - 플로팅·자동 이동 없음, 계산 결과와 '은퇴 나이 계산' 뒤에만 둔다(본문보다 광고가 커지지 않게) · 금융상품은 넣지 않는다
// - 가격은 싣지 않는다(실시간 가격과 달라질 수 있어서). 링크가 없는 계산기는 아무것도 그리지 않는다.
import { ListGroup, ListRow, Icon, Notice } from '../../ui/index.js';
import { COUPANG_PICKS } from '../../firemap-v2/coupangPicks.js';
import { logEvent } from '../../utils/live.js';

export const COUPANG_DISCLOSURE = '이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.';
const isIssuedLink = (u) => /^https:\/\/link\.coupang\.com\/a\/[A-Za-z0-9]+$/.test(String(u || ''));

export default function CoupangPick({ from }) {
  const pick = COUPANG_PICKS[from];
  if (!pick || !isIssuedLink(pick.url) || !pick.title) return null;
  const onClick = () => { try { logEvent('coupang_click', { from, id: pick.id }); } catch { /* ignore */ } };
  return (
    <div className="fm-coupang-pick">
      <Notice tone="accent" className="fm-coupang-pick__disclosure">{COUPANG_DISCLOSURE}</Notice>
      <ListGroup label="관련 상품 · 쿠팡">
        <ListRow lead={<Icon name="book" />} title={pick.title} desc={pick.desc} size="S"
          href={pick.url} target="_blank" rel="sponsored nofollow noopener noreferrer" onClick={onClick} />
      </ListGroup>
    </div>
  );
}
