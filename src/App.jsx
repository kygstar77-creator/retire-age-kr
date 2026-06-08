import { useEffect } from 'react';
import FireMapMVP from './components/FireMapMVP.jsx';

export default function App() {
  useEffect(() => {
    const text = '현재 계산 기준 · 연 수익률 8% · 물가 3%';
    const applyBadge = () => {
      const result = document.querySelector('.fm-result');
      if (!result || result.querySelector('.fm-assumption-inline')) return;
      const badge = document.createElement('span');
      badge.className = 'fm-assumption-inline';
      badge.textContent = text;
      result.appendChild(badge);
    };
    applyBadge();
    const observer = new MutationObserver(applyBadge);
    observer.observe(document.body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, []);

  return <FireMapMVP />;
}
