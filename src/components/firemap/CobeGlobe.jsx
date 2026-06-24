import { useEffect, useRef, useState } from 'react';

// 화려하지만 가벼운 글로우 지구본 — cobe(~5KB)를 esm.sh에서 동적 로드(번들 무영향).
// WebGL 불가 / 로드 실패 시에만 정적 SVG 글로우 폴백. prefers-reduced-motion은 회전만 멈춤(글로브는 그대로 표시).
// markers: [{ location:[lat,lon], size }], focus:[lat,lon] 으로 해당 지점을 정면으로 회전.
function hexToRgb(hex) {
  const h = (hex || '#ff5a00').replace('#', '');
  const n = parseInt(h.length === 3 ? h.split('').map((c) => c + c).join('') : h, 16);
  return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
}
const reduceMotion = () => { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { return false; } };
const webglOK = () => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl') || c.getContext('experimental-webgl')); } catch { return false; } };

export default function CobeGlobe({ markers = [], focus = null, accent = '#ff5a00', size = 300 }) {
  const canvasRef = useRef(null);
  const [fail, setFail] = useState(() => !webglOK());

  useEffect(() => {
    if (fail) return undefined;
    let globe = null; let raf = 0; let alive = true;
    let phi = focus ? (Math.PI + (-focus[1] * Math.PI) / 180) : 0;
    const theta = focus ? (focus[0] * Math.PI) / 180 * 0.6 : 0.25;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    (async () => {
      try {
        const mod = await import('https://esm.sh/cobe@0.6.3');
        if (!alive || !canvasRef.current) return;
        const createGlobe = mod.default;
        const m = markers.map((mk) => ({ location: mk.location, size: mk.size || 0.06 }));
        globe = createGlobe(canvasRef.current, {
          devicePixelRatio: dpr,
          width: size * dpr,
          height: size * dpr,
          phi,
          theta,
          dark: 1,
          diffuse: 1.2,
          mapSamples: 16000,
          mapBrightness: 7,
          baseColor: [0.28, 0.32, 0.45],
          markerColor: hexToRgb(accent),
          glowColor: hexToRgb(accent),
          markers: m,
          onRender: (state) => {
            if (!focus && !reduceMotion()) { phi += 0.006; }
            state.phi = phi;
            state.theta = theta;
          }
        });
      } catch (e) { if (alive) setFail(true); }
    })();
    return () => { alive = false; cancelAnimationFrame(raf); if (globe) { try { globe.destroy(); } catch { /* ignore */ } } };
  }, [fail, size, accent, JSON.stringify(markers), JSON.stringify(focus)]);

  if (fail) {
    // 정적 글로우 폴백: 어두운 구 + 펄스 점 (항상 렌더)
    return (
      <div style={{ width: size, height: size, margin: '0 auto', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }} aria-hidden="true">
        <div style={{ position: 'absolute', width: size * 0.78, height: size * 0.78, borderRadius: '50%', background: `radial-gradient(circle at 38% 32%, ${accent}55, #0d1430 62%)`, boxShadow: `0 0 60px ${accent}55, inset 0 0 40px #00000066` }} />
        <div style={{ position: 'absolute', width: size * 0.78, height: size * 0.78, borderRadius: '50%', border: '1px solid #ffffff14' }} />
        <span style={{ position: 'relative', fontSize: 40 }}>🌍</span>
        <style>{`@keyframes fmPulseDot{0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(1.6);opacity:1}}`}</style>
        {markers.slice(0, 6).map((mk, i) => (
          <span key={i} style={{ position: 'absolute', left: `${50 + Math.cos((i / Math.max(1, markers.length)) * 6.28) * 34}%`, top: `${50 + Math.sin((i / Math.max(1, markers.length)) * 6.28) * 34}%`, width: 9, height: 9, borderRadius: '50%', background: accent, boxShadow: `0 0 10px ${accent}`, animation: `fmPulseDot 1.8s ${i * 0.2}s ease-in-out infinite` }} />
        ))}
      </div>
    );
  }
  return <canvas ref={canvasRef} style={{ width: size, height: size, maxWidth: '100%', aspectRatio: '1', display: 'block', margin: '0 auto', contain: 'layout paint size' }} />;
}
