# 국토교통부 아파트 매매 실거래(공공데이터포털 1613000 RTMSDataSvcAptTradeDev) — 인천 28275(청라동·가정동·가좌동·석남동 등)·28290(당하동·원당동·마전동·불로동 등 검단)
# 옛 코드 28260은 2021-01·2026-10 모두 0건(2026-11-17 확인) — 새 코드로 옛 거래까지 다시 매겨진 것으로 보임. 구 이름은 쓰지 않고 동 이름만 쓴다.
# 계약 2021-01~2026-11, 2026-11-17 firemap-write-b 받음 (rtmolit.fetch 그대로)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = [f'{y}{m:02d}' for y in (2021, 2022, 2023, 2024, 2025) for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
for code in ('28275', '28290'):
    for ym in yms:
        p = os.path.join(out, f'{code}_{ym}_trade.json')
        if os.path.exists(p): continue
        rows = R.fetch('trade', code, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(code, ym, len(rows), flush=True)
