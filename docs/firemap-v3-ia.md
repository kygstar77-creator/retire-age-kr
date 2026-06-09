# FireMap v3 IA (정보구조 명세)

> FigJam 흐름: https://www.figma.com/board/eqaynreMLz41AwWvWzkse9
> 라우팅은 screen manifest(선언적 설정) 단일 진실원천에서 생성.

## 흐름 개요
home → question(1화면 1질문) → result → { experiment(비교) · advanced(고급 모듈) · city · share · community }
- experiment·advanced·city는 계산 후 "적용"으로 result에 회귀.
- community는 결과 이후 진입(계산 흐름 비방해), Supabase 연동.

## screen manifest 구조 (제안)
각 화면을 데이터로 선언 → 라우터·하단 네비·진행바·다음행동이 자동 생성.
필드: id, hash, title, type(home|question|result|module|share|community), nextActions[], guard(진입조건), component.

예시:
- { id:'home', hash:'#home', type:'home', nextActions:['question'] }
- { id:'question', hash:'#question', type:'question' }
- { id:'result', hash:'#result', type:'result', nextActions:['experiment','city','share','community'] }
- { id:'experiment', hash:'#experiment', type:'module', back:'result' }
- { id:'advanced', hash:'#advanced', type:'module', back:'result' }   // 건보료·양도세·연금·환율 모듈 호스트
- { id:'city', hash:'#city', type:'module', back:'result' }           // (구 curation, 호환 alias 유지)
- { id:'share', hash:'#share', type:'share', back:'result' }
- { id:'community', hash:'#community', type:'community', back:'result' } // 신규, Supabase

## 화면별 목적/구성
- Home: 한 줄 약속 + 신뢰 칩(브라우저 저장·참고용·투자권유 아님) + 시작 CTA.
- Question: 한 화면당 하나. 진행바, 단위 칩, 슬라이더+스텝퍼.
- Result: 요약(퇴사나이·자산수명) / 진단(점수·상태) / **핵심 레버 2개** / 다음행동(비교·도시·공유). 피드 같지 않게 그룹화.
- Experiment(비교): 조건 조정 + 현재 vs What-If 2선 오버레이 차트, 탭 인디케이터.
- Advanced(모듈): 건보료/해외체류/현금흐름/세금/환율 — 각 입력·가정·결과·적용.
- City: 국내·해외 도시 생활비 프리셋 → 자산수명 비교(참고 시나리오 고지).
- Share: 결과 이미지 / 요약 / 기본 링크 / 조건 링크(Base64 난독화) / 커뮤니티용 카피.
- Community: 결과 이후 익명 피드백·스토리(Supabase RLS, 개인 금융입력은 opt-in 없이는 미저장).

## 변경 메모(코드)
- 현재 'curation' = City 역할. v3에선 'city'를 정식 라우트로, 'curation'은 호환 alias.
- Result는 레버 4개→상위 2개로 축약, 다음행동 그룹 분리(작업 중).
