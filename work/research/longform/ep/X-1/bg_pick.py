# X-1 v3 실사 재료 고르기(10/17 PD) — stock/credits.json(pexelsvid.py)에서 눈으로 본 클립만 골라 video/public/bg/x1/로(소리 뺀 h264) + bg_plan.json
#   py -3.12 work/research/longform/ep/X-1/bg_pick.py
# 고른 기준: 실존 얼굴·상표·간판·번호판·읽히는 숫자 없음(프레임 10·50·90% 눈 확인 10/17). 뺀 것: 얼굴(가족·창가·은행 창구 6192867 등), 상표(아마존 상자·화물선 ONE/HMM·항공사 꼬리·단말기 상표),
#   지폐 초상 크게(4275306·3977228·11471492·39060971), 숫자 비침(휴대폰 계산기 8704·유로 10권), 광고 문구(3736790), 2021·2020 달력, 그린 스크린, 정치색 여권.
import json, os, subprocess, sys, imageio_ffmpeg
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__)); VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
PICK = {  # id: (쓸 수 있는 초, 무엇)
 5466769: (14, '나무 탁자 위 손이 달러 다발을 셈(얼굴 없음)'), 6326929: (20, '빨간 탁자 위 두 손이 지폐 뭉치를 셈·옆 공책(C-2와 같은 클립)'),
 5466779: (15, '위에서 본 손이 달러 지폐 두 더미를 나눔(초상 작게)'), 7735914: (23, '흐린 유리 너머 손에 든 달러 지폐'), 7735915: (23, '탁자 위 달러 지폐와 영수증, 앞 유리컵 흐림'),
 35054136: (11, '손이 갈색 지갑에 지폐를 넣음'), 34596756: (26, '손이 지갑 속 지폐를 넘김'),
 18757432: (16, '공항 대합실 바닥 높이에서 본 배낭·여행 가방(사람 멀리 뒷모습)'), 10821823: (20, '공항 출국장 넓은 홀 빠른 화면(사람 아주 작게)'),
 8044782: (11, '햇빛 비치는 공항 바닥을 끌고 가는 민트색 여행 가방(다리만)'), 4241635: (8, '주황 조명 통로를 가방 끌고 걷는 뒷모습(멀리)'), 8044821: (12, '창살 그림자 진 공항 바닥, 가방 끄는 다리'),
 3723453: (45, '비행기 창밖 날개·이륙'), 3740041: (11, '비행기 창 너머 노을 날개'), 7308237: (11, '노트북 위 여권과 탑승권'), 7009802: (17, '세계 지도 위 동전들'),
 32111755: (5, '교토 기요미즈데라 본당과 숲(사람 아주 작게)'), 38556529: (6, '교토 금각사와 연못'),
 11158789: (12, '하늘·주황 바탕 위 카드 단말기에 카드를 댐(손만)'), 8830802: (7, '카운터에서 카드를 단말기에 꽂음(손만)'), 6685174: (17, '꽃 옆 카드 단말기 영수증 출력부'),
 9218138: (15, '위에서 본 노트북 자판과 카드 든 손'), 7428839: (21, '플래너에 펜으로 적는 손'), 7593891: (11, '계산기를 두드리는 손(C-2와 같은 클립)'), 5923592: (10, '계산기와 서류, 펜 든 손'),
 7546415: (6, '노트북 옆 영수증 더미를 보는 손'), 6186015: (15, '휴대폰을 쥔 손 가까이'), 6963836: (22, '휴대폰 자판을 누르는 손톱'), 5778854: (7, '서류에 서명하는 손'), 8439245: (7, '서류에 서명하는 손 가까이'),
 8369980: (7, '동전 탑을 쌓는 손, 화분 배경'), 8661806: (23, '흰 탁자 위 동전 탑에 동전을 올림'), 5651783: (8, '동전 가까이 초점 이동'), 7829075: (9, '빨간 돼지 저금통과 나무토막'),
 10452020: (10, '항구 크레인 옆 화물선(위에서, 상표 안 읽힘)'), 29904000: (48, '위에서 본 컨테이너 부두와 크레인'), 31879939: (20, '위에서 본 바다 물결'), 9806390: (35, '위에서 본 어두운 바다 물결'),
}
ff = imageio_ffmpeg.get_ffmpeg_exe()
cr = {c['id']: c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
out = os.path.join(VID, 'public', 'bg', 'x1'); os.makedirs(out, exist_ok=True)
clips = []
for cid, (sec, what) in PICK.items():
    c = cr[cid]; dst = os.path.join(out, f'{cid}.mp4')
    if not os.path.exists(dst):
        subprocess.run([ff, '-loglevel', 'error', '-y', '-i', os.path.join(EP, 'stock', c['file']), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p',
                        '-vf', 'scale=1920:-2', dst], check=True)
    c['used'] = True
    clips.append({'file': f'bg/x1/{cid}.mp4', 'id': cid, 'start': 0, 'usable_sec': sec, 'what': what, 'author': c['author'], 'author_url': c['author_url'], 'page': c['page'], 'license': c['license']})
json.dump({'name': 'X-1', 'made': '2026-10-17', 'note': '실존 얼굴·상표·간판·읽히는 숫자 0(프레임 10·50·90% 눈 확인). 영상은 -an h264 1920. 설명란 출처는 stock/credits.json desc_line(used=true).', 'clips': clips},
          open(os.path.join(EP, 'bg_plan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(list(cr.values()), open(os.path.join(EP, 'stock', 'credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(clips), '클립 →', out)
