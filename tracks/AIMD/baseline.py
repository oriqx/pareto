# Copyright (c) 2026 ORIQX AG. MIT licensed.
"""
AIMD simulation of H2O — entry point.

Born-Oppenheimer MD with RHF/STO-3G, finite-difference forces,
velocity Verlet integrator.

Reference STO-3G energy: -74.963 Ha
"""

import numpy as np
from aimd import aimd, write_xyz
from constants import BOHR_TO_ANG

if __name__ == "__main__":
    atoms = [
        ("O", [ 0.000,  0.000,  0.000]),
        ("H", [ 0.000,  0.757,  0.586]),
        ("H", [ 0.000, -0.757,  0.586]),
    ]
    masses      = np.array([15.999, 1.008, 1.008])
    n_electrons = 10  # O:8 + H:1 + H:1

    # Bending mode: H1 and H2 move in ±y (zero net momentum)
    v_bend   = 0.002  # Bohr/a.u.t
    init_vel = np.zeros((3, 3))
    init_vel[1] = [0.0,  v_bend, 0.0]
    init_vel[2] = [0.0, -v_bend, 0.0]

    traj, energies = aimd(atoms, masses, n_electrons, n_steps=10, dt_fs=0.5,
                          init_velocities=init_vel,
                          xyz_file="aimd_h2o_trajectory.xyz")

    print("\n--- Summary ---")
    print(f"{'Step':>5}  {'Energy (Ha)':>14}  {'O-H1 (A)':>10}  {'O-H2 (A)':>10}")
    for i, (pos, e) in enumerate(zip(traj, energies)):
        r1 = np.linalg.norm(pos[1] - pos[0]) * BOHR_TO_ANG
        r2 = np.linalg.norm(pos[2] - pos[0]) * BOHR_TO_ANG
        print(f"{i:>5}  {e:>14.6f}  {r1:>10.4f}  {r2:>10.4f}")
