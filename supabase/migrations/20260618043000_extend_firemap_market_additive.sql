-- Additive only: new nullable columns for the market collector.
-- Existing rows/cols/RPC (fm_market_latest) untouched. Applied to project cvhskxdwqubmshdgkzhj.
ALTER TABLE public.firemap_market
  ADD COLUMN IF NOT EXISTS asset_class text,
  ADD COLUMN IF NOT EXISTS name        text,
  ADD COLUMN IF NOT EXISTS currency    text,
  ADD COLUMN IF NOT EXISTS ret_1d      numeric,
  ADD COLUMN IF NOT EXISTS ret_ytd     numeric,
  ADD COLUMN IF NOT EXISTS source      text;

NOTIFY pgrst, 'reload schema';
