# URQSE — A Semi-Closed Urban–Rural Quantitative Spatial Equilibrium

**Implementation spec for a testable web app** · v1.0 · November 2026

Built from: *Model_ver3.docx* (the proposal), Ravallion, Chen & Sangraula (2007, WB WPS 4199), Suh & Moss (2021, *Agriculture* 11:54), and the attached `solver.py` / `stacktime.py`. A reference implementation accompanies this file (`urqse.py`, `test_urqse.py`, 9 tests passing). Every equation in §3–§5 is implemented there, and the numbers in §4 come from it.

---

## 0. Summary

| Question | Answer |
|---|---|
| Is the urban block sound? | Mostly. It is the Ahlfeldt–Redding–Sturm–Wolf (ARSW 2015) structure. It has four fixable errors (wage normalisation, mixed indices in the "solve B" step, a missing closed form for rents, an under-identified unknown set). See §1.1. |
| Is the rural block sound? | No, not as written. (i) The migration condition $E[U_R]=E[U_C]$ implicitly makes the urban–rural margin **fully open**, which is the opposite of the semi-closed goal. (ii) The proposed land elasticity 2.479 from Suh & Moss is a **crop-reallocation** elasticity, not a production-function exponent. (iii) In data-rich countries most rural workers are not farmers. See §1.2. |
| The fix | Treat every county as a location with **two job types** (non-farm, farm) inside **one** Fréchet choice. Residence moves through a second, slower margin. Total population is **semi-closed** with a single parameter $\eta$ ($\eta=0$ closed, $\eta\to\infty$ open). |
| "Until rural people have enough for extra land" | **Consolidation** stopping rule: stop when farmland per farm worker reaches a target. No domestic inflow ($\eta=0$); exogenous international immigration; owner-operator land tenure. §3.9, §12 |
| Asset prices | Farmland and urban land are priced as the PV of model-generated rent paths. There is an optional Capozza–Helsley conversion option at the urban fringe. §3.10 |
| Solver | Don't use Newton on the nested problem, and don't port your general solver. Use a **vectorised fixed point in logs with Anderson acceleration**: 12 outer iterations against 256 with plain damping on the test economy. Fall back to JAX + Newton–Krylov. Use **exact hat algebra** for counterfactuals. Your solvers are well engineered for macro frameworks but have the wrong granularity here. §6 |
| Front end | Streamlit is fine for v1 **if** the solver is a separate pure package and all satellite processing is offline. For animated multi-period maps at scale, move to Dash or FastAPI + MapLibre/deck.gl. §8 |

---

## 1. Critical evaluation of *Model_ver3*

### 1.1 Urban block (ARSW-type)

| # | Issue in the proposal | Why it matters | Fix (in this spec) |
|---|---|---|---|
| U1 | Labour-market clearing $H_j=\sum_i \pi_{ij\mid i}N_i$ is homogeneous of degree 0 in $w$. | $w$ is identified **only up to scale**, so a solver will drift or report a singular Jacobian. | Normalise: geometric mean of non-farm $w$ = 1, then rescale to observed mean earnings (§5 step 1). |
| U2 | The "solve productivity endowments" equation mixes $i$ and $j$ and substitutes the rent FOC into itself. | It is not a well-defined equation. | Use the Cobb-Douglas cost shares. Commercial floor demand is $\frac{1-\beta}{\beta}\frac{w_jH_j}{r_j}$, so **rents have a closed form** given wages (eq. R). $B_j$ then follows from zero profit. No root-finding is needed. |
| U3 | The unknown set $\{A,B,\underline{L},w,r\}$ is listed with data $\{N,H,L,t\}$ but the order is not exploited. | It invites a joint Newton solve on $5Z$ unknowns. | Only $w$ needs iteration (a contraction). Everything else is recursive and closed form (§5). |
| U4 | The developer section is struck through but $L=\underline{L} r^{\mu}$ is kept. | Fine, but $\mu$ is unparameterised. | Use $\mu\approx0.5$ for floor space (Baum-Snow & Han 2024, U.S. tract average), with exurban/rural tracts higher (§7). |
| U5 | The Fréchet logsum $\Gamma(1-1/\lambda)\Phi^{1/\lambda}$ is correct but needs $\lambda>1$. | — | Assert $\lambda>1$ in code. |
| U6 | No agglomeration or amenity spillovers. | Without them the equilibrium is unique and well behaved. With them, multiple equilibria are possible. | Optional $\gamma_B$ with a uniqueness check (Allen, Arkolakis & Li 2024). Default off. |
| U7 | Land rents go nowhere (implicitly to absentee landlords). | Welfare and asset-price results depend on who owns land. | Make ownership explicit: absentee (default), local per-capita rebate, or a national fund. |

### 1.2 Rural block and migration

