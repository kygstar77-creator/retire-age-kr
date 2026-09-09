// 파이어 유형 테스트 — 표지 · 12문항 · 결과(공유 카드). 도시 적용은 미리보기(샌드박스)로만.
import { useState, useEffect } from 'react';
import { TopBar, Card, SectionHead, Button, ProgressBar, ListGroup, ListRow, BottomCTA, toast } from '../../ui/index.js';
import { QUESTIONS, ARCHETYPES, scoreAnswers, recommendCities } from '../../firemap-v2/cityTypeTest.js';
import { buildScenario } from '../../firemap-v2/scenarios.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { shareToKakao } from '../../utils/kakaoShare.js';
import { track } from '../../firemap-v2/dailyData.js';
import '../../ui/screens/firetype.css';

const TEST_URL = 'https://firemap.kr/#firetype';
const eok = (n) => formatWon(Math.round(n || 0));

function Cover({ onStart }) {
  return (
    <Card variant="dark" padding="lg" className="sc-ft-cover">
      <span className="sc-ft-kick">12문항 · 1분</span>
      <h2 className="sc-ft-title">나는 어떤<br /><b>파이어족</b>일까?</h2>
      <p className="sc-ft-sub">유형과 내게 맞는 국내·해외 도시 Top3를 찾아줘요 · 로그인 없이 바로</p>
      <Button variant="primary" size="lg" full onClick={onStart}>테스트 시작하기</Button>
      <p className="ds-caption ds-mt-3 ds-textcenter">참고용 결과예요 · 투자 자문이 아니에요</p>
    </Card>
  );
}

function Quiz({ idx, onPick, onBack }) {
  const q = QUESTIONS[idx];
  return (
    <>
      <ProgressBar value={idx} max={QUESTIONS.length} thin />
      <Card padding="lg">
        <SectionHead kicker={`${idx + 1} / ${QUESTIONS.length}`} title={q.q} />
        <div className="ds-stack">
          {q.opts.map((o, i) => (
            <Button key={i} variant="secondary" size="lg" full className="sc-ft-opt" onClick={() => onPick(i)}>{o.t}</Button>
          ))}
        </div>
        <Button variant="ghost" size="sm" className="ds-mt-3" onClick={onBack}>‹ 이전</Button>
      </Card>
    </>
  );
}

