"""Download and build all data used by the Demography Pyramid web app.

Run from the repo root:  python3 scripts/build_data.py
Raw downloads are cached in data_raw/ (git-ignored); outputs go to docs/data/.

Sources
  * UN World Population Prospects 2024 - population on 1 January by single age and sex,
    1950-2023 (estimates) and 2024-2100 (medium variant).
  * World Bank WDI API - GDP, health expenditure (total / government / out-of-pocket),
    social contributions, life expectancy, ...
  * ILOSTAT - labour income share, employment-to-population ratios by 10-year age band,
    SDG 1.3.1 pension coverage.
  * OECD - Pensions at a Glance (retirement age, public pension spending, average wage),
    SOCX public old-age cash spending.
  * scripts/curated_pensions.csv - approximate mandatory pension contribution rates.
"""
import csv
import gzip
import io
import json
import os
import statistics
import subprocess
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data_raw")
OUT = os.path.join(ROOT, "docs", "data")

WPP_BASE = "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/"
WPP_FILES = [
    "WPP2024_Population1JanuaryBySingleAgeSex_Medium_1950-2023.csv.gz",
    "WPP2024_Population1JanuaryBySingleAgeSex_Medium_2024-2100.csv.gz",
]
KEEP_LOC_TYPES = {"Country/Area", "World", "Geographic region", "Subregion", "SDG region",
                  "Income group", "Development group"}

WB_INDICATORS = {
    "gdp": "NY.GDP.MKTP.CD",
    "gdp_pc": "NY.GDP.PCAP.CD",
    "gdp_pc_ppp": "NY.GDP.PCAP.PP.CD",
    "health_pc": "SH.XPD.CHEX.PC.CD",
    "health_gov_pc": "SH.XPD.GHED.PC.CD",
    "health_oop_pc": "SH.XPD.OOPC.PC.CD",
    "health_gdp": "SH.XPD.CHEX.GD.ZS",
    "soc_contrib_rev": "GC.REV.SOCL.ZS",   # social contributions, % of revenue
    "revenue_gdp": "GC.REV.XGRT.GD.ZS",    # revenue excl. grants, % of GDP
    "life_exp": "SP.DYN.LE00.IN",
    "emp_pop_15": "SL.EMP.TOTL.SP.ZS",
}
OECD_FLOWS = {
    "pag": "OECD.ELS.SPD,DSD_PAG@DF_PAG,",
    "socx_old": "OECD.ELS.SPD,DSD_SOCX_AGG@DF_PUB_OLD,",
}
ILO_IND = {
    "labour_share": "LAP_2GDP_NOC_RT_A",
    "emp_age": "EMP_DWAP_SEX_AGE_RT_A",
    "emp_model": "EMP_2WAP_SEX_AGE_RT_A",
    "coverage": "SDG_0131_SEX_SOC_RT_A",
}
LATEST = 2025  # ignore projections beyond this year in economic series


