# FireMap V3 product plan

V3 is not a feature dump. It is the productized version of the FIRE map concept.

## Product principle

- Result screen: summary, diagnosis, next action only.
- Experiment screen: numeric simulation only.
- Advanced modules: health insurance, overseas stay, cashflow, tax, and exchange assumptions must be usable calculators, not loose text cards.
- Chart: yearly data, clear x/y labels, selected-age card, and current-vs-improved comparison.
- City scenarios: monthly cost, exchange rate, stay period, extra cost, and runway impact.
- Share: image, summary text, short link, and condition link should be useful for communities.
- Community/Supabase: post-calculation space only. Do not disturb the core calculator flow.
- GA, AdSense, OG, privacy, and disclaimer build post-processing must be preserved.

## V3 information architecture

1. Home
   - One clear promise.
   - Trust chips: browser storage, reference-only calculation, no investment advice.

2. Questions
   - One question per screen.
   - Fast values must align in a clean grid.
   - Current value must not be duplicated awkwardly.

3. Result
   - FIRE current position.
   - Survival age and score.
   - Top two levers only.
   - Next actions: experiment, city, share.
   - No unusable advanced button until advanced modules are real.

4. Experiment
   - Target retirement age.
   - Monthly living cost.
   - Monthly investment.
   - Annual return.
   - Improved living cost.
   - Yearly chart.

5. Advanced modules
   - Health insurance module.
   - Overseas stay module.
   - Cashflow module.
   - Tax module.
   - FX module.
   - Each module must have inputs, assumptions, result, and apply action.

6. City
   - Domestic and overseas options.
   - Monthly cost, savings, runway impact.
   - Later: FX and cost data update.

7. Share
   - Result image.
   - Summary copy.
   - Basic link.
   - Condition link.
   - Community-ready copy.

8. Community and Supabase
   - Feedback and community stories after calculator result.
   - Auth/RLS before any real data storage.
   - Do not store personal financial input without explicit opt-in.

## V3 release gates

- Build Check success.
- FireMap Mobile QA success on main push.
- Mobile URL hands-on review.
- No horizontal overflow.
- Buttons must be usable with thumb.
- Graph must be readable without explanation.
- Result page must not feel like a long ungrouped feed.
- AdSense/GA post-build scripts must remain.
- No main rollback needed after release.

## Deferred beyond V3

- Full Supabase community.
- Login.
- Saved result history.
- API-based city cost updates.
- API-based FX updates.
- Tax rule automation.
