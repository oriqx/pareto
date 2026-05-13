# Track: Ab-Initio Molecular Dynamics (AIMD)

---

## 1. Challenge Objective

You are given a working Python implementation of **Ab Initio Molecular Dynamics (AIMD)** for the water molecule ($H_2O$), built from scratch using NumPy and Scipy. The simulation runs a Born-Oppenheimer MD trajectory: at each timestep, it solves the Restricted Hartree-Fock (RHF) Self-Consistent Field (SCF) equations to obtain the electronic energy and forces, then propagates the nuclei using the Velocity Verlet algorithm.

The program is correct — but it is entirely sequential, CPU-only, and not portable across hardware.

**Your mission:** Rewrite this program using the **ORIQX primitives** (See [docs/ORIQX_PRIMITIVES.md](docs/ORIQX_PRIMITIVES.md)) by decomposing each computational step into hardware-agnostic operations. ORIQX will then automatically route, compile, and execute those primitives on the most efficient available hardware — CPU, GPU, TPU, QPU, or hybrid combinations — without you changing a single line of your submission code.

This is not about rewriting the physics. It is about expressing the *same computation* in a form that a platform can optimize, schedule, and dispatch across heterogeneous hardware.

---

## 2. AIMD Program: Steps and Mathematics

The program lives across six files: `baseline.py` (entry point), `aimd.py` (integrator), `scf.py` (electronic structure), `integrals.py` (McMurchie-Davidson engine), `basis.py` (STO-3G basis), `constants.py` (physical constants). The basis construction (`basis.py`) is provided as-is — participants do not need to decompose it. The five computational stages to rewrite are:

| Stage | Description | Key operation |
|---|---|---|
| 1 | One-electron integrals | $S_{\mu\nu},\; T_{\mu\nu},\; V_{\mu\nu} \ \Rightarrow\ H = T + V$ |
| 2 | Two-electron integrals (ERI) | $g_{\mu\nu\lambda\sigma} = (\mu\nu\|\lambda\sigma)$, rank-4 tensor $\mathcal{O}(N^4)$ |
| 3 | RHF SCF | $\mathbf{F}\mathbf{C} = \mathbf{S}\mathbf{C}\boldsymbol{\varepsilon}$, iterate until $\|E_\text{new}-E_\text{prev}\| < \tau$ |
| 4 | Forces (finite differences) | $F \approx -\dfrac{E(\mathbf{R}+\Delta x) - E(\mathbf{R}-\Delta x)}{2\Delta x}$ |
| 5 | Velocity Verlet MD | $\mathbf{R}(t{+}\Delta t) = \mathbf{R} + \mathbf{v}\Delta t + \tfrac{1}{2}\mathbf{M}^{-1}\mathbf{F}\Delta t^2$ |

---

### Stage 1 — One-Electron Integral Matrices

Three $N_\text{basis} \times N_\text{basis}$ matrices are built analytically using the McMurchie-Davidson (MD) recurrence scheme.

**Overlap matrix:**
$$S_{\mu\nu} = \langle \chi_\mu | \chi_\nu \rangle = \int \chi_\mu^*(\mathbf{r})\, \chi_\nu(\mathbf{r})\, d\mathbf{r}$$

**Kinetic energy matrix:**
$$T_{\mu\nu} = \langle \chi_\mu | -\tfrac{1}{2}\nabla^2 | \chi_\nu \rangle$$

**Nuclear attraction matrix:**

$$V_{\mu\nu}=\sum_A\langle\chi_\mu|-\frac{Z_A}{|\mathbf{r}-\mathbf{R}_A|}|\chi_\nu\rangle$$

The core Hamiltonian is $H_{\mu\nu} = T_{\mu\nu} + V_{\mu\nu}$.

The MD recurrence uses Hermite Gaussian expansion coefficients $E^{ij}_t$ and auxiliary Coulomb integrals $R^{tuv}_n$ (involving the Boys function $F_n(T)$ ).

**Code:** 

