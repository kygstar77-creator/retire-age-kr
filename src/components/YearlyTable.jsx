import { formatEok } from '../utils/formatters.js';

export default function YearlyTable({ rows }) {
  return (
    <section className="panel table-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">추이</p>
          <h2>연도별 자산 흐름</h2>
        </div>
      </div>

      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>연도</th>
              <th>나이</th>
              <th>상태</th>
              <th>금융자산</th>
              <th>인출액</th>
              <th>순자산</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr className={row.financialAsset <= 0 ? 'depleted-row' : ''} key={`${row.year}-${row.age}`}>
                <td>{row.year}</td>
                <td>{row.age}세</td>
                <td>{row.status}</td>
                <td>{formatEok(row.financialAsset)}</td>
                <td>{formatEok(row.withdrawal)}</td>
                <td>{formatEok(row.netWorth)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
