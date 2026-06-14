import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function AssetCompareChart({ ages, current, improved, depletionAge, improvedDepletionAge, retirementAge, currentLabel = '현재 계획', improvedLabel = '절감안' }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = canvasRef.current.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 260);
    grad.addColorStop(0, 'rgba(47,111,222,0.28)');
    grad.addColorStop(1, 'rgba(47,111,222,0.01)');
    const axis = '#9aa3bf';
    const grid = 'rgba(128,128,128,0.12)';

    const depletionLines = {
      id: 'depletionLines',
      afterDatasetsDraw(chart) {
        const xs = chart.scales.x;
        const area = chart.chartArea;
        const marks = [[retirementAge, '#ff5a00', `파이어 ${retirementAge}세`], [depletionAge, '#9aa3bf', `현재 고갈 ${depletionAge}세`], [improvedDepletionAge, '#2f6fde', `절감안 고갈 ${improvedDepletionAge}세`]];
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
          if (i === 0) { // 파이어 마커만 텍스트(고갈 나이는 범례에 표시)
            c.fillStyle = color; c.font = '700 10px sans-serif';
            c.textAlign = x > (area.left + area.right) / 2 ? 'right' : 'left';
            c.fillText(text, x + (c.textAlign === 'right' ? -3 : 3), area.top + 9);
          }
          c.restore();
        });
      }
    };

    chartRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ages,
        datasets: [
          { label: improvedLabel, data: improved, borderColor: '#2f6fde', backgroundColor: grad, fill: true, borderWidth: 2, pointRadius: 0, tension: 0.35 },
          { label: currentLabel, data: current, borderColor: '#9aa3bf', fill: false, borderWidth: 2, borderDash: [5, 4], pointRadius: 0, tension: 0.35 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 18 } },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { title: (items) => `${items[0].label}세`, label: (item) => `${item.dataset.label} ${(item.parsed.y / 1e8).toFixed(1)}억` } }
        },
        scales: {
          x: { ticks: { color: axis, font: { size: 10 }, maxTicksLimit: 6, callback(v) { return `${this.getLabelForValue(v)}세`; } }, grid: { color: grid } },
          y: { min: 0, beginAtZero: true, ticks: { color: axis, font: { size: 10 }, callback: (v) => `${(v / 1e8).toFixed(0)}억` }, grid: { color: grid } }
        }
      },
      plugins: [depletionLines]
    });
    return () => { if (chartRef.current) chartRef.current.destroy(); };
  }, [ages, current, improved, depletionAge, improvedDepletionAge, retirementAge, currentLabel, improvedLabel]);

  return <div className="fm-compare-chart"><canvas ref={canvasRef} /></div>;
}
