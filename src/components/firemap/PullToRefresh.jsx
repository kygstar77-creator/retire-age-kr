import { useEffect, useRef, useState } from 'react';

// 당겨서 새로고침 — 스크롤 맨 위에서 아래로 당기면 페이지를 새로고침해요(모바일 표준 제스처).
// 전역 터치 리스너로 동작. 일반 스크롤은 방해하지 않도록 '맨 위 + 아래로 당김'일 때만 개입.
const THRESHOLD = 64;

export default function PullToRefresh() {
  const [dist, setDist] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  const startY = useRef(0);
  const active = useRef(false);
  const scroller = useRef(null);
  const distRef = useRef(0);

  useEffect(() => {
    const atTop = (el) => (el ? el.scrollTop <= 0 : (window.scrollY || document.documentElement.scrollTop || 0) <= 0);
    const onStart = (e) => {
      if (e.touches.length !== 1 || refreshing) { active.current = false; return; }
      const t = e.target;
      scroller.current = (t && t.closest) ? t.closest('.fm-scroll') : null;
      if (atTop(scroller.current)) { startY.current = e.touches[0].clientY; active.current = true; distRef.current = 0; } else { active.current = false; }
    };
    const onMove = (e) => {
      if (!active.current) return;
      const dy = e.touches[0].clientY - startY.current;
      if (dy > 0 && atTop(scroller.current)) {
        const d = Math.min(96, dy * 0.5);
        distRef.current = d;
        setDist(d);
        if (d > 6 && e.cancelable) e.preventDefault();
      } else {
        active.current = false; distRef.current = 0; setDist(0);
      }
    };
    const onEnd = () => {
      if (active.current && distRef.current >= THRESHOLD) {
        setRefreshing(true);
        setTimeout(() => { try { window.location.reload(); } catch { /* ignore */ } }, 220);
      }
      active.current = false; distRef.current = 0; setDist(0);
    };
    document.addEventListener('touchstart', onStart, { passive: true });
    document.addEventListener('touchmove', onMove, { passive: false });
    document.addEventListener('touchend', onEnd, { passive: true });
    document.addEventListener('touchcancel', onEnd, { passive: true });
    return () => {
      document.removeEventListener('touchstart', onStart);
      document.removeEventListener('touchmove', onMove);
      document.removeEventListener('touchend', onEnd);
      document.removeEventListener('touchcancel', onEnd);
    };
  }, [refreshing]);

  const show = dist > 0 || refreshing;
  const ready = dist >= THRESHOLD;
  return (
    <div aria-hidden="true" style={{
      position: 'fixed', top: 0, left: 0, right: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
      height: refreshing ? 44 : Math.min(56, dist), zIndex: 70, pointerEvents: 'none',
      opacity: show ? 1 : 0, transition: active.current ? 'none' : 'height .2s ease, opacity .2s ease'
    }}>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12, fontWeight: 800, color: '#ff5a00',
        background: '#fff', border: '1px solid rgba(255,90,0,0.3)', borderRadius: 999, padding: '6px 13px',
        boxShadow: '0 6px 16px -8px rgba(232,67,28,0.5)'
      }}>
        <span style={{ display: 'inline-block', transform: `rotate(${refreshing ? 0 : Math.min(180, dist * 2)}deg)`, transition: 'transform .1s linear' }}>{refreshing ? '⟳' : '↓'}</span>
        {refreshing ? '새로고침 중…' : ready ? '놓으면 새로고침' : '당겨서 새로고침'}
      </span>
    </div>
  );
}
