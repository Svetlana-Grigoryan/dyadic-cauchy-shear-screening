# v1.0.1 - AMC reproducibility release

This release corresponds to the final reviewer-ready manuscript.

## Verified claims

- analytic family-level four-step scalar recurrence is documented in the manuscript;
- direct enumeration of all 252 admissible Cauchy parameters;
- representative identity `L^4 = D8 I` and normalized Jordan type `J4(1)^4`;
- exact vector periods 51, 102, and 204;
- coherent row-major serialization of the isolated AES linear reference;
- two independently written MILP formulations with optimum 25 in the defined support relaxation;
- solver-independent verification of the printed weight-25 witness.

## Important scope limitation

The value 25 is a theorem only for the stated MDS-support relaxation. This release does not assert unrestricted DDT/LAT/BCT compatibility, nonlinear subspace-trail resistance, implementation optimality, or security of a complete cipher.

- Corrected LAT mask propagation to the binary adjoint C_D8^{-T} and added exact orbit certificates.