`integrals.py` → `overlap_primitive`, `kinetic_primitive`, `nuclear_primitive`, `contracted_integral` (how to evaluate a single integral)

`scf.py` → `build_overlap_kinetic`, `build_nuclear` (assembly of the full $N \times N$ matrices for RHF)

---

### Stage 3 — Two-Electron Repulsion Integrals (ERI Tensor)

The most expensive step: a rank-4 tensor of $N_\text{basis}^4$ elements.

$$g_{\mu\nu\lambda\sigma}=(\mu\nu|\lambda\sigma)=\iint\frac{\chi_\mu(\mathbf{r}_1)\chi_\nu(\mathbf{r}_1)\chi_\lambda(\mathbf{r}_2)\chi_\sigma(\mathbf{r}_2)}{|\mathbf{r}_1 - \mathbf{r}_2|}\, d\mathbf{r}_1 \, d\mathbf{r}_2$$

For STO-3G $H_2O$ this is a $7^4 = 2401$-element tensor. Each element is a multi-center integral evaluated via the MD recursion.

**Code:** 

`integrals.py` → `eri_primitive`, `contracted_integral` (how to evaluate a single four-center integral) 

`scf.py` → `build_eri_tensor(basis)` (quadruple loop assembling the full $N^4$ tensor for RHF)

---

### Stage 4 — RHF Self-Consistent Field (SCF)

The SCF is an iterative fixed-point algorithm to solve the Roothaan-Hall equations $\mathbf{F}\mathbf{C} = \mathbf{S}\mathbf{C}\boldsymbol{\varepsilon}$.

**Orthogonalization:** Compute $\mathbf{X} = \mathbf{S}^{-1/2}$ via eigendecomposition:
$$\mathbf{S} = \mathbf{U}\boldsymbol{\Lambda}\mathbf{U}^\top \qquad \Rightarrow \qquad \mathbf{X} = \mathbf{U}\boldsymbol{\Lambda}^{-1/2}\mathbf{U}^\top$$

**SCF iteration** (until $|E_\text{new} - E_\text{prev}| < \tau$):

1. Build Coulomb and exchange matrices from density $\mathbf{D}$:

$$J_{\mu\nu} = \sum_{\lambda\sigma} g_{\mu\nu\lambda\sigma}\, D_{\lambda\sigma} \qquad K_{\mu\nu} = \sum_{\lambda\sigma} g_{\mu\lambda\nu\sigma}\, D_{\lambda\sigma}$$

2. Build Fock matrix: $\mathbf{F} = \mathbf{H} + \mathbf{J} - \tfrac{1}{2}\mathbf{K}$

3. Transform to orthogonal basis: $\mathbf{F}' = \mathbf{X}^\top \mathbf{F}\, \mathbf{X}$

4. Diagonalize: $\mathbf{F}'\mathbf{C}' = \mathbf{C}'\boldsymbol{\varepsilon}$, recover $\mathbf{C} = \mathbf{X}\mathbf{C}'$

5. Build new density matrix ($N_\text{occ} = N_e/2$ occupied orbitals):

$$\mathbf{D} = 2\sum_{i=1}^{N_\text{occ}} \mathbf{c}_i \mathbf{c}_i^\top$$

6. Compute total electronic energy:

$$E_\text{total} = \frac{1}{2}\text{Tr}\left[\mathbf{D}(\mathbf{H} + \mathbf{F})\right] + E_\text{nuc}$$

where $E_\text{nuc} = \sum_{A<B} Z_A Z_B / R_{AB}$ is the nuclear repulsion energy.

**Code:** 

`scf.py` → `rhf_scf(atoms_bohr, n_electrons)`

---

### Stage 5 — Force Computation (Finite Differences)

Analytical gradients are not implemented. Instead, atomic forces are estimated by central finite differences over the SCF energy surface:

$$F_{id} = -\frac{\partial E}{\partial R_{i,d}} \approx -\frac{E(\mathbf{R_{i,d}} + \Delta x) - E(\mathbf{R_{i,d}} - \Delta x)}{2\Delta x}$$

