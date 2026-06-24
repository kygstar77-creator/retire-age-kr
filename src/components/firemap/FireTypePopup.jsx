import { useEffect, useState } from 'react';
import { track } from '../../firemap-v2/dailyData.js';

// 결과 직후 1회성 화려한 풀스크린 팝업 — 파이어 유형 테스트로 유도(유입 루프).
// 닫거나 시작하면 일정 기간 재노출 자제(localStorage). 비로그인·무설치.
const KEY = 'fm_firetype_popup_v1';
const SUPPRESS_DAYS = 21;
function suppressed() {
  try { const v = localStorage.getItem(KEY); if (!v) return false; const t = Number(v); return t ? (Date.now() - t) < SUPPRESS_DAYS * 86400000 : true; } catch { return false; }
}

export default function FireTypePopup({ onMove }) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (suppressed()) return undefined;
    const t = setTimeout(() => { setOpen(true); try { track('firetype_popup_view'); } catch { /* ignore */ } }, 1400);
    return () => clearTimeout(t);
  }, []);
  if (!open) return null;
  const stamp = () => { try { localStorage.setItem(KEY, String(Date.now())); } catch { /* ignore */ } };
  const go = () => { stamp(); try { track('firetype_popup_go'); } catch { /* ignore */ } setOpen(false); if (onMove) onMove('firetype'); };
  const close = () => { stamp(); try { track('firetype_popup_close'); } catch { /* ignore */ } setOpen(false); };

  return (
    <div role="dialog" aria-modal="true" onClick={close} style={{
      position: 'fixed', inset: 0, zIndex: 9000, display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: 22, background: 'rgba(7,9,22,0.72)', backdropFilter: 'blur(3px)', animation: 'fmPopFade .25s ease'
    }}>
      <style>{`
        @keyframes fmPopFade{from{opacity:0}to{opacity:1}}
        @keyframes fmPopUp{from{opacity:0;transform:translateY(16px) scale(.96)}to{opacity:1;transform:none}}
        @keyframes fmPopGlow{0%,100%{opacity:.5}50%{opacity:.9}}
        @keyframes fmPopFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
      `}</style>
      <div onClick={(e) => e.stopPropagation()} style={{
        position: 'relative', width: '100%', maxWidth: 340, borderRadius: 24, overflow: 'hidden', textAlign: 'center',
        background: 'radial-gradient(130% 90% at 50% 0%, #241b54, #0c1026 72%)', border: '1px solid #ffffff1f',
        padding: '30px 22px 24px', color: '#fff', animation: 'fmPopUp .4s cubic-bezier(.2,1.1,.3,1)'
      }}>
        <div aria-hidden="true" style={{ position: 'absolute', top: -60, left: '50%', transform: 'translateX(-50%)', width: 200, height: 120, background: 'radial-gradient(circle, #ff7a3c88, transparent 60%)', filter: 'blur(14px)', animation: 'fmPopGlow 2.4s ease-in-out infinite' }} />
        <button type="button" aria-label="닫기" onClick={close} style={{ position: 'absolute', top: 12, right: 14, border: 0, background: 'transparent', color: '#9aa1c4', fontSize: 22, lineHeight: 1, cursor: 'pointer' }}>×</button>
        <div style={{ position: 'relative', fontSize: 52, animation: 'fmPopFloat 3s ease-in-out infinite' }}>🌍</div>
        <p style={{ position: 'relative', margin: '6px 0 4px', fontSize: 12.5, fontWeight: 800, letterSpacing: '.04em', color: '#ffd9c2' }}>잠깐, 하나 더!</p>
        <h2 style={{ position: 'relative', margin: '0 0 8px', fontSize: 23, fontWeight: 900, lineHeight: 1.3 }}>나는 어떤 <span style={{ background: 'linear-gradient(90deg,#ff8a4c,#ffd166)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent' }}>파이어족</span>일까?</h2>
        <p style={{ position: 'relative', margin: '0 0 18px', fontSize: 13.5, lineHeight: 1.6, color: '#c7cce0' }}>9문항으로 내 유형 + 나에게 맞는<br /><b style={{ color: '#fff' }}>국내·해외 도시 Top3</b>를 찾아드려요.</p>
        <button type="button" onClick={go} style={{ position: 'relative', width: '100%', padding: '14px', borderRadius: 14, border: 0, fontSize: 15.5, fontWeight: 800, color: '#1a1330', background: 'linear-gradient(90deg,#ff8a4c,#ffd166)', cursor: 'pointer', boxShadow: '0 8px 26px #ff7a3c55' }}>내 파이어 유형 보기 →</button>
        <button type="button" onClick={close} style={{ position: 'relative', marginTop: 10, background: 'transparent', border: 0, color: '#8b91ad', fontSize: 12.5, fontWeight: 700, cursor: 'pointer' }}>다음에 할게요</button>
      </div>
    </div>
  );
}
