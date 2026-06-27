// 한 화면(뷰)에서 팝업은 하나만 노출. 먼저 자격을 통과해 claim한 팝업이 뜨고, 나머지는 다음 방문/새로고침으로 양보.
// 모듈 전역 플래그 → SPA 내 화면 이동에선 유지(같은 세션 중복 방지), 전체 새로고침 시 초기화(다음 방문에 다른 팝업 기회).
let claimed = null;
export function claimPopup(name) {
  if (claimed && claimed !== name) return false;
  claimed = name;
  return true;
}
export function popupClaimedBy() { return claimed; }
