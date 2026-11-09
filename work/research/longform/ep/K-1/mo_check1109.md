# K-1 렌더본 mo 구간 확인 (23:14, 2026-11-09 motion)
대상: work/video/out/k1_ds.mp4(11/9 14:20, meta.video, 509.0초) · 같은 props k1.json(09:13). 잰 도구: bgcheck 기록 k1_ds.mp4.bgcheck.json(14:22, 파일 mtime 일치) · lfrender.still_runs(렌더본 직접) · overlap.json(ovcheck, props 기준) · 프레임 3장 직접 봄(mo_check1109/).

| mo | 시각 구간 | 장면 | 같은 판 길이(기준 ≤20) | 렌더본 최장 정지(U5 ≤8) | 겹침(overlap.json) | ⑥ UI 상자 2개↑ 프레임 | 상자 1개 프레임 | 글자 줄 중앙(기준 ≤8, 영상 전체 기준) | 큰 글자 최소 |
|---|---|---|---|---|---|---|---|---|---|
| over | 57.4~75.0 | 1장 5% 선(DaysOver) | 17.6초 | 3.0초 | 0 | 0/17 | 4/17(71~74초) | 7 | 9.8% |
| cross | 197.7~212.8 | 3장 고정·변동(CrossOver) | 15.1초 | 2.5초 | 0 | 0/15 | 0/15 | 12 | 9.8% |
| dots | 326.1~344.4 | 4장 같은 쪽 달(SameDirDots) | 18.3초 | 5.0초 | 0 | 0/18 | 0/18 | 10 | 9.4% |

- 영상 전체: ⑥ box_frac 0.0 · 같은 판 최장 18.3초(=dots) · 정지 최장 6.0초(499초, mo 아님) · 겹침 0(509프레임, 1초 간격) · bgcheck ok=True.
- 겹침 근거 신선도: overlap.json(09:28)은 props·K-1이 쓰는 motion tsx(DaysOver·CrossOver·SameDirDots)보다 새것. 그 뒤 바뀐 motion tsx(PayBlocks·RaiseStairs 11:31)는 K1.tsx가 안 쓴다.
- 자막 띠 가림: 프레임 3장(72.5·209·342초, 960px) — 자막 띠 y 약 470~520, 출처 줄 y 약 441 · 범례 y 약 430 · 그래프는 그 위에서 끝남, 가림 없음. 자막 띠 가림을 자동으로 재는 관문은 롱폼에 없어 프레임 3장 눈으로만 확인(구간 전부는 아님).
- 참고(고칠 일 아님): cross·dots의 글자 줄 중앙 12·10은 LINES_MAX 8을 넘지만, 관문은 영상 전체 중앙 7로 재서 통과. 축·범례·값 글자가 셈에 든 것. dots 판은 18.3초라 BOARD_MAX 20에 1.7초 남음(움직임 판은 5.8초 변화 구간 있음).

## 공개 전에 걸리는 것 1건 (PD 몫)
lfrender screen 기록이 렌더본과 안 맞는다: `screen_ok_for_upload('k1_ds.mp4')` = False '화면 관문 뒤 렌더본이 바뀌었다 — lfrender.py screen 다시'. out/k1.screen.json은 size 44,674,510(= k1_part_8000-11999 크기, k1.mp4는 169,627,440)·mtime 10:45:24(k1.mp4 10:45:42), out/k1_ds.screen.json은 11/5 16:03 129,135,726바이트(옛 렌더). 위 표의 정지·겹침 수치는 통과라 `py -3.12 work/lfrender.py screen research/longform/ep/K-1`을 다시 돌리면 기록이 맞춰질 것(내가 돌리면 PD의 기록 파일을 쓰게 돼 안 돌림).