function Result({ answers, simulation, onMove, onRestart, onPreviewCity }) {
  const { archetype: A, axes } = scoreAnswers(answers);
  const recs = recommendCities(axes, simulation, buildScenario, 3);
  const match = ARCHETYPES[A.match];
  const [reveal, setReveal] = useState(false);
  useEffect(() => {
    track('firetype_result', { type: A.id, top: recs[0] && recs[0].city.city, qa: (answers || []).join(''), nq: (answers || []).length });
    try { localStorage.setItem('fm_firetype_done', '1'); } catch { /* 유형 확인 완료 → 홈 권유 팝업 중단 */ }
    const t = setTimeout(() => setReveal(true), 120);
    return () => clearTimeout(t);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const share = async () => {
    track('firetype_share', { type: A.id });
    const title = `나는 ${A.name} (${A.nick}) ☕🔥`;
    const desc = `추천 도시 ${recs.map((r) => r.city.city).join('·')} · 12문항으로 내 파이어 유형 찾기`;
    // v=ft2: 보충 폰트(og-fonts-ft) 적용 후 새 URL로 분리 → 카카오/CDN의 폰트픽스 이전 캐시 우회(재크롤)
    const ogImg = `https://firemap.kr/og?mode=firetype&v=ft2&tn=${encodeURIComponent(A.name)}&nk=${encodeURIComponent(A.nick)}&ct=${encodeURIComponent(recs.map((r) => r.city.city).join('·'))}`;
    try { await shareToKakao({ title, description: desc, imageUrl: ogImg, linkUrl: TEST_URL }); return; }
    catch { /* 폴백 */ }
    try { await navigator.clipboard.writeText(`${title}\n${desc}\n${TEST_URL}`); toast.good('링크를 복사했어요 · 단톡방에 붙여넣어 봐요'); }
    catch { toast.bad('공유가 안 됐어요 · 잠시 후 다시 해봐요'); }
  };
  const copy = async () => { try { await navigator.clipboard.writeText(TEST_URL); toast.good('링크를 복사했어요'); track('firetype_share', { type: A.id, via: 'copy' }); } catch { /* ignore */ } };
  // 도시 적용 = 미리보기(샌드박스)로만. 저장은 미리보기 화면에서 사용자가 명시적으로. 기존 저장값 무손상.
  const pickCity = (krw) => { if (onPreviewCity) { onPreviewCity(krw); return; } if (onMove) onMove('cities'); };

  return (
    <>
      <Card variant="dark" padding="lg" className="sc-ft-share">
        <span className="sc-ft-kick">내 파이어 유형</span>
        <div className={`sc-ft-emoji${reveal ? ' is-on' : ''}`} aria-hidden="true">{A.emoji}</div>
        <h2 className="sc-ft-name">{A.name}</h2>
        <p className="sc-ft-nick">“{A.nick}”</p>
        <p className="sc-ft-tag">{A.tagline}</p>
        <ListGroup className="sc-ft-list">
          <ListRow size="S" lead="💪" title="강점" desc={A.strong} chevron={false} />
          <ListRow size="S" lead="👀" title="주의" desc={A.watch} chevron={false} />
          {A.action && <ListRow size="S" lead="👉" title="추천 행동" desc={A.action} chevron={false} />}
        </ListGroup>
        <p className="ds-caption ds-mt-3">잘 맞는 유형 · {match.emoji} {match.nick}</p>

        <ListGroup label="내게 맞는 도시 Top3" className="sc-ft-list ds-mt-3">
          {recs.map((r, i) => (
            <ListRow
              key={r.city.city} size="M"
              lead={<span className="sc-ft-rank num">{i + 1}</span>}
              title={`${r.city.flag} ${r.city.city}`}
              desc={`${r.city.country} · 월 ${eok(r.city.krw)}${r.fireAge ? ` · ${r.fireAge}세 파이어` : ''}`}
              trail={<span className="num">{r.score}점</span>}
              onClick={() => pickCity(r.city.krw)}
            />
          ))}
        </ListGroup>
        <p className="ds-caption ds-mt-2">도시를 누르면 그 생활비로 미리보기를 열어요</p>
      </Card>

      <Button variant="ghost" size="sm" full onClick={copy}>🔗 링크만 복사</Button>
      <BottomCTA secondary={{ label: '다시 하기', onClick: onRestart }} primary={{ label: '💬 카드로 공유', onClick: share }} />
      <p className="ds-caption ds-textcenter">입력과 취향으로 추정한 결과예요 · 비용·비자·의료는 다를 수 있어요</p>
    </>
  );
}

export default function FireTypeTest({ simulation, onChange, onMove, onBack, onPreviewCity }) {
  const [stage, setStage] = useState('cover'); // 'cover' | 'quiz' | 'result'
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState([]);
  void onChange;
  const start = () => { track('firetype_start'); setAnswers([]); setIdx(0); setStage('quiz'); };
  const pick = (oi) => {
    const next = [...answers]; next[idx] = oi; setAnswers(next);
    if (idx + 1 >= QUESTIONS.length) setStage('result'); else setIdx(idx + 1);
  };
  const back = () => { if (idx === 0) setStage('cover'); else setIdx(idx - 1); };
  const restart = () => { setStage('cover'); setIdx(0); setAnswers([]); };

  return (
    <main className="fm-screen fm-scroll ds-screen-gap">
      <TopBar title="파이어 유형" onBack={onBack} />
      {stage === 'cover' && <Cover onStart={start} />}
      {stage === 'quiz' && <Quiz idx={idx} onPick={pick} onBack={back} />}
      {stage === 'result' && <Result answers={answers} simulation={simulation} onMove={onMove} onRestart={restart} onPreviewCity={onPreviewCity} />}
    </main>
  );
}
