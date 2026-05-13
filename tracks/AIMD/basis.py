# Copyright (c) 2026 ORIQX AG. MIT licensed.
"""
STO-3G basis set loader and basis function builder.

Reads parameters from sto3g.dat and constructs contracted Gaussian
basis functions for each atom in the molecule.
"""

import os
import numpy as np
from integrals import primitive_norm
from constants import CHARGES

_DAT_FILE = os.path.join(os.path.dirname(__file__), "sto-3g.dat")


def load_sto3g(path=_DAT_FILE):
    """Parse sto3g.dat → dict matching STO3G structure."""
    data = {}
    current_elem  = None
    current_shell = None
    current_prims = []

    def _flush():
        if current_elem is not None and current_shell is not None:
            data.setdefault(current_elem, []).append((current_shell, current_prims[:]))

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts[0].isalpha() and len(parts) == 2:
                _flush()
                current_elem  = parts[0]
                current_shell = parts[1]
                current_prims = []
            else:
                current_prims.append(tuple(float(x) for x in parts))

    _flush()
    return data


STO3G = load_sto3g()


def build_basis(atoms_bohr):
    """
    Build list of contracted basis functions from atom list.
    atoms_bohr: list of (symbol, [x, y, z]) in Bohr.
    """
    basis = []
    for sym, center in atoms_bohr:
        center = np.array(center, dtype=float)
        if sym not in STO3G:
            raise NotImplementedError(f"Element {sym} not in STO-3G table")
        for shell_type, prims in STO3G[sym]:
            exps = [p[0] for p in prims]
            if shell_type == "S":
                coeffs = [p[1] for p in prims]
                basis.append({"center": center, "angular": (0,0,0),
                               "exps": exps, "coeffs": coeffs,
                               "norms": [primitive_norm(a,0,0,0) for a in exps]})
            elif shell_type == "SP":
                cS = [p[1] for p in prims]
                cP = [p[2] for p in prims]
                basis.append({"center": center, "angular": (0,0,0),
                               "exps": exps, "coeffs": cS,
                               "norms": [primitive_norm(a,0,0,0) for a in exps]})
                for ang in [(1,0,0), (0,1,0), (0,0,1)]:
                    basis.append({"center": center, "angular": ang,
                                   "exps": exps, "coeffs": cP,
                                   "norms": [primitive_norm(a,*ang) for a in exps]})
    return basis
