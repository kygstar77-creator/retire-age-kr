import { defaultInputs } from '../utils/retirementSimulator.js';
import { questions } from './data.js';

defaultInputs.salaryGrowthRate ??= 0;

const asset = questions.find((item) => item.key === 'financialAsset');
if (asset) {
  asset.step = 5000000;
  asset.unit = '500만 원 단위';
}

if (!questions.some((item) => item.key === 'salaryGrowthRate'))