#!/usr/bin/env python3
"""Independent release-integrity checks for Supplementary Material S1."""
from __future__ import annotations
import csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = {
    'README.md','requirements.txt','verify_full_certificate.py','verify_family.py',
    'verify_aes_serialization.py','activity_milp_forward_logged.py',
    'activity_milp_independent.py','verify_activity_witness.py',
    'verify_release.py','aes_serialization_results.json','family_summary.json',
    'gamma_family.csv','full_certificate_results.json','screening_record.json',
    'screening_schema.json','solver_forward_full.log','solver_independent_full.log',
    'SHA256SUMS','manuscript_source.tex','lat_adjoint_orbits.json'
}
missing=sorted(p for p in REQUIRED if not (ROOT/p).is_file())
if missing:
    raise SystemExit(f'Missing required files: {missing}')

try:
    import jsonschema
except ImportError as exc:
    raise SystemExit('Install requirements.txt before running this check.') from exc

record=json.loads((ROOT/'screening_record.json').read_text())
schema=json.loads((ROOT/'screening_schema.json').read_text())
jsonschema.validate(record, schema)

family=json.loads((ROOT/'family_summary.json').read_text())
if family.get('admissible_parameters') != 252:
    raise SystemExit('family_summary.json does not report 252 admissible parameters')
with (ROOT/'gamma_family.csv').open(newline='') as fh:
    rows=list(csv.DictReader(fh))
if len(rows) != 252:
    raise SystemExit(f'gamma_family.csv has {len(rows)} rows, expected 252')

aes=json.loads((ROOT/'aes_serialization_results.json').read_text())
if aes.get('coordinates') != 'row-major input and row-major output':
    raise SystemExit('AES serialization is not the required row-major/row-major convention')
if aes.get('order') != 8:
    raise SystemExit('Unexpected isolated AES operator order')
expected_fixed={'1':16,'2':32,'4':64,'8':128}
if aes.get('fixed_dimensions_F2') != expected_fixed:
    raise SystemExit('Unexpected AES fixed-space dimensions')


full=json.loads((ROOT/'full_certificate_results.json').read_text())
if sorted(full.get('lat_adjoint_orbit_intersections', [])) != [45,46,47,47,49]:
    raise SystemExit('Unexpected LAT adjoint-orbit intersections')
adj=json.loads((ROOT/'lat_adjoint_orbits.json').read_text())
if adj.get('orbit_lengths') != [51,51,51,51,51]:
    raise SystemExit('Unexpected LAT adjoint-orbit lengths')
if adj.get('lat_diagonal_intersections') != [46,47,49,45,47]:
    raise SystemExit('Unexpected LAT adjoint-orbit data')

# Verify all digests listed in SHA256SUMS. The manifest intentionally omits itself.
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
    if not line.strip():
        continue
    digest, rel = line.split(maxsplit=1)
    rel=rel.lstrip('*')
    path=ROOT/rel
    if not path.is_file():
        raise SystemExit(f'Manifest path missing: {rel}')
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f'SHA-256 mismatch: {rel}')
print('release_integrity OK')
print('required_files', len(REQUIRED))
print('family_rows', len(rows))
print('aes_order', aes['order'])
print('aes_fixed_spaces', aes['fixed_dimensions_F2'])
