#!/usr/bin/env python3
from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results'
required=['aes_serialization_results.json','family_summary.json','gamma_family.csv','full_certificate_results.json','screening_record.json','screening_schema.json']
missing=[x for x in required if not (R/x).is_file()]
if missing: raise SystemExit(f'missing repository result files: {missing}')
family=json.loads((R/'family_summary.json').read_text())
with (R/'gamma_family.csv').open(newline='') as f: rows=list(csv.DictReader(f))
aes=json.loads((R/'aes_serialization_results.json').read_text())
assert family['admissible_parameters']==252 and len(rows)==252
assert aes['coordinates']=='row-major input and row-major output'
assert aes['order']==8
assert aes['fixed_dimensions_F2']=={'1':16,'2':32,'4':64,'8':128}
print('repository_integrity OK')
