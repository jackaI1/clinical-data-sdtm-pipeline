"""Fail CI if the complete Python/R workflow drops expected study outputs."""
import csv
import json
import re
from pathlib import Path
import sys

root = Path(sys.argv[1])
output = root/'demo/output'
manifest = json.loads((output/'manifest.json').read_text())
assert manifest['subjects_input']==120
assert manifest['subjects_released']==119
assert manifest['queries']==5
assert manifest['quarantined_records']==16
assert json.loads((output/'roundtrip.json').read_text())['equal'] is True
for d in ['DM','VS','LB','AE','EX','DS']:
    assert (output/f'sdtm/{d}.csv').read_bytes()==(output/f'roundtrip_sdtm/{d}.csv').read_bytes()
for name in ['report.html','km.png','demographics.csv','cox.csv','ph_test.csv','analysis_population.csv','session-info.txt']:
    assert (root/'analysis'/name).stat().st_size>0, name
with (root/'analysis/analysis_population.csv').open() as f:
    rows = list(csv.DictReader(f))
assert len(rows)==119
assert len({r['USUBJID'] for r in rows})==119
assert {r['event'] for r in rows}=={'0','1'}
report = (root/'analysis/report.html').read_text()
images = re.findall(r'<img[^>]+src=[\"\']([^\"\']+)',report)
assert images and all(src.startswith('data:image/') for src in images), 'Report must embed its curve image'
assert '/Users/' not in report and '/home/runner/' not in report, 'Report leaked local paths'
print('Verified six domains, five queries, 119 analysis subjects and complete R report artifacts.')
