# Proposal M7: a metro nest inside the state model (single-polar)

*Approved 2026-11-24 with the defaults in §11. M7a is implemented for Iowa: spec §3.11 (locations
without a farm sector) and §3.12 (the nest); this file is kept as the design record.*

## 1. What it adds

Two views of one equilibrium:

- **State view (unchanged in what it shows).** Rural counties, the suburbs and the core, semi-closed
  ($\eta=0$). The core's metro area is one residential choice, called the *metro nest*.
- **City view (new).** The metro nest split into census tracts, each with its own jobs, floor space,
  amenities and commuting.

A city policy (upzoning, a transit line, a neighbourhood amenity) changes tract fundamentals. That
changes the metro's overall appeal, which changes the state equilibrium: rural out-migration, suburbs
and the stop period all respond. The metro is an **open city relative to the state**: inside it, people
sort across tracts at the utility the rest of the state offers. The state stays semi-closed, so the
feedback runs both ways and there is no exogenous $\bar U$ for the city.

Single-polar: one nest, the in-state part of the Metropolitan Statistical Area that holds the core
county. Every other county, including those of other metros, stays a county.

## 2. Locations

- $\mathcal C$: counties outside the nest (rural counties and other metros' counties).
- $\mathcal K$: tracts of the nest. The nest's out-of-state part, if any, joins the external zone.
- $\mathcal J=\mathcal C\cup\mathcal K\cup\{\text{ext}\}$: all workplaces and residences.

**The within-period block (§3.2–3.5) runs unchanged on $\mathcal J$.** Workers living anywhere choose a
workplace and sector over all of $\mathcal J$ with the Fréchet($\lambda$) choice (L). Commuting between a
tract and a county uses the travel time between the tract's and the county's population centres.
Floor space (R), non-farm production (Z) and farm production (F) are per location as now. Only the
**residence choice** is nested.

## 3. Nested residence choice

Tract utility $u_k$ is (§3.2) evaluated at tract $k$. The nest's value is the CES aggregate of its tracts

$$
u_M=\Big(\sum_{k\in\mathcal K}u_k^{\lambda_M}\Big)^{1/\lambda_M},
$$

and residents choose between the counties and the nest with $\lambda_R$, then between tracts with $\lambda_M$:

$$
N_c=\bar N\frac{u_c^{\lambda_R}}{\sum_{c'}u_{c'}^{\lambda_R}+u_M^{\lambda_R}},\qquad
N_M=\bar N\frac{u_M^{\lambda_R}}{\sum_{c'}u_{c'}^{\lambda_R}+u_M^{\lambda_R}},\qquad
N_k=N_M\frac{u_k^{\lambda_M}}{\sum_{k'}u_{k'}^{\lambda_M}} .
\tag{S'}
$$

$W=(\sum_c u_c^{\lambda_R}+u_M^{\lambda_R})^{1/\lambda_R}$ and the semi-closure in (S) are unchanged.

- **Consistency:** $\lambda_M\ge\lambda_R$ (moving within the metro is at least as elastic as moving
  across the state). This is the condition for (S') to come from utility maximisation (nested Fréchet /
  GEV). Assert it in `Params`.
- **Collapse:** with $\lambda_M=\lambda_R$, (S') is a flat choice over $\mathcal C\cup\mathcal K$. This is
  the bridge to the current model and the basis of the reproduction test (§8).
- **State view:** a metro county's residents, jobs and rents are sums (or job-/resident-weighted means)
  over its tracts. The state map draws counties as it does now.

## 4. Calibration (§5, extended)

Steps 1–6 run on $\mathcal J$ as now. Step 7 splits:

- 7a. Within the nest: $\ln A_k=\frac1{\lambda_M}\ln N_k+(1-\alpha)\ln r_k-\frac1\lambda\ln\Phi_k$, normalised
  within the nest.
- 7b. Across the state: the nest's level is set so that $N_M$ is matched by (S') with $\lambda_R$, together
  with the counties' $A_c$ as now.

Step 8 (flow offsets) runs on $\mathcal C\cup\{M\}$ (§6). The exact-inversion bar ($10^{-7}$) applies to
every tract.

## 5. Data (offline, `build_state` + a new `build_metro`)

| Item | Source | Note |
|---|---|---|
| Tracts, geometry | Census cartographic boundary file 2022, tracts | |
| Tract population centres | 2020 Census centers of population, tract | as for counties |
| Residents $N_k$ (workers) | LODES8 RAC JT00, summed from blocks | ACS tract 5-year as a check |
| Jobs $H_{Uk},H_{Ak}$ | LODES8 WAC JT00; farm = CNS01 (NAICS 11) | wage and salary jobs only; scaled so tract totals sum to the county's BEA-based totals (as in M2) |
| Floor space $L_k$ | GHSL GHS-BUILT-V, tract zonal sums | 100 m pixels |
| Farmland $T^F_k$ | CDL, tract zonal sums | |
| Farm wage | the county's $w_{A}^{obs}$ for each of its tracts | no tract farm earnings exist; `# VERIFY` |
| Non-farm wage level | metro-wide normalisation | the inversion recovers relative tract wages from jobs and residents |
| Travel times | OSRM, tract to tract and tract to county | car only; transit needs GTFS and a new routing dependency (ask first) |

## 6. Dynamics

v1: the path (§3.8) moves residents between $\mathcal C$ and the nest with the current flows, using
$\ln u_M$ as the nest's value. **Within the nest, residents re-sort to (S') every period** (moving inside
a metro is fast compared with leaving the countryside). Cheaper, and it keeps $\nu,\tau,\delta$ at the
county level where they are calibrated. `# VERIFY`; a v2 can add within-metro flows.

The consolidation stop rule (§3.9) is unchanged: it reads rural counties only.

## 7. City policies (what the city view lets a user change)

| Policy | Enters as |
|---|---|
| Upzoning a set of tracts | $\underline L_k\times(1+z)$ for $k$ in the set |
| Transit or road improvement | $t_{kk'}\times(1-c)$ on chosen tract pairs, or into a chosen set |
| Neighbourhood amenity | $A_k\times(1+a)$ |
| Downtown productivity | $b_k\times(1+p)$ |

Each is a change in fundamentals, so exact hat algebra (§5) applies as for the current shocks.
Agglomeration and amenity spillovers with travel-time decay (Ahlfeldt et al. 2015) belong at tract
scale and are the natural next step (M7b), off by default with the Allen–Arkolakis–Li check. They are
not part of M7a.

## 8. Tests (added to §10)

1. With $\lambda_M=\lambda_R$, the nested solve equals the flat solve on $\mathcal C\cup\mathcal K$.
2. Tract sums reproduce the metro counties' totals of the county model on the same data (residents,
   jobs; rents as weighted means).
3. Zero city policy gives no change anywhere (levels and hat algebra).
4. A city policy confined to the nest still moves rural $N$ (feedback is on), and conservation holds:
   $\sum N$ + cumulative immigration is constant with $\eta=0$.
5. Inversion reproduces tract and county data to $10^{-7}$.
6. Homogeneity of degree 0 in $(w,r)$ and the income accounting identity, on the nested economy.
7. Property tests (hypothesis) on random nested economies with $|\mathcal C|+|\mathcal K|\le 15$.

## 9. Size and speed

$|\mathcal J|$ is roughly 100 to 300 for a mid-size metro (Des Moines, Omaha) and over 1,000 for
Chicago or Houston. The dense engine takes about 7 s for 400 locations (§2), and the page solves in the
browser. v1 targets metros up to about 400 tracts with the dense engine. Larger metros need the sparse
commuting cutoff (§6.4) or block groups merged to fewer zones. In the page: the city view at the
baseline and the long run; the path solves the nest each period, so it is the slow part.

## 10. Multi-polar (later, M7c)

The design extends without a new idea: each Metropolitan Statistical Area becomes a nest with its own
$\lambda_{M}$ (all $\ge\lambda_R$), and workplace choice already spans every location, so commuting
between metros is in (L) already. Two things change elsewhere:

- "The core" becomes per nest: the core productivity shock asks which metro, and the state view
  labels each metro's core.
- A metro with several job centres (Dallas–Fort Worth) needs no special treatment: its tracts carry
  the job centres, and no single core has to be named inside the nest.

The cost is size (every metro's tracts at once) and the UI.

## 11. Decisions needed before code

1. **Locations without a sector.** Most city tracts have no farm jobs and no farmland, and the model
   works in $\ln H_A$. The nest needs a per-location sector set: the farm option is absent where
   $H_{Ak}=0$ (structural zeros in (L), no (F) block there). This is the model change declined for
   whole counties earlier today. Once made, it also lets the 17 states with zero-farm counties be built.
   Without it, tracts would have to be merged until each has farm jobs, which defeats the city view.
2. **Within-nest mobility:** instant re-sorting each period (proposed) or flows.
3. **$\lambda_M$:** a default equal to $\lambda_R$ (the flat case) with a slider, or an estimate.
   Candidates: the spread of tract-level residence shares against tract utilities, as in step 7a.
   `# VERIFY`.
4. **Size cap** for v1 (about 400 tracts), or block-group merging for larger metros.
5. **Metros crossing state lines** (Omaha–Council Bluffs, Kansas City, St. Louis): the out-of-state part
   joins the external zone (proposed), or the nest crosses the state line.