| # | Issue | Why it matters | Fix |
|---|---|---|---|
| R1 | Migration stops when $E[U_R]=E[U_C]$ with representative agents. | This is an **infinitely elastic** urban–rural margin, i.e. fully open, which contradicts the semi-closed aim. It also forces $A_R>A_C$ to rationalise low rural wages, which the note itself flags as at odds with the literature. | Put residence on a **Fréchet choice** with finite elasticity $\lambda_R$. Only the *marginal* mover is indifferent; average utilities can differ permanently (the Lagakos-type persistent gap). |
| R2 | $\beta_R$ set from Suh & Moss "1% land → 2% crop output". | Their Table 5 gives **crop** supply elasticity to land of 2.479 in a differential supply system where livestock supply falls by 1.151 at the same time. It measures land being reallocated *between outputs*, not the technology. A Cobb-Douglas exponent above 1 also breaks CRS and the closed form. Share-weighting their own Table 5 gives an aggregate output elasticity well below 1. | Calibrate from **cost shares**. In the same paper's data (USDA-ERS, 1948–2011), the land share rose from 13.7% to 15.1% and labour fell from 67% to 22%. Net of capital and intermediates, $\theta_T=0.151/(0.151+0.22)\approx0.41$. Then over-identify it county by county with NASS cash rents (§5 step 5). |
| R3 | $w_R=B_R(\text{Land}/N_R)^{\beta_R}$ treats every rural resident as a farmer. | In the U.S. and other data-rich countries farm jobs are a small minority of rural employment, so the "rural wage = farm MPL" mapping fails. | Two job types in every county. Rural residents mostly hold **non-farm** jobs. The farm block governs land use and land rents. |
| R4 | "$B=$ Output index / Input index" and "$B=d\text{Output}/d\text{Input}$". | The USDA TFP series is a **growth index**, not a level. A derivative is a marginal product, not TFP. | Use the ERS index for **growth** of $\tilde A$ in scenarios. Recover the **level** $\tilde A_j$ by inversion so the model matches observed farm jobs, wages and land (§5 step 6). |
| R5 | $Y=B_RK^{\alpha}L^{\beta}H^{\gamma}$ with "sum equal to 0". | Typo for CRS ($\alpha+\beta+\gamma=1$). It also re-uses $\alpha,\beta$, which already mean goods share and urban labour share. | Rename to $(a_K,a_X,a_T,a_H)$ and optimise $K$ and intermediates $X$ out (eq. F). |
| R6 | $r_R$ guessed as $0.7\times$ urban. | Arbitrary. Ravallion et al. find urban poverty lines about 30% above rural on average, an implied rural/urban cost-of-living ratio near 0.77, but that is for developing countries. | Make rural floor rents **endogenous**, the same as urban (eq. R). Validate against BEA Regional Price Parities. |
| R7 | The paper design compares LAC and SSA. | This conflicts with "data-rich countries" and with what satellite + county data can support. | Treat LAC/SSA as a later extension. Build on U.S. states (or EU NUTS-3, Korea 시군구) first. |
| R8 | "Same intervention" problem (a transport cut ≠ the same welfare change). | Real, and solvable. | Normalise by the **partial-equilibrium welfare shock** $s$ (the change in the logsum holding population fixed) and report the *migration response per unit of $s$*. §4 gives it in closed form and shows exactly which parameters make it differ across countries. |

### 1.3 What the attached papers can and can't do

- **Suh & Moss (2021).** Useful for **input cost shares** (land ≈ 15%, labour ≈ 22%, intermediates ≈ 62% by 2011) and for the qualitative point that land expansion shifts output toward crops. Not usable as a production-function exponent (R2). Their sample is the U.S. aggregate, which is good for a U.S. application.
- **Ravallion, Chen & Sangraula (2007).** Useful for the **urban–rural cost-of-living gap** (about 1.3× urban/rural on average) as a prior for non-U.S. cases, and for validation moments on poverty urbanisation. It is about developing countries using 1993–2002 data, so for data-rich countries use local price indices (BEA RPP).

---

## 2. Scope and design principles

1. **Unit of analysis:** counties within one state (or region). U.S. states have roughly 3–254 counties. The dense $Z\times Z$ engine runs at **0.35 s for 100 locations, 6.9 s for 400** (static solve with semi-closure, reference code). An optional sub-county grid is supported via a sparse commuting cutoff (§6.4).
2. **Satellite data enter as measurement of states**, not as live inputs. Population, built volume, cropland and suitability are preprocessed into county tables offline (§8).
3. **Long run vs. path:** a static equilibrium (where things end up) and a dynamic path (how fast and in what order). The path stops when a user-defined rural land–labour condition is met.
4. **Semi-closed:** the region's total population responds to its welfare with elasticity $\eta$. Inside the region, residence responds with $\lambda_R$ (long run) or flow parameters $(\nu,\tau)$ (path).
5. **Every block is closed form except two fixed points** (wages/rents given residents; residents given utilities).

---

## 3. The model

### 3.1 Notation

| Symbol | Meaning |
|---|---|
| $n,i,j\in\{1..Z\}$ | locations (counties); $i$ = residence, $j$ = workplace |
| $s\in\{U,A\}$ | job type: non-farm ($U$), farm ($A$) |
| $N_i$ | resident workers; $\bar N=\sum_i N_i$ |
| $H_{js}$ | jobs at $j$ in sector $s$ |
| $t_{ij}$ | travel time (minutes) |
| $L_n$ | floor space; $r_n$ floor rent |
| $T^F_n$ | farmland in use; $\bar T^F_n$ suitable farmland frontier; $\rho_n$ farmland rent |
| $A_n$ | residential amenity; $b_n$ non-farm productivity; $\tilde A_n$ farm productivity (net of $K,X$) |
| $\xi_{An}$ | farm-job wedge: non-pecuniary value, selection, and the "agricultural productivity gap" |

### 3.2 Preferences and within-period choice

A worker living in $i$ draws Fréchet($\lambda$) shocks over $(j,s)$:

$$
U_{ijs\omega}=\frac{A_i\, w_{js}\,\xi_{s j}\, e^{-\kappa t_{ij}}}{r_i^{\,1-\alpha}}\;\varepsilon_{ijs\omega},\qquad \xi_{Uj}\equiv1 .
$$

Conditional choice probabilities and supply to each job:

$$
\pi_{js\mid i}=\frac{\left(w_{js}\xi_{sj}e^{-\kappa t_{ij}}\right)^{\lambda}}{\Phi_i},\quad
\Phi_i=\sum_{j,s}\left(w_{js}\xi_{sj}e^{-\kappa t_{ij}}\right)^{\lambda},\quad
H_{js}=\sum_i \pi_{js\mid i}N_i .
\tag{L}
$$

Expected income of a resident of $i$ is $\bar y_i=\sum_{j,s}\pi_{js\mid i}w_{js}$. It uses the *paid* wage, not the wedge-adjusted one. Expected utility is

