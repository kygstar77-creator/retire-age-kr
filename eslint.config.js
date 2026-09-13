// 선언되지 않은 이름과 안 쓰는 이름을 잡는 최소 설정.
// 이유: 저축 기능을 걷어낼 때 Leaderboard의 myAdvance와 ShareSheet의 family가 호출부에만 남아
// 빌드는 통과하는데 랭킹 화면과 공유 링크 버튼이 런타임에 통째로 죽어 있었다.
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';

export default [
  {
    files: ['src/**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: 'module',
      globals: { ...globals.browser, ...globals.es2021 },
      parserOptions: { ecmaFeatures: { jsx: true } }
    },
    plugins: { 'react-hooks': reactHooks },
    rules: {
      'no-undef': 'error',
      'no-unused-vars': ['warn', { args: 'none', varsIgnorePattern: '^_' }],
      'react-hooks/rules-of-hooks': 'error'
    }
  },
  {
    files: ['functions/**/*.js', 'work/**/*.mjs', 'tests/**/*.mjs', 'scripts/**/*.{js,mjs}'],
    languageOptions: { ecmaVersion: 2023, sourceType: 'module', globals: { ...globals.node, ...globals.browser } },
    rules: { 'no-undef': 'error' }
  }
];
