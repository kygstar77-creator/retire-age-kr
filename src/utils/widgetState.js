// 위젯 상태 1벌 — 결과 화면 위젯 카드와(나중에) 앱 위젯 브리지가 같은 함수를 읽는다.
// 2026-09-14 저축 기능을 걷어내면서 연속 기록·저축 앞당김을 뺐다. 이제 계산 결과만 본다.
export function hasCalculated() {
  try { return !!localStorage.getItem('firemap-inputs-v3'); } catch { return false; }
}

export function buildWidgetState(simulation) {
  const inp = (simulation && simulation.inputs) || {};
  const cur = Number(inp.currentAge) || 0;
  const earliest = (simulation && simulation.earliestRetirementAge) || null;
  const fireAge = earliest || inp.targetRetirementAge || null;
  const dday = (earliest && fireAge && cur) ? Math.max(0, Math.round((fireAge - cur) * 365.25)) : null;
  const asset = Number(inp.financialAsset) || 0;
  const target = Math.round((simulation && simulation.requiredFireAssetByFourPercent) || 0);
  const progressPct = target > 0 ? Math.max(0, Math.min(100, Math.round((asset / target) * 100))) : 0;
  return {
    calculated: hasCalculated(),
    earliestAge: earliest,
    fireAgeYears: fireAge || null,
    dday,
    progressPct,
    target,
    asset,
    updatedAt: Date.now()
  };
}

// 앱(Capacitor) 단계에서 네이티브 위젯 브리지가 읽을 스냅샷. 웹에선 localStorage에만 둔다.
export function syncWidgetSnapshot(simulation) {
  try {
    const st = buildWidgetState(simulation);
    localStorage.setItem('fm_widget_state', JSON.stringify(st));
    return st;
  } catch { return null; }
}
