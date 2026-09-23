import { questions } from './data.js';

const q = questions.find((item) => item.key === 'financialAsset');
if (q) {
  q.step = 5000000;
  q.unit = '500만 원 단위';
}
