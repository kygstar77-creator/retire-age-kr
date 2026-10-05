// 모션 부품 미리보기 전용 입구(본편 Root와 따로) — npx remotion render src/motion/preview/entry.ts <id> <out> --props=<json>
import {registerRoot} from 'remotion';
import {PreviewRoot} from './PreviewRoot';
registerRoot(PreviewRoot);
