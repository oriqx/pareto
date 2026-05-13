# Copyright (c) 2026 ORIQX AG. MIT licensed.
"""
AIMD velocity Verlet integrator and trajectory utilities.

Provides: maxwell_boltzmann_velocities, aimd, write_xyz
"""

import numpy as np
from scf import rhf_scf, compute_forces
from constants import BOHR_TO_ANG, ANG_TO_BOHR, FS_TO_AUT, AMU_TO_AU, KB_AU


def maxwell_boltzmann_velocities(masses_amu, temperature_K, seed=None):
    """Maxwell-Boltzmann velocities at temperature T; zero net linear momentum."""
    rng       = np.random.default_rng(seed)
    masses_au = masses_amu * AMU_TO_AU
    sigma     = np.sqrt(KB_AU * temperature_K / masses_au)
    vel       = rng.normal(0.0, sigma[:, None], (len(masses_amu), 3))
    vel      -= vel.mean(axis=0)
    return vel


def aimd(atoms_ang, masses_amu, n_electrons, n_steps=5, dt_fs=0.5,
         init_velocities=None, temperature_K=None, seed=None, xyz_file=None):
    symbols   = [a[0] for a in atoms_ang]
    positions = np.array([a[1] for a in atoms_ang]) * ANG_TO_BOHR

    if temperature_K is not None:
        velocities = maxwell_boltzmann_velocities(masses_amu, temperature_K, seed=seed)
    elif init_velocities is not None:
        velocities = np.array(init_velocities, dtype=float)
    else:
        velocities = np.zeros_like(positions)

    inv_masses = (1.0 / (masses_amu * AMU_TO_AU))[:, None]
    dt         = dt_fs * FS_TO_AUT

    trajectory = [positions.copy()]
    energies   = []

    temp_tag = f" | T = {temperature_K} K" if temperature_K else ""
    print(f"AIMD | {' '.join(symbols)} | {n_steps} steps | dt = {dt_fs} fs{temp_tag}\n")

    xyz_f = open(xyz_file, "w") if xyz_file else None

    atoms_bohr = list(zip(symbols, positions.tolist()))
    forces     = compute_forces(atoms_bohr, n_electrons)
    e0         = rhf_scf(atoms_bohr, n_electrons)
    energies.append(e0)
    if xyz_f:
        _write_frame(xyz_f, symbols, positions, e0, 0)
    print(f"  step 0 | E = {e0:.6f} Ha")

    for step in range(1, n_steps + 1):
        positions_new = positions + velocities*dt + 0.5*forces*inv_masses*dt**2
        atoms_new     = list(zip(symbols, positions_new.tolist()))
        forces_new    = compute_forces(atoms_new, n_electrons)
        velocities    = velocities + 0.5*(forces + forces_new)*inv_masses*dt
        positions     = positions_new
        forces        = forces_new

        e = rhf_scf(atoms_new, n_electrons)
        energies.append(e)
        trajectory.append(positions.copy())
        if xyz_f:
            _write_frame(xyz_f, symbols, positions, e, step)

        print(f"  step {step} | E = {e:.6f} Ha", end="")
        if len(symbols) == 2:
            bond = np.linalg.norm(positions[1] - positions[0]) * BOHR_TO_ANG
            print(f" | bond = {bond:.4f} A")
        else:
            r1 = np.linalg.norm(positions[1] - positions[0]) * BOHR_TO_ANG
            r2 = np.linalg.norm(positions[2] - positions[0]) * BOHR_TO_ANG
            print(f" | O-H1 = {r1:.4f} A | O-H2 = {r2:.4f} A")

    if xyz_f:
        xyz_f.close()
        print(f"Trajectory written to {xyz_file}  ({len(trajectory)} frames)")

    return trajectory, energies


###################################################################################
################################  NO DECOMPOSE    #################################
###################################################################################

def _write_frame(f, symbols, pos, e, step):
    pos_ang = pos * BOHR_TO_ANG
    f.write(f"{len(symbols)}\n")
    f.write(f"step={step} E={e:.6f}Ha\n")
    for sym, r in zip(symbols, pos_ang):
        f.write(f"{sym}  {r[0]:12.6f}  {r[1]:12.6f}  {r[2]:12.6f}\n")
    f.flush()


def write_xyz(filename, symbols, trajectory, energies):
    with open(filename, "w") as f:
        for step, (pos, e) in enumerate(zip(trajectory, energies)):
            _write_frame(f, symbols, pos, e, step)
    print(f"Trajectory written to {filename}  ({len(trajectory)} frames)")
