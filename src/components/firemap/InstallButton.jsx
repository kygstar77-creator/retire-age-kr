import { useEffect, useState } from 'react';
import { installAvailable, onInstallChange, promptInstall } from '../../utils/installPrompt.js';
import { track } from '../../firemap-v2/dailyData.js';

// 안드로이드: 네이티브 설치 프롬프트. (iOS는 매니페스트+apple-touch로 '공유→홈화면 추가' 아이콘 제공)
export default function InstallButton() {
  const [avail, setAvail] = useState(installAvailable());
  useEffect(() => onInstallChange(() => setAvail(installAvailable())), []);
  if (!avail) return null;
  const click = async () => {
    track('install_click');
    const outcome = await promptInstall();
    track('install_result', { outcome: outcome || 'none' });
  };
  return (
    <button type="button" className="fm-install-btn" onClick={click}>
      📲 홈 화면에 추가하고 매일 체크하기
    </button>
  );
}
