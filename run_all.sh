#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/results"
python ../src/verify_full_certificate.py
python ../src/verify_family.py
python ../src/verify_aes_serialization.py
python ../src/activity_milp_forward_logged.py | tee solver_forward_full.log
python ../src/activity_milp_independent.py | tee solver_independent_full.log
python ../src/verify_activity_witness.py
cd "$ROOT"
python src/verify_repository.py
