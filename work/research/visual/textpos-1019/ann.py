# 90장 눈으로 본 기록(10/19, 3x3 안내선 판 view_*.jpg로 한 장씩 봄). 번호 = data.json rows 순서.
# pos: 큰 글 덩어리의 가운데가 놓인 칸(위/가운데/아래 × 왼/가운데/오른). '넓게' = 화면 폭 거의 끝까지(가운데 칸으로 셈).
# under: 띠 = 아래 검정·회색 띠나 짙은 그라데이션 위 / 상자 = 글자 뒤 색 상자 / 사진 = 사진 위에 바로(띠 없음) / 그래픽 = 단색 그림판
# subj: 주인공(얼굴·사물) 자리
A = {}
def put(rng, **kw):
    for i in rng: A[i] = dict(kw)
put(range(0, 5),  pos='아래-넓게', lines=2, under='띠', subj='위쪽(실제 얼굴·삽화)')        # 수페TV
put(range(5, 10), pos='아래-넓게', lines=2, under='띠', subj='위 오른쪽 진행자+위 왼쪽 삽화')  # 소수몽키
put(range(10, 15), pos='아래-넓게', lines=2, under='띠', subj='위쪽 얼굴(가운데~오른쪽)')     # 월부
A[12] = dict(pos='아래-가운데', lines=2, under='띠', subj='오른쪽 얼굴')
A[13] = dict(pos='아래-가운데', lines=2, under='사진', subj='가운데 인물(글자가 몸 아래쪽을 덮음, 밝은 벽)')
put(range(15, 20), pos='아래-넓게', lines=2, under='띠', subj='오른쪽 얼굴')                # 김작가
A[16] = dict(pos='아래-넓게', lines=2, under='상자', subj='위쪽 얼굴 둘')
A[18] = dict(pos='아래-왼쪽', lines=2, under='띠', subj='오른쪽 얼굴')
put(range(20, 25), pos='아래-넓게', lines=2, under='띠', subj='위쪽 얼굴')                  # 부읽남
put(range(25, 30), pos='아래-넓게', lines=2, under='띠', subj='위쪽 얼굴·책')              # 박곰희
A[25]['pos'] = A[26]['pos'] = A[29]['pos'] = '아래-왼쪽'
put(range(30, 35), pos='아래-넓게', lines=2, under='띠', subj='가운데 캐릭터(위)')          # 똑재(회색 그라데이션)
put(range(35, 40), pos='아래-넓게', lines=2, under='띠', subj='위쪽 얼굴')                  # 머니인사이드
put(range(40, 45), pos='아래-왼쪽', lines=3, under='띠', subj='오른쪽 얼굴')                # 815머니톡
put(range(45, 50), pos='아래-왼쪽', lines=2, under='사진', subj='여러 곳(사진마다 다름)')    # 슈카월드
A[49] = dict(pos='아래-가운데', lines=1, under='사진', subj='위쪽 얼굴 둘(아래는 어두운 책상)')
put(range(50, 55), pos='아래-왼쪽', lines=2, under='사진', subj='가운데 상반신·손(얼굴 없음), 글자는 옷 위')  # 은퇴머니
put(range(55, 60), pos='아래-넓게', lines=2, under='띠', subj='위쪽 얼굴(가운데~오른쪽)')   # 싱글파이어
put(range(60, 65), pos='가운데-왼쪽', lines=3, under='사진', subj='가운데~오른쪽 진행자(어두운 방), 글자가 몸 일부를 덮음')  # 김범곤
put(range(65, 70), pos='아래-가운데', lines=2, under='띠', subj='위쪽 얼굴')                # ETF 아는 형
A[66] = dict(pos='가운데-넓게', lines=2, under='그래픽', subj='없음(남색 그림판, 상품 이름 3개)')
A[67]['under'] = A[69]['under'] = '상자'
A[68] = dict(pos='아래-왼쪽', lines=2, under='사진', subj='오른쪽 얼굴(어두운 유리 사진)')
put(range(70, 75), pos='아래-넓게', lines=2, under='띠', subj='캐릭터(왼쪽 또는 오른쪽)')   # 오십의 경제지도
A[72] = dict(pos='위-오른쪽', lines=2, under='사진', subj='왼쪽 캐릭터·아래 탁자 소품, 글자는 위 오른쪽 하늘·건물 빈 곳')
A[73]['pos'] = '아래-왼쪽'
put(range(75, 80), pos='아래-왼쪽', lines=2, under='사진', subj='가운데 상반신·손(얼굴 없음), 글자는 셔츠 위')  # 연금왕 배형
A[76] = dict(pos='가운데-왼쪽', lines=2, under='사진', subj='가운데 상반신, 글자는 짙은 셔츠 위')
A[78]['lines'] = 3
put(range(80, 85), pos='아래-넓게', lines=2, under='띠', subj='위 양쪽 얼굴 둘')            # 투자360
put(range(85, 90), pos='아래-가운데', lines=2, under='사진', subj='가운데 인물(글자가 몸 위)') # 자람들
A[86]['subj'] = '오른쪽 인물, 글자는 가운데~오른쪽 어두운 빈 곳'