$$
u_i=\Gamma\!\left(1-\tfrac1\lambda\right)\frac{A_i}{r_i^{1-\alpha}}\,\Phi_i^{1/\lambda}.
$$

> **Why one Fréchet over $(j,s)$:** it nests the urban commuting model and gives a smooth, finite-elasticity farm/non-farm margin. Observed farm earnings then identify the wedge $\xi_A$ separately from rural amenities $A$, which resolves R1. Panel evidence (Hicks, Kleemans, Li & Miguel 2021) finds that most cross-sectional sector gaps are selection. Read $\xi_A$ as a reduced-form wedge, not a pure distortion.

### 3.3 Non-farm production

$Y_j=B_jH_{Uj}^{\beta}(L^c_j)^{1-\beta}$, perfect competition. Zero profit gives the wage–rent frontier:

$$
w_{Uj}=\beta\,B_j^{1/\beta}\left(\frac{1-\beta}{r_j}\right)^{\frac{1-\beta}{\beta}},\qquad
L^c_j=\frac{1-\beta}{\beta}\frac{w_{Uj}H_{Uj}}{r_j}.
\tag{Z}
$$

Optional agglomeration: $B_j=b_j\,(H_{Uj}/T_j)^{\gamma_B}$.

### 3.4 Farm production (corrected rural block)

Gross output with capital $K$, intermediates $X$ (traded at national prices $R,p_X$), land and labour, CRS:

$$
Q_j=B^A_j\,H_{Aj}^{a_H}K_j^{a_K}X_j^{a_X}(T^F_j)^{a_T},\qquad a_H+a_K+a_X+a_T=1 .
$$

Optimising out $K$ and $X$ (output price $p_A$ set nationally or on world markets, which suits a small region of a data-rich country) leaves value added net of $K,X$ payments:

$$
V_j=\tilde A_j\,H_{Aj}^{\theta_H}(T^F_j)^{\theta_T},\quad
\theta_T=\frac{a_T}{a_T+a_H},\ \theta_H=1-\theta_T,
$$
$$
w_{Aj}=\theta_H\tilde A_j\left(\frac{T^F_j}{H_{Aj}}\right)^{\theta_T},\qquad
\rho_j=\theta_T\frac{V_j}{T^F_j}=\frac{\theta_T}{\theta_H}\frac{w_{Aj}H_{Aj}}{T^F_j}.
\tag{F}
$$

This is the proposal's $w_R=B_R(\text{Land}/N_R)^{\beta_R}$, with $\beta_R=\theta_T\approx0.4$ instead of 2.479 and applied to farm jobs only. TFP shocks enter as $\hat{\tilde A}=\hat B_A^{1/(a_T+a_H)}$.

### 3.5 Floor space

Supply $L_n=\underline{L}_n r_n^{\mu}$. Market clearing with residential plus commercial expenditure gives the closed form

$$
r_n=\left(\frac{(1-\alpha)\,\bar y_n N_n+\frac{1-\beta}{\beta}w_{Un}H_{Un}}{\underline{L}_n}\right)^{\frac{1}{1+\mu}} .
\tag{R}
$$

(No separate residential/commercial rents by default. Add a wedge $r^c=(1+\zeta)r^r$ if zoning matters.)

### 3.6 Residence choice and semi-closure (long run)

Residents choose a county with Fréchet($\lambda_R$), $\lambda_R<\lambda$ (moving home is less elastic than changing jobs):

$$
N_i=\bar N\,\frac{u_i^{\lambda_R}}{\sum_k u_k^{\lambda_R}},\qquad
W=\Big(\sum_k u_k^{\lambda_R}\Big)^{1/\lambda_R},\qquad
\bar N=\bar N_0\left(\frac{W}{\bar U}\right)^{\eta}.
\tag{S}
$$

$\eta=0$ means a closed region. $\eta\to\infty$ means fully open ($W=\bar U$). The proposal's knife-edge equalisation is the limit $\lambda_R\to\infty$, which is why it behaved badly.

### 3.7 Equilibrium

Given fundamentals $\{A,b,\tilde A,\underline{L},T^F,\xi_A,t\}$ and parameters, an equilibrium is $\{N,w_U,w_A,r\}$ satisfying (L), (Z), (F), (R), (S). Reduced to unknowns: $x=(\ln r,\ln w_A)\in\mathbb R^{2Z}$ given $N$ (inner), and $\ln N\in\mathbb R^{Z}$ (outer). $w_U$ is eliminated by (Z).

### 3.8 Dynamics (the path)

Each period $t$: solve the within-period block (§3.2–3.5) given $N_t$, giving $\ln u_{nt}$. Then residents relocate by dynamic logit flows (Artuç–Chaudhuri–McLaren; Caliendo–Dvorkin–Parro):

$$
\mu_{in,t}=\frac{\exp\!\big((\ln u_{nt}+\delta_n-\tau_{in})/\nu\big)}{\sum_m\exp\!\big((\ln u_{mt}+\delta_m-\tau_{im})/\nu\big)},\qquad
N_{n,t+1}=\sum_i\mu_{in,t}N_{it}\;(+\text{semi-closed inflow}).
$$

- $\tau_{in}$: migration cost (distance-based; $\tau_{ii}=0$). $1/\nu$: migration elasticity.
- $\delta_n$ are **calibrated so that the observed $N$ is a steady state** (reference: `calibrate_flows`). Without this step the baseline drifts with no shock. This matters because the static amenities are calibrated for $\lambda_R$, not $(\nu,\tau)$.
- v1 uses **myopic** agents (value = current $\ln u$). v2 uses forward-looking values $v_{nt}=\ln u_{nt}+\nu\ln\sum_m\exp((\beta v_{m,t+1}-\tau_{nm})/\nu)$, solved by **dynamic hat algebra** (CDP 2019) with observed gross flows. That removes the need to know $\tau$ and $\delta$ separately.
- Semi-closed inflow: $\bar N_{t+1}=\bar N_t\,(\bar N^*_t/\bar N_t)^{\phi}$ with partial adjustment $\phi$ toward the target in (S).

