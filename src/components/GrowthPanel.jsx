import { Copy, ExternalLink, Share2 } from 'lucide-react';
import { useState } from 'react';
import { Button, Space } from 'antd';
import { buildShareText, buildShareUrl } from '../utils/shareState.js';

export default function GrowthPanel({ inputs, simulation }) {
  const [copied, setCopied] = useState('');

  const copy = async (type) => {
    const text = type === 'link'
      ? buildShareUrl(inputs)
      : `${buildShareText(simulation)}\n\n${buildShareUrl(inputs)}`;

    await navigator.clipboard.writeText(text);
    setCopied(type);
    window.setTimeout(() => setCopied(''), 1800);
  };

  return (
    <section className="growth-panel">
      <div>
        <p className="eyebrow">공유</p>
        <h2>내 결과를 링크로 저장하기</h2>
        <p>
          입력값이 담긴 링크를 만들어 친구나 커뮤니티에서 바로 비교할 수 있습니다.
          앱 설치나 회원가입은 필요 없습니다.
        </p>
      </div>
      <Space wrap className="growth-actions-antd">
        <Button type="primary" icon={<Share2 size={18} />} onClick={() => copy('link')}>
          {copied === 'link' ? '링크 복사됨' : '계산 링크 복사'}
        </Button>
        <Button icon={<Copy size={18} />} onClick={() => copy('summary')}>
          {copied === 'summary' ? '요약 복사됨' : '결과 요약 복사'}
        </Button>
        <Button icon={<ExternalLink size={18} />} href="#legal">
          안내 보기
        </Button>
      </Space>
    </section>
  );
}
