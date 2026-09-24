# 시군구 코드를 실거래 API로 직접 확인해서 찾는다.
#   py -3.12 work/lawdscan.py 41 202606 202608     → 경기도(41) 유효 코드 + 지역명
#
# 왜 이렇게 하나: 법정동코드를 어디서 베껴 오면 그게 맞는지 확인할 길이 없다.
# 행정표준코드 API(1741000)는 403(별도 승인)이라 못 쓴다.
# 그래서 국토부 실거래 API에 직접 물어본다 — 응답이 오면 그 코드는 실재하고,
# 응답 안의 법정동명으로 지역 이름까지 같이 얻는다. 지어낸 값이 섞일 수 없다.
#
# 사장님 2026-09-24: "부동산은 니가 서울 경기도 등등 구역 돌아다니면서 저평가 단지 찾고 있는 거야?"
# 그때까지 서울 25개 구만 봤다(work/research/rt/ 602개 파일 전부 11로 시작).
import sys, os, re, json, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'research', 'sgg_found.json')
KEY = [l.split('=', 1)[1].strip() for l in open(r'C:\Users\강영준\Documents\datago_key.txt', encoding='utf-8-sig') if l.startswith('KEY=')][0]
EP = 'RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev'

def probe(lawd, ym):
    """그 코드로 아파트 매매가 잡히나. 잡히면 (건수, 법정동 예시)."""
    q = urllib.parse.urlencode({'serviceKey': KEY, 'LAWD_CD': lawd, 'DEAL_YMD': ym, 'numOfRows': '20', 'pageNo': '1'})
    try:
        s = urllib.request.urlopen('https://apis.data.go.kr/1613000/' + EP + '?' + q, timeout=20).read().decode('utf-8', 'ignore')
    except Exception:
        return 0, None
    try: root = ET.fromstring(s)
    except Exception: return 0, None
    items = root.findall('.//item')
    if not items: return 0, None
    dongs = [ (it.findtext('umdNm') or '').strip() for it in items ]
    dongs = [d for d in dongs if d]
    return len(items), (dongs[0] if dongs else None)

def main():
    pre = sys.argv[1] if len(sys.argv) > 1 else '41'
    yms = sys.argv[2:] or [time.strftime('%Y%m')]
    found = {}
    try: found = json.load(open(OUT, encoding='utf-8'))
    except Exception: pass
    t0 = time.time(); hit = 0
    for n in range(1000):
        code = f'{pre}{n:03d}'
        if code in found: continue
        got, dong = 0, None
        for ym in yms:                       # 한 달에 거래가 없을 수 있으니 여러 달 본다
            got, dong = probe(code, ym)
            if got: break
            time.sleep(0.12)
        if got:
            found[code] = {'dong': dong, 'n': got}
            hit += 1
            print(f'{code}  거래 {got:>3}건  예: {dong}')
            json.dump(found, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        time.sleep(0.12)
    print(f'\n{pre}로 시작하는 유효 시군구 {len(found)}개 (이번에 새로 {hit}개) · {int(time.time()-t0)}초')
    print('저장', OUT)

if __name__ == '__main__': main()
