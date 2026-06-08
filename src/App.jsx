import { useEffect } from 'react';
import FireMapMVP from './components/FireMapMVP.jsx';

export default function App() {
  useEffect(() => {
    const text = '현재 계산 기준 · 연 수익률 8% · 물가 3%';
    const applyPolish = () => {
      document.querySelectorAll('.fm-actions button').forEach((button) => {
        if (button.textContent === '초기화') button.hidden = true;
      });
      document.querySelectorAll('.fm-text-card h2, .fm-graph h2').forEach((title) => {
        title.style.fontSize = '30px';
        title.style.lineHeight = '1.15';
        title.style.letterSpacing = '-0.07em';
      });
      const result = document.querySelector('.fm-result');
      if (!result || result.querySelector('.fm-assumption-inline')) return;
      const badge = document.createElement('span');
      badge.className = 'fm-assumption-inline';
      badge.textContent = text;
      result.appendChild(badge);
    };
    applyPolish();
    const observer = new MutationObserver(applyPolish);
    observer.observe(document.body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, []);

  return <FireMapMVP />;
}
