import { useEffect, useRef, useState } from 'react';

// 당겨서 새로고침 — 페이지 맨 위(window 스크롤 0)에서 아래로 당길 때만 새로고침.
// 이 앱은 .fm-scroll가 아니라 window가 스크롤되므로 window 스크롤 위치를 기준으로 판정한다.
const THRESHOLD = 64;
const scrollTop = () => (window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0);

export default function PullToRefresh() {
  const [dist, setDist] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  const startY = useRef(0);
  const active = useRef(false);
  const distRef = useRef(0);

  useEffect(() => {
    const onStart = (e) => {
      if (e.touches.length !== 1 || refreshing) { active.current = false; return; }
      if (scrollTop() <= 0) { startY.current = e.touches[0].clientY; active.current = true; distRef.current = 0; } else { active.current = false; }
    };
    const onMove = (e) => {
      if (!active.current) return;
      // 손가락을 뗼지 않은 채 스크롤이 0보다 커지면(중간으로 이동) 즉시 중단
      if (scrollTop() > 0) { active.current = false; distRef.current = 0; setDist(0); return; }
      const dy = e.touches[0].clientY - startY.current;
      if (dy > 0) {
        const d = Math.min(96, dy * 0.5);
        distRef.current = d;
        setDist(d);
        if (d > 6 && e.cancelable) e.preventDefault();
      } else {
        distRef.current = 0; setDist(0);
      }
    };
    const onEnd = () => {
      if (active.current && distRef.current >= THRESHOLD && scrollTop() <= 0) {
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