### 3.9 "Until the countryside has enough people for the extra land"

Your phrasing allows two readings. Both are supported, and the app should let the user pick:

- **(a) Consolidation reading.** Rural people leave until farmland per farm worker $T^F/H_A$ rises to a target (enough land each).
- **(b) Frontier reading.** Rural labour grows until there are enough workers to bring extra suitable land into cultivation.

**Stopping rule** (both readings): stop the path at the first $t$ where

$$
\frac{\sum_{n\in\mathcal R}T^F_{n}}{\sum_{n\in\mathcal R}H_{An,t}}\ \gtrless\ (1\pm\varepsilon)\times\text{baseline},
$$

or when the frontier binds ($T^F_n=\bar T^F_n$ in a share of rural counties), or at steady state.

**Extensive land margin** (needed for reading b; spec only, not in reference v1): plots in county $n$ have quality $q\sim\text{Pareto}(q_{\min},k)$ on suitable area $\bar T^F_n$ (from FAO GAEZ / USDA soil productivity indices). A plot is farmed if $q\,\tilde\rho_n\ge c_n$ (a per-hectare fixed cost). Then

$$
T^F_n=\bar T^F_n\min\!\left\{1,\left(\frac{q_{\min}\tilde\rho_n}{c_n}\right)^{k}\right\},\qquad
\text{effective land }=\bar T^F_n\frac{k}{k-1}q_{\min}^{k}\,q^{*\,1-k}_n .
$$

This is closed form, so the frontier responds smoothly to labour. More farm workers raise $\tilde\rho$ (F) and pull marginal land in. $k$ comes from the dispersion of soil productivity within the county.

### 3.10 Asset prices

- **Farmland:** $P^F_{n,t}=\sum_{s\ge1}(1+i)^{-s}\rho_{n,t+s}+\text{Gordon terminal}$, computed along the simulated path (perfect foresight) or with static expectations ($\rho_t/(i-g)$).
- **Urban land/housing:** the same applied to the land component of $r_n$. With $L=\underline{L} r^\mu$ and a land share $\phi_L$ in floor-space production, land rent per hectare is $\phi_L r_nL_n/T^B_n$.
- **Fringe conversion (Capozza–Helsley):** farmland at the edge converts to built use when urban land value minus conversion cost exceeds farmland value plus the option value of waiting. With $T^B_n+T^F_n\le T_n$, the built area $T^B$ grows and $\underline{L}_n\propto T^B_n$ shifts. This is how cities physically consume farmland.
- **Calibration point:** observed farmland price/rent ratios embed discount-rate and expectation shocks the model doesn't explain. The U.S. cropland price-to-cash-rent ratio rose from about 20 in 1998 to 36 in 2025. Back out $(i-g)$ by region from that ratio and **hold it fixed** in counterfactuals, so price changes come only from model rents.

---

## 4. Analytic core: why migration responses differ (solves R8)

Two locations, C (non-farm only) and R (farm only), no cross-commuting. All blocks are log-linear, so the indirect utility elasticities to own population are

$$
\psi_C=\frac{k+1-\alpha}{1+\mu+k},\ \ k=\tfrac{1-\beta}{\beta};\qquad
\psi_R=\theta_T+\frac{(1-\alpha)\theta_H}{1+\mu}.
$$

Let $s=d\ln u_C$ be the partial-equilibrium urban welfare shock (population held fixed), $\pi_C$ the urban share, $x=d\ln(N_C/N_R)$, and $n=d\ln\bar N$. Then

$$
\begin{pmatrix}\lambda_R(\psi_C-\psi_R) & 1+\lambda_R(\psi_C\pi_R+\psi_R\pi_C)\\
1+\eta(\pi_C\psi_C+\pi_R\psi_R) & \eta\pi_C\pi_R(\psi_C-\psi_R)\end{pmatrix}
\begin{pmatrix}n\\x\end{pmatrix}=\begin{pmatrix}\lambda_R s\\ \eta\pi_C s\end{pmatrix},
$$

and for a closed region ($\eta=0$):

$$
\boxed{\;x=\frac{\lambda_R\,s}{1+\lambda_R\left[\psi_C(1-\pi_C)+\psi_R\pi_C\right]},\qquad d\ln N_R=-\pi_C\,x\;}
$$

*(Verified numerically against the full solver: `test_two_location_closed_form`, $\eta\in\{0,1.5\}$.)*

**Reading:** for the *same* welfare shock $s$, rural out-migration is smaller where (i) the land share $\theta_T$ is higher (diminishing returns to farm labour bite harder), (ii) housing supply is less elastic, (iii) the region is more open ($\eta>0$: the city fills from outside instead of from the countryside), or (iv) residence is less elastic ($\lambda_R$). This is the decomposition the LAC/SSA comparison needs: compare $x/s$, not $x$ per % transport cut.

### 4.1 Illustrative results (synthetic 25-county state, reference code)

| Scenario | Rural residents | Farmland per farm worker (rural) | Farm wage | Farmland rent | Core floor rent | Region pop. |
|---|---|---|---|---|---|---|
| Core productivity +10%, $\theta_T=0.15$, closed | −6.2% | +10.9% | +1.6% | −8.4% | +11.7% | 0 |
| same, $\theta_T=0.40$, closed | −5.6% | +6.2% | +2.4% | −3.5% | +11.5% | 0 |
| same, $\theta_T=0.40$, $\eta=2$ | +0.2% | +2.4% | +1.0% | −1.4% | +15.8% | +6.6% |
| Uniform 20% travel-time cut, closed | **+1.6%** | −1.8% | — | +1.1% | — | 0 |

