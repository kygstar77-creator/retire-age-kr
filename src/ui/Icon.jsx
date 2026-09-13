// DS-31 Icon — 자체 선 아이콘 세트. OS 이모지는 기기마다 달라 보여서 쓰지 않는다(6차 결정서: 섹션 이모지 금지).
// 24 뷰박스 · 선 1.8 · currentColor. 크기는 size(px)로, 색은 부모 글자색을 따른다.
const P = {
  flag: 'M6 21V4M6 4h11l-2.2 3.6L17 11H6',
  menu: 'M4 6h16M4 12h16M4 18h16',
  trophy: 'M8 21h8M12 17v4M6 4h12v5a6 6 0 0 1-12 0zM6 6H3.5v1A3.5 3.5 0 0 0 7 11M18 6h2.5v1A3.5 3.5 0 0 1 17 11',
  sliders: 'M4 7h9m3 0h4M4 17h4m3 0h9M13 4.5v5M8 14.5v5',
  coins: 'M12 3c-4 0-7 1.3-7 3s3 3 7 3 7-1.3 7-3-3-3-7-3zM5 6v6c0 1.7 3 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3 3 7 3s7-1.3 7-3v-6',
  stethoscope: 'M6 3v6a5 5 0 0 0 10 0V3M11 14v2a4 4 0 0 0 8 0v-2M19 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4z',
  receipt: 'M6 3h12v18l-3-2-3 2-3-2-3 2V3zM9 8h6M9 12h6',
  bank: 'M3 9l9-5 9 5H3zM5 9v8M10 9v8M14 9v8M19 9v8M3 21h18',
  map: 'M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2V6zM9 4v14M15 6v14',
  compass: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM15.5 8.5l-2 5-5 2 2-5 5-2z',
  leaf: 'M20 4C10 4 4 10 4 20c10 0 16-6 16-16zM4 20c4-5 8-8 12-10',
  chat: 'M4 5h16v11H9l-5 4V5z',
  newspaper: 'M4 5h16v14H4zM8 9h4v4H8zM14 9h3M14 13h3M8 17h9',
  play: 'M6 4l14 8-14 8V4z',
  book: 'M5 4h10a3 3 0 0 1 3 3v13H8a3 3 0 0 0-3 3V4zM5 17a3 3 0 0 1 3-3h10',
  settings: 'M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM19 12l2-1-1-3-2 .5-1.5-1.5.5-2-3-1-1 2h-2l-1-2-3 1 .5 2L6.5 8.5 4.5 8l-1 3 2 1v2l-2 1 1 3 2-.5 1.5 1.5-.5 2 3 1 1-2h2l1 2 3-1-.5-2 1.5-1.5 2 .5 1-3-2-1v-2z',
  file: 'M6 3h8l4 4v14H6V3zM14 3v4h4M9 12h6M9 16h6',
  lock: 'M6 11h12v10H6zM8 11V8a4 4 0 0 1 8 0v3',
  mail: 'M3 6h18v12H3zM3 7l9 6 9-6',
  user: 'M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM4 21a8 8 0 0 1 16 0',
  bell: 'M6 16V11a6 6 0 0 1 12 0v5l2 2H4l2-2zM10 21h4',
  eyeoff: 'M3 3l18 18M10 6.5A9 9 0 0 1 21 12a12 12 0 0 1-2.5 3.2M6.5 8A12 12 0 0 0 3 12s3 6 9 6a8 8 0 0 0 3-.6M9.5 9.5a3 3 0 0 0 4.2 4.2',
  moon: 'M20 14A8 8 0 0 1 10 4a8 8 0 1 0 10 10z',
  phone: 'M7 2h10v20H7zM11 18h2',
  chartbar: 'M4 20h16M6 16v-5M11 16V6M16 16v-8M21 16v-3',
  chartline: 'M4 19h16M4 15l5-5 4 4 7-7',
  calendar: 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4',
  cake: 'M4 13h16v7H4zM6 13V9h12v4M9 9V6M12 9V5M15 9V6',
  home: 'M4 11l8-7 8 7v9h-5v-6H9v6H4v-9z',
  globe: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM2 12h20M12 2c3 3 3 17 0 20M12 2c-3 3-3 17 0 20',
  buildings: 'M3 21V8h7v13M10 21V4h8v17M14 8h1M14 12h1M14 16h1M6 12h1M6 16h1M3 21h18',
  fork: 'M7 3v7a2 2 0 0 0 4 0V3M9 3v18M17 3c-2 0-3 3-3 6v3h3v9',
  pin: 'M12 22s7-6 7-12a7 7 0 1 0-14 0c0 6 7 12 7 12zM12 7a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
  check: 'M5 12l5 5 9-10',
  alert: 'M12 3l10 18H2L12 3zM12 10v5M12 18v.5',
  coffee: 'M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8zM17 9h2a2 2 0 0 1 0 4h-2M7 3v2M10 3v2M13 3v2',
  eye: 'M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12zM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
  arrow: 'M5 12h14M13 6l6 6-6 6',
  link: 'M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5',
  share: 'M12 3v12M7 8l5-5 5 5M5 14v6h14v-6',
  edit: 'M4 20h4l11-11-4-4L4 16v4zM13 7l4 4',
  heart: 'M12 21s-8-5-8-11a4 4 0 0 1 8-2 4 4 0 0 1 8 2c0 6-8 11-8 11z',
  question: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 1-1 1.7M12 17v.5',
  fire: 'M12 3c1 4-4 6-4 11a4 4 0 0 0 8 0c0-3-2-4-1-7 2 1 4 4 4 7a7 7 0 0 1-14 0c0-6 6-8 7-11z',
  calc: 'M6 3h12v18H6zM9 7h6M9 12h1M12 12h1M15 12h1M9 15h1M12 15h1M15 15h4',
  star: 'M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.3l1.1-6.2L3 9.7l6.2-.9L12 3z',
  target: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zM12 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z',
  island: 'M3 20h18M12 20V9M12 9c-4-3-7-2-8 1 3-1 5 0 8-1zM12 9c4-3 7-2 8 1-3-1-5 0-8-1zM12 9c0-3 2-5 5-6-2 2-3 4-5 6z',
  search: 'M10 4a6 6 0 1 0 0 12 6 6 0 0 0 0-12zM20 20l-5.5-5.5',
  close: 'M6 6l12 12M18 6L6 18',
  smile: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM8 14s1.5 2 4 2 4-2 4-2M9 9h.5M14.5 9h.5'
};

export function Icon({ name, size = 18, className = '', title }) {
  const d = P[name] || P.flag;
  return (
    <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden={title ? undefined : 'true'} role={title ? 'img' : undefined}>
      {title && <title>{title}</title>}
      <path d={d} />
    </svg>
  );
}
