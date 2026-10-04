"""cloud yt-quality 1003 시제품(work/video/src/motion-proto) 순수 함수 시험을 node --test로 돌린다.
node가 없거나 22.6보다 낮으면(타입 지우기 미지원) 건너뛴다. 무거운 의존성 없음.
실행: py -3.12 -m pytest work/tests/test_yt_quality_video.py
"""
import os
import re
import shutil
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEST = os.path.join(ROOT, 'work', 'video', 'tests', 'yt_quality_proto.test.mjs')


def node_version():
    node = shutil.which('node')
    if not node:
        return None, None
    out = subprocess.run([node, '--version'], capture_output=True, text=True).stdout.strip()
    m = re.match(r'v(\d+)\.(\d+)', out)
    return node, (int(m.group(1)), int(m.group(2))) if m else None


class YtQualityProtoTest(unittest.TestCase):
    def test_node_suite_passes(self):
        node, ver = node_version()
        if not node or not ver or ver < (22, 6):
            self.skipTest('node 22.6+ 없음')
        pkg = os.path.join(ROOT, 'work', 'video', 'package.json')
        if os.path.exists(pkg) and '"type": "commonjs"' in open(pkg, encoding='utf-8').read():
            self.skipTest('PC work/video는 commonjs — .ts 이름 내보내기를 node --test가 못 읽음(10/5 순돌이, 프로토타입은 Remotion 번들에서 씀)')
        args = [node]
        if ver < (22, 18):
            args.append('--experimental-strip-types')
        r = subprocess.run(args + ['--test', TEST], capture_output=True, text=True, encoding='utf-8', cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout[-3000:] + r.stderr[-2000:])
        self.assertRegex(r.stdout, r'# fail 0')

    def test_protos_are_import_free(self):
        # 순수 함수 파일은 다른 파일을 import하지 않아야 node가 그대로 읽는다
        for name in ('captionTiming.ts', 'numberSpeech.ts'):
            src = open(os.path.join(ROOT, 'work', 'video', 'src', 'motion-proto', name), encoding='utf-8').read()
            self.assertNotRegex(src, r'(?m)^\s*import\s', name)


if __name__ == '__main__':
    unittest.main()