Three lessons for the paper design:
1. **A transport cut is not an urban-welfare shock.** A uniform cut *decentralises* residents (the core loses 3%), so it is the opposite of the Harris–Todaro intuition. To pull people out of farming you need cuts on links into the core, or urban productivity gains.
2. **Semi-closure dominates.** With $\eta=2$ the city grows from outside and rural counties barely change. $\eta$ is the parameter to estimate carefully.
3. **Land prices move against people.** Out-migration lowers farmland rents (land and labour are complements), so the asset-price channel is a natural brake and an outcome worth reporting.

---

## 5. Calibration (exact model inversion)

**Data per county:** $N_i$, $H_{Uj}$, $H_{Aj}$ (with $\sum H=\sum N$, or add an external zone for cross-border commuters, which the code enforces), $L_n$, $T^F_n$, $t_{ij}$, observed farm earnings $w^{obs}_{Aj}$, mean non-farm earnings.

1. **Effective wages** $\tilde w_{js}=w_{js}\xi_{sj}$: iterate $\ln\tilde w\leftarrow\ln\tilde w+\frac1\lambda(\ln H^{data}-\ln H^{model})$ and normalise (ARSW contraction; about 10³ cheap vectorised steps). Unique up to scale.
2. **Farm wedge:** $\xi_{Aj}=\tilde w_{Aj}/w^{obs}_{Aj}$. This is the measured "agricultural gap" in utility terms.
3. **Rents** from (R) with observed $L$: $r_n=E_n/L_n$. Then $\underline{L}_n=L_n/r_n^{\mu}$.
4. **Non-farm productivity** from (Z): $B_j=(w_{Uj}/\beta)^{\beta}(r_j/(1-\beta))^{1-\beta}$.
5. **Over-identification test:** model farmland rent $\rho_j=\frac{\theta_T}{\theta_H}\frac{w_{Aj}H_{Aj}}{T^F_j}$ against **NASS county cash rents**. Alternatively, estimate $\theta_T$ county by county from this ratio, which is a cleaner use of data than any published elasticity.
6. **Farm productivity:** $\tilde A_j=w_{Aj}(H_{Aj}/T^F_j)^{\theta_T}/\theta_H$.
7. **Amenities** from (S): $\ln A_i=\frac{1}{\lambda_R}\ln N_i+(1-\alpha)\ln r_i-\frac1\lambda\ln\Phi_i$ (normalised). Set $\bar U=W$ so the baseline is an equilibrium for any $\eta$.
8. **Flow offsets** $\delta$ (for the path): iterate $\delta\leftarrow\delta+\nu(\ln N-\ln \mu(\delta)^\top N)$ until $N$ is stationary.

All of this is closed form except steps 1 and 8. The reference code reproduces jobs, farm wages and residents to $10^{-7}$ relative or better.

**Counterfactuals:** prefer **exact hat algebra**. Write the equilibrium in changes $\hat x=x'/x$. A travel-time change enters as $\hat d_{ij}=e^{-\kappa\Delta t_{ij}}$, and only baseline shares ($\pi_{js|i}$, expenditure shares) are needed. Unobservable levels never enter, so measurement error in $A,b$ doesn't contaminate the counterfactual.

---

## 6. Solvers

### 6.1 Review of `solver.py` / `stacktime.py`

These are a careful, production-grade engine for **period-indexed macro frameworks** (EViews/TROLL-like): cells are `(alias, period)`, equations are ASTs evaluated one cell at a time.

**What is genuinely good, and worth porting as ideas:**
- **SCC condensation** (`tarjan_cross_period`, stacktime L1866) with the DAG evaluated once and only true cycles iterated. Same principle as block-recursive QSE solving.
- **Graph tearing** (`_tear_set`, L1087): a greedy feedback vertex set, then Anderson on the torn cells only. Good design.
- **Anderson with per-unknown scaling** and a scale-invariant floor (L1794–1801). Exactly what mixed-magnitude systems (rents in $/m² vs. populations in 10⁵) need.
- **Sparse grouped-FD Newton** for big cycles with Jacobian reuse across years (L1025–1050).
- **Verify-and-repair pass** (`_off_cells`, L1301–1388) and the replay short-circuit. Honest convergence reporting.
- **Flips = calibration targets.** "Pin observed X, free fundamental Y" *is* model inversion. KKT min-norm flips (solver.py L978) are a principled way to spread a target over several shocks.

**Issues (some general, some specific bugs):**

| Where | Issue | Consequence |
|---|---|---|
| stacktime L1804–1853, solver L1642 | **Step-based** stop test ($\max|\Delta|/|x|<$ tol). Your own comment (L1633–1641) documents near-unit-root blocks needing about 417 sweeps. With contraction rate $\rho$ the true error is about step$\cdot\rho/(1-\rho)$, so 50× the step at $\rho=0.98$. | Can stop at a non-solution. Use **residual** tests ($\|G(x)-x\|$ on the undamped map) or estimate $\hat\rho$ and test step$/(1-\hat\rho)$. |
| stacktime L1849 | After an accepted Anderson step, `md` is recomputed with the pure relative formula `abs(nw-o)/(abs(o)+1e-12)`, **not** `_conv_delta`. | Reintroduces the near-zero "check identity" pathology `_conv_delta` (L2139) was written to fix. A one-line fix: use `_conv_delta(nw, o)`. |
| stacktime L1843 | The merit gate evaluates two full fixed-point residuals per Anderson proposal. | An accepted AA step costs about 3 sweeps. Gate on the *next* GS residual instead (free), or use safeguarded AA (restart on residual increase), as in the reference code. |
| stacktime L999–1002, `_seed_value` → 0.0 | Zero seeds. | For multiplicative models ($w^\lambda$, $r^{1-\alpha}$, logs) zero seeds produce NaN/∞. QSE must be solved in **logs** with positive seeds. |
| stacktime L1683 | IM Newton step damped by 0.5. | Turns quadratic convergence into linear. Use a line search (Armijo) instead of fixed damping. |
| stacktime L2011 | Null-propagation loop up to `len(unknowns)+1` passes. | O(n²) worst case. Propagate along the dependency graph once in topological order. |
| stacktime L98–99 | Cache eviction clears all 64 entries at once. | Thrash under many edits. Use an LRU (`OrderedDict`). |
| stacktime L363–844; solver L1741–1746 | Flips solved by an outer Broyden/FD loop where **each residual is a full block solve**. Indirect flips are sequential and order-dependent (the code says so and defers the joint solve). | Expensive and path-dependent. Solve the **augmented system** (swap endogenous/exogenous inside the same Newton/Anderson system) or use the implicit function theorem $dx/dp=-J_x^{-1}J_p$. |
| tolerances | Flip acceptance at 1e-9 (stacktime L616), 1e-7 (solver L1243, stacktime L818), 1e-6 (KKT, solver L1040). | Inconsistent "held" semantics across flip types. Centralise in one tolerance policy. |
| architecture | Scalar AST evaluation per cell. A county QSE has $Z$ equations, **each summing over $Z$ (or $2Z$) terms**. | Thousands of times slower than vectorised numpy for the same math. The year/frequency machinery is irrelevant here. |

