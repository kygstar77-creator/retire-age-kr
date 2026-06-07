// ───────────────────────────────────────────────────────────────────
// Ant Design 테마 설정 (단일 진입점)
//
// 디자인 시스템을 적용할 때는 이 파일의 값만 교체하면 됩니다.
// main.jsx 의 <ConfigProvider theme={antdTheme}> 에 주입됩니다.
//
// 현재 값은 기존 styles.css 의 색상/형태를 antd 토큰으로 옮겨둔 것이라
// "antd 컴포넌트 + 기존 팔레트" 상태로 동작합니다. 나중에 디자인 시스템의
// 토큰(JSON/Figma 등)을 받으면 아래 token 값만 바꿔치우면 전체에 반영됩니다.
// ───────────────────────────────────────────────────────────────────

export const antdTheme = {
  token: {
    // 브랜드 / 상태 색상
    colorPrimary: '#25624f',
    colorSuccess: '#1d8a64',
    colorWarning: '#b07c00',
    colorError: '#9c2b1f',
    colorInfo: '#25624f',

    // 텍스트 / 배경
    colorText: '#17212c',
    colorTextSecondary: '#55636f',
    colorBgLayout: '#f2f4f6',

    // 형태
    borderRadius: 8,
    borderRadiusLG: 16,
    controlHeight: 40,

    // 타이포그래피
    fontFamily:
      'Inter, Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    fontSize: 15,
  },
  components: {
    // 카드/패널은 기존 디자인의 큰 라운드를 유지
    Card: { borderRadiusLG: 16 },
    Button: { fontWeight: 700 },
    Table: { headerColor: '#5c6b76', borderRadius: 12 },
  },
};

// 판정 상태 → antd Tag 색상 매핑 (statusMeta 의 키와 1:1)
export const statusTagColor = {
  stable: 'success',
  caution: 'warning',
  risk: 'error',
  neutral: 'default',
};
