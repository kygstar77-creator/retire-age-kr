// 계산기 3종 공통 측정(V4, growth 10/1 16:46 제안): 화면은 그대로, 이벤트 두 개만.
// calc_input_start{calc} — 기본값에서 처음 손댄 순간 1회. calc_result{calc, amount_bucket} — 손댄 뒤 결과가 2초 멈춰 있으면 1회.
// 기본값 그대로 보이는 결과는 screen_view와 같아서 세지 않는다. 금액은 구간 번호만 보낸다(원 단위 금액은 안 보냄).
import { useEffect, useRef } from 'react';
import { logEvent } from '../../utils/live.js';

export default function useCalcEvents(calc, deps, bucket) {
  const key = JSON.stringify(deps);
  const initial = useRef(key);
  const started = useRef(false);
  const resulted = useRef(false);

  useEffect(() => {
    if (!started.current && key === initial.current) return undefined; // 기본값 그대로(StrictMode 두 번 실행 포함)
    if (!started.current) {
      started.current = true;
      try { logEvent('calc_input_start', { calc }); } catch { /* ignore */ }
    }
    if (resulted.current || bucket == null) return undefined;
    const t = setTimeout(() => {
      resulted.current = true;
      try { logEvent('calc_result', { calc, amount_bucket: bucket }); } catch { /* ignore */ }
    }, 2000);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
}