def fetch(url, path, headers=None):
    """Download url to path once (uses curl: avoids macOS Python certificate issues)."""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    print("  downloading", url)
    cmd = ["curl", "-sSfL", "--retry", "3", "--max-time", "900", "-o", path + ".part", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    subprocess.run(cmd, check=True)
    os.replace(path + ".part", path)
    return path


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- population
def build_population():
    print("WPP population")
    pop = defaultdict(lambda: defaultdict(lambda: ([0] * 101, [0] * 101)))
    meta = {}
    for fn in WPP_FILES:
        path = fetch(WPP_BASE + fn, os.path.join(RAW, fn))
        with gzip.open(path, "rt", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r["LocTypeName"] not in KEEP_LOC_TYPES:
                    continue
                loc = int(r["LocID"])
                if loc not in meta:
                    meta[loc] = {
                        "id": loc, "name": r["Location"], "iso3": r["ISO3_code"] or None,
                        "type": r["LocTypeName"], "parent": int(r["ParentID"]) if r["ParentID"] else None,
                    }
                age = int(r["AgeGrpStart"])
                m, fm = pop[loc][int(r["Time"])]
                m[age] = round(float(r["PopMale"]) * 1000)
                fm[age] = round(float(r["PopFemale"]) * 1000)
    os.makedirs(os.path.join(OUT, "pop"), exist_ok=True)
    for loc, years in pop.items():
        ys = sorted(years)
        doc = {"y0": ys[0], "m": [years[y][0] for y in ys], "f": [years[y][1] for y in ys]}
        with open(os.path.join(OUT, "pop", f"{loc}.json"), "w") as f:
            json.dump(doc, f, separators=(",", ":"))
        meta[loc]["pop2025"] = sum(years[2025][0]) + sum(years[2025][1]) if 2025 in years else None
        # 5-yearly summary used to colour the world map without loading every pyramid
        summ = {"pop": [], "med": [], "s65": []}
        for y in range(1950, 2101, 5):
            tot = [a + b for a, b in zip(*years[y])]
            n = sum(tot)
            acc, med = 0, 0
            for age, v in enumerate(tot):
                if acc + v >= n / 2:
                    med = age + (n / 2 - acc) / v if v else age
                    break
                acc += v
            summ["pop"].append(n)
            summ["med"].append(round(med, 1))
            summ["s65"].append(round(100 * sum(tot[65:]) / n, 2) if n else 0)
        meta[loc]["summary"] = summ
    return meta


# ---------------------------------------------------------------- world bank
def latest_by_country(rows):
    """rows: iterable of (iso3, year, value) -> {iso3: (value, year)} with year <= LATEST."""
    best = {}
    for iso, y, v in rows:
        if v is None or not iso or int(y) > LATEST:
            continue
        if iso not in best or int(y) > best[iso][1]:
            best[iso] = (v, int(y))
    return best


def build_worldbank():
    print("World Bank")
    out = {}
    for key, ind in WB_INDICATORS.items():
        path = os.path.join(RAW, f"wb_{ind}.json")
        fetch(f"https://api.worldbank.org/v2/country/all/indicator/{ind}?format=json&per_page=20000&date=2005:{LATEST}", path)
        data = json.load(open(path))[1] or []
        out[key] = latest_by_country((d["countryiso3code"], d["date"], d["value"]) for d in data)
    return out


# ---------------------------------------------------------------- ILO
def read_ilo(key):
    ind = ILO_IND[key]
    path = os.path.join(RAW, f"ilo_{ind}.csv")
    url = f"https://rplumber.ilo.org/data/indicator/?id={ind}&format=.csv"
    if key == "emp_age":
        url += "&classif1=AGE_10YRBANDS"
    fetch(url, path)
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def build_ilo():
    print("ILO")
    res = {}
    rows = read_ilo("labour_share")
    res["labour_share"] = latest_by_country((r["ref_area"], r["time"], num(r["obs_value"])) for r in rows)

    rows = read_ilo("coverage")
    res["pension_coverage"] = latest_by_country(
        (r["ref_area"], r["time"], num(r["obs_value"])) for r in rows
        if r["sex"] == "SEX_T" and r["classif1"] == "SOC_CONTIG_PENSION")

    # employment-to-population ratio by 10-year age band, both sexes + by sex, latest year
    bands = ["Y15-24", "Y25-34", "Y35-44", "Y45-54", "Y55-64", "YGE65"]
    by = defaultdict(dict)  # (iso, sex) -> {year: {band: v}}
    for r in read_ilo("emp_age"):
        b = r["classif1"].replace("AGE_10YRBANDS_", "")
        v = num(r["obs_value"])
        if b in bands and v is not None and int(r["time"]) <= LATEST:
            by[(r["ref_area"], r["sex"])].setdefault(int(r["time"]), {})[b] = v
    emp = {}
    for (iso, sex), yrs in by.items():
        full = [y for y, d in yrs.items() if len(d) == len(bands) and y >= LATEST - 12]
        if not full:
            continue
        y = max(full)
        emp.setdefault(iso, {"year": y})[{"SEX_T": "t", "SEX_M": "m", "SEX_F": "f"}.get(sex, sex)] = [
            round(yrs[y][b], 1) for b in bands]
    # modelled fallback: 15-24 and 25+ only
    model = defaultdict(dict)
    for r in read_ilo("emp_model"):
        if r["sex"] == "SEX_T" and r["time"] == "2024":
            model[r["ref_area"]][r["classif1"].replace("AGE_YTHADULT_", "")] = num(r["obs_value"])
    res["emp_age"] = emp
    res["emp_model"] = model
    return res


# ---------------------------------------------------------------- OECD
def build_oecd():
    print("OECD")
    res = {"ret_m": {}, "ret_f": {}, "ret_future_m": {}, "pension_gdp": {}, "avg_wage": {}, "socx_old": {}}
    meas = {"CRPLF22": None, "FRPLF22": None, "PEP": "pension_gdp", "AWGW": "avg_wage"}
    for key, flow in OECD_FLOWS.items():
        path = os.path.join(RAW, f"oecd_{key}.csv")
        fetch(f"https://sdmx.oecd.org/public/rest/data/{flow}/all?dimensionAtObservation=AllDimensions",
              path, {"Accept": "application/vnd.sdmx.data+csv; charset=utf-8"})
        with open(path, encoding="utf-8-sig") as f:
            # the API may return "CODE: Label" headers/cells; keep the codes only
            rows = [{k.split(":")[0]: (c.split(":")[0] if k != "DATAFLOW" else c) for k, c in r.items()}
                    for r in csv.DictReader(f)]
        for r in rows:
            v = num(r["OBS_VALUE"])
            if v is None:
                continue
            iso, y, m, unit = r["REF_AREA"], int(r["TIME_PERIOD"]), r["MEASURE"], r["UNIT_MEASURE"]
            if key == "pag":
                if m == "CRPLF22" and r["SEX"] in ("M", "F"):
                    res["ret_" + r["SEX"].lower()][iso] = v
                elif m == "FRPLF22" and r["SEX"] == "M":
                    res["ret_future_m"][iso] = v
                elif m == "PEP" and unit == "PT_B1GQ":
                    if iso not in res["pension_gdp"] or y > res["pension_gdp"][iso][1]:
                        res["pension_gdp"][iso] = (v, y)
                elif m == "AWGW" and unit == "USD_EXC":
                    res["avg_wage"][iso] = (v, y)
            elif unit == "PT_B1GQ" and y <= LATEST:
                if iso not in res["socx_old"] or y > res["socx_old"][iso][1]:
                    res["socx_old"][iso] = (v, y)
    return res


def read_curated():
    path = os.path.join(ROOT, "scripts", "curated_pensions.csv")
    with open(path) as f:
        lines = [l for l in f if not l.startswith("#")]
    return {r["iso3"]: r for r in csv.DictReader(io.StringIO("".join(lines)))}


# ---------------------------------------------------------------- assemble
def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    meta = build_population()
    wb = build_worldbank()
    ilo = build_ilo()
    oecd = build_oecd()
    cur = read_curated()

    econ = {}
    for loc, m in meta.items():
        iso = m["iso3"]
        if m["type"] != "Country/Area" or not iso:
            continue
        e = {"src": {}}

        def put(name, pair, src, scale=1.0):
            if pair:
                e[name] = round(pair[0] * scale, 4)
                e["src"][name] = f"{src} {pair[1]}"

        for k in WB_INDICATORS:
            put(k, wb[k].get(iso), "World Bank")
        if "soc_contrib_rev" in e and "revenue_gdp" in e:
            e["soc_contrib_gdp"] = round(e["soc_contrib_rev"] * e["revenue_gdp"] / 100, 3)
            e["src"]["soc_contrib_gdp"] = "World Bank (derived)"
        put("labour_share", ilo["labour_share"].get(iso), "ILO modelled")
        put("pension_coverage", ilo["pension_coverage"].get(iso), "ILO SDG 1.3.1")
        if iso in ilo["emp_age"]:
            e["emp_age"] = ilo["emp_age"][iso]
            e["src"]["emp_age"] = f"ILO LFS {ilo['emp_age'][iso]['year']}"
        elif iso in ilo["emp_model"]:
            mm = ilo["emp_model"][iso]
            y, a = mm.get("Y15-24"), mm.get("YGE25")
            if y is not None and a is not None:
                e["emp_age"] = {"year": 2024, "t": [y, a * 1.05, a * 1.08, a * 1.05, a * 0.85, a * 0.3]}
                e["src"]["emp_age"] = "ILO modelled 2024 (15-24/25+, age shape assumed)"

        # pension spending % GDP: OECD PaG > SOCX old-age cash > curated
        if iso in oecd["pension_gdp"]:
            put("pension_gdp", oecd["pension_gdp"][iso], "OECD Pensions at a Glance")
        elif iso in oecd["socx_old"]:
            put("pension_gdp", oecd["socx_old"][iso], "OECD SOCX old-age cash")
        elif cur.get(iso, {}).get("pension_spend_gdp"):
            e["pension_gdp"] = float(cur[iso]["pension_spend_gdp"])
            e["src"]["pension_gdp"] = "curated approx."
        if iso in oecd["ret_m"]:
            e["ret_m"], e["ret_f"] = oecd["ret_m"][iso], oecd["ret_f"].get(iso, oecd["ret_m"][iso])
            e["src"]["ret_age"] = "OECD PaG 2023 (current, entry at 22)"
            if iso in oecd["ret_future_m"]:
                e["ret_future"] = oecd["ret_future_m"][iso]
        elif cur.get(iso, {}).get("ret_age_m"):
            e["ret_m"], e["ret_f"] = float(cur[iso]["ret_age_m"]), float(cur[iso]["ret_age_f"])
            e["src"]["ret_age"] = "curated approx."
        if iso in oecd["avg_wage"]:
            put("avg_wage", oecd["avg_wage"][iso], "OECD average worker wage (USD)")
        if iso in cur:
            c = cur[iso]
            e["contrib_ee"], e["contrib_er"] = float(c["contrib_employee"]), float(c["contrib_employer"])
            e["src"]["contrib"] = "curated approx. (OECD PaG / SSA SSPTW)" + (f" - {c['note']}" if c["note"] else "")
        econ[iso] = e

    # fallback estimate of pension spending where nothing is known:
    # spending/GDP = kappa * coverage * share of pop aged 65+, kappa = median over known countries
    def share65(loc):
        d = json.load(open(os.path.join(OUT, "pop", f"{loc}.json")))
        i = 2023 - d["y0"]
        tot = sum(d["m"][i]) + sum(d["f"][i])
        return (sum(d["m"][i][65:]) + sum(d["f"][i][65:])) / tot

    iso2loc = {m["iso3"]: loc for loc, m in meta.items() if m["iso3"] and m["type"] == "Country/Area"}
    ks = []
    for iso, e in econ.items():
        if "pension_gdp" in e and e.get("pension_coverage"):
            ks.append(e["pension_gdp"] / (e["pension_coverage"] / 100 * share65(iso2loc[iso]) * 100))
    kappa = statistics.median(ks)
    print(f"  pension kappa (spend%GDP per covered 65+ %pop) = {kappa:.3f} from {len(ks)} countries")
    for iso, e in econ.items():
        if "pension_gdp" not in e:
            cov = (e.get("pension_coverage") or 30) / 100
            e["pension_gdp"] = round(kappa * cov * share65(iso2loc[iso]) * 100, 2)
            e["src"]["pension_gdp"] = "estimated from ILO coverage x 65+ share"

    summary = {loc: m.pop("summary") for loc, m in meta.items()}
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump({"years": list(range(1950, 2101, 5)), "loc": summary}, f, separators=(",", ":"))
    locs = sorted(meta.values(), key=lambda m: (m["type"] != "World", m["type"] != "Country/Area", m["name"]))
    with open(os.path.join(OUT, "locations.json"), "w") as f:
        json.dump(locs, f, separators=(",", ":"), ensure_ascii=False)
    with open(os.path.join(OUT, "econ.json"), "w") as f:
        json.dump(econ, f, separators=(",", ":"), ensure_ascii=False)
    print(f"done: {len(locs)} locations, {len(econ)} countries with economic data")


if __name__ == "__main__":
    main()
