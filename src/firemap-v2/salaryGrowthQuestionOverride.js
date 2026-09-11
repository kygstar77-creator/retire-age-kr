import { defaultInputs } from '../utils/retirementSimulator.js';
import { questions } from './data.js';

defaultInputs.salaryGrowthRate = defaultInputs.salaryGrowthRate ?? 0;

questions.splice(4, 0, {
  key: 'salaryGrowthRate', type: 'percent', label: '연봉상승률', title: '월 적립금을 매년 얼마나 늘릴까요?', helper: '연봉이 오르는 만큼 월 적립금도 같이 올리는 시나리오예요.', min: 0, max: 10, step: 0.5, presets: [0, 2, 3