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
