import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function AssetCompareChart({ ages, current, improved, currentLabel = '현재 계획', improvedLabel = '절감안' }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = canvasRef.current.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 200);
    grad.addColorStop(0, 'rgba(47,111,222,0.28)');
    grad.addColorStop(1, 'rgba(47,111,222,0.01)');
    const axis = '#9aa3bf';
    const grid = 'rgba(128,128,128,0.12)';
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
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: (items) => `${items[0].label}세`,
              label: (item) => `${item.dataset.label} ${(item.parsed.y / 1e8).toFixed(1)}억`
            }
          }
        },
        scales: {
          x: { ticks: { color: axis, font: { size: 10 }, maxTicksLimit: 6, callback(v) { return `${this.getLabelForValue(v)}세`; } }, grid: { color: grid } },
          y: { min: 0, beginAtZero: true, ticks: { color: axis, font: { size: 10 }, callback: (v) => `${(v / 1e8).toFixed(0)}억` }, grid: { color: grid } }
        }
      }
    });
    return () => { if (chartRef.current) chartRef.current.destroy(); };
  }, [ages, current, improved, currentLabel, improvedLabel]);

  return <div className="fm-compare-chart"><canvas ref={canvasRef} /></div>;
}
