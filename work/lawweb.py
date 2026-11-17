# law.go.kr 웹(lsSideInfoP)에서 조문 본문 텍스트를 받아 저장한다. 법령 API(OC=test)가 "사용자 검증 실패"일 때 쓴다(2026-11-03 firemap-write).
# 실행: PYTHONIOENCODING=utf-8 py -3.12 work/lawweb.py 주택임대차보호법 제3조의3 <pkg>/raw<날짜>/파일.txt  (Windows에서 한글 인자는 Git Bash로)
import sys, re, urllib.request, urllib.parse, html, time
law, jo, out = sys.argv[1], sys.argv[2], sys.argv[3]
u = "https://www.law.go.kr/" + urllib.parse.quote(f"법령/{law}/{jo}")
r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"}), timeout=20).read().decode("utf-8","replace")
m = re.search(r'src="(/LSW/[^"]*lsSideInfoP[^"]*)"', r)
if not m:
    # 2026-11-17 firemap-write: 법령 웹이 조문을 자바스크립트로만 불러오게 바뀌어 lsSideInfoP 틀이 없다(lsInfoR.do도 '기본정보 조회 실패').
    # 예전엔 AttributeError로 죽어 원인을 못 봤다. 지금은 이렇게 알리고 끝낸다 — 그때는 브라우저(Playwright)나 2차 출처 2곳으로 확인한다.
    seq = re.search(r'id="lsiSeq" value="(\d+)"', r)
    sys.exit(f"법령 웹 구조 바뀜: lsSideInfoP 없음(lsiSeq={seq.group(1) if seq else '?'}) — 브라우저로 {u} 를 열거나 2차 출처 2곳으로 확인")
src = html.unescape(m.group(1))
b = urllib.request.urlopen(urllib.request.Request("https://www.law.go.kr"+src, headers={"User-Agent":"Mozilla/5.0","Referer":u}), timeout=20).read().decode("utf-8","replace")
t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
t = html.unescape(re.sub(r"<[^>]+>", "\n", t)); t = "\n".join(l.strip() for l in t.splitlines() if l.strip())
open(out, "w", encoding="utf-8").write(f"# {u}\n# {'https://www.law.go.kr'+src}\n# 받은 날 {time.strftime('%Y-%m-%d %H:%M')}\n\n{t}\n")
print(len(t))
