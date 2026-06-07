import { Card, Tag } from 'antd';
import { formatAge, formatEok, statusMeta } from '../utils/formatters.js';
import { statusTagColor } from '../theme.js';

export default function ScenarioComparison({ simulation }) {
  const { inputs, scenarios } = simulation;

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">비교</p>
          <h2>1년 더 근무 효과</h2>
        </div>
      </div>

      <div className="scenario-grid">
        {scenarios.map((scenario) => (
          <Card key={scenario.extraYears} className="scenario-card" variant="outlined">
            <div className="scenario-header">
              <strong>{scenario.retirementAge}세 퇴사</strong>
              <Tag color={statusTagColor[scenario.status]}>
                {statusMeta[scenario.status].label}
              </Tag>
            </div>
            <dl>
              <div>
                <dt>추가 근무</dt>
                <dd>{scenario.extraYears}년</dd>
              </div>
              <div>
                <dt>고갈 나이</dt>
                <dd>{formatAge(scenario.depletionAge)}</dd>
              </div>
              <div>
                <dt>{inputs.simulationUntilAge}세 잔여 금융자산</dt>
                <dd>{formatEok(scenario.finalFinancialAsset)}</dd>
              </div>
            </dl>
          </Card>
        ))}
      </div>
    </section>
  );
}
