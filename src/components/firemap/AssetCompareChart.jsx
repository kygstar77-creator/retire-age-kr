import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function AssetCompareChart({ ages, current, improved, depletionAge, improvedDepletionAge, currentLabel = '현재 계획', improvedLabel = '절감안' }) {
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
        const marks = [[depletionAge, '#9aa3bf', currentLabel], [improvedDepletionAge, '#2f6fde', improvedLabel]];
        marks.forEach(([age, color, label]) => {
          if (!age) return;
          const idx = ages.indexOf(age);
          if (idx < 0) return;
          const x = xs.getPixelForValue(idx);
          const c = chart.ctx;
          c.save();
          c.setLineDash([4, 4]); c.strokeStyle = color; c.lineWidth = 1.5;
          c.beginPath(); c.moveTo(x, area.top); c.lineTo(x, area.bottom); c.stroke();
          c.setLineDash([]); c.fillStyle = color; c.font = '700 10px sans-serif'; c.textAlign = 'center';
          c.fillText(`${label} 고갈 ${age}세`, x, area.top - 2);
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
        layout: { padding: { top: 14 } },
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
  }, [ages, current, improved, depletionAge, improvedDepletionAge, currentLabel, improvedLabel]);

  return <div className="fm-compare-chart"><canvas ref={canvasRef} /></div>;
}
