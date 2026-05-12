"""
RHF SCF and finite-difference force computation.

Provides: build_overlap_kinetic, build_nuclear, build_eri_tensor,
          nuclear_repulsion, rhf_scf, compute_forces
"""

import numpy as np
from integrals import (contracted_integral, overlap_primitive,
                       kinetic_primitive, nuclear_primitive, eri_primitive)
from basis import build_basis
from constants import CHARGES


def build_overlap_kinetic(basis):
    n = len(basis)
    S, T = np.zeros((n,n)), np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            S[i,j] = contracted_integral(overlap_primitive, basis[i], basis[j])
            T[i,j] = contracted_integral(kinetic_primitive, basis[i], basis[j])
    return S, T


def build_nuclear(basis, atoms_bohr):
    n = len(basis)
    V = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            v = 0.0
            for sym, C in atoms_bohr:
                Z  = CHARGES[sym]
                Cv = np.array(C)
                v += contracted_integral(
                    lambda *args, _C=Cv, _Z=Z: nuclear_primitive(*args, _C, _Z),
                    basis[i], basis[j])
            V[i,j] = v
    return V


def build_eri_tensor(basis):
    n = len(basis)
    g = np.zeros((n,n,n,n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    g[i,j,k,l] = contracted_integral(
                        eri_primitive, basis[i], basis[j], basis[k], basis[l])
    return g


def nuclear_repulsion(atoms_bohr):
    n = len(atoms_bohr)
    e = 0.0
    for i in range(n):
        for j in range(i+1, n):
            zi = CHARGES[atoms_bohr[i][0]]
            zj = CHARGES[atoms_bohr[j][0]]
            r  = np.linalg.norm(np.array(atoms_bohr[i][1]) - np.array(atoms_bohr[j][1]))
            e += zi * zj / r
    return e


def rhf_scf(atoms_bohr, n_electrons, max_iter=100, tol=1e-8):
    basis   = build_basis(atoms_bohr)
    n_basis = len(basis)
    n_occ   = n_electrons // 2

    S, T  = build_overlap_kinetic(basis)
    V     = build_nuclear(basis, atoms_bohr)
    H     = T + V
    g     = build_eri_tensor(basis)
    e_nuc = nuclear_repulsion(atoms_bohr)

    eig, U = np.linalg.eigh(S)
    X = U @ np.diag(1.0 / np.sqrt(eig)) @ U.T

    D      = np.zeros((n_basis, n_basis))
    e_prev = 0.0

    for _ in range(max_iter):
        J = np.einsum("pqrs,rs->pq", g, D)
        K = np.einsum("prqs,rs->pq", g, D)
        F = H + J - 0.5*K

        Fp      = X.T @ F @ X
        eps, Cp = np.linalg.eigh(Fp)
        C       = X @ Cp

        D     = 2 * C[:, :n_occ] @ C[:, :n_occ].T
        e_new = 0.5 * np.sum(D * (H + F)) + e_nuc

        if abs(e_new - e_prev) < tol:
            return e_new
        e_prev = e_new

    return e_prev


def compute_forces(atoms_bohr, n_electrons, fd_step=0.005):
    symbols   = [a[0] for a in atoms_bohr]
    positions = np.array([a[1] for a in atoms_bohr], dtype=float)
    forces    = np.zeros_like(positions)
    for i in range(len(symbols)):
        for d in range(3):
            pf = positions.copy(); pf[i,d] += fd_step
            pb = positions.copy(); pb[i,d] -= fd_step
            ef = rhf_scf(list(zip(symbols, pf.tolist())), n_electrons)
            eb = rhf_scf(list(zip(symbols, pb.tolist())), n_electrons)
            forces[i,d] = -(ef - eb) / (2*fd_step)
    return forces
