// Tally 움직임 부품 ① 장면 틀 — 제목·형광 부제·흰 보드·정확한 값 칩([자막])·말 자막·출처를 안전 구역 안에만 둔다(2026-10-03 cloud/r1-remake-1003)
// 안전 구역: 오른쪽 아래 25%×20%(x>1440·y>864, 유튜브 끝 화면·구독 버튼 자리)와 맨 아래 5%(y>1026)에는 글자·그림을 두지 않는다.
// 보드(흰 판)는 x 100~1820 · y 236~852, 말 자막은 가운데 · 아래 끝 y 1024(1줄 60px, 한 쪽 18자), 출처 y 864~886. 토큰은 parts/fm(T·F)과 같다.
// 자막 규격 근거 research/longform/caption-spec-1011.md(상위 26편 실측, 10/11 순돌이 지시). 끝 화면 구간은 capX=760으로 옮겨 오른쪽 아래 금지 구역을 비운다.
// ── 10/17 롱폼 화면 기준(work/research/longform/visual-gap-1017.md 7절, 관문 work/bgcheck.py) ──
//   · 제목은 위 가운데 큰 글씨(최대 110px). 관문 잣대(426×240 줄였다 키운 OCR 상자)로 100px = 8.96%, 110px ≈ 9.8%. 판의 가장 큰 글자가 9% 이상(수페 9.1~9.6%, 우리 5.4~6.7%였다).
//     제목이 길어 줄면(한글 13자 넘음) 판 안 핵심 숫자를 110px 이상으로 둔다. 판 하나의 글자 줄은 8줄 이하(수페 7~9, 우리 10~13).
//   · art: 판마다 아이콘·사람 그림·사진 중 하나(수페 도식 화면 대부분). 무료 출처만, license 칸 필수. 실존 인물 얼굴·상표 금지.
//       icon = lucide-react 이름(ISC, 예 'PiggyBank') · src = public 아래 그림/사진(Pexels 등, credits.json에 출처)
//       국기는 node_modules/flag-icons/flags/4x3/<코드>.svg(MIT)를 public/flags/로 복사해 src로(kind 'flag')
//   · 같은 판은 20초까지. 판↔꽉 찬 실사(TallyBroll·StockShot)↔표를 번갈아 화면 전체 컷이 분당 3회 이상 나게 한다.
//   · bg(판 뒤에 어둡게 깐 실사)는 10/17부터 기본 아님 — 경쟁 롱폼 '배경 실사 5/5'는 대담 영상이라서였다. 실사는 판 뒤가 아니라 화면을 꽉 채운 장면으로.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing, OffthreadVideo, Img, staticFile} from 'remotion';
import * as Lucide from 'lucide-react';
import {T, F, CL, FONT_CSS, Flame} from '../parts/fm';
import {wordTimings, paginate, activeWord, pageOf, CaptionPage} from '../motion-proto/captionTiming';

export const SAFE = {W: 1920, H: 1080, left: 120, textRight: 1400, brX: 1440, brY: 864, bottom: 1026};
export const BOARD = {x: 100, y: 236, w: 1720, h: 616};

// ── 10/16 디자인 기준 v3: 장면 뒤 실사 사진·영상 — 10/17부터 롱폼 기본 아님(위 머리말). 쓰던 편 호환으로 남김 ──
// bg를 주면 화면 전체에 깔고(천천히 확대), 위를 어둡게 덮어 제목·부제·브랜드를 흰 글자로, 보드는 흰 카드로 띄운다. src = work/video/public 기준 경로.
export type TallyBg = {src: string; start?: number; kind?: 'video' | 'image'; x?: number};
const TallyBgLayer: React.FC<{bg: TallyBg}> = ({bg}) => {
  const f = useCurrentFrame();
  const z = 1.03 + Math.min(0.09, f * 0.00025);
  const st: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, objectFit: 'cover', objectPosition: `${bg.x ?? 50}% 50%`, transform: `scale(${z})`};
  const vid = bg.kind === 'video' || /\.mp4$/i.test(bg.src);
  return (
    <>
      {vid ? <OffthreadVideo src={staticFile(bg.src)} muted startFrom={Math.round((bg.start ?? 0) * 30)} style={st} /> : <Img src={staticFile(bg.src)} style={st} />}
      <div style={{position: 'absolute', inset: 0, background: 'rgba(8,9,12,0.38)'}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 300, background: 'linear-gradient(rgba(0,0,0,0.72), rgba(0,0,0,0))'}} />
      <div style={{position: 'absolute', left: 0, bottom: 0, width: 1920, height: 260, background: 'linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0.6))'}} />
    </>
  );
};
const SH = '0 2px 0 rgba(0,0,0,0.6), 0 0 18px rgba(0,0,0,0.55)';

