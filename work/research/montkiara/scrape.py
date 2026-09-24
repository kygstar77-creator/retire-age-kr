import json, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
rows=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    pg=b.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36")
    for page_no in (1,2):
        u="https://www.propertyguru.com.my/condo-for-rent/in-mont-kiara-q9qzw"+(f"/{page_no}" if page_no>1 else "")
        pg.goto(u,timeout=60000,wait_until="domcontentloaded"); pg.wait_for_timeout(5000)
        txt=pg.inner_text("body")
        links=[a.get_attribute("href") for a in pg.query_selector_all("a[href]")]
        links=[l for l in links if l and "/property-listing/" in l]
        # 매물 블록: "RM x /mo" 로 시작해 "Listed on" 까지
        for m in re.finditer(r"RM ([\d,]+) /mo\s*\n+\s*RM ([\d.]+) psf\s*\n+\s*(.+?)\n+\s*(.+?)\n+([\s\S]{0,120}?)([\d,]+) sqft\s*\n+\s*(\w[\w /]*)\n+(?:Built: (\d{4})\s*\n+)?Listed on ([^\n(]+)", txt):
            rent,psf,proj,addr,beds_raw,size,ptype,built,listed = m.groups()
            b2=[x.strip() for x in beds_raw.strip().split("\n") if x.strip()]
            rows.append({"project":proj.strip(),"addr":addr.strip(),"rent_rm":rent,"psf":psf,
                         "beds":b2[0] if b2 else "", "baths":b2[1] if len(b2)>1 else "",
                         "park":b2[2] if len(b2)>2 else "",
                         "sqft":size,"type":ptype.strip(),"built":built or "","listed":listed.strip()})
    b.close()
seen=set(); uniq=[]
for r in rows:
    k=(r["project"],r["rent_rm"],r["sqft"])
    if k in seen: continue
    seen.add(k); uniq.append(r)
print(json.dumps({"n":len(uniq),"rows":uniq[:20],"links":links[:5]},ensure_ascii=False,indent=1))
