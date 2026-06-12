// 익명 사용자에게 기기별 고정 '재미 닉네임' 부여 (DB 저장 X, 표시용)
const ADJ = ['알뜰한', '불꽃', '부지런', '현명한', '단단한', '느긋한', '용감한', '빛나는', '조용한', '대담한', '똑똑한', '꾸준한', '자유로운', '강철', '황금', '날쌘', '포근한', '단호한', '상냥한', '짠물'];
const ANI = ['너구리', '다람쥐', '여우', '수달', '고슴도치', '부엉이', '펭귄', '코알라', '두더지', '거북', '햄스터', '판다', '늑대', '수리', '담비', '오소리', '토끼', '족제비', '비버', '고래'];

export function funHandle(seed) {
  if (!seed) return '익명의 파이어족';
  let h = 2166136261;
  for (let i = 0; i < seed.length; i += 1) { h ^= seed.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  const a = ADJ[h % ADJ.length];
  const n = ANI[Math.floor(h / ADJ.length) % ANI.length];
  const num = (h % 90) + 10;
  return `${a} ${n}${num}`;
}

export const displayName = (row) => (row && row.nickname ? row.nickname : funHandle(row && row.client_id));
