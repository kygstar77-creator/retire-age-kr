# 무대 상한 계산 — "계산기+광고"로 한 시장에서 월 최대 얼마까지 가능한가 (bizdev 2026-10-01)
#   py -3.12 work/global_ceiling.py
# 입력은 [실측]/[공식]/[2차]/가정 을 칸마다 적는다. 가정 숫자를 바꾸려면 아래 MARKETS만 고친다.
# 식: 월 수익 = 검색수 × 검색엔진 배수 × 우리가 가져오는 클릭 비율 × 방문당 PV × 1,000PV당 광고 수익
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KR = json.load(open(os.path.join(HERE, 'research', 'global', 'kr_calc_demand.json'), encoding='utf-8'))

MARKETS = {
    '한국(돈·노동 계산기)': dict(
        searches=KR['fin_total'],  # [실측] 네이버 검색광고 2026-10-01, '계산' 포함 키워드 중 돈·노동 계열 합
        engine_mult=1.6,           # 가정: 구글·다음을 더하면 네이버의 1.6배(확인 안 함)
        pv_per_visit=1.5,          # 가정
        rpm_krw=2_500,             # 가정: revenue_model 기본값(한국 애드센스 페이지 RPM, 실측 없음)
    ),
    '한국(계산기 전체)': dict(searches=KR['calc_total'], engine_mult=1.6, pv_per_visit=1.5, rpm_krw=2_500),
}
SHARES = [0.02, 0.10, 0.30, 1.00]  # 우리 사이트가 가져오는 클릭 비율: 2%(현실 1년차 이상) · 10%(분야 1등) · 30%(독점급) · 100%(이론 상한)

def month(m, share):
    return m['searches'] * m['engine_mult'] * share * m['pv_per_visit'] * m['rpm_krw'] / 1000

# 전 세계: 검색어 합이 아니라 '실제로 있는 사이트 규모'로 잰다(research/global/research-raw.md).
USD_KRW = 1_400  # 가정(환율 실측 안 함)
EPMV_USD = {'미국': 16.31, '영국': 14.24, '캐나다': 18.25, '호주': 16.31}  # [2차] Ezoic 공개 EPMV(방문 1,000회당, 2020~21 전 분야) repmv.com
SITES = {  # 월 방문 [2차] Similarweb·Semrush 추정
    'calculator.net': 59_760_000, 'omnicalculator.com': 14_420_000,
    'walletburst.com(FIRE)': 257_000 / 3, 'engaging-data.com(FIRE)': 385_000 / 3,
}

def global_month(visits, epmv=16.31):
    return visits * epmv / 1000 * USD_KRW

if __name__ == '__main__':
    print('\n== 전 세계(영어) — 실존 사이트 규모 × 미국 EPMV $16.31 (가정 환율 1,400원)')
    for k, v in SITES.items():
        print(f'{k}: 월 방문 {v:,.0f} → 월 {global_month(v):,.0f}원')
    need = 100_000_000 / (16.31 / 1000 * USD_KRW)
    print(f'월 1억에 필요한 영어권 월 방문: {need:,.0f} (calculator.net의 {need/59_760_000*100:.1f}%, omni의 {need/14_420_000*100:.0f}%)')
    print()

    print('월 수익(원) — 가져오는 클릭 비율별')
    print('시장 | ' + ' | '.join(f'{int(s*100)}%' for s in SHARES))
    for name, m in MARKETS.items():
        print(name + ' | ' + ' | '.join(f'{month(m, s):,.0f}' for s in SHARES))
    for name, m in MARKETS.items():
        need = 100_000_000 / (m['searches'] * m['engine_mult'] * m['pv_per_visit'] * m['rpm_krw'] / 1000)
        print(f'{name}: 월 1억에 필요한 클릭 비율 {need*100:,.0f}% (100% 넘으면 이 시장 광고만으로 불가)')

# ─────────────────────────────────────────────────────────────
# 나라별 법에 맞는 계산기를 한 사이트에(사장님 10/1 17:04 아이디어) — 이 구조 하나의 상한 (bizdev 10/1 17:2x)
#   py -3.12 work/global_ceiling.py hub
# 근거 [2차]: salaryaftertax.com 약 15개국·월 50.2만~55.5만 방문(Semrush 2026-06·Similarweb 2026-04),
#   thesalarycalculator.co.uk 영국 1위 월 230만(research-raw.md), countrytaxcalc.com 111개국·화면 광고 없음(10/1 직접 열어 봄),
#   talent.com 78개국(구인 사이트에 계산기를 붙인 구조, 월 1,463만 방문은 구인 포함이라 계산기 몫 아님).
# 단가: EPMV $3(애드센스만, research-raw 레드팀 계산) / $16(Ezoic 공개값 미국, 프리미엄 광고망 수준). 비영어권 단가는 확인 안 함.
HUB = {
    # 이름: (나라 수, 나라당 월 방문, 근거)
    '현실선: salaryaftertax 규모(15개국)': (15, 525_000 / 15, '[2차] 실존 다국가 허브 1곳 규모 그대로'),
    '잘됨: 나라마다 1위 사이트의 10%(15개국)': (15, 230_000, '가정: 영국 1위 230만의 10%를 15개국 모두에서'),
    '최상: 나라마다 1위 사이트의 10%(30개국)': (30, 230_000, '가정: 단가 높은 나라 30개 전부. 비영어권 언어·원문 갱신 포함'),
}

def hub():
    print('\n== 나라별 세금·실수령 계산기 허브 — 월 수익(원), 환율 1,400 가정')
    print('경우 | 월 방문 | EPMV $3(애드센스만) | EPMV $16(프리미엄 광고망)')
    for k, (n, per, why) in HUB.items():
        v = n * per
        print(f'{k} | {v:,.0f} | {global_month(v, 3):,.0f} | {global_month(v, 16):,.0f}  ({why})')
    for e in (3, 16):
        need = 100_000_000 / (e / 1000 * USD_KRW)
        print(f'EPMV ${e}: 월 1억 = 월 방문 {need:,.0f} = salaryaftertax의 {need/525_000:.0f}배 = 영국 1위의 {need/2_300_000:.1f}배')

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'hub':
    hub()
