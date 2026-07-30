# Dyadic Cauchy-MDS shear-layer screening

Reproducibility repository for the manuscript **Four-step projective recurrence in a dyadic Cauchy--MDS shear layer** by Sergo A. Episkoposian and Svetlana A. Grigoryan.

## Scientific scope

The manuscript proves a family-level four-step scalar recurrence for a shear-coupled dyadic kernel over characteristic two and studies a dyadic Cauchy-MDS instance over the AES field. The repository contains the exact computations that are explicitly marked as computational in the paper. It does not claim a complete cipher design or complete nonlinear cryptanalysis.

## Repository layout

- `src/`: verification and optimization programs.
- `results/`: machine-readable outputs and complete solver logs.
- `manuscript/`: final LaTeX source and PDF.
- `docs/`: Russian GitHub/Zenodo publication guide.
- `CITATION.cff`, `.zenodo.json`: release metadata.

## Reproduce

```bash
python -m venv .venv
. .venv/bin/activate             # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
./run_all.sh
```

Expected headline results:

- 252 admissible parameters scanned directly;
- representative `L^4 = D8 I`;
- exact vector periods 51, 102, 204;
- isolated AES reference order 8 under row-major input/output;
- binary AES fixed-space dimensions 16, 32, 64, 128;
- support-relaxation optimum 25 in both MILP formulations;
- witness weight 25.

## Citation and DOI

The DOI will be added after the GitHub release is archived on Zenodo. Do not replace `USERNAME` or insert a DOI until the corresponding repository and Zenodo record actually exist.

## Licenses

Software: MIT. Documentation and author manuscript: CC BY 4.0 unless superseded by the journal publishing agreement.
