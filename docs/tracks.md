# Tracks

Three pre-scaffolded tracks plus a fourth "design your own" lane.

All four run in **Studio** with no install (browser, `uniqx` pre-installed, key pre-injected) — or locally via the [quickstart](quickstart.md) if you prefer your own Python environment.

## DFT — density functional theory

**Starter problem**: H₂O at STO-3G. Compute the SCF ground-state energy and the isotropic NMR shielding tensors.

**SDK surface**:
- `uniqx.domains.chemistry.basis.extract_basis(geometry, basis_name)`
- `uniqx.domains.chemistry.hartree_fock.rhf_module(geometry, basis_info)`
- `uniqx.domains.chemistry.nmr_full.nmr_full_module(geometry, basis_info)`

**Where to push**:
- Larger basis sets (6-31G, cc-pVDZ) — watch the cost column climb
- Larger molecules (methane, methanol, alanine) — watch the gateway split the graph into more execution blocks
- Geometry optimization on top of the SCF
- Compare convergence behaviour at different `max_iter` values

**Baseline**: PySCF reference for accuracy comparison. Ships in [tracks/dft/baseline.py](../tracks/dft/baseline.py).

---

## CFD — computational fluid dynamics

**Starter problem**: 2-D Lattice-Boltzmann Poiseuille channel, 64 × 16 grid, Re=100, 200 steps. Tracks the kinetic-energy diagnostic over time.

**SDK surface**:
- `uniqx.cfd.ChannelFlow(nx, ny, Re)` or `uniqx.cfd.LidDrivenCavity(n, Re)`
- `uniqx.cfd.build_lbm_step_module(flow)` → `(module, runtime_inputs, metadata)`
- `uniqx.cfd.build_diffusion_step_module(nx, ny, alpha, n_steps)` — thermal diffusion via `expv`

**Where to push**:
- Scale the grid to 256 × 64 or beyond
- Cavity flow at Re=1000 vs. Re=100 — the Pareto front moves
- Couple LBM with the diffusion step for a thermal channel
- Compare BGK collision against a multi-relaxation-time variant (you'd build the operator yourself)

**Baseline**: NumPy reference LBM step in [tracks/cfd/baseline.py](../tracks/cfd/baseline.py).

---

## MD — molecular dynamics

**Starter problem**: 64 argon atoms in a periodic box, Lennard-Jones 6-12, velocity-Verlet integrator, NVE ensemble, 500 steps.

**SDK surface**:
- `uniqx.domains.common.spatial.pairwise_distances`, `neighbor_list` (pure Python pre-computation)
- `uniqx.ops` — primitive operations to trace force and integrator kernels
- `@uniqx.to_module` to wrap the per-step kernel

**Status**: The SDK ships spatial utilities but does not ship a packaged MD integrator. The starter scaffolds one for you in [tracks/md/](../tracks/md/) — `lj_forces.py` traces the LJ pairwise force, `velocity_verlet.py` traces the integrator step. **This is the most open-ended track**: you are likely to want to extend or replace the integrator, swap in a different force field, or add thermostatting. That is the point.

**Where to push**:
- Larger systems (256, 1024 atoms) — neighbor list cost vs. force cost shifts
- Different force fields: Buckingham, harmonic bonds, plain Coulomb
- Langevin or Nosé-Hoover thermostatting
- A learned force field (one of the chemistry modules sketches a GNN pattern)

**Baseline**: NumPy reference integrator in [tracks/md/baseline.py](../tracks/md/baseline.py). Compare total-energy drift over a fixed trajectory.

---

## Bring your own

You may submit against a workload that is not one of the three tracks above. To qualify:

1. **State the problem precisely** — one paragraph in `results.json.workload_description`. The judges should understand the scientific question from that paragraph alone.
2. **Provide a baseline** — a NumPy / SciPy / PySCF / domain-standard reference run in `baseline.py`. Without a baseline, the judges cannot score Performance.
3. **Use `uniqx` for the heavy lifting** — at least one module must be traced with `@uniqx.to_module` and submitted through `preflight()` → `submit()`. A submission that doesn't engage the SDK doesn't engage the hackathon.

Custom workloads are scored on the same four criteria as the pre-defined tracks. Originality of the workload itself counts toward Creativity. The bar for Robustness is higher because the judges have no prior reference run to compare against — show your homework.

### Starting points

The fastest way to bootstrap a custom workload is to fork one of the curated examples:

- **15 examples in this repo** — see [`examples/INDEX.md`](../examples/INDEX.md). Covers foundational tracing, chemistry, quantum simulation, optimization, ML, and two real-world demonstrators.
- **Full gallery (60+)** — [app.oriqx.com/examples](https://app.oriqx.com/examples). Sign in with your hackathon account to browse and open any notebook in Studio.

Every example follows the same `problem → trace → preflight → run → oracle-compare` skeleton — you replace the problem, keep the skeleton, and you have a runnable submission.
