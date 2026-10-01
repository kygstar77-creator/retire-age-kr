# X-KR-1 디자인 검수 심사(제미나이). 대표 이미지 1080 + 시트 2 미리보기 PDF + 시트 1 인쇄 PDF.
import sys, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-flash-lite-latest']
ASK = """You are a senior product designer judging, coldly, a Korean paid Excel household-budget template (9,900 KRW) sold on Kmong/Litt.ly. Answer in Korean.
Files: 1) product thumbnail 1080x1080 (shown ~200px wide in marketplace grids) 2) sheet 2 'retirement age' preview PDF 3) sheet 1 monthly ledger print PDF.
Context: competing budget-template thumbnails on Kmong page 1 show screenshots of charts/tables and '노후 필요 금액'; this product's one differentiator is a per-line '은퇴 +N일' (how many days this monthly expense delays retirement), in orange only.
Criteria: ① one number + one action, 4 colors only (white/ink/gray/orange) ② thumbnail readable at ~200px ③ is the differentiator visible within 3 seconds ④ sheet layout clarity/trust.
First line 'Score: N' (1-10). Then the biggest problem, then up to 2 fixes. Do not comment on wording."""
def part(f, mt): return {'inline_data': {'mime_type': mt, 'data': base64.b64encode(open('build/' + f, 'rb').read()).decode()}}
parts = [{'text': ASK}, part('thumb-1080.png', 'image/png'), part('sheet2-preview.pdf', 'application/pdf'), part('sheet1-print.pdf', 'application/pdf')]
body = {'contents': [{'parts': parts}]}
for m in MODELS:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
        print(f'[모델 {m}]'); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e:
        print(f'[{m} 실패 {e}]', file=sys.stderr)
