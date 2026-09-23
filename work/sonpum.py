# 자동 손품 영상 — 사장님 아이디어(2026-09-23): 네이버 부동산을 대신 돌아다니며 단지마다 매매·전세·월세·세대수·준공·역·학교를 보여주고 해설한다.
#   python work/sonpum.py "마포구 공덕동" 37.5445 126.9515 [단지수=5]
# 흐름: 지도(사람 속도) → 단지 마커 클릭 → 단지 정보·매매/전세/월세 화면 캡처 → 장면마다 해설 문장 → edge-tts(무료) 음성 → ffmpeg(imageio-ffmpeg) 합치기 → work/research/sonpum/<동네>_<날짜>.mp4
# 규칙: 화면 숫자만 읽는다(예측·권유 없음). 네이버 부동산은 과다 요청을 막으므로 장면당 3~6초, 하루 1~2동네.
import sys, os, re, json, time, asyncio, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import edge_tts, imageio_ffmpeg
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'
FF = imageio_ffmpeg.get_ffmpeg_exe(); VOICE = 'ko-KR-SunHiNeural'
area, lat, lng = sys.argv[1], sys.argv[2], sys.argv[3]; N = int(sys.argv[4]) if len(sys.argv) > 4 else 5
day = time.strftime('%Y-%m-%d'); OUT = os.path.join(HERE, 'research', 'sonpum', f'{area.replace(" ", "_")}_{day}'); os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(os.environ.get('TEMP', 'C:/Temp'), 'sonpum_' + day); os.makedirs(TMP, exist_ok=True)   # ffmpeg·cv는 ASCII 경로

def font(sz):
    p = os.path.join(FD, 'pd700.ttf'); return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', sz)

def caption(png, text, out):
    im = Image.open(png).convert('RGB'); dr = ImageDraw.Draw(im); W, H = im.size; f = font(30)
    lines, cur = [], ''
    for w in text.split():
        if dr.textlength(cur + ' ' + w, font=f) > W - 120: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    lines.append(cur); h = 44 * len(lines) + 30
    dr.rectangle([0, H - h, W, H], fill=(0, 0, 0));
    for i, l in enumerate(lines): dr.text((60, H - h + 15 + i * 44), l, font=f, fill=(255, 255, 255))
    im.save(out)

def tts(text, mp3):
    asyncio.run(edge_tts.Communicate(text, VOICE, rate='+5%').save(mp3))

def txt(page): return re.sub(r'[\u200b\xa0]+', ' ', page.evaluate('document.body.innerText'))
def close_popup(page):
    for sel in ('text=다시 보지 않기', 'button.btn_close', '[class*=close]'):
        try:
            el = page.locator(sel).first
            if el.count() and el.is_visible(timeout=800): el.click(); page.wait_for_timeout(500); break
        except Exception: pass

PANEL_JS = """() => { const all=[...document.querySelectorAll('div,section,article')].filter(e=>/세대 \/ 총/.test(e.innerText||'') && e.innerText.length<4000); all.sort((a,b)=>a.innerText.length-b.innerText.length); return all.length? all[0].innerText : '' }"""
def panel(page):
    # 화면 텍스트 실측(2026-09-23): 단지명/유형/아파트/세대수/534세대/동수/총 10동/사용승인일/2003.12.05/면적/108.04㎡ ~ 189.8㎡/최근 매매 실거래가/26억/2026.09.15, 18층, 108㎡/매매가28억 5,000~34억 2,000/전세가15억
    import re as _re
    lines = [l.strip() for l in txt(page).splitlines() if l.strip()]
    try:
        u = lines.index('유형'); name = lines[u - 1]
        def val(label):
            k = lines.index(label, u); return lines[k + 1]
        se = _re.search(r'([\d,]+)세대', val('세대수')); dong = _re.search(r'(\d+)동', val('동수')); ymd = _re.match(r'(\d{4})\.(\d{2})', val('사용승인일')); ar = _re.match(r'([\d.]+)㎡\s*~\s*([\d.]+)㎡', val('면적'))
        info = {'세대': int(se.group(1).replace(',', '')) if se else 0, '동': dong.group(1) if dong else '?', '준공': f'{ymd.group(1)}년 {int(ymd.group(2))}월' if ymd else '?', '면적': f'{ar.group(1)}~{ar.group(2)}㎡' if ar else val('면적')}
        info['매매가'] = next((l[3:].strip() for l in lines[u:u + 30] if l.startswith('매매가')), '')
        info['전세가'] = next((l[3:].strip() for l in lines[u:u + 30] if l.startswith('전세가')), '')
        try:
            k = lines.index('최근 매매 실거래가', u); info['실거래'] = lines[k + 1] + ' (' + lines[k + 2] + ')'
        except ValueError: info['실거래'] = ''
        return name, info
    except (ValueError, IndexError):
        return '', {}

