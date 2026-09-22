# 텔레그램 봇으로 보고 보내기 — 화면 조작 없이 HTTP라 예약 루틴이 무인으로 보낼 수 있다.
#
# 준비(한 번): 사장님이 텔레그램에서 BotFather에게 /newbot → 봇 토큰을 받아
#   C:\Users\강영준\Documents\telegram_bot.txt 에  TOKEN=123456:ABC...  한 줄로 저장.
#   그다음 그 봇과 대화방(또는 그룹)에서 아무 메시지나 하나 보낸 뒤
#   python work/tgreport.py setup   → 그 방의 chat_id를 찾아 같은 파일에 CHAT_ID=... 로 적는다.
#
#   python work/tgreport.py send "메시지"          # 문자열 전송
#   python work/tgreport.py sendfile <경로>         # 텍스트 파일 내용 전송(4,000자 넘으면 나눠 보냄)
import sys, os, json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
KEYFILE = r'C:\Users\강영준\Documents\telegram_bot.txt'

def load():
    if not os.path.exists(KEYFILE):
        print('설정 없음:', KEYFILE, '— TOKEN=... 을 저장한 뒤 setup 을 실행'); sys.exit(2)
    kv = {}
    for line in open(KEYFILE, encoding='utf-8-sig'):
        if '=' in line:
            k, v = line.strip().split('=', 1); kv[k.strip().upper()] = v.strip()
    return kv

def save(kv):
    open(KEYFILE, 'w', encoding='utf-8').write(''.join(f'{k}={v}\n' for k, v in kv.items()))

def api(token, method, data=None):
    url = f'https://api.telegram.org/bot{token}/{method}'
    body = urllib.parse.urlencode(data).encode() if data else None
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=30) as r:
        return json.load(r)

def setup():
    kv = load()
    if 'TOKEN' not in kv: print('TOKEN 줄이 없음'); sys.exit(2)
    me = api(kv['TOKEN'], 'getMe')
    print('봇:', me['result']['username'])
    upd = api(kv['TOKEN'], 'getUpdates')
    chats = {}
    for u in upd.get('result', []):
        m = u.get('message') or u.get('channel_post') or {}
        c = m.get('chat')
        if c: chats[c['id']] = c.get('title') or c.get('username') or c.get('first_name') or str(c['id'])
    if not chats:
        print('대화가 없음 — 봇에게(또는 봇을 넣은 그룹에서) 메시지를 하나 보낸 뒤 다시 실행'); sys.exit(3)
    for cid, name in chats.items(): print('chat_id', cid, '|', name)
    cid = list(chats)[-1]
    kv['CHAT_ID'] = str(cid); save(kv)
    api(kv['TOKEN'], 'sendMessage', {'chat_id': cid, 'text': '파이어맵 보고 봇 연결 확인'})
    print('저장:', KEYFILE, '→ CHAT_ID =', cid, '(확인 메시지 보냄)')

def send(text):
    kv = load()
    if 'CHAT_ID' not in kv: print('CHAT_ID 없음 — setup 먼저'); sys.exit(2)
    text = text.strip() or '(빈 보고)'
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)]
    for ch in chunks:
        r = api(kv['TOKEN'], 'sendMessage', {'chat_id': kv['CHAT_ID'], 'text': ch, 'disable_web_page_preview': 'true'})
        if not r.get('ok'): print('전송 실패:', r); sys.exit(1)
    print('전송 완료', len(chunks), '건')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'send'
    if cmd == 'setup': setup()
    elif cmd == 'sendfile': send(open(sys.argv[2], encoding='utf-8').read())
    else: send(' '.join(sys.argv[2:]))