for each atom $i$ and Cartesian direction $d \in \{x, y, z\}$. Each call requires $2 \times N_\text{atoms} \times 3$ full SCF calculations — for $H_2O$, that is **18 SCF calls per step**.

**Code:** 

`scf.py` → `compute_forces(atoms_bohr, n_electrons)`

---

### Stage 6 — Velocity Verlet MD Integration

Born-Oppenheimer MD propagates nuclei classically on the ground-state energy surface. The Velocity Verlet algorithm is time-reversible and symplectic:

$$\mathbf{R}(t+\Delta t) = \mathbf{R}(t) + \mathbf{v}(t)\,\Delta t + \frac{1}{2}\mathbf{M}^{-1}\mathbf{F}(t)\,\Delta t^2$$

$$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \frac{1}{2}\mathbf{M}^{-1}\left[\mathbf{F}(t) + \mathbf{F}(t+\Delta t)\right]\Delta t$$

where $\mathbf{M}$ is the diagonal mass matrix (in atomic units, $m_\text{AMU} \times 1822.888$).

Initial velocities can be drawn from the Maxwell-Boltzmann distribution at temperature $T$:

$$\sigma_{i,d} = \sqrt{\frac{k_B T}{m_i}} \qquad v_{i,d} \sim \mathcal{N}(0, \sigma_{i,d}^2)$$

followed by removal of the net linear momentum: $\mathbf{v} \leftarrow \mathbf{v} - \langle \mathbf{v} \rangle$.

**Code:** 

`aimd.py` → `aimd(...)`, `maxwell_boltzmann_velocities(...)`

---

## 3. Deliverables

All submissions must follow the structure specified in `templates/submission`. Read that document before starting.

In addition to the deliverables listed in `templates/submission`, this challenge specifically requires:

### Annotated Decomposition Map

A written document (PDF or Markdown) mapping each stage of the original program to the ORIQX primitives used, structured as:

| Stage | Original code | ORIQX primitive(s) | Rationale |
|---|---|---|---|
| SCF iteration | `for _ in range(max_iter)` | `ux.fori_loop` | Prevents loop unrolling in IR |
| … | … | … | … |

Explain **why** each mapping was chosen, including any trade-offs between different primitive options (e.g., `ux.einsum` vs explicit loops for the ERI contraction, `ux.fori_loop` vs `ux.scan_loop` for the MD steps).

### Working ORIQX Implementation

A Python file (`aimd_oriqx.py`) that:

1. Defines the full AIMD pipeline inside `@ux.trace`-decorated functions.
2. Connects to the ORIQX gateway and submits the computation.
3. Retrieves and parses results using `ux.get` and `ux.parse_result`.
4. Produces a trajectory in the same `.xyz` format as `aimd_h2o_trajectory.xyz` for comparison.

The implementation must be runnable with:

```bash
UNIQX_GATEWAY=<provided-gateway> UNIQX_API_KEY=<provided-key> python aimd_oriqx.py
```

### Numerical Validation

A table comparing your ORIQX implementation against the reference NumPy code for the first 5 MD steps of $H_2O$:

| Step | $E_\text{ref}$ (Ha) | $E_\text{ORIQX}$ (Ha) | $\Delta E$ | O-H1 (Å) | O-H2 (Å) |
|---|---|---|---|---|---|
| 0 | -74.963xxx | … | … | … | … |
| … | | | | | |

Acceptable tolerance: $|\Delta E| < 10^{-5}$ Ha per step.

Reference values: 

H₂O at STO-3G: RHF total energy ≈ −74.96 Ha (PySCF reference). The starter checks within 5 mHa.

---

## Resources

- ORIQX SDK documentation: https://docs.oriqx.com
- Reference implementation: `run_h2o.py`, `aimd.py`, `scf.py`, `integrals.py`, `basis.py`
- Reference trajectory for validation: `aimd_h2o_trajectory.xyz`
- Gateway and API key: provided on the day of the hackathon
- Studio (IR visualization): https://studio.oriqx.com
