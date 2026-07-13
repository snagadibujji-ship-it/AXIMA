#!/usr/bin/env python3
"""
PROMETHEUS Level 2 — Computational Beast
Linear Algebra, Multivariate Calculus, ODE Systems, Probability, Discrete Math

Built by: Ghias + Kiro
"""

import math
from typing import List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════
# 2.1 MATRIX ENGINE
# ═══════════════════════════════════════════════════════════════

class Matrix:
    """Full-featured matrix with all linear algebra operations."""

    def __init__(self, data: List[List[float]]):
        self.data = [list(row) for row in data]
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    @staticmethod
    def identity(n: int) -> 'Matrix':
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    @staticmethod
    def zeros(rows: int, cols: int) -> 'Matrix':
        return Matrix([[0]*cols for _ in range(rows)])

    def __repr__(self):
        lines = []
        for row in self.data:
            formatted = [f"{x:.4g}" if x != int(x) else str(int(x)) for x in row]
            lines.append('[' + ', '.join(f"{s:>8s}" for s in formatted) + ']')
        return '\n'.join(lines)

    def __getitem__(self, idx):
        return self.data[idx]

    def __eq__(self, other):
        if not isinstance(other, Matrix): return False
        return self.rows == other.rows and self.cols == other.cols and \
               all(abs(self[i][j]-other[i][j]) < 1e-10 for i in range(self.rows) for j in range(self.cols))

    # ─── ARITHMETIC ───

    def __add__(self, other: 'Matrix') -> 'Matrix':
        assert self.rows == other.rows and self.cols == other.cols
        return Matrix([[self[i][j] + other[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        assert self.rows == other.rows and self.cols == other.cols
        return Matrix([[self[i][j] - other[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix([[self[i][j] * other for j in range(self.cols)] for i in range(self.rows)])
        if isinstance(other, Matrix):
            assert self.cols == other.rows
            result = [[sum(self[i][k]*other[k][j] for k in range(self.cols)) for j in range(other.cols)] for i in range(self.rows)]
            return Matrix(result)
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def transpose(self) -> 'Matrix':
        return Matrix([[self[j][i] for j in range(self.rows)] for i in range(self.cols)])

    # ─── DETERMINANT (cofactor expansion + optimization) ───

    def det(self) -> float:
        """Compute determinant using LU decomposition for speed."""
        assert self.rows == self.cols, "Determinant only for square matrices"
        n = self.rows
        if n == 1: return self[0][0]
        if n == 2: return self[0][0]*self[1][1] - self[0][1]*self[1][0]
        if n == 3:
            return (self[0][0]*(self[1][1]*self[2][2]-self[1][2]*self[2][1])
                   -self[0][1]*(self[1][0]*self[2][2]-self[1][2]*self[2][0])
                   +self[0][2]*(self[1][0]*self[2][1]-self[1][1]*self[2][0]))
        # General: Gaussian elimination
        m = [row[:] for row in self.data]
        sign = 1
        for col in range(n):
            # Partial pivoting
            max_row = max(range(col, n), key=lambda r: abs(m[r][col]))
            if abs(m[max_row][col]) < 1e-12: return 0
            if max_row != col:
                m[col], m[max_row] = m[max_row], m[col]
                sign *= -1
            for row in range(col+1, n):
                factor = m[row][col] / m[col][col]
                for j in range(col, n):
                    m[row][j] -= factor * m[col][j]
        return sign * math.prod(m[i][i] for i in range(n))

    # ─── INVERSE (Gauss-Jordan elimination) ───

    def inverse(self) -> Optional['Matrix']:
        """Compute matrix inverse using Gauss-Jordan elimination."""
        assert self.rows == self.cols
        n = self.rows
        # Augment with identity
        aug = [self.data[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]

        for col in range(n):
            # Pivot
            max_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
            if abs(aug[max_row][col]) < 1e-12: return None  # Singular
            aug[col], aug[max_row] = aug[max_row], aug[col]

            # Scale pivot row
            pivot = aug[col][col]
            for j in range(2*n):
                aug[col][j] /= pivot

            # Eliminate column
            for row in range(n):
                if row == col: continue
                factor = aug[row][col]
                for j in range(2*n):
                    aug[row][j] -= factor * aug[col][j]

        return Matrix([row[n:] for row in aug])

    # ─── ROW ECHELON FORM (RREF) ───

    def rref(self) -> Tuple['Matrix', List[int]]:
        """Reduced Row Echelon Form. Returns (rref_matrix, pivot_columns)."""
        m = [row[:] for row in self.data]
        rows, cols = self.rows, self.cols
        pivots = []
        pivot_row = 0

        for col in range(cols):
            if pivot_row >= rows: break
            # Find pivot
            max_row = max(range(pivot_row, rows), key=lambda r: abs(m[r][col]))
            if abs(m[max_row][col]) < 1e-12: continue

            m[pivot_row], m[max_row] = m[max_row], m[pivot_row]
            pivot = m[pivot_row][col]
            for j in range(cols):
                m[pivot_row][j] /= pivot

            for row in range(rows):
                if row == pivot_row: continue
                factor = m[row][col]
                for j in range(cols):
                    m[row][j] -= factor * m[pivot_row][j]

            pivots.append(col)
            pivot_row += 1

        return Matrix(m), pivots

    # ─── RANK ───

    def rank(self) -> int:
        _, pivots = self.rref()
        return len(pivots)

    # ─── EIGENVALUES (characteristic polynomial → solve) ───

    def eigenvalues(self) -> List[complex]:
        """Compute eigenvalues by solving det(A - λI) = 0."""
        assert self.rows == self.cols
        n = self.rows

        if n == 1:
            return [self[0][0]]

        if n == 2:
            # λ² - trace*λ + det = 0
            tr = self[0][0] + self[1][1]
            d = self.det()
            disc = tr*tr - 4*d
            if disc >= 0:
                return [round((tr + math.sqrt(disc))/2, 10), round((tr - math.sqrt(disc))/2, 10)]
            else:
                real = tr/2
                imag = math.sqrt(-disc)/2
                return [complex(real, imag), complex(real, -imag)]

        if n == 3:
            # Use QR iteration (simplified power iteration for dominant eigenvalue)
            return self._qr_eigenvalues()

        # General: QR algorithm
        return self._qr_eigenvalues()

    def _qr_eigenvalues(self) -> List[float]:
        """QR iteration for eigenvalues (works for any size)."""
        n = self.rows
        m = [row[:] for row in self.data]

        # QR iteration (30 steps usually enough)
        for _ in range(50):
            q, r = self._qr_decompose(m)
            # A_new = R * Q
            m = [[sum(r[i][k]*q[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

        # Eigenvalues are on the diagonal (approximately)
        eigenvals = [round(m[i][i], 8) for i in range(n)]
        return sorted(eigenvals, reverse=True)

    def _qr_decompose(self, m) -> Tuple[List[List[float]], List[List[float]]]:
        """QR decomposition using Gram-Schmidt."""
        n = len(m)
        q = [[0.0]*n for _ in range(n)]
        r = [[0.0]*n for _ in range(n)]

        for j in range(n):
            # v = column j of A
            v = [m[i][j] for i in range(n)]

            for i in range(j):
                # r[i][j] = q_i · v
                r[i][j] = sum(q[k][i]*v[k] for k in range(n))
                # v = v - r[i][j] * q_i
                for k in range(n):
                    v[k] -= r[i][j] * q[k][i]

            # r[j][j] = ||v||
            r[j][j] = math.sqrt(sum(x*x for x in v))
            if r[j][j] > 1e-12:
                for k in range(n):
                    q[k][j] = v[k] / r[j][j]

        return q, r

    # ─── SOLVE Ax = b ───

    def solve(self, b: List[float]) -> Optional[List[float]]:
        """Solve Ax = b using Gaussian elimination with back-substitution."""
        assert self.rows == self.cols and len(b) == self.rows
        n = self.rows

        # Augmented matrix [A|b]
        aug = [self.data[i][:] + [b[i]] for i in range(n)]

        # Forward elimination
        for col in range(n):
            max_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
            if abs(aug[max_row][col]) < 1e-12: return None
            aug[col], aug[max_row] = aug[max_row], aug[col]

            for row in range(col+1, n):
                factor = aug[row][col] / aug[col][col]
                for j in range(n+1):
                    aug[row][j] -= factor * aug[col][j]

        # Back substitution
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = (aug[i][n] - sum(aug[i][j]*x[j] for j in range(i+1, n))) / aug[i][i]

        return [round(v, 10) for v in x]

    # ─── TRACE ───

    def trace(self) -> float:
        assert self.rows == self.cols
        return sum(self[i][i] for i in range(self.rows))

    # ─── LU DECOMPOSITION ───

    def lu(self) -> Tuple['Matrix', 'Matrix']:
        """LU decomposition: A = LU."""
        assert self.rows == self.cols
        n = self.rows
        L = [[0.0]*n for _ in range(n)]
        U = [row[:] for row in self.data]

        for i in range(n):
            L[i][i] = 1.0
            for j in range(i+1, n):
                if abs(U[i][i]) < 1e-12: continue
                factor = U[j][i] / U[i][i]
                L[j][i] = factor
                for k in range(i, n):
                    U[j][k] -= factor * U[i][k]

        return Matrix(L), Matrix(U)

    # ─── POWER ───

    def power(self, n: int) -> 'Matrix':
        """Compute A^n using repeated squaring."""
        if n == 0: return Matrix.identity(self.rows)
        if n == 1: return Matrix(self.data)
        if n % 2 == 0:
            half = self.power(n // 2)
            return half * half
        return self * self.power(n - 1)


# ═══════════════════════════════════════════════════════════════
# 2.2 VECTOR CALCULUS
# Partial derivatives, gradient, Hessian, Lagrange multipliers
# ═══════════════════════════════════════════════════════════════

class VectorCalculus:
    """Multivariate calculus operations."""

    def gradient(self, f_expr: str, variables: List[str]) -> List[str]:
        """Compute gradient ∇f = (∂f/∂x₁, ∂f/∂x₂, ...)."""
        from prometheus import Prometheus
        engine = Prometheus()
        grad = []
        for var in variables:
            result = engine.process(f"differentiate {f_expr}")
            # Partial derivative: treat other vars as constants
            # Use the calculus engine with specific variable
            from prometheus import Tokenizer, Parser, Calculus, PrettyPrinter, Simplifier
            tok = Tokenizer()
            par = Parser()
            calc = Calculus()
            simp = Simplifier()
            pp = PrettyPrinter()
            tokens = tok.tokenize(f_expr)
            ast = par.parse(tokens)
            deriv = calc.differentiate(ast, var)
            deriv = simp.simplify(deriv)
            grad.append(pp.to_string(deriv))
        return grad

    def hessian(self, f_expr: str, variables: List[str]) -> List[List[str]]:
        """Compute Hessian matrix H[i][j] = ∂²f/∂xᵢ∂xⱼ."""
        from prometheus import Tokenizer, Parser, Calculus, PrettyPrinter, Simplifier
        tok = Tokenizer()
        par = Parser()
        calc = Calculus()
        simp = Simplifier()
        pp = PrettyPrinter()

        tokens = tok.tokenize(f_expr)
        ast = par.parse(tokens)
        n = len(variables)
        H = []
        for i in range(n):
            row = []
            # First partial
            d1 = calc.differentiate(ast, variables[i])
            d1 = simp.simplify(d1)
            for j in range(n):
                # Second partial
                d2 = calc.differentiate(d1, variables[j])
                d2 = simp.simplify(d2)
                row.append(pp.to_string(d2))
            H.append(row)
        return H

    def divergence(self, F: List[str], variables: List[str]) -> str:
        """Compute divergence: div(F) = ∂F₁/∂x₁ + ∂F₂/∂x₂ + ..."""
        from prometheus import Tokenizer, Parser, Calculus, PrettyPrinter, Simplifier
        tok, par, calc, simp, pp = Tokenizer(), Parser(), Calculus(), Simplifier(), PrettyPrinter()

        parts = []
        for f_comp, var in zip(F, variables):
            tokens = tok.tokenize(f_comp)
            ast = par.parse(tokens)
            d = calc.differentiate(ast, var)
            d = simp.simplify(d)
            parts.append(pp.to_string(d))
        return ' + '.join(parts)

    def curl(self, F: List[str], variables: List[str] = ['x','y','z']) -> List[str]:
        """Compute curl of 3D vector field: curl(F) = ∇ × F."""
        assert len(F) == 3 and len(variables) == 3
        from prometheus import Tokenizer, Parser, Calculus, PrettyPrinter, Simplifier
        tok, par, calc, simp, pp = Tokenizer(), Parser(), Calculus(), Simplifier(), PrettyPrinter()

        def pd(expr_str, var):
            tokens = tok.tokenize(expr_str)
            ast = par.parse(tokens)
            d = calc.differentiate(ast, var)
            return pp.to_string(simp.simplify(d))

        x, y, z = variables
        Fx, Fy, Fz = F
        # curl = (∂Fz/∂y - ∂Fy/∂z, ∂Fx/∂z - ∂Fz/∂x, ∂Fy/∂x - ∂Fx/∂y)
        return [
            f"{pd(Fz, y)} - {pd(Fy, z)}",
            f"{pd(Fx, z)} - {pd(Fz, x)}",
            f"{pd(Fy, x)} - {pd(Fx, y)}",
        ]


# ═══════════════════════════════════════════════════════════════
# 2.3 ODE SYSTEMS (2nd order, constant coefficient)
# ═══════════════════════════════════════════════════════════════

class ODESystem:
    """Solve 2nd order constant coefficient ODEs and systems."""

    def solve_2nd_order(self, a: float, b: float, c: float, rhs: str = '0') -> str:
        """Solve ay'' + by' + cy = rhs.
        Returns general solution as string."""
        steps = []
        steps.append(f"ODE: {a}y'' + {b}y' + {c}y = {rhs}")
        steps.append("")

        # Homogeneous solution: characteristic equation ar² + br + c = 0
        steps.append("Characteristic equation: " + f"{a}r² + {b}r + {c} = 0")
        disc = b*b - 4*a*c

        if disc > 0:
            r1 = (-b + math.sqrt(disc)) / (2*a)
            r2 = (-b - math.sqrt(disc)) / (2*a)
            steps.append(f"Roots: r₁ = {r1:.4g}, r₂ = {r2:.4g} (real distinct)")
            yh = f"C₁·e^({r1:.4g}t) + C₂·e^({r2:.4g}t)"
        elif disc == 0:
            r = -b / (2*a)
            steps.append(f"Root: r = {r:.4g} (repeated)")
            yh = f"(C₁ + C₂·t)·e^({r:.4g}t)"
        else:
            alpha = -b / (2*a)
            beta = math.sqrt(-disc) / (2*a)
            steps.append(f"Roots: r = {alpha:.4g} ± {beta:.4g}i (complex)")
            yh = f"e^({alpha:.4g}t)[C₁·cos({beta:.4g}t) + C₂·sin({beta:.4g}t)]"

        steps.append(f"Homogeneous solution: y_h = {yh}")

        if rhs == '0':
            steps.append(f"\nGeneral solution: y = {yh}")
        else:
            steps.append(f"\nFor particular solution, use undetermined coefficients or variation of parameters.")
            steps.append(f"General solution: y = y_h + y_p = {yh} + y_p")

        return '\n'.join(steps)

    def solve_system_2x2(self, A: 'Matrix') -> str:
        """Solve X' = AX for 2x2 system."""
        steps = []
        steps.append("System: X' = AX")
        steps.append(f"A =\n{A}")
        steps.append("")

        eigenvals = A.eigenvalues()
        steps.append(f"Eigenvalues: λ₁ = {eigenvals[0]:.4g}, λ₂ = {eigenvals[1]:.4g}")

        if all(isinstance(e, float) for e in eigenvals):
            if eigenvals[0] != eigenvals[1]:
                steps.append(f"\nGeneral solution:")
                steps.append(f"  X(t) = C₁·v₁·e^({eigenvals[0]:.4g}t) + C₂·v₂·e^({eigenvals[1]:.4g}t)")
                steps.append(f"  where v₁, v₂ are eigenvectors")
                # Classify equilibrium
                if eigenvals[0] < 0 and eigenvals[1] < 0:
                    steps.append(f"\n  Equilibrium: STABLE NODE (both λ < 0)")
                elif eigenvals[0] > 0 and eigenvals[1] > 0:
                    steps.append(f"\n  Equilibrium: UNSTABLE NODE (both λ > 0)")
                else:
                    steps.append(f"\n  Equilibrium: SADDLE POINT (opposite signs)")
        else:
            alpha = eigenvals[0].real
            beta = abs(eigenvals[0].imag)
            steps.append(f"\nComplex eigenvalues: {alpha:.4g} ± {beta:.4g}i")
            if alpha < 0:
                steps.append(f"  Equilibrium: STABLE SPIRAL")
            elif alpha > 0:
                steps.append(f"  Equilibrium: UNSTABLE SPIRAL")
            else:
                steps.append(f"  Equilibrium: CENTER (periodic)")
            steps.append(f"\n  X(t) = e^({alpha:.4g}t)[C₁·cos({beta:.4g}t)·v_r + C₂·sin({beta:.4g}t)·v_i]")

        return '\n'.join(steps)


# ═══════════════════════════════════════════════════════════════
# 2.4 PROBABILITY ENGINE
# ═══════════════════════════════════════════════════════════════

class Probability:
    """Probability distributions, Bayes, expected value."""

    # ─── DISTRIBUTIONS ───

    def normal_pdf(self, x: float, mu: float = 0, sigma: float = 1) -> float:
        return (1/(sigma*math.sqrt(2*math.pi))) * math.exp(-0.5*((x-mu)/sigma)**2)

    def binomial(self, n: int, k: int, p: float) -> float:
        """P(X=k) for Binomial(n,p)."""
        comb = math.factorial(n) // (math.factorial(k) * math.factorial(n-k))
        return comb * (p**k) * ((1-p)**(n-k))

    def poisson(self, k: int, lam: float) -> float:
        """P(X=k) for Poisson(λ)."""
        return (lam**k * math.exp(-lam)) / math.factorial(k)

    def exponential_pdf(self, x: float, lam: float) -> float:
        return lam * math.exp(-lam * x) if x >= 0 else 0

    # ─── BAYES' THEOREM ───

    def bayes(self, prior: float, likelihood: float, evidence: float) -> float:
        """P(A|B) = P(B|A) * P(A) / P(B)."""
        return (likelihood * prior) / evidence

    # ─── EXPECTED VALUE & VARIANCE ───

    def expected_value(self, values: List[float], probs: List[float]) -> float:
        """E[X] = Σ xᵢ·P(xᵢ)."""
        return sum(x*p for x, p in zip(values, probs))

    def variance(self, values: List[float], probs: List[float]) -> float:
        """Var(X) = E[X²] - (E[X])²."""
        ex = self.expected_value(values, probs)
        ex2 = sum(x*x*p for x, p in zip(values, probs))
        return ex2 - ex*ex

    def std_dev(self, values: List[float], probs: List[float]) -> float:
        return math.sqrt(self.variance(values, probs))

    # ─── COMBINATORICS ───

    def combinations(self, n: int, r: int) -> int:
        return math.factorial(n) // (math.factorial(r) * math.factorial(n-r))

    def permutations(self, n: int, r: int) -> int:
        return math.factorial(n) // math.factorial(n-r)

    # ─── HYPOTHESIS TESTING ───

    def z_score(self, x: float, mu: float, sigma: float) -> float:
        return (x - mu) / sigma

    def confidence_interval(self, mean: float, std: float, n: int, z: float = 1.96) -> Tuple[float, float]:
        """95% CI by default (z=1.96)."""
        margin = z * std / math.sqrt(n)
        return (mean - margin, mean + margin)


# ═══════════════════════════════════════════════════════════════
# 2.5 DISCRETE MATH & NUMBER THEORY (Extended)
# ═══════════════════════════════════════════════════════════════

class DiscreteMath:
    """Extended number theory and discrete mathematics."""

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """Extended Euclidean: returns (gcd, x, y) where ax + by = gcd."""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1

    def chinese_remainder(self, remainders: List[int], moduli: List[int]) -> int:
        """Chinese Remainder Theorem: solve system of congruences."""
        M = 1
        for m in moduli:
            M *= m

        result = 0
        for r, m in zip(remainders, moduli):
            Mi = M // m
            _, yi, _ = self.extended_gcd(Mi, m)
            result += r * Mi * yi

        return result % M

    def mod_pow(self, base: int, exp: int, mod: int) -> int:
        """Fast modular exponentiation: base^exp mod mod."""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp >>= 1
            base = (base * base) % mod
        return result

    def euler_totient(self, n: int) -> int:
        """Compute Euler's totient φ(n)."""
        result = n
        p = 2
        temp = n
        while p * p <= temp:
            if temp % p == 0:
                while temp % p == 0:
                    temp //= p
                result -= result // p
            p += 1
        if temp > 1:
            result -= result // temp
        return result

    def is_primitive_root(self, g: int, p: int) -> bool:
        """Check if g is a primitive root mod p."""
        if math.gcd(g, p) != 1:
            return False
        phi = self.euler_totient(p)
        # Check: g^(phi/q) ≠ 1 mod p for all prime factors q of phi
        temp = phi
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                if self.mod_pow(g, phi // d, p) == 1:
                    return False
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            if self.mod_pow(g, phi // temp, p) == 1:
                return False
        return True

    def solve_recurrence(self, coeffs: List[float], initial: List[float], n: int) -> float:
        """Solve linear recurrence: aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ + ...
        coeffs: [c₁, c₂, ...], initial: [a₀, a₁, ...]"""
        order = len(coeffs)
        seq = list(initial)
        while len(seq) <= n:
            next_val = sum(coeffs[i] * seq[-(i+1)] for i in range(order))
            seq.append(next_val)
        return seq[n]

    def solve_recurrence_closed(self, coeffs: List[float]) -> str:
        """Find closed form of linear recurrence via characteristic equation."""
        # For aₙ = c₁aₙ₋₁ + c₂aₙ₋₂: characteristic eq r² - c₁r - c₂ = 0
        if len(coeffs) == 2:
            c1, c2 = coeffs
            # r² - c1*r - c2 = 0
            disc = c1*c1 + 4*c2
            if disc > 0:
                r1 = (c1 + math.sqrt(disc)) / 2
                r2 = (c1 - math.sqrt(disc)) / 2
                return f"a(n) = A·({r1:.4g})^n + B·({r2:.4g})^n"
            elif disc == 0:
                r = c1 / 2
                return f"a(n) = (A + B·n)·({r:.4g})^n"
            else:
                alpha = c1 / 2
                beta = math.sqrt(-disc) / 2
                return f"a(n) = ({alpha:.4g})^n·[A·cos({beta:.4g}·n) + B·sin({beta:.4g}·n)]"
        return "Use matrix method for higher order recurrences"
