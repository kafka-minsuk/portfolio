"""The calibration report (reports/{state}_{year}_CALIBRATION.md) and its xi_A county map (SVG,
plain strings; no plotting dependency). Every number in the report comes from run_state.run."""

from html import escape
from pathlib import Path

import numpy as np

from ..data.build_state import STATE_NAME

SURFACE, INK, INK_2, MID = "#fcfcfb", "#0b0b0b", "#52514e", "#f0efec"
LOW, HIGH = "#2a78d6", "#e34948"  # diverging poles (dataviz reference palette)
NO_FARM = "#c9c8c4"  # counties without a farm sector (spec §3.11)
BREAKS = np.array([-1.0, -0.5, -0.2, 0.2, 0.5, 1.0])  # ln(xi_A / state median)


def _mix(a, b, f):
    ca = [int(a[k : k + 2], 16) for k in (1, 3, 5)]
    cb = [int(b[k : k + 2], 16) for k in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(ca, cb))


BIN_COLORS = [_mix(MID, LOW, f) for f in (1.0, 0.66, 0.33)] + [MID] + [_mix(MID, HIGH, f) for f in (0.33, 0.66, 1.0)]


def _ring(coords, x0, y1, k):
    return "M" + "L".join(f"{(x - x0) * k:.1f},{(y1 - y) * k:.1f}" for x, y in coords) + "Z"


def xi_map_svg(shp, fips, names, xi, title="", width=760) -> str:
    """Choropleth of ln(xi_A / median) on the 2022 Census cartographic counties (EPSG:5070)."""
    g = shp.loc[fips].to_crs(5070).geometry.simplify(400)
    x0, y0, x1, y1 = g.total_bounds
    k = (width - 40) / (x1 - x0)
    h = (y1 - y0) * k
    dev = np.log(xi / np.nanmedian(xi))
    bins = np.where(np.isfinite(dev), np.digitize(np.nan_to_num(dev), BREAKS), -1)  # -1: no farm sector
    paths = []
    for geom, f, nm, v, b in zip(g, fips, names, xi, bins):
        polys = getattr(geom, "geoms", [geom])
        d = "".join(_ring(p.exterior.coords, x0, y1, k) for p in polys)
        fill, tip = (NO_FARM, "no farm sector") if b < 0 else (BIN_COLORS[b], f"xi_A = {v:.3f}")
        paths.append(f'<path d="{d}" fill="{fill}"><title>{escape(nm)} ({f}): {tip}</title></path>')
    labels = ["< -1.0", "-1.0 to -0.5", "-0.5 to -0.2", "-0.2 to 0.2", "0.2 to 0.5", "0.5 to 1.0", "> 1.0"]
    sw = (width - 40) / 7
    legend = "".join(
        f'<rect x="{20 + i * sw:.1f}" y="{h + 62:.1f}" width="{sw - 2:.1f}" height="12" rx="2" fill="{c}"/>'
        f'<text x="{20 + i * sw + sw / 2:.1f}" y="{h + 90:.1f}" font-size="11" text-anchor="middle" fill="{INK_2}">{escape(lab)}</text>'
        for i, (c, lab) in enumerate(zip(BIN_COLORS, labels))
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h + 110:.0f}" font-family="system-ui, sans-serif">'
        f'<rect width="100%" height="100%" fill="{SURFACE}"/>'
        f'<text x="20" y="22" font-size="15" font-weight="600" fill="{INK}">Farm-job wedge xi_A by county, {escape(title)}</text>'
        f'<text x="20" y="40" font-size="12" fill="{INK_2}">ln(xi_A / state median {np.nanmedian(xi):.3f}); '
        f"blue = farm jobs less attractive than their paid wage implies, relative to the median county"
        f"{'; grey = no farm sector' if np.isnan(xi).any() else ''}</text>"
        f'<g transform="translate(20,50)" stroke="{SURFACE}" stroke-width="1">{"".join(paths)}</g>{legend}</svg>\n'
    )


def _f(x, d=3):
    return f"{x:,.{d}f}"


