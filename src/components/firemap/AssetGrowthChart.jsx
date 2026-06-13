import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

// 자산을 "내가 넣은 돈(원금)"과 "알아서 불어난 돈(수익)"으로 쌓아 보여주는 스택 영역 차트.
export default function AssetGrowthChart({ ages, principal, gains, retirementAge, depletionAge }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = canvasRef.current.getContext('2d');
    const gainGrad = ctx.createLinearGradient(0, 0, 0, 260);
    gainGrad.addColorStop(0, 'rgba(255,90,0,0.55)');
    gainGrad.addColorStop(1, 'rgba(255,90,0,0.12)');
    const axis = '#9aa3bf';
    const grid = 'rgba(128,128,128,0.12)';

    const markers = {
      id: 'growthMarkers',
      afterDatasetsDraw(chart) {
        const xs = chart.scales.x;
        const area = chart.chartArea;
        const marks = [[retirementAge, '#ff5a00', `퇴사 ${retirementAge}세`], [depletionAge, '#9aa3bf', `고갈 ${depletionAge}세`]];
        marks.forEach(([age, color, text], i) => {
          if (!age) return;
          const idx = ages.indexOf(age);
          if (idx < 0) return;
          const x = xs.getPixelForValue(idx);
          const c = chart.ctx;
          c.save();
          c.setLineDash([4, 4]); c.strokeStyle = color; c.lineWidth = 1.5;
          c.beginPath(); c.moveTo(x, area.top); c.lineTo(x, area.bottom); c.stroke();
          c.setLineDash([]);
          c.fillStyle = color; c.font = '700 10px sans-serif';
          c.textAlign = x > (area.left + area.right) / 2 ? 'right' : 'left';
          c.fillText(text, x + (c.textAlign === 'right' ? -3 : 3), area.top + 9 + i * 12);
          c.restore();
        });
      }
    };

    chartRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ages,
        datasets: [
          { label: '내가 넣은 돈', data: principal, borderColor: '#2f6fde', backgroundColor: 'rgba(47,111,222,0.35)', fill: 'origin', borderWidth: 2, pointRadius: 0, tension: 0.3 },
          { label: '불어난 돈', data: gains, borderColor: '#ff5a00', backgroundColor: gainGrad, fill: '-1', borderWidth: 2, pointRadius: 0, tension: 0.3 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 18 } },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: (items) => `${items[0].label}세`,
              label: (item) => `${item.dataset.label} ${(item.parsed.y / 1e8).toFixed(1)}억`,
              footer: (items) => {
                const sum = items.reduce((a, it) => a + (it.parsed.y || 0), 0);
                return `합계 ${(sum / 1e8).toFixed(1)}억`;
              }
            }
          }
        },
        scales: {
          x: { ticks: { color: axis, font: { size: 10 }, maxTicksLimit: 6, callback(v) { return `${this.getLabelForValue(v)}세`; } }, grid: { color: grid } },
          y: { stacked: true, min: 0, beginAtZero: true, ticks: { color: axis, font: { size: 10 }, callback: (v) => `${(v / 1e8).toFixed(0)}억` }, grid: { color: grid } }
        }
      },
      plugins: [markers]
    });
    return () => { if (chartRef.current) chartRef.current.destroy(); };
  }, [ages, principal, gains, retirementAge, depletionAge]);

  return <div className="fm-compare-chart"><canvas ref={canvasRef} /></div>;
}
