# Examples — bring-your-own starting points

62 notebooks lifted from the upstream `uniqx` gallery. Use any of them as scaffolding when designing a custom workload for the "bring-your-own" track.

Every notebook follows the same skeleton: problem definition → trace with `uniqx` → `preflight()` → submit to whichever route the engine recommends → compare to a classical oracle. The user code is identical regardless of the route the engine picks — that is the hardware-agnostic property the hackathon scores you on.

## Foundational — read these first

| Notebook | What it teaches |
|---|---|
| [`getting_started.ipynb`](notebooks/getting_started.ipynb) | Vector add, matmul, eigs. Trace + submit + parse round-trip. |
| [`hybrid_cpu_gpu_qpu.ipynb`](notebooks/hybrid_cpu_gpu_qpu.ipynb) | The hackathon's central theme — same code, three hardware routes, `preflight()` shows the tradeoff. |
| [`hardware_aware_dialects.ipynb`](notebooks/hardware_aware_dialects.ipynb) | How the lowering pipeline decides what runs where. |
| [`benchmark_chemistry_routes.ipynb`](notebooks/benchmark_chemistry_routes.ipynb) | Benchmark the same chemistry workload across every available route. |

## Algorithm primers

| Notebook | Algorithm |
|---|---|
| [`algorithm_grover_primer.ipynb`](notebooks/algorithm_grover_primer.ipynb) | Grover amplitude amplification |
| [`algorithm_qae_primer.ipynb`](notebooks/algorithm_qae_primer.ipynb) | Quantum amplitude estimation |
| [`algorithm_qite_primer.ipynb`](notebooks/algorithm_qite_primer.ipynb) | Quantum imaginary-time evolution |
| [`algorithm_hybrid_quantization_primer.ipynb`](notebooks/algorithm_hybrid_quantization_primer.ipynb) | Hybrid classical/quantum quantization |

## Chemistry — DFT track and beyond

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`chemistry_ground_state.ipynb`](notebooks/chemistry_ground_state.ipynb) | H₂ ground-state energy | Exact diagonalization |
| [`chemistry_hamiltonian_representations.ipynb`](notebooks/chemistry_hamiltonian_representations.ipynb) | Build / inspect molecular Hamiltonians | PySCF |
| [`vqe_ground_state.ipynb`](notebooks/vqe_ground_state.ipynb) | Variational ground state | eigsh |
| [`two_electron_chemistry_vqe.ipynb`](notebooks/two_electron_chemistry_vqe.ipynb) | Two-electron VQE end-to-job | FCI |
| [`real_space_quantum_chemistry.ipynb`](notebooks/real_space_quantum_chemistry.ipynb) | Real-space basis instead of Gaussians | PySCF |
| [`nmr_notebook.ipynb`](notebooks/nmr_notebook.ipynb) | Isotropic shielding tensors | PySCF / NMR prop |
| [`geometry_optimization.ipynb`](notebooks/geometry_optimization.ipynb) | Equilibrium geometry via gradients | PySCF |
| [`ligand_geometry_optimization.ipynb`](notebooks/ligand_geometry_optimization.ipynb) | Ligand pose / strain optimisation | UFF |
| [`conformer_search.ipynb`](notebooks/conformer_search.ipynb) | Conformer enumeration | RDKit |
| [`transition_state.ipynb`](notebooks/transition_state.ipynb) | Saddle-point search | dimer / eigenvector following |
| [`neb_reaction_path.ipynb`](notebooks/neb_reaction_path.ipynb) | Nudged elastic band | classical NEB |
| [`photoisomerization.ipynb`](notebooks/photoisomerization.ipynb) | Excited-state dynamics | TDDFT |
| [`allosteric_simulation.ipynb`](notebooks/allosteric_simulation.ipynb) | Protein allosteric coupling | MD biophysics |

## Physics — CFD, MD, spin systems

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`aerodynamic_modeling.ipynb`](notebooks/aerodynamic_modeling.ipynb) | Aerodynamic flow modelling | NumPy CFD |
| [`spin_chain_ground_state.ipynb`](notebooks/spin_chain_ground_state.ipynb) | TFI lowest eigenvalue | Lanczos |
| [`spin_chain_dynamics.ipynb`](notebooks/spin_chain_dynamics.ipynb) | e^{-iHt}·ψ | scipy.expm |
| [`large_spin_chain_dynamics.ipynb`](notebooks/large_spin_chain_dynamics.ipynb) | Larger-N spin chain | block expm |
| [`quantum_simulation.ipynb`](notebooks/quantum_simulation.ipynb) | Generic Hamiltonian simulation | Trotter |
| [`poisson_solve_grid.ipynb`](notebooks/poisson_solve_grid.ipynb) | Lu = b on a 2D grid | LU |
| [`kinetic_eigenmodes_grid.ipynb`](notebooks/kinetic_eigenmodes_grid.ipynb) | Eigenmodes of ∇² | Lanczos |

## Numerical linear algebra and graphs

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`least_squares_regression.ipynb`](notebooks/least_squares_regression.ipynb) | lstsq(X, y) | Normal equations |
| [`low_rank_denoising.ipynb`](notebooks/low_rank_denoising.ipynb) | Truncated-SVD denoising | LAPACK |
| [`pagerank_dominant_eigenvector.ipynb`](notebooks/pagerank_dominant_eigenvector.ipynb) | PageRank | Power iteration |
| [`graph_spectral_clustering.ipynb`](notebooks/graph_spectral_clustering.ipynb) | Spectral clustering | eigh + KMeans |
| [`partition_function_logsumexp.ipynb`](notebooks/partition_function_logsumexp.ipynb) | logsumexp Boltzmann sampling | scipy |