**Verdict:** don't port the engine. Port three ideas: **(1)** block decomposition at the *module* level (choice block → floor block → farm block → residence), **(2)** scaled, safeguarded Anderson, and **(3)** flips as a generic "target X by freeing Y" calibration API in the app.

### 6.2 Recommended solver stack

| Layer | Problem | Method | Why |
|---|---|---|---|
| Calibration step 1 | $H(\tilde w)=H^{data}$ | ARSW contraction in logs | Provably convergent, O(Z²) per step, vectorised |
| Inner (given $N$) | $x=G(x)$, $x=(\ln r,\ln w_A)$ | damped fixed point + **Anderson(m=6)**, residual stop at 1e-11 | 25 iterations on the test economy |
| Outer (residence + $\eta$) | $\ln N=G(\ln N)$ | Anderson on the nested map, inner warm-started | **12 outer iterations vs. 256** with plain damping |
| Fallback / large $Z$ | joint $F(x,\ln N)=0$ | **JAX** `jit` + `jacfwd` → Newton with line search ($Z\lesssim3000$); `scipy.optimize.newton_krylov` matrix-free (grid) | Exact Jacobians, quadratic convergence, no FD noise |
| Counterfactuals | equilibrium in changes | **exact hat algebra** | Needs only shares; robust to level mismeasurement |
| Path | flows + within-period block | sequential; v2 **dynamic hat algebra** with forward-looking values | Standard; scales to hundreds of periods |
| Uniqueness | with $\gamma_B>0$ | Allen–Arkolakis–Li (2024) spectral-radius condition on the elasticity matrix; warn in the UI if violated | Avoids silently picking one of several equilibria |

**Why not plain Newton by default:** the nested map is a contraction in logs for the defaults, Newton on $3Z$ unknowns needs a dense Jacobian of $(3Z)^2$ terms for a gain of a few iterations, and FD Jacobians on gravity sums are noisy. Use Newton (via JAX) when Anderson stalls or for calibration-with-targets (flip-style) problems.

### 6.3 Convergence contract (for the app)

Every solve returns `{converged, iterations, residual_inf, rho_hat, method}`. The UI shows a red badge if `residual_inf > 1e-8` and never renders unconverged maps as results.

### 6.4 Scaling

Memory and time are dominated by the $Z\times Z\times 2$ choice tensor. For a sub-county grid, truncate commuting at $t_{ij}>120$ min (sparse CSR) and compute $\Phi_i$ by sparse matrix–vector products. That is about O(nnz) per iteration.

---

## 7. Parameters (defaults, sources, and what to estimate instead)

| Param | Default | Range / evidence | Better: estimate from |
|---|---|---|---|
| $1-\alpha$ housing share | 0.25 | 0.24–0.33 in U.S. expenditure data | CEX/ACS rent-to-income by county |
| $\beta$ non-farm labour share | 0.80 | ARSW 2015 | BEA county compensation / GDP |
| $\lambda$ Fréchet (jobs) | 6.8 | ARSW ≈ 6.8 | LODES OD gravity, PPML |
| $\kappa\lambda$ commuting semi-elasticity | 0.08 /min | about 0.07–0.10 in Berlin/U.S. studies (verify for your state) | **PPML on LODES OD flows**: $\ln E[\text{flow}_{ij}]=\text{FE}_i+\text{FE}_j-\kappa\lambda t_{ij}$ |
| $\mu$ floor supply | 0.5 | about 0.5 floor space / 0.3 units on average across U.S. urban tracts (Baum-Snow & Han 2024); higher exurban and rural | Tract-level BSH estimates aggregated to county |
| $\theta_T$ land share (farm VA net of K, X) | 0.40 | 0.15/(0.15+0.22) from USDA-ERS shares in Suh & Moss | **County cash rents** (§5 step 5) |
| $\lambda_R$ residence elasticity | 3 | long-run county mobility elasticities are small single digits | IRS SOI county flows |
| $\nu,\tau$ flows | 2, $\tau=\tau_0+\tau_1\ln d$ | ACM/CDP framework | PPML gravity on IRS gross flows |
| $\eta$ semi-closure | 1 (sweep 0–5) | the key unknown; §4 shows it dominates | state-level net in-migration vs. welfare shocks (shift-share) |
| $i-g$ (land discount) | from price/rent | U.S. cropland price/rent ≈ 36 in 2025, i.e. ≈ 2.8% | NASS county land values & rents |
| $\gamma_B$ agglomeration | 0 (option 0.03–0.07) | ARSW and the urban literature | leave off unless needed; check uniqueness |
| $k$ plot-quality Pareto shape | 3 | — | within-county dispersion of soil productivity (SSURGO/NCCPI or GAEZ) |

