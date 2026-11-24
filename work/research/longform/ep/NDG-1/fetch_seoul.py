# NDG-1 대조군 — 서울 25개 구 아파트 매매만(전월세·오피스텔 빼고) 2021-01~2026-11 받기 (youtube-loop 2026-11-24)
# editor 반론(review_editor_gemini_1124.md ②-2 '서울 전체 대조군 없음')에 답하려고. 이미 있는 파일은 신고 기한 지난 뒤 받은 것만 건너뜀(rtmolit 규칙).
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..')
sys.path.insert(0, W); import rtmolit
OUT = os.path.join(W, 'research', 'rt')
sgg = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
months = [f'{y}{m:02d}' for y in range(2021, 2027) for m in range(1, 13) if f'{y}{m:02d}' <= '202611']
calls = 0
for lawd, name in sgg.items():
    for ym in months:
        p = os.path.join(OUT, f'{lawd}_{ym}_trade.json')
        ny, nm = (int(ym[:4]) + 1, 1) if ym[4:] == '12' else (int(ym[:4]), int(ym[4:]) + 1)
        settled = time.mktime((ny, nm, 1, 0, 0, 0, 0, 0, -1)) + 31 * 86400
        if os.path.exists(p) and os.path.getmtime(p) >= settled: continue
        try:
            rows = rtmolit.fetch('trade', lawd, ym); calls += 1
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        except Exception as e: print(f'{name} {ym} 실패: {e}', flush=True)
        time.sleep(0.2)
    print(f'{name} 끝 (누적 호출 {calls})', flush=True)
print('완료', calls)