// 판마다 그림 하나(10/17) — kind는 무엇을 넣었는지(관문·기록용), license는 출처·라이선스 한 줄(예 'lucide ISC', 'Pexels 12345 무료', '자체 제작')
export type TallyArt = {kind: 'icon' | 'person' | 'photo' | 'flag'; license: string; icon?: string; src?: string; color?: string; size?: number};
export const TallyArtView: React.FC<{art: TallyArt; size?: number; dark?: boolean}> = ({art, size, dark}) => {
  const z = size ?? art.size ?? 104;
  if (art.icon) {
    const I = (Lucide as unknown as Record<string, React.FC<{size?: number; color?: string; strokeWidth?: number}>>)[art.icon];
    if (!I) throw new Error(`TallyArt: lucide 아이콘 이름 없음 '${art.icon}'`);
    return <div style={{width: z, height: z, borderRadius: z * 0.28, background: dark ? 'rgba(255,255,255,0.12)' : T.soft, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none'}}>
      <I size={z * 0.62} color={art.color ?? T.accent} strokeWidth={2.2} /></div>;
  }
  if (art.src) return <Img src={staticFile(art.src)} style={{width: art.kind === 'photo' ? z * 1.5 : z, height: z, objectFit: art.kind === 'photo' ? 'cover' : 'contain', borderRadius: art.kind === 'photo' ? 16 : 0, flex: 'none'}} />;
  throw new Error('TallyArt: icon·src 중 하나가 있어야 한다');
};

// 제목 크기: 한글 1em, 공백 0.3em, 그 밖 0.56em로 어림해 (1560 − 그림 칸) 안에 한 줄로. 최대 110px(관문 9%는 101px 이상), 최소 60px
export const titleSize = (t: string, room = 1560) => { const u = [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.3 : 0.56), 0); return Math.max(60, Math.min(110, Math.floor(room / Math.max(1, u)))); };

export type TallyLine = {text: string; cap?: string | null; frames: number};
export const tallyStarts = (lines: TallyLine[]) => { const out: number[] = []; let a = 0; for (const l of lines) { out.push(a); a += l.frames; } return out; };
export const tallyAt = (lines: TallyLine[], i: number | null | undefined) => (i == null || i < 0 || i >= lines.length) ? 1e9 : tallyStarts(lines)[i];
export const tallyIdx = (lines: TallyLine[], f: number) => { const st = tallyStarts(lines); let k = -1; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };

// 출처는 자르지 않고 글자를 줄여 한 줄(x 120~1400)에 넣는다 — 한글 1em, 영문·숫자 0.56em로 어림
export const srcSize = (src: string) => { const u = [...('출처 ' + src)].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : 0.56), 0); return Math.max(13, Math.min(19, Math.floor((SAFE.textRight - SAFE.left) / u))); };

// 말 자막 쪽 나누기: 한 쪽 공백 뺀 18자, 5자 이하로 남는 꼬리 쪽은 앞 쪽에 붙인다(caption-spec 4장)
const CAP_MAX = 18, CAP_TAIL = 5;
const nsp = (t: string) => t.replace(/\s/g, '').length;
export const capPages = (text: string): CaptionPage[] => {
  const pages = paginate(text.split(/\s+/).filter(Boolean), CAP_MAX);
  if (pages.length > 1 && nsp(pages[pages.length - 1].text) <= CAP_TAIL) { const b = pages.pop() as CaptionPage; const a = pages.pop() as CaptionPage; pages.push({first: a.first, last: b.last, text: a.text + ' ' + b.text}); }
  return pages;
};
// 한 줄(nowrap)이 상자 maxWidth 1400 안에 들도록: 한글 1em, 그 밖 0.56em, 공백 0.3em로 어림해 60px에서 줄인다
const capSize = (t: string) => { const u = [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.3 : 0.56), 0); return Math.min(60, Math.floor(1330 / Math.max(1, u))); };