**On "updated distributions":** keep **Fréchet** for location choice. Nothing more recent beats it for closed-form gravity, and its logsum gives the welfare measure. The modern updates are elsewhere: (i) **two elasticities** ($\lambda$ for jobs, $\lambda_R$ or $1/\nu$ for residence) instead of one; (ii) **dynamic logit (Gumbel) flows** for the path; (iii) a **Pareto plot-quality** distribution for the land frontier (closed form, §3.9); (iv) the **selection-aware** reading of the farm gap ($\xi_A$). If you need correlated tastes across nearby counties, use a nested Fréchet (cross-nested by commuting zone) with a nesting parameter.

---

## 8. Data pipeline (U.S. first; same schema for other data-rich countries)

| Model object | U.S. source | Satellite / grid source | Notes |
|---|---|---|---|
| $N_i$ residents | Census PEP / ACS | GHS-POP, WorldPop, LandScan (100 m–1 km) | Use census totals for calibration and satellite rasters for sub-county shares and change detection |
| $H_{Uj},H_{Aj}$ jobs | BEA CAINC25N (incl. farm proprietors), LODES WAC | — | LODES under-counts farm proprietors, so take farm jobs from BEA |
| $t_{ij}$ | OSM + r5py/OSRM | — | centroid-to-centroid, population-weighted |
| Commuting flows (estimate $\kappa\lambda$) | LODES OD, ACS county flows | — | — |
| $L_n$ floor space | — | **GHSL GHS-BUILT-V** (building volume), Microsoft/Overture footprints | volume ≈ floor space × storey height |
| $T^F_n$ farmland | Census of Agriculture | **USDA Cropland Data Layer (30 m, annual)**, NLCD | CDL also gives crop mix |
| $\bar T^F_n$, plot quality | SSURGO/NCCPI | FAO GAEZ v4 | frontier and Pareto $k$ |
| $w^{obs}_A$ | BEA CAINC45 farm income, Census of Ag labour expense | — | — |
| $\rho_n$ cash rents, land values | NASS county cash rents; NASS land values | — | over-identification test and asset-price calibration |
| Housing prices/rents | FHFA county HPI, Zillow, ACS gross rent | — | urban asset-price validation |
| Price levels | BEA Regional Price Parities | — | validation of $r$ |
| Migration flows | IRS SOI county-to-county, ACS flows | — | $\nu,\tau$, dynamic hat algebra |

Other data-rich targets with the same schema: EU NUTS-3 (Eurostat, LUCAS, CORINE/Copernicus), UK (ONS census OD, LSOA), Korea 시군구 (KOSIS 인구이동, 국토부 실거래가, 농업면적조사), Japan.

**Satellite preprocessing is offline:** Google Earth Engine or Microsoft Planetary Computer → zonal statistics per county with `exactextract` → versioned Parquet (`data/{state}/{year}/county.parquet`) plus Cloud-Optimised GeoTIFFs for display. The app never processes rasters.

---

## 9. Web app

### 9.1 Recommendation

**v1: Streamlit**, with three conditions: (1) the model is a pure package (`urqse/`) with no Streamlit imports, (2) inputs are precomputed Parquet, (3) solves are cached (`st.cache_data` keyed on params + scenario hash).

Where Streamlit hurts: the whole script reruns on every widget change, animation of time paths is clunky, and there is no good multi-user job queue.

| Option | Use when |
|---|---|
| **Streamlit + pydeck** | prototype, single user, ≤ 250 counties, path ≤ 100 periods |
| **Panel (HoloViz) + datashader** | you want raster overlays and linked brushing, still pure Python |
| **Dash** | finer callback control, animated time sliders, moderate multi-user |
| **FastAPI + MapLibre/deck.gl (React)** | production, many users, async solve jobs (Celery/RQ), raster tiles via TiTiler |

### 9.2 Layout

```
urqse/
  model/        params.py  fundamentals.py  blocks.py (choice, floor, farm, residence)
                equilibrium.py (inner/outer, Anderson, JAX Newton)  hat_algebra.py
                dynamics.py (flows, stop rules, frontier)  assets.py
  calibrate/    invert.py  estimate_gravity.py (PPML)  checks.py (cash-rent overid)
  data/         loaders.py  schema.py (pandera)  build_state.py (offline pipeline)
  app/          streamlit_app.py  components/ (map, sliders, diagnostics panel)
  tests/        test_identities.py  test_inversion.py  test_limits.py
                test_closed_form.py  test_dynamics.py  test_assets.py  test_hat_algebra.py
```

### 9.3 Screens

1. **State picker** → county map (basemap COG + choropleth: residents, farm jobs, cropland share, rents).
2. **Calibration report**: fit errors, the $\xi_A$ map (farm wedge), the cash-rent over-ID scatter, a parameter panel.
3. **Scenario builder**: travel-time changes (draw a corridor or a % cut on links into the core), productivity shocks ($b$, $\tilde A$), land shocks (frontier, conversion), $\eta$ slider, stop rule.
4. **Results**: long-run Δ maps; path animation with the stop marker; land price paths (farmland vs. urban); welfare decomposition; the §4 diagnostic $x/s$.
5. **Diagnostics**: convergence contract, uniqueness check, sensitivity tornado over $(\eta,\lambda_R,\theta_T,\mu)$.

---

## 10. Test plan (reference tests exist for all items marked ✓)