def write_report(r, out_dir: Path):
    st, yr = r["state"], r["year"]
    out_dir.mkdir(parents=True, exist_ok=True)
    c = r["counties"]
    cdf = r["cdf"]
    f0, f = r["cal0"].fundamentals, r["cal"].fundamentals
    farm_c = r["data"].HA[c] > 0
    xi = np.where(farm_c, f.xi_A[c], np.nan)  # NaN: no farm sector (spec §3.11)
    map_name = f"{st}_{yr}_xi_A.svg"
    name = STATE_NAME.get(st, st)
    iowa = st == "IA"  # the interpretive paragraphs were written for Iowa's numbers; other states get the tables
    (out_dir / map_name).write_text(xi_map_svg(r["shp"], r["fips"], cdf["name"].tolist(), xi, f"{name} {yr}"))

    g = r["gravity"]
    head = g["in-state, off-diagonal (headline)"]
    th = r["theta"]
    chosen = th[next(k for k in th if "(chosen" in k)]
    m3 = r["m3"]  # None where BEA farm earnings are not positive in every county
    xi3 = m3["cal"].fundamentals.xi_A[c] if m3 else np.full(int(c.sum()), np.nan)
    o3 = m3["overid"]["theta_T = 0.40 (default)"] if m3 else None
    th3 = th[next(k for k in th if "(M3 choice)" in k)]
    acc, acc3 = r["accounts"], (m3["accounts"] if m3 else None)
    wA_old = cdf["wA_bea_earn_usd"].to_numpy(float)
    w_job = (cdf["farm_labour_bill_usd"] / cdf["HA_bea"]).to_numpy(float)
    o0 = r["overid"]["theta_T = 0.40 (default)"]
    o1 = next(v for k, v in r["overid"].items() if k != "theta_T = 0.40 (default)")
    flows = r["flows"]
    Zc = int(c.sum())
    own_share = float(np.trace(flows[:Zc, :Zc]) / flows[:Zc, :Zc].sum())
    N = r["data"].N
    usd = r["usd"]
    kind = cdf["kind"].to_numpy(str)
    pub = r["pub"]
    names = cdf["name"].to_numpy(str)
    obs = cdf["cash_rent_usd_acre"].to_numpy(float)
    wA_usd = cdf["wA_obs_usd"].to_numpy(float)
    th_c = chosen["county"]

    L = []
    w = L.append

    def n(text):  # Iowa-only narrative; a lambda, so its numbers are only computed for Iowa
        if iowa:
            w(text())

    w(f"# {name} {yr} calibration report (milestone M3, farm wage revised in M3b)\n")
    if not iowa:
        w("Tables only: the interpretive paragraphs of the Iowa report (`reports/IA_2022_CALIBRATION.md`) were written "
          f"for Iowa's numbers and are not repeated here. Read {name}'s numbers on their own.\n")
    w(f"Generated by `python -m urqse.calibrate.run_state {st} {yr}` from `data/{st}/{yr}/` (M2 build, "
      f"`reports/{st}_{yr}_REPORT.md`) and LODES8 OD {yr}. {Zc} counties plus the external zone. "
      f"Wage unit: state mean non-farm earnings per non-farm worker (ACS head) = {usd:,.0f} $. "
      "w_A,obs is farm labour earnings per farm worker (M2 report, `wA_obs_usd`)"
      + (f"; M3 used BEA farm earnings per BEA farm job and a wage unit per BEA non-farm job ({m3['usd']:,.0f} $). "
         "Section 0 compares the two.\n" if m3 else ".\n"))  # fmt: skip

    w("## Estimates\n")
    w("| Parameter | Estimate | Default | Note |\n|---|---|---|---|")
    w(f"| kappa*lam (per minute) | **{head.kappa_lam:.4f}** (cluster-origin SE {head.se_cluster_origin:.4f}; "
      f"robust {head.se_robust:.4f}; plain Poisson {head.se_plain:.5f}) | 0.08 | PPML, in-state county pairs, own-county flows excluded |")
    w(f"| kappa*lam with own-county flows | {g['in-state, own-county flows included'].kappa_lam:.4f} "
      f"(cluster SE {g['in-state, own-county flows included'].se_cluster_origin:.4f}) | | own time is the M2 area proxy |")
    w(f"| theta_T, state | **{r['theta_hat']:.3f}** | 0.40 | rent bill / (rent bill + farm labour bill w_A,obs H_A) |")
    w(f"| theta_T, county median (IQR) | {np.nanmedian(th_c):.3f} ({np.nanpercentile(th_c, 25):.3f} to {np.nanpercentile(th_c, 75):.3f}) | | same definition |")
    w(f"| over-ID corr(model rho, NASS rent) | {o0['corr']:.3f} (logs {o0['corr_log']:.3f}) | | {o0['n']} published counties |")
    w(f"| over-ID level ratio model/NASS | {o0['level_ratio']:.3f} at theta_T = 0.40; {o1['level_ratio']:.3f} at {r['theta_hat']:.3f} | | farmland-weighted |\n")
    w(f"The {name} parameter set is `urqse.calibrate.run_state.state_params('{st}', {yr})`: `Params()` with "
      f"kappa_lam and theta_T replaced by the values in `src/urqse/calibrate/estimates/{st}_{yr}.json`. "
      "The global defaults in `params.py`, and so the web app's synthetic scenario, are unchanged.\n")

    if m3:
        w("## 0. Farm wage: M3 vs now\n")
        w("M3 = w_A,obs from BEA farm earnings (wages + proprietors' income) per BEA farm job, theta_T from earnings net "
          "of owner land rent. Now = farm labour earnings per farm worker: 5-year mean farm compensation per farm "
          "wage job, applied to every farm job, divided over ACS farm workers; theta_T from the spec §5 labour bill. "
          "Both columns are recomputed in this run from the same county table (`wA_bea_earn_usd` vs `wA_obs_usd`) "
          "and the same kappa*lam. Over-ID rows at theta_T = 0.40.\n")
        w("| | M3 | now |\n|---|---|---|")
        st_old = cdf["farm_earn_usd"].sum() / cdf["HA_bea"].sum()
        st_new = cdf["farm_labour_bill_usd"].sum() / cdf["HA"].sum()
        rows = [
            ("state farm wage, $", f"{st_old:,.0f} per BEA job", f"{st_new:,.0f} per worker ({cdf['farm_labour_bill_usd'].sum() / cdf['HA_bea'].sum():,.0f} per BEA job)"),
            ("county range, $", f"{wA_old.min():,.0f} to {wA_old.max():,.0f}", f"{wA_usd.min():,.0f} to {wA_usd.max():,.0f}"),
            ("farm / non-farm wage (state, same head or job basis)", f"{st_old / m3['usd']:.2f}", f"{st_new / usd:.2f}"),
            ("xi_A median (own wage unit)", f"{np.median(xi3):.3f}", f"{np.median(xi):.3f}"),
            ("xi_A median in M3's per-job unit", f"{np.median(xi3):.3f}", f"{np.median(xi) * m3['usd'] / usd:.3f}"),
            ("xi_A min to max", f"{xi3.min():.3f} to {xi3.max():.3f}", f"{xi.min():.3f} to {xi.max():.3f}"),
            ("s.d. of ln xi_A", f"{np.std(np.log(xi3)):.3f}", f"{np.std(np.log(xi)):.3f}"),
            ("corr(ln xi_A, ln w_A,obs)", f"{np.corrcoef(np.log(xi3), np.log(wA_old))[0, 1]:.3f}", f"{np.corrcoef(np.log(xi), np.log(wA_usd))[0, 1]:.3f}"),
            ("over-ID corr (levels)", f"{o3['corr']:.3f}", f"{o0['corr']:.3f}"),
            ("over-ID corr (logs)", f"{o3['corr_log']:.3f}", f"{o0['corr_log']:.3f}"),
            ("over-ID OLS slope", f"{o3['slope']:.3f}", f"{o0['slope']:.3f}"),
            ("over-ID log-log slope", f"{o3['slope_log']:.3f}", f"{o0['slope_log']:.3f}"),
            ("over-ID level ratio at 0.40", f"{o3['level_ratio']:.3f}", f"{o0['level_ratio']:.3f}"),
            ("over-ID level ratio at the state theta_T", f"{m3['overid'][next(k for k in m3['overid'] if 'estimated' in k)]['level_ratio']:.3f} (theta_T {m3['p'].theta_T:.3f})", f"{o1['level_ratio']:.3f} (theta_T {r['theta_hat']:.3f})"),
            ("s.d. of ln(model/NASS)", f"{o3['sd_log_ratio']:.3f}", f"{o0['sd_log_ratio']:.3f}"),
            ("theta_T state", f"{m3['p'].theta_T:.3f}", f"{r['theta_hat']:.3f}"),
            ("theta_T county median (p10 to p90)", f"{np.median(th3['county']):.3f} ({np.percentile(th3['county'], 10):.3f} to {np.percentile(th3['county'], 90):.3f})",
             f"{np.median(th_c):.3f} ({np.percentile(th_c, 10):.3f} to {np.percentile(th_c, 90):.3f})"),
            ("theta_T county min to max", f"{th3['county'].min():.3f} to {th3['county'].max():.3f}", f"{th_c.min():.3f} to {th_c.max():.3f}"),
            ("counties with theta_T > 1", f"{int((th3['county'] > 1).sum())}", f"{int((th_c > 1).sum())}"),
            ("model farm labour bill w_A H_A, $M", f"{acc3['labour'] / 1e6:,.0f}", f"{acc['labour'] / 1e6:,.0f}"),
            ("model owner-operated land rent omega rho T^F, $M", f"{acc3['owner_rent'] / 1e6:,.0f}", f"{acc['owner_rent'] / 1e6:,.0f}"),
            ("model farm worker income (§12.1 operator income x H_A), $M", f"{acc3['operator'] / 1e6:,.0f}", f"{acc['operator'] / 1e6:,.0f}"),
            ("  / BEA farm earnings 2022", f"{acc3['operator_over_E']:.2f}", f"{acc['operator_over_E']:.2f}"),
            ("labour + owner rent + landlord rent = w_A H_A + rho T^F (rel. error)", f"{acc3['identity_rel']:.0e}", f"{acc['identity_rel']:.0e}"),
        ]  # fmt: skip
        for lab, a, b in rows:
            w(f"| {lab} | {a} | {b} |")
        e_mean = acc["E"] / r["earn_2022_over_mean"]
        n(lambda: f"\n**Operator-income double count.** In M3, w_A H_A already held proprietors' income, owned-land rent "
          f"included, and §12.1 then added omega rho T^F on top ({acc3['owner_rent'] / 1e6:,.0f} $M counted twice); "
          f"model farm worker income came to {acc3['operator_over_E']:.2f}x BEA farm earnings in a record year only because "
          "the M2 job scaling had cut w_A H_A to "
          f"{acc3['labour'] / acc3['E']:.2f} of those earnings. Now w_A H_A is compensation at the hired "
          "rate only, so the land rent enters once. The model's farm worker income is "
          f"{acc['operator'] / 1e6:,.0f} $M against BEA farm earnings of {acc['E'] / 1e6:,.0f} $M in {yr} and "
          f"{e_mean / 1e6:,.0f} $M on the {r['earn_years'][0]} to {r['earn_years'][1]} mean ({acc['operator'] / e_mean:.2f}x). "
          "In 2022 BEA earnings exceed labour at the hired rate plus owned-land cash rent by the rest of proprietors' "
          "income (returns to operators' capital, livestock and the boom); on the 5-year mean they fall short, i.e. operators "
          "earned less than the hired wage plus a market rent on their land in an average year (inferred from these two "
          "totals). The income identity holds to rounding in both.\n")
    else:
        w("## 0. Farm wage: M3 comparison\n")
        w(f"Not computed: BEA farm earnings per farm job are not positive in every county "
          f"({int((wA_old <= 0).sum())} counties at or below 0), so the M3 definition of w_A,obs has no logarithm.\n")

    w("## 1. Inversion fit (spec §5)\n")
    w("| Parameter set | wage contraction | baseline solve | max rel. error HU / HA / wA / N |\n|---|---|---|---|")
    for lab, cal in (("default `Params()`", r["cal0"]), (f"{name} estimates", r["cal"])):
        e = cal.max_rel_error
        wi, bi = cal.wage_info, cal.baseline.info
        w(f"| {lab} | converged={wi.converged}, {wi.iterations} it, residual {wi.residual_inf:.1e} | "
          f"converged={bi.converged}, residual {bi.residual_inf:.1e} | "
          f"{e['HU']:.1e} / {e['HA']:.1e} / {e['wA']:.1e} / {e['N']:.1e} |")
    w(f"\nLargest relative error of the calibrated fundamentals against jobs, farm wages and residents: "
      f"{max(r['cal'].max_rel_error.values()):.1e} (bar 1e-7). Flow offsets: converged={r['cal'].flow_info.converged}, "
      f"residual {r['cal'].flow_info.residual_inf:.1e}.\n")

    w("## 2. Farm-job wedge xi_A\n")
    w(f"![xi_A map]({map_name})\n")
    w("xi_A = (effective farm wage) / (observed farm labour earnings per worker), both in units of mean non-farm "
      "earnings per worker (spec §5 step 2). Its level is pinned by the normalisation that the job-weighted mean non-farm "
      "wage equals 1, so read it relative to the non-farm wedge of 1.\n")
    w("| Group | counties | median xi_A | min | max |\n|---|---|---|---|---|")
    for k in ("core", "suburb", "rural"):
        m = (kind == k) & farm_c
        if not m.any():
            continue
        w(f"| {k} | {m.sum()} | {np.median(xi[m]):.3f} | {xi[m].min():.3f} | {xi[m].max():.3f} |")
    w(f"| all with a farm sector | {int(farm_c.sum())} | {np.nanmedian(xi):.3f} | {np.nanmin(xi):.3f} | {np.nanmax(xi):.3f} |\n")
    if not farm_c.all():
        w(f"{int((~farm_c).sum())} counties have no farm sector (spec §3.11) and no xi_A: "
          f"{', '.join(names[~farm_c])}.\n")
    r_xi = float(np.corrcoef(np.log(xi[farm_c]), np.log(wA_usd[farm_c]))[0, 1])
    n(lambda: f"corr(ln xi_A, ln observed farm wage) = {r_xi:.3f} (M3: "
      f"{np.corrcoef(np.log(xi3), np.log(wA_old))[0, 1]:.3f}). With default kappa*lam = 0.08 the median is "
      f"{np.median(f0.xi_A[c]):.3f}; xi_A depends on kappa*lam through the effective wages, not on theta_T. The "
      "measured farm wage now varies across counties by a factor of "
      f"{wA_usd.max() / wA_usd.min():.1f} (M3: {wA_old.max() / wA_old.min():.1f}), so xi_A is no longer the inverse of "
      "a land-income measure. It still mirrors the measured wage: the effective farm wage that reproduces farm job "
      "counts varies little across counties, so cross-county variation in pay passes into xi_A. Of the log variance "
      f"of the per-worker wage ({np.var(np.log(wA_usd)):.4f}), the per-job wage contributes {np.var(np.log(w_job)):.4f} "
      f"and the conversion to ACS heads (1/scale) {np.var(np.log(m3['scale'])):.4f}. A median below 1 "
      f"({np.median(xi):.2f}) says farm jobs are filled at a lower utility price than their pay would imply relative "
      "to non-farm jobs (amenity of farm work, or the per-head pay "
      "overstating what part-time proprietors earn in farm work). The per-county values are in the county table "
      "at the end.\n")

    w("## 3. Cash-rent over-identification test (spec §5 step 5)\n")
    w("Model rent rho_j = (theta_T/theta_H) w_Aj H_Aj / T^F_j is in wage units per hectare. In dollars per acre: "
      f"rho x {usd:,.0f} $ x 0.40469 ha/acre. NASS: 2022 county cash rent, non-irrigated cropland. "
      f"T^F: CDL cropland. The {int((~pub & farm_c).sum())} counties whose rent NASS did not publish (filled in M2 with the "
      "'other counties' value) are left out of the statistics.\n")
    w("| | theta_T = 0.40 | theta_T estimated |\n|---|---|---|")
    for key, lab, d in (("corr", "correlation (levels)", 3), ("corr_log", "correlation (logs)", 3),
                        ("slope", "OLS slope NASS on model", 3), ("intercept", "OLS intercept, $/acre", 1),
                        ("slope_log", "log-log slope", 3), ("level_ratio", "level ratio model/NASS (farmland-weighted)", 3),
                        ("median_ratio", "median county ratio model/NASS", 3), ("sd_log_ratio", "s.d. of ln(model/NASS)", 3)):  # fmt: skip
        w(f"| {lab} | {_f(o0[key], d)} | {_f(o1[key], d)} |")
    m0 = o0["model"]
    w(f"\nNASS rents span {obs[pub].min():.0f} to {obs[pub].max():.0f} $/acre; model rents at theta_T = 0.40 span "
      f"{m0[pub].min():.0f} to {m0[pub].max():.0f} $/acre. Correlation and log slope do not depend on theta_T "
      "(it scales every county's rent by the same factor).\n")
    n(lambda: f"**Level.** At 0.40 the model rent is {o0['level_ratio']:.2f} of NASS. The model wage bill w_A H_A is now the "
      "farm labour bill in dollars (per-worker wage x workers = per-job wage x BEA jobs), so the M2 job scaling no "
      f"longer shrinks it (M3: {o3['level_ratio']:.2f}, {m3['unscaled_ratio']:.2f} without the scaling). At the "
      f"estimated theta_T = {r['theta_hat']:.3f} the level ratio is {o1['level_ratio']:.2f}: theta_T is fitted to the "
      "same rent bill, up to CDL vs published-county weights.\n")
    n(lambda: "**Pattern.** The sign has flipped: model rent is now lower where NASS rent is higher "
      f"(corr {o0['corr']:.2f}, logs {o0['corr_log']:.2f}; M3 {o3['corr']:.2f}). With a farm wage that varies "
      "little, model rent per hectare is proportional to farm jobs per hectare of CDL cropland, and those are high "
      "in southern Iowa's livestock and pasture counties, where cash rents are lowest. The M3 positive correlation "
      "came from the land and capital returns inside BEA farm earnings, which track land quality by construction. "
      "With T^F = Census of Agriculture land in farms (pasture included) instead of CDL cropland, the log "
      f"correlation of the labour bill per hectare with NASS rent is {r['corr_log_farmland']:.2f}: most of the "
      "negative sign is farm labour that works pasture and livestock, not cropland. The largest deviations from "
      "the median ratio:\n")
    w("| County | kind | NASS $/acre | model $/acre (0.40) | model/NASS | farm wage $/worker | farm jobs per 100 ha T^F |\n|---|---|---|---|---|---|---|")
    idx = np.nonzero(pub)[0][o0["outliers"]]
    HA = r["data"].HA[c]
    TF = r["data"].TF[c]
    for j in idx:
        w(f"| {names[j]} | {kind[j]} | {obs[j]:.0f} | {m0[j]:.0f} | {m0[j] / obs[j]:.2f} | {wA_usd[j]:,.0f} | {100 * HA[j] / TF[j]:.2f} |")
    n(lambda: "\nThe test fails in sign under a labour-only wage and passed in sign in M3 only because land income sat in "
      "the wage. The spec's (F) ties the rent per hectare to labour per hectare with one Cobb-Douglas share; "
      "Iowa's labour intensity per hectare falls with land quality. See §7.\n")

    w("## 4. theta_T from rent shares\n")
    w("From (F), rho T^F = (theta_T/theta_H) x (farm labour bill), so theta_T = rent bill / (rent bill + labour bill). "
      "Rent bill = NASS cash rent x CDL cropland. Labour bill = w_A,obs x H_A, which is now farm labour earnings in "
      "dollars, so the spec §5 literal definition is the chosen one and the M3 netting of owner land rent out of "
      "BEA earnings is no longer needed. The rows below it are sensitivities and the M3 definitions.\n")
    w("| Labour bill | state theta_T | county median | p10 | p90 | min | max |\n|---|---|---|---|---|---|---|")
    for lab, v in th.items():
        q = np.nanpercentile(v["county"], [50, 10, 90])
        w(f"| {lab} | {v['state']:.3f} | {q[0]:.3f} | {q[1]:.3f} | {q[2]:.3f} | {np.nanmin(v['county']):.3f} | {np.nanmax(v['county']):.3f} |")
    e0, e1 = r["earn_years"]
    n(lambda: f"\n**Choice:** state theta_T = **{r['theta_hat']:.3f}** vs the 0.40 default and {m3['p'].theta_T:.3f} in M3. "
      f"{int((th_c > 1).sum())} counties exceed 1 (M3: {int((th3['county'] > 1).sum())}). The single-year row uses {yr} "
      "compensation per wage job instead of the 5-year mean. The CoA row prices every farm job at Census of "
      "Agriculture hired labour expense per BEA farm wage job; that expense is larger than BEA compensation (M2 "
      f"report), so it lowers theta_T. The M3 rows use BEA farm earnings ({e0} to {e1} for the mean row) and are kept "
      "for comparison; they move with the farm-income cycle, the labour bill does not.\n")

    w("## 5. kappa*lam by PPML on LODES\n")
    w(f"LODES8 OD {yr}, JT00 (all jobs), S000, block pairs summed to residence-county x workplace-county. "
      f"Files: `{st.lower()}_od_main`, `{st.lower()}_od_aux` (out-of-state residents working in {st}) and the aux "
      f"files of {', '.join(s.upper() for s in r['neighbor_states'])} ({st} residents working there). "
      f"Out-of-state blocks count only if they lie in the {len(r['ext_counties'])} counties of the M2 external zone, "
      "whose travel time is the time to the nearest of them; other out-of-state blocks are dropped. "
      f"Total flows used: {flows.sum():,.0f}; in-state {flows[:Zc, :Zc].sum():,.0f}, own-county share "
      f"{own_share:.3f}; external zone row {flows[-1].sum():,.0f}, column {flows[:, -1].sum():,.0f}. "
      f"Travel time: `travel.npz` (OSRM car minutes, own-county = M2 area proxy).\n")
    w("ln E[flow_ij] = FE_i + FE_j - kappa*lam t_ij, by Poisson pseudo-ML (Newton, numpy; "
      "`urqse.calibrate.gravity`). SEs: plain = inverse Poisson information (assumes Var = mean; far too small "
      "under overdispersion), robust = Eicker-White HC0, cluster = sandwich clustered by origin county.\n")
    w("| Sample | kappa*lam | SE cluster | SE robust | SE plain | pairs | zeros | pseudo-R2 | converged (residual) |\n"
      "|---|---|---|---|---|---|---|---|---|")
    for lab, v in g.items():
        w(f"| {lab} | {v.kappa_lam:.4f} | {v.se_cluster_origin:.4f} | {v.se_robust:.4f} | {v.se_plain:.5f} | "
          f"{v.n_obs} | {v.n_zero} | {v.pseudo_r2:.3f} | {v.info.converged} ({v.info.residual_inf:.0e}) |")
    cap90, cap60 = g["in-state, off-diagonal, t <= 90 min"], g["in-state, off-diagonal, t <= 60 min"]
    if not iowa:
        w(f"\nRestricted to pairs within 90 minutes kappa*lam is {cap90.kappa_lam:.4f}, within 60 minutes {cap60.kappa_lam:.4f}.\n")
    n(lambda: f"\nThe headline {head.kappa_lam:.4f} per minute is about {head.kappa_lam / 0.08:.0%} of the 0.08 default. "
      "The exponential-in-minutes form does not fit all trip lengths with one slope: restricted to pairs within 90 "
      f"minutes it is {cap90.kappa_lam:.4f}, within 60 minutes {cap60.kappa_lam:.4f}, close to the default. Long "
      "pairs (median in-state off-diagonal time "
      f"{np.median(r['data'].t[:Zc, :Zc][~np.eye(Zc, dtype=bool)]):.0f} min) carry more flow than a steep exponential "
      "allows (weekly commuters, multi-site employers, LODES assigning jobs to a firm's reporting address are "
      "candidate reasons, not tested). Including own-county flows gives "
      f"{g['in-state, own-county flows included'].kappa_lam:.4f}: the {own_share:.0%} of workers who stay in their "
      "county pin the slope at the short end through the area-based own-time proxy, so that number is partly a "
      "property of the proxy. The headline is the spec's specification on all off-diagonal pairs; the model uses one "
      "kappa*lam for every pair including own, so this choice matters for counterfactuals. `# VERIFY`.\n")

    w("## 6. Saved outputs\n")
    w(f"- `data/{st}/{yr}/calibrated.npz` (git-ignored): fips, every `Fundamentals` field, the baseline N, wU, wA, r, "
      f"rho, the Params used (JSON), and $ per wage unit. Calibrated with the {name} estimates.")
    w(f"- `src/urqse/calibrate/estimates/{st}_{yr}.json` (tracked): kappa_lam and theta_T with sources.")
    w(f"- `tests/snapshots/{st}_{yr}.json` (tracked): pinned summary numbers; `tests/test_snapshot_iowa.py` "
      "skips when the data are absent.")
    w(f"- `reports/{map_name}`: the xi_A map.\n")

    n(lambda: "## 7. What looks wrong or uncertain\n")
    n(lambda: f"1. **Over-ID fails in sign under a labour-only wage** (log corr {o0['corr_log']:.2f}, M3 {o3['corr_log']:.2f}). "
      "Rent per hectare in (F) is proportional to labour per hectare, which in Iowa is highest in pasture and livestock "
      f"counties with the lowest cash rents. Counting pasture in T^F turns the log correlation to {r['corr_log_farmland']:.2f}. "
      "Candidates, not tested here: T^F = land in farms or cropland + pasture weighted by rent; a county land-quality "
      "shifter in the farm production function (spec change, not made); rents taken from NASS directly when M4 "
      "prices land. The state rent level pins theta_T; the cross-county rent pattern from (F) is not usable, and "
      "the county theta_T column inherits the same labour-per-hectare pattern.")
    n(lambda: "2. **Proprietor labour is imputed** at the hired wage per BEA wage job. A BEA proprietor job is any sole "
      "proprietor or partner, many part-time, and after the ACS scaling the per-worker wage is highest where the "
      f"scaling cut most farm jobs (county max {wA_usd.max():,.0f} $). `# VERIFY` against ARMS operator hours if needed.")
    n(lambda: "3. **Two hired-labour sources disagree.** Census of Agriculture hired labour expense is "
      f"{cdf['hired_labor_coa_usd'].sum() / cdf['farm_comp_usd'].sum():.2f}x BEA farm compensation in {yr} (M2 report). BEA is used because its jobs are the ones H_A counts; with the CoA level "
      f"theta_T would be {th[next(k for k in th if k.startswith('CoA'))]['state']:.3f}. `# VERIFY`.")
    n(lambda: f"4. **kappa*lam is {head.kappa_lam / 0.08:.0%} of the default on all pairs** but {cap60.kappa_lam:.3f} on "
      "pairs within an hour, and it rises with own-county flows. The semi-elasticity is not constant in minutes, so a "
      "single kappa*lam is a compromise: the headline fits long-distance flows, the capped estimates fit the "
      "commutes a travel-time cut would change. A log-time or piecewise decay is the fix if M4/M5 counterfactuals "
      "lean on it.")
    n(lambda: f"5. **theta_T** by county ranges {th_c.min():.2f} to {th_c.max():.2f}, none above 1; the single-year and 5-year "
      f"wage rows differ by {abs(th[next(k for k in th if k.startswith('same, single'))]['state'] - r['theta_hat']):.3f}. "
      "All estimates are tagged `verify` in the estimates JSON.")
    n(lambda: "6. The external zone's LODES flows cover only the 39 border counties (Iowa residents working there come "
      "from six neighbour-state aux files) and its travel time is to the nearest of them, so it is a convention, "
      "not a place; it is left out of the headline and changes kappa*lam little.\n")

    w("## County table\n")
    w("Model rent at theta_T = 0.40. theta_T by county under the chosen definition. `*` = NASS rent filled in M2.\n")
    w("| FIPS | Name | Kind | xi_A | xi_A (M3) | NASS rent $/ac | model rent $/ac | model/NASS | theta_T | farm wage $/worker | BEA farm earnings $/job | N |\n"
      "|---|---|---|---|---|---|---|---|---|---|---|---|")
    for j in range(Zc):
        star = "" if pub[j] else "*"
        if not farm_c[j]:
            w(f"| {r['fips'][j]} | {names[j]} | {kind[j]} | no farm sector | | | | | | | | {N[j]:,.0f} |")
            continue
        w(f"| {r['fips'][j]} | {names[j]} | {kind[j]} | {xi[j]:.3f} | {xi3[j]:.3f} | {obs[j]:.0f}{star} | {m0[j]:.0f} | "
          f"{m0[j] / obs[j]:.2f} | {th_c[j]:.3f} | {wA_usd[j]:,.0f} | {wA_old[j]:,.0f} | {N[j]:,.0f} |")
    (out_dir / f"{st}_{yr}_CALIBRATION.md").write_text("\n".join(L) + "\n")
