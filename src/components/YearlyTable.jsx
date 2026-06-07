import { Table } from 'antd';
import { formatEok } from '../utils/formatters.js';

const columns = [
  { title: '연도', dataIndex: 'year', key: 'year', align: 'left' },
  { title: '나이', dataIndex: 'age', key: 'age', align: 'right', render: (age) => `${age}세` },
  { title: '상태', dataIndex: 'status', key: 'status', align: 'left' },
  { title: '금융자산', dataIndex: 'financialAsset', key: 'financialAsset', align: 'right', render: (v) => formatEok(v) },
  { title: '인출액', dataIndex: 'withdrawal', key: 'withdrawal', align: 'right', render: (v) => formatEok(v) },
  { title: '순자산', dataIndex: 'netWorth', key: 'netWorth', align: 'right', render: (v) => formatEok(v) }
];

export default function YearlyTable({ rows }) {
  const dataSource = rows.map((row) => ({ ...row, key: `${row.year}-${row.age}` }));

  return (
    <section className="panel table-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">추이</p>
          <h2>연도별 자산 흐름</h2>
        </div>
      </div>

      <Table
        columns={columns}
        dataSource={dataSource}
        size="middle"
        pagination={false}
        scroll={{ x: 'max-content' }}
        rowClassName={(row) => (row.financialAsset <= 0 ? 'depleted-row' : '')}
      />
    </section>
  );
}
