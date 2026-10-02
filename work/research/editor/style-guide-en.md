# English style guide (firemap-editor-en, 2026-10-02)

For anyone writing English on a FireMap venture page, kit template, product listing or video. Builders who stamp `.edit.json` themselves check these first. Rules come from real fixes on X-V1 (playbooks/editor-en.md has the before/after tables).

## Voice
- Write like GOV.UK or MoneySavingExpert: short sentences, plain verbs, "you". In money niches full of hype ("escape the trap", "secret band", "unlock"), plain wording is what reads as human.
- No stock phrases: delve, unlock, seamless, empower, navigate (figuratively), "in today's…", "whether you're X or Y", "look no further", "it's important to note".
- No rule-of-three lists or em-dash chains just for rhythm. One idea per sentence.
- Contractions are fine in body text ("it's zero from £125,140"). Not in legal lines.

## Words
- "take-home pay" hyphenated in body text and labels. Unhyphenated "Take home pay" only in title/H1 where it matches the search term.
- "National Insurance" in full on warnings and in any sentence that also mentions Northern Ireland. "NI" only for National Insurance in obviously tax context. Never use "NI" twice with two meanings.
- Thresholds follow the code: `>=` → "From £X", `>` → "Above £X".
- Keep the page's existing apostrophe style (straight vs curly). Consistency beats typography.

## Truth
- Every claim about data must match the code, not the intent. Check fmkit.js and any `?s=` style links: a query string reaches the host's servers. Promise only what we do ("we never log your exact salary") and say what the host sees.
- When a fix comes from shared code, grep kit/template-en.html in the same run.
- Never change numbers, tax facts, sources, "Estimate only, not tax advice" or FSMA-style lines ("This is arithmetic, not advice…"). Don't tell people what to do with pensions.

## Edges
- Test copy at £0, the lowest band and exact thresholds. If a sentence reads as nonsense at the edge ("you work for tax until 9:00am"), give the edge its own line.
- Share cards are posted by the user, so they speak as the user ("I work for tax & NI until…").

## Process
1. Read the visible text, then run `py -3.12 work/aitell.py` (deploy.py check does this).
2. Compare with 3 top competitors in the niche (titles, labels, how they phrase warnings).
3. Unsure → `py -3.12 work/second_opinion.py <file> 사용자` and ask where it sounds AI-written to a native reader.
4. Record the change as a before/after row in playbooks/editor-en.md, refresh `.edit.json` with `deploy.py hash`.
