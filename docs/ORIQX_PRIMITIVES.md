# ORIQX Primitives Available

All primitives below are accessible via `import uniqx as ux`. Computations must be expressed inside a `@ux.trace`-decorated function; the decorator captures the dataflow graph as hardware-agnostic IR. Nothing executes locally — the IR is submitted to the ORIQX gateway for scheduling.

## Linear Algebra

| Primitive | Signature | Maps to (in original code) |
|---|---|---|
| `ux.matmul` | `(A, B)` → matrix | `X.T @ F @ X`, `X @ Cp`, `C[:,:n_occ] @ C[:,:n_occ].T` |
| `ux.dot` | `(u, v)` → scalar | `np.linalg.norm(...)` (via squared norm) |
| `ux.einsum` | `(A, B, subscripts, result_type)` | `np.einsum("pqrs,rs->pq", g, D)` — J and K matrix builds |
| `ux.transpose` | `(x, permutation)` | `.T` on matrices |
| `ux.diag` | `(x, *, result_type, k=0)` | `np.diag(1/sqrt(eig))` |
| `ux.kron` | `(a, b)` | Kronecker products in operator embedding |
| `ux.norm` | `(x, *, result_type, axis, ord)` | `np.linalg.norm(pos[i] - pos[j])` — interatomic distances |

## Eigenvalue Decomposition

| Primitive | Signature | Maps to |
|---|---|---|
| `ux.eigs` | `(A, *, k, which, hermitian, precision)` → `(eigvals, eigvecs)` | `np.linalg.eigh(S)` and `np.linalg.eigh(Fp)` |

For the full diagonalization inside SCF, use `which="smallest"` with `k=n_basis` to recover all eigenpairs. `hermitian=True` for symmetric matrices (S, F').

## Reductions and Arithmetic

| Primitive | Use case |
|---|---|
| `ux.reduce_sum` | `np.sum(D * (H + F))` — energy trace |
| `ux.reduce_mean` | removing net linear momentum from velocities |
| `ux.add`, `ux.sub`, `ux.mul`, `ux.div` | Fock matrix assembly, Verlet update |
| `ux.sqrt`, `ux.pow` | $\mathbf{X} = \mathbf{U}\boldsymbol{\Lambda}^{-1/2}\mathbf{U}^\top$, kinetic energy in Verlet |
| `ux.abs` | convergence criterion $|E_\text{new} - E_\text{prev}|$ |
| `ux.exp`, `ux.erf` | Boys function $F_n(T)$; Gaussian normalization factors |

## Tensor Slicing and Reshaping

| Primitive | Use case |
|---|---|
| `ux.slice` | Extract occupied orbital columns $\mathbf{C}[:,: N_\text{occ}]$ |
| `ux.gather` | Index-based selection of basis function subsets |
| `ux.concatenate` | Assembling block matrices or trajectories |
| `ux.reshape` | Reshaping ERI tensor for batched contractions |

## Control Flow

| Primitive | Signature | Use case |
|---|---|---|
| `ux.fori_loop` | `(lower, upper, body_fn, init_val)` | SCF iteration loop; finite-difference loop over atoms × directions; MD timestep loop |
| `ux.scan_loop` | `(lower, upper, body_fn, init_carry)` → stacked outputs | MD trajectory: collect `(energy, positions, velocities)` at each step |
| `ux.cond` | `(pred, true_fn, false_fn, *operands)` | SCF convergence gate; branch on backend strategy |

> **Critical rule:** Python `for` loops inside `@ux.trace` are **unrolled at trace time** and produce a copy of the IR for each iteration. For SCF (up to 100 iterations) and MD (up to 50+ steps), this generates enormous, unoptimizable graphs. Always use `ux.fori_loop` or `ux.scan_loop` for iteration counts larger than ~5.

## High-Level Physics Primitives

| Primitive | Use case in this challenge |
|---|---|
| `ux.linear_solve(A, b, *, hermitian, positive_definite)` | Solving $\mathbf{S}\mathbf{x} = \mathbf{b}$ variants in orthogonalization |
| `ux.expv(A, v, t, *, hermitian)` | Time evolution of quantum states if extending to TDDFT |
| `ux.optimize(init, *, method, fn)` | Geometry optimization post-MD |

