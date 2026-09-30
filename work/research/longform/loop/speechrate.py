"""경쟁 롱폼 말 속도 실측(RULES '목소리 고정·말 속도' 규칙 2의 기준값).
유튜브 자동 자막(json3, 단어별 시작 시각)만 받는다 — 영상 파일은 받지 않는다(약관).
  받기: py -3.12 -m yt_dlp --skip-download --write-auto-subs --sub-langs "ko.*" --sub-format json3 -o "%(id)s" <url>  (subs/ 폴더)
  재기: py -3.12 work/research/longform/loop/speechrate.py [우리 대본.md 우리 길이초]
잰 값 두 가지:
  gross  = 전체 음절 / (첫 말 ~ 마지막 말) — 쉼 포함, 시청자가 느끼는 '진행 속도'
  speech = 전체 음절 / (단어 사이 간격이 0.6초 미만인 구간 합) — 쉼 뺀 말 자체 속도
음절 = 한글 글자 + 숫자(숫자는 자막 표기에 따라 달라 참고용).
"""
import sys, os, re, json, glob, statistics
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); SUBS = os.path.join(HERE, 'subs')
PAUSE = 0.6

def words(fn):
    ev = json.load(open(fn, encoding='utf-8')).get('events', [])
    out = []
    for e in ev:
        t0 = e.get('tStartMs', 0)
        for s in e.get('segs') or []:
            w = s.get('utf8', '').strip()
            if w and w != '\n': out.append(((t0 + s.get('tOffsetMs', 0)) / 1000, w))
    return sorted(out)

def rate(fn):
    ws = words(fn)
    if len(ws) < 50: return None
    syl = lambda w: len(re.findall('[가-힣0-9]', w))
    total = sum(syl(w) for _, w in ws)
    gross = total / (ws[-1][0] - ws[0][0])
    sp, n = 0.0, 0
    for (a, w), (b, _) in zip(ws, ws[1:]):
        if b - a < PAUSE: sp += b - a; n += syl(w)
    return {'syl': total, 'sec': round(ws[-1][0] - ws[0][0]), 'gross': round(gross, 2), 'speech': round(n / sp, 2) if sp else None}

if __name__ == '__main__':
    rows = {}
    for fn in sorted(glob.glob(os.path.join(SUBS, '*.ko-orig.json3'))) or sorted(glob.glob(os.path.join(SUBS, '*.ko.json3'))):
        vid = os.path.basename(fn).split('.')[0]
        r = rate(fn)
        if r: rows[vid] = r; print(vid, r)
    g = [r['gross'] for r in rows.values()]; s = [r['speech'] for r in rows.values() if r['speech']]
    summ = {'n': len(rows), 'gross_median': round(statistics.median(g), 2), 'gross_range': [min(g), max(g)],
            'speech_median': round(statistics.median(s), 2), 'speech_range': [min(s), max(s)]}
    if len(sys.argv) > 2:
        txt = open(sys.argv[1], encoding='utf-8').read()
        summ['ours'] = {'file': sys.argv[1], 'syl': len(re.findall('[가-힣0-9]', txt)), 'sec': float(sys.argv[2])}
        summ['ours']['gross'] = round(summ['ours']['syl'] / summ['ours']['sec'], 2)
    print(json.dumps(summ, ensure_ascii=False))
    json.dump({'rows': rows, 'summary': summ}, open(os.path.join(HERE, 'speechrate.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
