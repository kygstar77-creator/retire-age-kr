// 계산기별 쿠팡 관련 상품 1개 — 쿠팡 파트너스(AF9074391)에서 발급받은 link.coupang.com 주소만 넣는다.
// 비어 있으면 그 계산기에는 칸이 안 보인다(CoupangPick.jsx). 상품은 계산기 주제와 직접 관련된 비금융 상품만(coupang-policy.md 12).
// { id: 기록용 짧은 이름, title: 쿠팡 상품명 그대로, desc: 이 계산기와 왜 관련 있는지 한 줄, url: 발급 링크 }
export const COUPANG_PICKS = {
  // 10/1 17:22 firemap-youtube-loop 발급(curl 302 → lptag=AF9074391). desc는 편집 통과 전이라 비워 둔다(제목만이면 검수 대상 아님, editor 17:15).
  salary: { id: 'ledger-05custard', title: '아이코닉 잘 쓰는 습관 가계부, 05Custard, 1개', url: 'https://link.coupang.com/a/hutbIQImpE' },
  severance: { id: 'book-quit-prep', title: '퇴사를 준비하는 나에게:어쩌다 말고 제대로 퇴사를 위한 일대일 맞춤 상담실, 위즈덤하우스, 이슬기 저', url: 'https://link.coupang.com/a/hutlDDyiDQ' },
  unemployment: { id: 'book-cert-itq2', title: '2026 시나공 컴퓨터활용능력 2급 필기 기출문제집, 길벗', url: 'https://link.coupang.com/a/huthTl2Aqy' }
};