// 말 자막(가운데·아래 끝 y 1024, 한 쪽 18자) — TallyFrame·TallyBroll이 같이 쓴다
export const TallyCaption: React.FC<{lines: TallyLine[]; capX?: number}> = ({lines, capX = 960}) => {
  const f = useCurrentFrame();
  const k = tallyIdx(lines, f);
  const line = k >= 0 ? lines[k] : null; if (!line) return null;
  const st = tallyStarts(lines)[k];
  const lo = interpolate(f, [st, st + 5], [0, 1], CL);
  const pages = capPages(line.text); const tm = wordTimings(line.text, line.frames, 0.92);
  const page = pages[pageOf(pages, Math.max(0, activeWord(tm, f - st)))]?.text ?? line.text;
  return (
    <div style={{position: 'absolute', left: capX - 700, width: 1400, bottom: 56, display: 'flex', justifyContent: 'center', opacity: lo}}>
      <div style={{...F, fontWeight: 700, fontSize: capSize(page), lineHeight: 1.25, color: '#fff', background: T.ink, padding: '10px 32px', borderRadius: 12, whiteSpace: 'nowrap', maxWidth: 1400}}>{page}</div>
    </div>
  );
};

export const TallyFrame: React.FC<{title: string; sub?: string | null; source?: string | null; chapter?: string | null; lines: TallyLine[]; children?: React.ReactNode; board?: boolean; capX?: number; bg?: TallyBg | null; art?: TallyArt | null}> =
  ({title, sub, source, chapter, lines, children, board = true, capX = 960, bg = null, art = null}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 10], [0, 1], CL);
  const hl = interpolate(f, [6, 22], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const k = tallyIdx(lines, f);
  let cap: string | null = null; let capAt = 0;
  for (let i = 0; i <= k; i++) if (lines[i]?.cap) { cap = lines[i].cap as string; capAt = tallyStarts(lines)[i]; }
  const co = interpolate(f, [capAt, capAt + 8], [0, 1], CL);
  return (
    <AbsoluteFill style={{background: bg ? '#000' : T.bg}}>
      <style>{FONT_CSS}</style>
      {bg ? <TallyBgLayer bg={bg} /> : null}
      {/* 10/17: 브랜드·장 칩은 왼쪽 위 작게, 제목은 위 가운데 크게(최대 110px), 그림(art)은 제목 왼쪽 */}
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10, opacity: o}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: bg ? '#fff' : T.ink2, textShadow: bg ? SH : undefined}}>파이어맵</span>
        {chapter ? <div style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', background: T.accent, borderRadius: 8, padding: '1px 10px', marginLeft: 8}}>{chapter}</div> : null}
      </div>
      <div style={{position: 'absolute', left: 180, width: 1560, top: sub ? 50 : 70, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 24}}>
          {art ? <TallyArtView art={art} size={Math.min(112, titleSize(title, 1430) + 2)} dark={!!bg} /> : null}
          <div style={{...F, fontWeight: 700, fontSize: titleSize(title, art ? 1430 : 1560), color: bg ? '#fff' : T.ink, lineHeight: 1.1, letterSpacing: -2, whiteSpace: 'nowrap', textShadow: bg ? SH : undefined}}>{title}</div>
        </div>
        {sub ? (
          <div style={{position: 'relative', display: 'inline-block', marginTop: 8}}>
            <div style={{position: 'absolute', left: -6, top: 4, bottom: 2, width: `calc(${hl * 100}% + 12px)`, background: T.soft, borderRadius: 6}} />
            <div style={{...F, position: 'relative', fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{sub}</div>
          </div>
        ) : null}
      </div>
      {board ? <div style={{position: 'absolute', left: BOARD.x, top: BOARD.y, width: BOARD.w, height: BOARD.h, background: bg ? 'rgba(255,255,255,0.96)' : '#fff', border: bg ? 'none' : `2px solid ${T.line}`, borderRadius: 24, opacity: o, boxShadow: bg ? '0 20px 60px rgba(0,0,0,0.45)' : undefined}} /> : null}
      {children}
      {cap ? (
        <div style={{position: 'absolute', left: 130, top: 252, maxWidth: 1660, opacity: co, transform: `translateY(${(1 - co) * -8}px)`,
          background: T.ink, borderRadius: 10, padding: '7px 16px', display: 'flex', gap: 12, alignItems: 'baseline'}}>
          <span style={{...F, fontWeight: 700, fontSize: 20, color: T.daccent, whiteSpace: 'nowrap'}}>{/\d/.test(cap) ? '정확한 값' : '참고'}</span>
          <span style={{...F, fontWeight: 700, fontSize: 24, color: '#fff', lineHeight: 1.3, wordBreak: 'keep-all'}}>{cap}</span>
        </div>
      ) : null}
      <TallyCaption lines={lines} capX={capX} />
      {source ? <div style={{...F, fontWeight: 500, fontSize: srcSize(source), color: bg ? '#e8eaee' : T.ink3, textShadow: bg ? SH : undefined, position: 'absolute', left: SAFE.left, top: 864, whiteSpace: 'nowrap'}}>출처 {source}</div> : null}
    </AbsoluteFill>
  );
};
