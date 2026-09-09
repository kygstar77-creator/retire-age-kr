// 레거시 Header — 아직 옮기지 않은 도구 화면용 얇은 어댑터. 새 화면은 ui/TopBar를 직접 쓴다.
import { TopBar } from '../../ui/index.js';

export default function Header({ tag, onBack }) {
  return <TopBar title={tag} onBack={onBack} onHome={() => { window.location.hash = '#home'; }} />;
}