def listings(page, nm):
    # 매물 카드 실측: 집주인마포자이 108동 / 매매28억 5,000 / 아파트135/113m², 3/19층, 남서향 / 설명 한 줄 / … 제공 / 중개사 / 확인매물 26.09.23.
    import re as _re
    lines = [l.strip() for l in txt(page).splitlines() if l.strip()]
    out = []
    for k in range(1, len(lines) - 2):
        if lines[k].startswith(nm) and lines[k + 1].startswith('아파트') and _re.search(r'\d', lines[k]):
            m = _re.match(r'아파트\s*([\d./]+)m?[²㎡],\s*([\w/]+)층,\s*(\S+향)', lines[k + 1])
            dong = _re.search(r'(\d+동)', lines[k - 1]); desc = lines[k + 2] if not lines[k + 2].endswith('제공') else ''
            out.append({'가격': lines[k][len(nm):].strip(), '면적': m.group(1) if m else '', '층': m.group(2) if m else '', '향': m.group(3) if m else '', '동': dong.group(1) if dong else '', '설명': desc[:60]})
            if len(out) >= 3: break
    return out


scenes = []   # (png, narration)
with sync_playwright() as p:
    b = p.chromium.launch(headless=True); ctx = b.new_context(locale='ko-KR', viewport={'width': 1400, 'height': 900}, user_agent=UA); page = ctx.new_page()
    url = f'https://new.land.naver.com/complexes?ms={lat},{lng},16&a=APT&e=RETAIL'
    page.goto(url, wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(7000); close_popup(page); page.wait_for_timeout(1000)
    png = os.path.join(TMP, 's00.png'); page.screenshot(path=png)
    scenes.append((png, f'{area} 아파트 지도입니다. 네이버 부동산에 올라온 매물 호가를 단지별로 하나씩 보겠습니다. 오늘은 {day} 기준입니다.'))
    markers = page.locator('.marker_complex--apart')
    cnt = min(markers.count(), 40); print('마커', markers.count())
    picked = []
    for i in range(cnt):
        try:
            m = markers.nth(i); bb = m.bounding_box()
            if not bb or bb['y'] < 180 or bb['y'] > 860 or bb['x'] < 60 or bb['x'] > 1300: continue
            t = m.inner_text().replace('\n', ' ')
            ar = re.search(r'면적\s*([\d.]+)', t)
            if re.search(r'(^|\s)매\d', t) and ar and float(ar.group(1)) >= 59: picked.append((i, t, bb))
        except Exception: pass
    picked = picked[:N * 3]; print('후보', [t for _, t, _ in picked])
    k = 0
    for (i, t, bb) in picked:
        if k >= N: break
        try:
            page.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); page.wait_for_timeout(5000)
            m = re.search(r'complexes/(\d+)', page.url); no = m.group(1) if m else None
            name, info = panel(page)
            if not no or not info or info.get('세대', 0) < 100:
                print('건너뜀', name, info.get('세대')); page.goto(url, wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(4500); close_popup(page); markers = page.locator('.marker_complex--apart'); continue
            k += 1
            head = f"{k}번째 단지, {name}. {info['세대']:,}세대 {info['동']}개 동, {info['준공']} 준공, 전용 {info['면적']}. 매매 호가 {info['매매가'] or '없음'}, 전세 호가 {info['전세가'] or '없음'}." + (f" 최근 실거래 {info['실거래']}." if info.get('실거래') else '')
            for code, nm in (('A1', '매매'), ('B1', '전세'), ('B2', '월세')):
                page.goto(f'https://new.land.naver.com/complexes/{no}?ms={lat},{lng},16&a=APT&b={code}&e=RETAIL', wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(5500); close_popup(page)
                ls = listings(page, nm); sp = os.path.join(TMP, f's{k:02d}_{code}.png'); page.screenshot(path=sp)
                if ls: nar = f"{name} {nm} 매물 {len(ls)}건. " + ' '.join(f"{x['동']} {x['가격']}, 전용 {x['면적'].split('/')[-1]}제곱미터 {x['층']}층 {x['향']}. {x['설명']}" for x in ls)
                else: nar = f"{name}은 지금 {nm} 매물이 없습니다."
                if code == 'A1': nar = head + ' ' + nar
                scenes.append((sp, nar))
            print(k, no, name, info, [len(listings(page, x)) for x in ('월세',)])
            page.goto(url, wait_until='domcontentloaded', timeout=60000); page.wait_for_timeout(5000); close_popup(page)
            markers = page.locator('.marker_complex--apart')
        except Exception as e: print('단지 실패', str(e)[:80])
    ctx.close(); b.close()

# 장면 → mp4
parts = []
for i, (png, nar) in enumerate(scenes):
    cap = os.path.join(TMP, f'c{i:02d}.png'); caption(png, nar, cap)
    mp3 = os.path.join(TMP, f'a{i:02d}.mp3'); tts(nar, mp3)
    seg = os.path.join(TMP, f'p{i:02d}.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-loop', '1', '-i', cap, '-i', mp3, '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p', '-vf', 'scale=1280:-2', '-shortest', seg], check=True)
    parts.append(seg)
lst = os.path.join(TMP, 'list.txt'); open(lst, 'w', encoding='utf-8').write(''.join(f"file '{p_.replace(chr(92), '/')}'\n" for p_ in parts))
final_tmp = os.path.join(TMP, 'final.mp4')
subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', final_tmp], check=True)
final = os.path.join(OUT, 'sonpum.mp4'); import shutil; shutil.copy(final_tmp, final)
json.dump([{'png': os.path.basename(p_), 'narration': n} for p_, n in scenes], open(os.path.join(OUT, 'scenes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for p_, _ in scenes: shutil.copy(p_, os.path.join(OUT, os.path.basename(p_)))
print('완성', final, os.path.getsize(final), 'bytes, 장면', len(scenes))