| Test | Property |
|---|---|
| ✓ inversion reproduces data | calibrated fundamentals regenerate $H_U,H_A,w_A$ to 1e-7 |
| ✓ baseline is the equilibrium | static solve from a perturbed start returns observed $N$, for $\eta\in\{0,2\}$ |
| ✓ farm-rent identity | $\rho T^F/(w_AH_A)=\theta_T/\theta_H$ exactly |
| ✓ transport cut raises welfare, closed population fixed | $W'>W$, $\sum N'=\sum N$ |
| ✓ semi-closure nests limits | $\eta=0$ ⇒ $\bar N$ fixed; $\bar N$ increasing in $\eta$ |
| ✓ two-location closed form | §4 formula vs. full solver (rel. error < 0.2%) |
| ✓ flow steady state + stop rule | no-shock path stays at baseline; the stop rule fires |
| ✓ Gordon terminal value | constant rent ⇒ $P=\rho(1+g)/(i-g)$ |
| hat algebra zero shock | $\hat x\equiv1$ |
| hat algebra = level solve | same counterfactual both ways |
| Walras / accounting | income = wages + land rents (+ ownership rule) |
| homogeneity | scaling all $w$ and $r$ by $c$ leaves allocations unchanged |
| property tests (hypothesis) | random $Z\le15$ economies converge, with positive values |
| regression snapshots | one real state (e.g. Iowa, Kansas) pinned outputs |

---

## 11. Roadmap

1. **M1 (static core):** the reference code → package, Iowa data build, calibration report, static counterfactuals. *Exit: inversion and over-ID checks on real data.*
2. **M2 (estimation):** PPML for $\kappa\lambda$ (LODES) and $\nu,\tau$ (IRS); $\theta_T$ from cash rents; $\eta$ sensitivity.
3. **M3 (path + land):** flow dynamics, stop rules, Pareto frontier, Capozza–Helsley conversion.
4. **M4 (assets):** price paths, ownership options, validation against NASS land values and FHFA.
5. **M5 (hat algebra + JAX):** fast counterfactuals, dynamic hat algebra, uniqueness checks.
6. **M6 (app polish / migrate front end if needed).**

## 12. Decisions (resolved, v1.1)

1. **Stop rule = consolidation (reading a).** Stop at the first $t$ with $\sum_{\mathcal R}T^F/\sum_{\mathcal R}H_{A,t}\ \ge (1+\varepsilon)\times$ baseline, or at steady state. The extensive frontier (§3.9 b) is deferred.
2. **No domestic inflow:** $\eta=0$. The region exchanges no people with the rest of the country. **External (international) immigration** is an exogenous scenario path $I_t\ge0$, allocated by §12.2.
3. **Land: independent owner-operators plus landlords**, with county tenure shares (§12.1).
4. First state: Iowa (then Kansas, Nebraska).

### 12.1 Land ownership block

Each county has an owner-operated share $\omega_n$ of farmland (Census of Agriculture, tenure by county). The rest is rented from landlords.

- **Farm operator income** per farm worker $=w_{An}+\omega_n\,\rho_nT^F_n/H_{An}$. Under full owner operation ($\omega=1$) this equals $V_n/H_{An}=w_{An}/\theta_H$, the residual claimant.
- **Landlord income** $(1-\omega_n)\rho_nT^F_n$ goes to a parameter-chosen recipient: share $\varsigma$ to residents of the same county, the rest out of the region.
- **Portability (important):** land income is *wealth* income. A farmer who moves keeps it (by renting the land out or selling it). So it **enters housing demand and welfare where the person lives, but not the location choice margin**: $\pi$ and $u$ use the wage only. Otherwise land ownership would mechanically pin farmers in place. The option `land_income_in_choice` (default False) allows a sensitivity check.
- **Consolidation mechanics:** when a farm worker leaves, their land is rented or sold to remaining operators at $\rho$ or $P^F$. Farmland per remaining operator rises, and so does their land-rent income: the consolidation dividend.
- **Asset prices:** $P^F$ is now also farm-household wealth. Report the wealth change of stayers versus leavers.

### 12.2 External immigration

$\bar N_{t+1}=\bar N_t+I_t$. New arrivals choose a county by the same residence logit as natives, with an optional gateway shifter $g_n$ (weights from ACS foreign-born recent arrivals): $\Pr(n)\propto g_n\exp((\ln u_{nt}+\delta_n)/\nu)$. Natives' flows (§3.8) are unchanged. The static long run solves (S) with $\eta=0$ and $\bar N=\bar N_0+\sum I$.

---

## References

- Ahlfeldt, Redding, Sturm & Wolf (2015). The Economics of Density. *Econometrica* 83(6).
- Allen & Arkolakis (2014). Trade and the Topography of the Spatial Economy. *QJE*.
- Allen, Arkolakis & Li (2024). On the Equilibrium Properties of Spatial Models. *AER: Insights* 6(4): 472–89.
- Artuç, Chaudhuri & McLaren (2010). Trade Shocks and Labor Adjustment. *AER*.
- Baum-Snow & Han (2024). The Microgeography of Housing Supply. *JPE* 132(6): 1897–1946.
- Caliendo, Dvorkin & Parro (2019). Trade and Labor Market Dynamics. *Econometrica* 87(3).
- Capozza & Helsley (1989/1990). The fundamentals of land prices and urban growth; The stochastic city. *JUE*.
- Dekle, Eaton & Kortum (2007). Unbalanced Trade. *AER P&P* (exact hat algebra).
- Fajgelbaum, Morales, Suárez Serrato & Zidar (2019). State Taxes and Spatial Misallocation. *REStud* 86(1).
- Gollin, Lagakos & Waugh (2014). The Agricultural Productivity Gap. *QJE*.
- Hamory (Hicks), Kleemans, Li & Miguel (2021). Reevaluating Agricultural Productivity Gaps with Longitudinal Microdata. *JEEA* 19(3).
- Lagakos, Mobarak & Waugh (2023). The Welfare Effects of Encouraging Rural–Urban Migration. *Econometrica*.
- Ravallion, Chen & Sangraula (2007). New Evidence on the Urbanization of Global Poverty. World Bank WPS 4199.
- Suh & Moss (2021). Examining the Input and Output Linkages in Agricultural Production Systems. *Agriculture* 11: 54.
- Walker & Ni (2015). Anderson Acceleration for Fixed-Point Iterations. *SIAM J. Numer. Anal.*
- USDA-NASS (2025). Land Values and Cash Rents; Zulauf & Sherrick (2026), farmdoc daily, on the price/rent ratio.
