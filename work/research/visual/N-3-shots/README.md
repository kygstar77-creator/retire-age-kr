# N-3 장면 (visual-designer 2026-11-01~)
- `n3boards.py` 판 → work/video/public/bg/n3/board/ (gitignore). P-3 p3boards.py·K-1 k1boards.py 부품 그대로. 숫자 출처 ep/N-3/calc_out.txt · 말 say_v1.txt 그대로.
- 1회차(11/1 19시): 0~2장 판 10장 r02·r03·r04·r06·r07·r08·r10·r11·r12·r14. 새 Agent 심사 1명(숫자·글자·주황 하나·AI 티) 7 통과·3 고칠 것(toc 체크 다 찍힘·1% 칸에 사람 5명·8천 80.5%→81%) → 고침.
- 2회차(11/1 23시): 3~7장 판 15장 r16·r17·r21~25·r27·r29·r31~34·r36·r38 (r18·r28은 motion PayBlocks·RaiseStairs). 새 Agent 심사 1명 9 통과·6 고칠 것(세전 416→417만원 반올림·도넛 세금 색 통일+범례·8천→1억 줄 '+2천만'·가족 타원 겹침·달력 동전·오른쪽 끝) → 고침.
- 남은 것: 계산기 화면 r40 · 스톡 Pexels 10줄(r01·05·09·13·15·20·26·30·35·39·41 중 r35 썸네일 사진 재사용 가능) · r19·r37은 motion 부품 · 전 줄 비교 그림 shotcmp(mkcmp.py 꼴)·경쟁 장면 대비 새 심사관 품질 판정.
- 3회차(11/2 09시): 스톡 Pexels 11줄 받음 → work/video/public/bg/n3/stock/(gitignore) · 출처 stock_credits.json(desc_line = 설명란 줄) · 고른 판 sc/sheet.jpg·sc/r2/sheet.jpg(sc/는 커밋 안 함) · sheetvid.py · payslip_point 앞 5.5초 얼굴 잘라냄·crosswalk_top 앞 12초 · two_piggy는 구상(저금통 둘)과 다른 동전 병 하나 · **남은 것: 계산기 r40 · 전 줄 shotcmp(N-3 경쟁 캡처부터) · 새 심사관 품질 판정**
- 4회차(11/2 17시): r40 계산기 판 n3_calc_site — firemap.kr/calc/salary 실제 화면 Playwright(cap_r40c.py, 412px·3배, 연봉 4천 기본 → +1000만 = 5천) · 화면 3,571,586원·공제 595,080원 = calc_out 4행 일치 · 손 동그라미(주황)는 실수령 하나, 연봉 칸엔 검은 화살표. **남은 것: N-3 경쟁 캡처 → 전 줄 shotcmp → 새 심사관 2명 품질 판정 → shot_check**
- 5회차(11/04 07시): 경쟁 캡처 60장(scratchpad, 커밋 안 함) → mkcmp.py+pick.json → ep/N-3/shotcmp/r01~41(경쟁 캡처 포함 — 커밋 안 함) · judge_brief.py → 새 Agent 2명 judge1_a/b.json → fill_plan.py · 나음 25·같음 3·못함 13(실사 11줄 전부·r37 꼴·r38 재심사). **남은 것: 실사 11줄 교체 → 2차 새 심사관 · 파일 없는 4줄(motion 부품) 경로 정리**