## Sampling and statistics

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`markov_chain_mixing.ipynb`](notebooks/markov_chain_mixing.ipynb) | MCMC mixing rates | Power method |
| [`variational_monte_carlo.ipynb`](notebooks/variational_monte_carlo.ipynb) | VMC sampling | PRNG |
| [`thermal_state_sampling.ipynb`](notebooks/thermal_state_sampling.ipynb) | Thermal-state samples | classical MCMC |
| [`random_walk_search.ipynb`](notebooks/random_walk_search.ipynb) | Random-walk search | classical walk |
| [`mcmc_cpu_vs_gpu.ipynb`](notebooks/mcmc_cpu_vs_gpu.ipynb) | Direct CPU vs GPU sampling — a model for reporting a hardware tradeoff. |

## Machine learning

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`neural_network_training.ipynb`](notebooks/neural_network_training.ipynb) | Gradient-based training step | NumPy backprop |
| [`dense_neural_network_hybrid.ipynb`](notebooks/dense_neural_network_hybrid.ipynb) | Hybrid dense MLP | classical MLP |
| [`generative_adversarial_step.ipynb`](notebooks/generative_adversarial_step.ipynb) | GAN training step | classical GAN |
| [`reinforcement_learning_step.ipynb`](notebooks/reinforcement_learning_step.ipynb) | RL action sampling | tabular Q-learning |
| [`binary_classification_quantum.ipynb`](notebooks/binary_classification_quantum.ipynb) | Binary classifier | logistic regression |
| [`kernel_svm_quantum_feature_map.ipynb`](notebooks/kernel_svm_quantum_feature_map.ipynb) | Kernel SVM | RBF kernel |
| [`vqc_softmax_readout.ipynb`](notebooks/vqc_softmax_readout.ipynb) | Variational quantum classifier | logistic |
| [`qml_loss_reduction.ipynb`](notebooks/qml_loss_reduction.ipynb) | QML loss reduction (QAE-as-mean) | numpy reduce |
| [`gradient_variance_diagnostic.ipynb`](notebooks/gradient_variance_diagnostic.ipynb) | Variance of gradients (barren-plateau diag) | numerical gradient |

## Optimisation

| Notebook | Problem | Classical oracle |
|---|---|---|
| [`qaoa_maxcut.ipynb`](notebooks/qaoa_maxcut.ipynb) | MaxCut on small graphs | Simulated annealing |
| [`qaoa_with_layer_norm.ipynb`](notebooks/qaoa_with_layer_norm.ipynb) | QAOA + LayerNorm trick | classical SA |
| [`combinatorial_qubo_optimization.ipynb`](notebooks/combinatorial_qubo_optimization.ipynb) | QUBO solver | tabu / simulated annealing |
| [`route_optimization.ipynb`](notebooks/route_optimization.ipynb) | Vehicle routing | OR-Tools |
| [`grid_expansion_planning.ipynb`](notebooks/grid_expansion_planning.ipynb) | Energy-grid expansion | MILP |

## Quantum + classical interop

| Notebook | What it shows |
|---|---|
| [`classical_quantum_interaction.ipynb`](notebooks/classical_quantum_interaction.ipynb) | Round-tripping data between classical and quantum kernels. |
| [`classical_quantum_roundtrip.ipynb`](notebooks/classical_quantum_roundtrip.ipynb) | Submit-and-resubmit pattern for hybrid loops. |
| [`constrained_param_unitary.ipynb`](notebooks/constrained_param_unitary.ipynb) | Parameter constraints on a unitary. |
| [`jax_gap_primitives.ipynb`](notebooks/jax_gap_primitives.ipynb) | JAX-style differentiable primitives mapped to gateway ops. |
| [`oqi_usecases.ipynb`](notebooks/oqi_usecases.ipynb) | Selected industrial use cases driven by `oqi` primitives. |

## Real-world demonstrators

| Notebook | What it shows |
|---|---|
| [`autonomous_driving_vla.ipynb`](notebooks/autonomous_driving_vla.ipynb) | Visual-language-action model with hybrid inference. |
| [`fraud_detection.ipynb`](notebooks/fraud_detection.ipynb) | Imbalanced classification + quantum kernel feature map. |
| [`threat_detection.ipynb`](notebooks/threat_detection.ipynb) | Anomaly detection with a hybrid scorer. |
| [`quantum_cryptography.ipynb`](notebooks/quantum_cryptography.ipynb) | QKD-style protocol primitive. |

## How to use these in a "bring your own" submission

1. Pick the notebook closest to the workload you want to build.
2. Copy it into `submissions/<team-handle>/submission.ipynb`.
3. Replace the problem definition with yours. Keep the `preflight()` → `submit()` → oracle-compare skeleton.
4. Fill in `results.json.workload_description` (required for `track: "custom"`).
5. Submit per [docs/submission.md](../docs/submission.md).

The judges score you on the *shape of your Pareto frontier* and the *quality of your justification*, not on which example you started from.
