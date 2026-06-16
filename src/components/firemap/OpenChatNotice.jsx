import { useState } from 'react';

const STYLE = `
.fm-oc{display:flex;align-items:center;gap:10px;background:#fef3c7;border:1px solid #fde68a;border-radius:14px;padding:11px 13px;margin:0 0 12px}
.fm-oc-tx{flex:1;font-size:13px;color:#92400e;font-weight:700;line-height:1.4}
.fm-oc-tx em{display:block;font-style:normal;font-weight:500;color:#b45309;font-size:11.5px;margin-top:2px}
.fm-oc-go{flex:0 0 auto;background:#fae100;color:#3c1e1e;border:none;border-radius:10px;padding:8px 13px;font-weight:800;font-size:13px;cursor:pointer;text-decoration:none}
.fm-oc-x{flex:0 0 auto;background:none;border:none;color:#b45309;font-size:16px;cursor:pointer;padding:2px 4px;line-height:1}
`;

const KEY = 'fm_oc_dismissed';

export default function OpenChatNotice() {
  const [off, setOff] = useState(() => { try { return localStorage.getItem(KEY) === '1'; } catch { return false; } });
  if (off) return null;
  const dismiss = () => { try { localStorage.setItem(KEY, '1'); } catch { /* ignore */ } setOff(true); };
  const go = () => { try { if (window.gtag) window.gtag('event', 'openchat_click', {}); } catch { /* ignore */ } };
  return (
    <div className='fm-oc'>
      <style>{STYLE}</style>
      <span className='fm-oc-tx'>💬 파이어맵 오픈채팅 열렸어요!<em>같은 목표의 파이어족과 실시간으로 이야기해요 (참여코드: firemap)</em></span>
      <a className='fm-oc-go' href='https://open.kakao.com/o/gIGNhUzi' target='_blank' rel='noopener noreferrer' onClick={go}>참여</a>
      <button type='button' className='fm-oc-x' onClick={dismiss} aria-label='닫기'>✕</button>
    </div>
  );
}
