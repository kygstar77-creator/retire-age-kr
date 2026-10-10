# script.md의 '- ' 줄을 voice.json 형식(sections/lines/say)으로 임시로 만든다(aitell script 측정용, 측정 뒤 삭제)
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
secs = []; cur = None; n = 0
for l in open('script.md', encoding='utf-8'):
    if l.startswith('## '): cur = {'title': l[3:].strip(), 'lines': []}; secs.append(cur)
    elif l.startswith('- ') and cur is not None:
        t = re.sub(r'\s*\(재사용[^)]*\)\s*$', '', l[2:].strip()); cur['lines'].append({'text': t, 'say': t}); n += 1
json.dump({'sections': secs}, open('voice.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
txt = ' '.join(x['say'] for s in secs for x in s['lines'])
print('말 줄', n, '· 글자(공백 제외)', len(txt.replace(' ', '')), '· 예상 길이(5.65음절/초)', round(len(re.sub(r'[^가-힣0-9]', '', txt)) / 5.65 / 60, 1), '분')
