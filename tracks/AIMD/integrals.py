"""
McMurchie-Davidson integral engine.

Provides: E, boys, R, overlap_primitive, kinetic_primitive,
          nuclear_primitive, eri_primitive, contracted_integral,
          primitive_norm
"""

import math
import numpy as np
from scipy.special import factorial2


def dfact(n):
    return factorial2(n) if n > 0 else 1


def primitive_norm(alpha, l, m, n):
    L = l + m + n
    num = (2 ** (2*L + 1.5)) * (alpha ** (L + 1.5))
    den = (math.pi ** 1.5) * dfact(2*l-1) * dfact(2*m-1) * dfact(2*n-1)
    return math.sqrt(num / den)


def E(i, j, t, Qx, a, b):
    """Hermite Gaussian expansion coefficient."""
    p = a + b
    q = a * b / p
    if t < 0 or t > i + j:
        return 0.0
    if i == j == t == 0:
        return math.exp(-q * Qx * Qx)
    if j == 0:
        return (1/(2*p) * E(i-1, j, t-1, Qx, a, b)
                - q*Qx/a * E(i-1, j, t,   Qx, a, b)
                + (t+1)  * E(i-1, j, t+1, Qx, a, b))
    return (1/(2*p) * E(i, j-1, t-1, Qx, a, b)
            + q*Qx/b * E(i, j-1, t,   Qx, a, b)
            + (t+1)  * E(i, j-1, t+1, Qx, a, b))


def boys(n, T):
    """Boys function F_n(T)."""
    if T < 1e-10:
        return 1.0 / (2*n + 1)
    F = 0.5 * math.sqrt(math.pi / T) * math.erf(math.sqrt(T))
    for m in range(n):
        F = ((2*m + 1)*F - math.exp(-T)) / (2*T)
    return F


def R(t, u, v, n, p, PCx, PCy, PCz, RPC):
    """Auxiliary Hermite Coulomb integral."""
    if t == u == v == 0:
        return (-2*p)**n * boys(n, p * RPC * RPC)
    val = 0.0
    if t > 0:
        val += ((t-1) * R(t-2, u, v, n+1, p, PCx, PCy, PCz, RPC)
                + PCx  * R(t-1, u, v, n+1, p, PCx, PCy, PCz, RPC))
    elif u > 0:
        val += ((u-1) * R(t, u-2, v, n+1, p, PCx, PCy, PCz, RPC)
                + PCy  * R(t, u-1, v, n+1, p, PCx, PCy, PCz, RPC))
    elif v > 0:
        val += ((v-1) * R(t, u, v-2, n+1, p, PCx, PCy, PCz, RPC)
                + PCz  * R(t, u, v-1, n+1, p, PCx, PCy, PCz, RPC))
    return val


def overlap_primitive(a, A, angA, b, B, angB):
    l1, m1, n1 = angA
    l2, m2, n2 = angB
    p = a + b
    Sx = math.sqrt(math.pi/p) * E(l1, l2, 0, A[0]-B[0], a, b)
    Sy = math.sqrt(math.pi/p) * E(m1, m2, 0, A[1]-B[1], a, b)
    Sz = math.sqrt(math.pi/p) * E(n1, n2, 0, A[2]-B[2], a, b)
    return Sx * Sy * Sz


def kinetic_primitive(a, A, angA, b, B, angB):
    l2, m2, n2 = angB
    term0 = b*(2*(l2+m2+n2)+3) * overlap_primitive(a, A, angA, b, B, angB)
    term1 = 0.0
    if l2 >= 2:
        term1 += -0.5*l2*(l2-1) * overlap_primitive(a, A, angA, b, B, (l2-2, m2,   n2  ))
    term1    += -2*b*b           * overlap_primitive(a, A, angA, b, B, (l2+2, m2,   n2  ))
    if m2 >= 2:
        term1 += -0.5*m2*(m2-1) * overlap_primitive(a, A, angA, b, B, (l2,   m2-2, n2  ))
    term1    += -2*b*b           * overlap_primitive(a, A, angA, b, B, (l2,   m2+2, n2  ))
    if n2 >= 2:
        term1 += -0.5*n2*(n2-1) * overlap_primitive(a, A, angA, b, B, (l2,   m2,   n2-2))
    term1    += -2*b*b           * overlap_primitive(a, A, angA, b, B, (l2,   m2,   n2+2))
    return term0 + term1


def nuclear_primitive(a, A, angA, b, B, angB, C, Z):
    l1, m1, n1 = angA
    l2, m2, n2 = angB
    p = a + b
    P = (a*A + b*B) / p
    RPC = np.linalg.norm(P - C)
    val = 0.0
    for t in range(l1+l2+1):
        for u in range(m1+m2+1):
            for v in range(n1+n2+1):
                val += (E(l1, l2, t, A[0]-B[0], a, b) *
                        E(m1, m2, u, A[1]-B[1], a, b) *
                        E(n1, n2, v, A[2]-B[2], a, b) *
                        R(t, u, v, 0, p, P[0]-C[0], P[1]-C[1], P[2]-C[2], RPC))
    return -2*math.pi/p * Z * val


def eri_primitive(a, A, angA, b, B, angB, c, C, angC, d, D, angD):
    l1, m1, n1 = angA; l2, m2, n2 = angB
    l3, m3, n3 = angC; l4, m4, n4 = angD
    p = a + b; q = c + d
    P = (a*A + b*B) / p
    Q = (c*C + d*D) / q
    RPQ = np.linalg.norm(P - Q)
    alpha = p * q / (p + q)
    val = 0.0
    for t in range(l1+l2+1):
        for u in range(m1+m2+1):
            for v in range(n1+n2+1):
                for tau in range(l3+l4+1):
                    for mu in range(m3+m4+1):
                        for nu in range(n3+n4+1):
                            val += (E(l1,l2,t,  A[0]-B[0],a,b) *
                                    E(m1,m2,u,  A[1]-B[1],a,b) *
                                    E(n1,n2,v,  A[2]-B[2],a,b) *
                                    E(l3,l4,tau,C[0]-D[0],c,d) *
                                    E(m3,m4,mu, C[1]-D[1],c,d) *
                                    E(n3,n4,nu, C[2]-D[2],c,d) *
                                    (-1)**(tau+mu+nu) *
                                    R(t+tau, u+mu, v+nu, 0, alpha,
                                      P[0]-Q[0], P[1]-Q[1], P[2]-Q[2], RPQ))
    return 2 * math.pi**2.5 / (p * q * math.sqrt(p+q)) * val


def contracted_integral(f, a, b, c=None, d=None):
    val = 0.0
    for ai, ci, ni in zip(a["exps"], a["coeffs"], a["norms"]):
        for aj, cj, nj in zip(b["exps"], b["coeffs"], b["norms"]):
            if c is None:
                val += ci*cj*ni*nj * f(ai, a["center"], a["angular"],
                                        aj, b["center"], b["angular"])
            else:
                for ak, ck, nk in zip(c["exps"], c["coeffs"], c["norms"]):
                    for al, cl, nl in zip(d["exps"], d["coeffs"], d["norms"]):
                        val += (ci*cj*ck*cl * ni*nj*nk*nl *
                                f(ai, a["center"], a["angular"],
                                  aj, b["center"], b["angular"],
                                  ak, c["center"], c["angular"],
                                  al, d["center"], d["angular"]))
    return val
