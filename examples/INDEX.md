# Examples — bring-your-own starting points

15 curated notebooks lifted from the upstream `uniqx` examples gallery. Use them as scaffolding when designing a custom workload for the "bring-your-own" track.

Each notebook follows the same skeleton: problem definition → trace with `uniqx` → `preflight()` → submit to whichever route the engine recommends → compare to a classical oracle. Your code is identical regardless of the route the engine picks — that is the hardware-agnostic property the hackathon scores you on.

The full gallery of 60+ examples lives at [app.oriqx.com/examples](https://app.oriqx.com/examples). The subset here is what we'd hand a hackathon team on day one.

## Foundational — read these first

| Notebook | What it teaches |
|---|---|
| [`getting_started.ipynb`](notebooks/getting_started.ipynb) | Vector add, matmul, eigs. Trace + submit + parse round-trip. |
| [`hybrid_cpu_gpu_qpu.ipynb`](notebooks/hybrid_cpu_gpu_qpu.ipynb) | The hackathon's central theme — same code, three hardware routes, `preflight()` shows the tradeoff. |
| [`hardware_aware_dialects.ipynb`](notebooks/hardware_aware_dialects.ipynb) | How the lowering pipeline decides what runs where. |

## Chemistry — DFT-track adjacent

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`chemistry_ground_state.ipynb`](notebooks/chemistry_ground_state.ipynb) | H₂ ground-state energy | Exact diagonalization |
| [`vqe_ground_state.ipynb`](notebooks/vqe_ground_state.ipynb) | Variational ansatz, parameter optimization | Eigsh |
| [`geometry_optimization.ipynb`](notebooks/geometry_optimization.ipynb) | Equilibrium geometry via gradient descent | PySCF |

## Physics / dynamics

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`spin_chain_dynamics.ipynb`](notebooks/spin_chain_dynamics.ipynb) | e^{-iHt}·ψ for transverse-field Ising | scipy.expm |
| [`poisson_solve_grid.ipynb`](notebooks/poisson_solve_grid.ipynb) | Lu = b on a 2D grid | LU |
| [`kinetic_eigenmodes_grid.ipynb`](notebooks/kinetic_eigenmodes_grid.ipynb) | Eigenmodes of ∇² | Lanczos |

## ML and optimization

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`neural_network_training.ipynb`](notebooks/neural_network_training.ipynb) | Gradient-based training step | NumPy backprop |
| [`qaoa_maxcut.ipynb`](notebooks/qaoa_maxcut.ipynb) | MaxCut on small graphs | Simulated annealing |
| [`route_optimization.ipynb`](notebooks/route_optimization.ipynb) | Vehicle routing | OR-Tools |
| [`mcmc_cpu_vs_gpu.ipynb`](notebooks/mcmc_cpu_vs_gpu.ipynb) | Direct CPU vs GPU sampling comparison — a model for how to *report* a hardware tradeoff. |

## Real-world demonstrators

| Notebook | What it shows |
|---|---|
| [`autonomous_driving_vla.ipynb`](notebooks/autonomous_driving_vla.ipynb) | Visual-language-action model with hybrid inference. |
| [`fraud_detection.ipynb`](notebooks/fraud_detection.ipynb) | Imbalanced classification, quantum kernel feature map. |

## How to use these in a "bring your own" submission

1. Pick the notebook closest to the workload you want to build.
2. Copy it into `submissions/<team-handle>/submission.ipynb`.
3. Replace the problem definition with yours. Keep the `preflight()` → `submit()` → oracle-compare skeleton.
4. Fill in `results.json.workload_description` (required for `track: "custom"`).
5. Submit per [docs/submission.md](../docs/submission.md).

The judges score you on the *shape of your Pareto frontier* and the *quality of your justification*, not on which example you started from.
