// 날짜 키 1벌 — 전부 기기(로컬) 날짜 기준. UTC(toISOString)와 섞어 쓰면 KST 00~09시에 '오늘'이 어긋나
// 스트릭이 끊기고 이번 달 합계가 달라진다. 저장·비교·표시 모두 여기 함수만 쓴다.
const p2 = (n) => String(n).padStart(2, '0');
export const ymdOf = (d) => `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}`;
export const ymOf = (d) => `${d.getFullYear()}-${p2(d.getMonth() + 1)}`;
export const todayStr = () => ymdOf(new Date());
export const yesterdayStr = () => ymdOf(new Date(Date.now() - 86400000));
export const monthStr = () => ymOf(new Date());
export const daysAgoStr = (n) => ymdOf(new Date(Date.now() - n * 86400000));
export const dayIdx = () => Math.floor(Date.now() / 86400000);
