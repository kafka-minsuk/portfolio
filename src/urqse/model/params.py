"""Structural parameters (spec §7, decisions in §12)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    alpha: float = 0.75  # goods share; housing share 1-alpha = 0.25. source=spec §7 (CEX/ACS)
    beta: float = 0.80  # non-farm labour share. source=spec §7 (ARSW 2015)
    lam: float = 6.8  # Frechet shape over (workplace, sector). source=spec §7 (ARSW)
    kappa_lam: float = 0.08  # commuting semi-elasticity per minute. source=spec §7  # VERIFY for the state
    mu: float = 0.5  # floor-space supply elasticity. source=spec §7 (Baum-Snow & Han 2024)
    theta_T: float = 0.40  # land share of farm value added net of K, X. source=spec §7
    lam_R: float = 3.0  # long-run residence elasticity. source=spec §7
    # Residence elasticity inside a metro nest relative to lam_R (spec §3.12); >= 1 for a nested
    # Frechet choice, 1 = the flat choice over counties and tracts.  # VERIFY: no estimate yet
    lam_M_over_R: float = 1.0
    nu: float = 2.0  # dynamic-logit dispersion; 1/nu is the migration elasticity. source=spec §7
    eta: float = 0.0  # semi-closure; 0 = closed region. source=spec §12 decision 2
    price_rent_ratio: float = 36.0  # farmland price / cash rent. source=spec §3.10 (U.S. cropland 2025)
    epsilon: float = 0.10  # consolidation target: land per farm worker >= (1+epsilon) x baseline. source=spec §12.1
    varsigma: float = 0.5  # share of landlord income paid to residents of the same county. source=none  # VERIFY
    land_income_in_choice: bool = False  # source=spec §12.1 (portability)
    # Migration cost tau = tau0 + tau1 ln(distance km), tau_ii = 0 (spec §7 gives the form, not values).
    # tau1 = nu makes the distance elasticity of gross flows equal to 1; tau0 is set so the synthetic
    # state's baseline gross county-to-county move rate is about 4% per period.
    tau0: float = 4.0  # source=placeholder until PPML on IRS SOI flows (M2)  # VERIFY
    tau1: float = 2.0  # source=placeholder until PPML on IRS SOI flows (M2)  # VERIFY
    phi: float = 0.2  # partial adjustment of the regional total toward (S) on the path (§3.8); only used when eta > 0  # VERIFY
    a_TH: float = 0.371  # gross-output land + labour share a_T + a_H (0.151 + 0.22). source=spec §1.2 R2 (Suh & Moss 2021)
    ss_tol: float = 1e-5  # path steady state: max |d ln N| per period below this

    def __post_init__(self):
        checks = {
            "lam > 1 (spec U5)": self.lam > 1.0,
            "0 < alpha < 1": 0.0 < self.alpha < 1.0,
            "0 < beta < 1": 0.0 < self.beta < 1.0,
            "0 < theta_T < 1": 0.0 < self.theta_T < 1.0,
            "lam_R > 0": self.lam_R > 0.0,
            "lam_M_over_R >= 1 (nested residence choice, spec §3.12)": self.lam_M_over_R >= 1.0,
            "mu >= 0": self.mu >= 0.0,
            "kappa_lam >= 0": self.kappa_lam >= 0.0,
            "nu > 0": self.nu > 0.0,
            "eta >= 0": self.eta >= 0.0,
            "price_rent_ratio > 0": self.price_rent_ratio > 0.0,
            "epsilon >= 0": self.epsilon >= 0.0,
            "0 <= varsigma <= 1": 0.0 <= self.varsigma <= 1.0,
            "0 < phi <= 1": 0.0 < self.phi <= 1.0,
            "0 < a_TH <= 1": 0.0 < self.a_TH <= 1.0,
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            raise ValueError("invalid parameters: " + ", ".join(failed))

    @property
    def lam_M(self) -> float:
        """Residence elasticity between tracts of a metro nest (spec §3.12)."""
        return self.lam_M_over_R * self.lam_R

    @property
    def theta_H(self) -> float:
        return 1.0 - self.theta_T

    @property
    def k_com(self) -> float:
        """Commercial floor spending per unit of the non-farm wage bill, (1-beta)/beta."""
        return (1.0 - self.beta) / self.beta

    @property
    def discount(self) -> float:
        """q = (1+g)/(1+i), pinned by the price/rent ratio: P/rho = q/(1-q) (spec §3.10)."""
        return self.price_rent_ratio / (1.0 + self.price_rent_ratio)
