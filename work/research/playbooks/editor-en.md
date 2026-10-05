# editor-en playbook (firemap-editor-en)

## Rules learned
- "NI" means both National Insurance and Northern Ireland on UK pay pages. Never use "NI" for both in one sentence. Region = "Northern Ireland" in full; "NI" only for National Insurance where the context is plainly tax.
- Compound adjective/noun on screen: "take-home pay" (GOV.UK style). Keep "Take Home Pay" unhyphenated only in title/H1/brand, where it matches the search term.
- A share card that the user posts speaks as the user: "My …" title → body in first person ("I work for tax & NI until…"), not "you".
- Check every claim about data against the code. "Your numbers stay in your browser" was false while FMKit.log sends a salary band + client id. Say exactly what leaves the browser.
- Test copy at the edges: £0k–£10k band and zero tax ("until 9:00am") read as nonsense. Give edge cases their own line.
- Re-check privacy promises every time code changes, not only copy. A '?s=<salary>' link added later made "stays in your browser" false: query strings reach the host's servers. Promise only what *we* do ("we never log your exact salary") and say what the host sees. URL fragments (#) are not sent to the server.
- Edge wording at exact thresholds: if the code uses >=, the copy says "From £X", not "Above £X".
- In a niche full of hype ("escape the trap", "secret tax band", "optimizer"), plain GOV.UK-style wording is the human-sounding choice; FSMA pages also must not tell people what to do with pensions.
- Keep straight apostrophes if the page already uses them (consistency beats typography).

## 2026-10-01 X-V1 uk-pay site/index.html — before / after
| Where | Before | After | Why |
|---|---|---|---|
| meta description | … England, Wales & NI. | … England, Wales & Northern Ireland. | "NI" already meant National Insurance earlier in the same sentence |
| result label | Your take home pay | Your take-home pay | body text style (GOV.UK) |
| 60% warning | Your salary is in the £100,000–£125,140 band, where the next £1,000 is taxed at an effective 60% (62% with NI). | You're in the £100,000–£125,140 band, where each extra £1,000 is taxed at an effective 60% (62% with National Insurance). | plainer; "NI" spelled out on a warning |
| Share card line | On £110k–£120k you work for tax & NI until 11:44am each 9-to-5 day | On £110k–£120k, I work for tax & NI until 11:44am each 9-to-5 day | card is "My take-home pay", posted by the user; 11:44am re-checked for £110k (34.2% of 8h) |
| Share card, no tax | On £0k–£10k you work for tax & NI until 9:00am each 9-to-5 day | On under £10k, I pay no Income Tax or NI | edge case read as nonsense |
| How it's calculated | Take home pay is your salary minus… | Take-home pay is your salary minus… | style |
| How it's calculated | …so it is zero from £125,140. | …so it's zero from £125,140. | tone |
| footer | Your numbers stay in your browser. | Your exact salary stays in your browser. We only log anonymous usage, such as which salary band was checked. | old line was untrue (fmkit.js logs calc_submit bucket) |

Unchanged on purpose: title, H1 (search-term order, matches competitors), "Of your next £1,000, you keep", tables and numbers, "Estimate only, not tax advice", HMRC/GOV.UK disclaimer, sources line.
Open (builder): links `60-percent-tax-trap/`, `privacy/`, `about/` have no page in site/ yet.

## 2026-10-01 10:31 X-V1 60-percent-tax-trap · privacy · about (+ index footer)
| Where | Before | After | Why |
|---|---|---|---|
| index + trap footer | Your exact salary/income stays in your browser. We only log anonymous usage, such as… | We never log your exact salary/income, only anonymous usage such as… | new ?s= links send the figure to GitHub Pages in the URL |
| privacy, first line | …is worked out in your browser and is never sent anywhere. | …is worked out in your browser, and we never log the exact figure. | same |
| privacy, Hosting | (nothing) | + When you follow a link from one of our calculators to another, the figure you entered goes in the page address (for example ?s=110000), so GitHub's servers receive it with that request. | say what the host sees |
| trap result, ≥ £125,140 | Above £125,140 the allowance is fully gone | From £125,140 the allowance is fully gone | code is >=; at exactly £125,140 the allowance is 0 |

Unchanged on purpose: titles, H1s, meta, examples table (re-checked), "This is arithmetic, not advice. Speak to a regulated adviser…", sources, about page.
- Fix the template, not just the page. The false privacy line fixed on uk-pay was still in kit/template-en.html, so every new site would copy it back. When a fix comes from shared code (fmkit.js), grep the kit templates in the same run.

## 2026-10-02 11:05 X-V1 re-check after beat-1st (07d853f)
| Where | Before | After | Why |
|---|---|---|---|
| result table, last row | Take home | Take-home pay | noun label in body = GOV.UK style; "Take home" alone reads clipped |

Checked, unchanged: scope line "rates from GOV.UK, checked 1 October 2026" (true), table note "Month is the yearly amount divided by 12 and rounded to the nearest pound…" (matches f() = Math.round), Year/Month headers. deploy.py check 4 pages OK. Not deployed by me — builder's next push carries it.
- Builders now stamp .edit.json "editor-en 역할" themselves. Shared rules for them: work/research/editor/style-guide-en.md.

## 2026-10-05 21:2x kit/template-en.html sweep (no English requests open; uk-pay unchanged since ee736ca except a code comment in fmkit.js)
| Where | Before | After | Why |
|---|---|---|---|
| form | wrong input → nothing on screen (only calc_invalid logged) | `<p id="err" role="alert">{{INVALID_MSG}}</p>` shown until input is valid | silent failure; error copy is ours to write |
| header comment | (none) | points to style-guide-en.md + 3 traps: ?s= links make "stay in your browser" false · share text is first person, test at £0/thresholds · INVALID_MSG says what to type, no "Invalid input"/"Oops" | every new site copies this file |

Checked, unchanged: footer disclaimer (true for the template — FMKit.share sends origin+pathname only, no figures), "Share result", "How it's calculated", "Rules as of". aitell 0.5.
- Error messages: say what to type and give an example. A bare "Invalid input" is the most machine-sounding line on a page.
