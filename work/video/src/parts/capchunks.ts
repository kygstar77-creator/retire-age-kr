// 자막 조각 나누기(React 없음 — work/capcheck.py가 node로 같은 함수를 돌려 대본을 검사한다).
// 10/16 22시 사장님 "문장·뜻 단위로 끊는다": 낱말 단위, 한 조각 최대 limit자(공백 포함). 끊는 자리 점수 —
//   문장부호(.,?!) 뒤·말 이음(~고·~서·~면·~는데·~지만·~니까·~요·~다) 뒤는 끊기 좋음, 꾸미는 말('내·이·그·한·몇·약·같은·지난' 등) 뒤와 숫자 덩이('1억 6천만원') 안·'~의' 뒤는 끊지 않음.
// 10/20 A50(n2s_middle 30.5초 '쪽엔 한가운데보다'): 조각이 조사·의존명사로 시작하면 안 된다 — 앞 낱말과 한 어절 묶음.
//   ① 의존명사(쪽·것·수·때·데…)는 앞 낱말이 꾸미는 꼴(받침 ㄴ·ㄹ: 받는·많은·할)일 때만 묶음으로 본다('그래서 줄 한가운데'의 줄은 그냥 명사).
//   ② 띄어 쓴 조사(보다·처럼·까지·에서…)로 시작하는 조각은 언제나 금지.
//   ③ 같은 날 덧붙임: 조각 안 쉼표는 피한다(쉼표 뒤에서 끊음). '~는' 꾸미는 꼴 벌점은 시험해 봤다가 뺐다 — 주제 '는'(평수는·종가는)과 못 가려 20편 대본에서 더 나빠진 줄이 나왔다.
const CAP_DET = new Set(['내', '이', '그', '저', '한', '두', '세', '네', '몇', '약', '총', '각', '첫', '이번', '지난', '같은', '다른', '이런', '그런', '저런', '모든', '어느', '무슨', '이 돈', '매달', '한 달', '올해', '작년', '지금']);
const CAP_GOOD = /([.,?!]|고|서|며|면|는데|은데|인데|지만|니까|라서|해서|려면|으면|어요|에요|예요|아요|죠|다|요|게)$/;
const BOUND = '(?:것|거|게|수|줄|데|때|때문|쪽|편|만큼|뿐|듯|채|척|중|동안|대로|정도|등|셈|탓|덕|김|무렵|터)';
const JOSA = '(?:이|가|은|는|을|를|에|엔|에서|에는|에도|도|만|으로|로|으론|론|의|이에요|예요|이야|이다|입니다|이죠|죠|이라|라|이고|고|인데|이라서|이면|면|처럼|보다|까지|밖에|이에|에게|냐는|냐고|냐|라는|라고|란|에요|야|지만|든지)?';
const BOUND_RE = new RegExp(`^${BOUND}${JOSA}[.,?!]*$`);
const JOSA_RE = /^(?:보다|처럼|까지|부터|만큼|에서|에게|에겐|한테|밖에|마다|조차|이나|라도|이랑|으로|로서|로써|에는|에도|의)(?![가-힣])/;
const adnominal = (w: string) => {
  const ch = w.replace(/[^가-힣]+$/, '').slice(-1); if (!ch) return false;
  const jong = (ch.charCodeAt(0) - 0xac00) % 28; return jong === 4 || jong === 8; // 받침 ㄴ·ㄹ
};
// prev 낱말 뒤에서 끊고 next 낱말로 새 조각을 시작하면 어절 묶음이 갈리나
export const badStart = (prev: string, next: string) => JOSA_RE.test(next) || (adnominal(prev) && BOUND_RE.test(next));

export const capChunksCore = (t: string, target: number, limit: number) => {
  const out: string[] = [];
  for (const sen of t.split(/(?<=[.?!])\s+/).filter(Boolean)) {
    const w = sen.split(/\s+/).filter(Boolean); const n = w.length; const L = sen.length; const k = Math.max(1, Math.round(L / target)); const tg = L / k;
    const len = (i: number, j: number) => w.slice(i, j).join(' ').length;
    const best: number[] = Array(n + 1).fill(Infinity); const prev: number[] = Array(n + 1).fill(0); best[0] = 0;
    for (let j = 1; j <= n; j++) for (let i = 0; i < j; i++) {
      const l = len(i, j); if (l > limit && j - i > 1) continue;
      const last = w[j - 1];
      let c = best[i] + 0.6 * (l - tg) * (l - tg) + (l < 4 ? 80 : 0);
      if (w.slice(i, j - 1).some((x) => /,$/.test(x))) c += 200;                         // 조각 안 쉼표('절반, 적게') — 쉼표 뒤에서 끊는다
      if (j < n) {
        if (/\d[억만천원%년월일분]*$/.test(last) && /^\d|^[천만억원]/.test(w[j])) c += 400;          // 숫자 덩이 안
        if (CAP_DET.has(last) || last.length === 1) c += 300;                             // 꾸미는 말·한 글자 뒤
        if (/의$/.test(last)) c += 150;
        if (badStart(last, w[j])) c += 2000;                                              // 조사·의존명사로 시작(A50)
        if (CAP_GOOD.test(last)) c -= 35;                                                  // 말 이음·문장부호 뒤
      }
      if (c < best[j]) { best[j] = c; prev[j] = i; }
    }
    const cut: string[] = []; for (let j = n; j > 0; j = prev[j]) cut.unshift(w.slice(prev[j], j).join(' '));
    out.push(...cut);
  }
  return out.map((c) => c.replace(/[.,]$/, ''));
};
