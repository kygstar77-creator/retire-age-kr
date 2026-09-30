import json,urllib.request,urllib.parse,sys,time
qs=sys.argv[1:]
for q in qs:
    u="https://gumroad.com/products/search?"+urllib.parse.urlencode({"query":q,"sort":"most_reviewed"})
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
    try: d=json.load(urllib.request.urlopen(r,timeout=30))
    except Exception as e: print(q,"ERR",e); continue
    ps=d.get("products",[])
    paid=[p for p in ps if p["price_cents"]>0]
    tot=sum(p["ratings"]["count"] for p in ps)
    print(f"## {q} | total={d['total']} | top{len(ps)} ratings sum={tot}")
    for p in ps[:5]:
        print(f"  {p['ratings']['count']:>5} r {p['ratings']['average']} | ${p['price_cents']/100:.2f} {p['currency_code']} | {p['name'][:70]} | {p['seller']['name']}")
    time.sleep(1)
