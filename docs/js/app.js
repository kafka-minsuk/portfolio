/* Demography Pyramids — population, value added and retirement costs by birth year. */
const BASE = 2025;          // calibration year for all economic data
const AGES = 101;           // 0..99 and 100+
const BIG_GROUP = 40;       // auto-load at most this many member countries for an aggregate

const PRESETS = {
  "G7": "USA JPN DEU GBR FRA ITA CAN",
  "G20 (countries)": "ARG AUS BRA CAN CHN FRA DEU IND IDN ITA JPN KOR MEX RUS SAU ZAF TUR GBR USA",
  "EU-27": "AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE",
  "OECD-38": "AUS AUT BEL CAN CHL COL CRI CZE DNK EST FIN FRA DEU GRC HUN ISL IRL ISR ITA JPN KOR LVA LTU LUX MEX NLD NZL NOR POL PRT SVK SVN ESP SWE CHE TUR GBR USA",
  "BRICS (2025)": "BRA RUS IND CHN ZAF EGY ETH IRN ARE IDN",
  "ASEAN": "BRN KHM IDN LAO MYS MMR PHL SGP THA VNM",
  "China + Japan + Korea": "CHN JPN KOR",
  "Nordics": "DNK FIN ISL NOR SWE",
};

// relative per-capita health cost by age (1 ≈ prime-age adult); typical OECD/EU Ageing Report shape
const HEALTH_CURVE = [[0, 1.6], [1, 0.7], [5, 0.45], [15, 0.5], [25, 0.6], [35, 0.7], [45, 0.95], [55, 1.35], [65, 2.0], [75, 3.0], [85, 4.0], [100, 4.4]];
// age–earnings (experience) profile
const AGE_PROD_CURVE = [[15, 0.45], [20, 0.6], [25, 0.8], [30, 0.92], [40, 1.05], [50, 1.1], [55, 1.08], [60, 1.0], [65, 0.9], [75, 0.75], [100, 0.6]];

const PROD_PRESETS = {
  flat: [{ b: 1900, m: 1 }, { b: 2100, m: 1 }],
  edu: [1920, 1940, 1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100].map(b => ({ b, m: +Math.min(3, Math.max(0.3, 1.01 ** (b - 1980))).toFixed(3) })),
  ai: [{ b: 1900, m: 1 }, { b: 1995, m: 1 }, { b: 2005, m: 1.3 }, { b: 2020, m: 1.5 }, { b: 2100, m: 1.5 }],
};
const SHOCK_PRESETS = {
  war: { year: 2030, dur: 3, a0: 18, a1: 45, sex: "m", pct: -5, label: "War" },
  pandemic: { year: 2030, dur: 1, a0: 70, a1: 100, sex: "b", pct: -5, label: "Pandemic" },
  baby: { year: 2030, dur: 10, a0: 0, a1: 0, sex: "b", pct: -30, label: "Birth slump" },
  migr: { year: 2030, dur: 10, a0: 20, a1: 35, sex: "b", pct: 2, label: "Immigration" },
};

const EDIT_FIELDS = [
  // key, header, title
  ["ret_m", "Ret. age M", "Statutory retirement age, men"],
  ["ret_f", "Ret. age F", "Statutory retirement age, women"],
  ["pension_gdp", "Pension % GDP", "Public pension spending, % of GDP"],
  ["pension_coverage", "Coverage %", "Share of people above pensionable age receiving a pension (ILO SDG 1.3.1); also used as share of workers contributing"],
  ["contrib_ee", "Contrib. EE %", "Mandatory pension contribution, employee, % of gross wage"],
  ["contrib_er", "Contrib. ER %", "Mandatory pension contribution, employer, % of gross wage"],
  ["labour_share", "Labour share %", "Labour income share of GDP (ILO)"],
  ["contrib_base", "Contrib. base %", "Share of labour income actually subject to pension contributions (ceilings, self-employment, informality). Default assumption 70%"],
  ["health_pc", "Health $/cap", "Current health expenditure per capita, US$"],
  ["health_gov_share", "Gov. health %", "Government share of health spending"],
];

// ------------------------------------------------------------------ state
const S = {
  sel: [], year: 2025, bin: 5, units: "pct", rightMode: "va", showBase: true,
  retMode: "country", retShift: 0, retUniform: 65,
  shocks: [], prod: PROD_PRESETS.flat.map(p => ({ ...p })), ageProfile: true, growth: 1.0, index: "wage",
  edits: load("dp.edits", {}), mapMetric: "s65", allowBig: new Set(),
};
const D = { locs: [], byId: new Map(), byIso: new Map(), econ: {}, summary: null, pop: new Map(), children: new Map() };

function load(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } }
function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage unavailable */ } }
const $ = id => document.getElementById(id);
const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
function interp(points, x) {
  if (x <= points[0][0]) return points[0][1];
  for (let i = 1; i < points.length; i++) {
    const [x1, y1] = points[i];
    if (x <= x1) { const [x0, y0] = points[i - 1]; return y0 + (y1 - y0) * (x - x0) / (x1 - x0); }
  }
  return points[points.length - 1][1];
}
const HEALTH_REL = Array.from({ length: AGES }, (_, a) => interp(HEALTH_CURVE, a));
const AGE_PROD = Array.from({ length: AGES }, (_, a) => interp(AGE_PROD_CURVE, a));

// ------------------------------------------------------------------ formatting
const fmtPct = (v, d = 1) => (v == null || !isFinite(v)) ? "–" : `${v.toFixed(d)}%`;
function fmtMoney(v) {
  if (v == null || !isFinite(v)) return "–";
  const a = Math.abs(v), s = v < 0 ? "−" : "";
  if (a >= 1e12) return `${s}$${(a / 1e12).toFixed(2)} tn`;
  if (a >= 1e9) return `${s}$${(a / 1e9).toFixed(1)} bn`;
  if (a >= 1e6) return `${s}$${(a / 1e6).toFixed(1)} m`;
  if (a >= 1e3) return `${s}$${(a / 1e3).toFixed(1)}k`;
  return `${s}$${a.toFixed(0)}`;
}
function fmtNum(v) {
  if (v == null || !isFinite(v)) return "–";
  const a = Math.abs(v);
  if (a >= 1e9) return `${(v / 1e9).toFixed(2)} bn`;
  if (a >= 1e6) return `${(v / 1e6).toFixed(2)} m`;
  if (a >= 1e3) return `${(v / 1e3).toFixed(1)}k`;
  return v.toFixed(0);
}

// ------------------------------------------------------------------ data loading
async function getJSON(url) { const r = await fetch(url); if (!r.ok) throw new Error(url); return r.json(); }
function loadPop(id) {
  if (!D.pop.has(id)) D.pop.set(id, getJSON(`data/pop/${id}.json`).then(d => (D.pop.set(id, d), d)));
  return D.pop.get(id);
}
const popReady = id => { const p = D.pop.get(id); return p && !(p instanceof Promise) ? p : null; };

function membersOf(id) {
  const loc = D.byId.get(id);
  if (!loc) return [];
  if (loc.type === "Country/Area") return [id];
  if (!["World", "Geographic region", "Subregion"].includes(loc.type)) return null; // membership unknown
  if (loc.type === "World") return D.locs.filter(l => l.type === "Country/Area").map(l => l.id);
  const out = [], walk = pid => (D.children.get(pid) || []).forEach(c => {
    const l = D.byId.get(c); if (l.type === "Country/Area") out.push(c); else walk(c);
  });
  walk(id);
  return out;
}

// ------------------------------------------------------------------ population with shocks
function rawPop(id, year) {
  const d = popReady(id); if (!d) return null;
  const i = clamp(year, d.y0, d.y0 + d.m.length - 1) - d.y0;
  return { m: d.m[i], f: d.f[i] };
}
function shockFactor(age, year, sex) {
  let f = 1;
  const b = year - age;
  for (const s of S.shocks) {
    if (s.sex !== "b" && s.sex !== sex) continue;
    const end = Math.min(s.year + s.dur - 1, year);
    for (let t = s.year; t <= end; t++) {
      const a = t - b;
      if (a >= s.a0 && a <= s.a1) f *= 1 + s.pct / 100;
    }
  }
  return f;
}
function shockedPop(id, year) {
  const p = rawPop(id, year); if (!p) return null;
  if (!S.shocks.length) return p;
  const m = new Array(AGES), f = new Array(AGES);
  for (let a = 0; a < AGES; a++) { m[a] = p.m[a] * shockFactor(a, year, "m"); f[a] = p.f[a] * shockFactor(a, year, "f"); }
  return { m, f };
}

// ------------------------------------------------------------------ economic model
let prodPts = null;
function refreshProd() { prodPts = [...S.prod].sort((x, y) => x.b - y.b).map(p => [p.b, p.m]); }
function cohortProd(b) { return prodPts.length ? interp(prodPts, b) : 1; }
function param(iso, k) {
  const e = S.edits[iso];
  if (e && e[k] != null && e[k] !== "") return +e[k];
  const c = D.econ[iso] || {};
  if (k === "health_gov_share") return c.health_gov_pc != null && c.health_pc ? 100 * c.health_gov_pc / c.health_pc : null;
  return c[k] ?? null;
}
// employment-to-population ratio by single age (index 0..5 bands: 15-24 … 65+)
function empBands(iso, sex) {
  const e = D.econ[iso]?.emp_age;
  const fallback = [40, 70, 75, 72, 55, 15];
  if (!e) return fallback;
  return e[sex] || e.t || fallback;
}
const bandOf = a => a < 15 ? -1 : a < 25 ? 0 : a < 35 ? 1 : a < 45 ? 2 : a < 55 ? 3 : a < 65 ? 4 : 5;
const retFrac = (a, R) => clamp(a + 1 - R, 0, 1);
function retAges(iso) {
  const m0 = param(iso, "ret_m") ?? 62, f0 = param(iso, "ret_f") ?? m0;
  if (S.retMode === "uniform") return { m: S.retUniform, f: S.retUniform, m0, f0 };
  return { m: m0 + S.retShift, f: f0 + S.retShift, m0, f0 };
}
/** per-age employment split into: working before retirement (contributing) and working after retirement */
function empProfile(iso, sex, R) {
  const bands = empBands(iso, sex === "m" ? "m" : "f").map(v => v / 100);
  const pre = new Array(AGES), post = new Array(AGES);
  for (let a = 0; a < AGES; a++) {
    const bi = bandOf(a), r = retFrac(a, R);
    const work = bi < 0 ? 0 : (a >= 55 ? bands[4] : bands[bi]);
    pre[a] = (1 - r) * work;
    post[a] = r * (bi < 0 ? 0 : bands[5]);
  }
  return { pre, post };
}

const calibCache = new Map();
function calibration(iso, id) {
  const key = `${iso}|${S.ageProfile}|${JSON.stringify(S.edits[iso] || {})}`;
  if (calibCache.has(key)) return calibCache.get(key);
  const c = D.econ[iso], p = rawPop(id, BASE);
  if (!c || !p || !c.gdp) return null;
  const gdp = c.gdp, R = retAges(iso), ap = a => (S.ageProfile ? AGE_PROD[a] : 1);
  const em = empProfile(iso, "m", R.m0), ef = empProfile(iso, "f", R.f0);
  let eff = 0, effPre = 0, ret = 0, pop = 0, hw = 0;
  const cov = clamp((param(iso, "pension_coverage") ?? 50) / 100, 0.01, 1);
  for (let a = 0; a < AGES; a++) {
    eff += (p.m[a] * (em.pre[a] + em.post[a]) + p.f[a] * (ef.pre[a] + ef.post[a])) * ap(a);
    effPre += (p.m[a] * em.pre[a] + p.f[a] * ef.pre[a]) * ap(a);
    ret += p.m[a] * retFrac(a, R.m0) + p.f[a] * retFrac(a, R.f0);
    pop += p.m[a] + p.f[a];
    hw += (p.m[a] + p.f[a]) * HEALTH_REL[a];
  }
  const ls = (param(iso, "labour_share") ?? 50) / 100;
  const vaPerEff = gdp / eff, wagePerEff = ls * vaPerEff;
  const pensionGdp = (param(iso, "pension_gdp") ?? 0) / 100;
  const P0 = ret > 0 ? pensionGdp * gdp / (ret * cov) : 0;
  let ee = param(iso, "contrib_ee"), er = param(iso, "contrib_er"), contribSrc = "curated";
  const base = clamp((param(iso, "contrib_base") ?? 70) / 100, 0, 1);
  if (ee == null && er == null) {
    if (c.soc_contrib_gdp) {
      // assume half of all social contributions go to pensions
      const rate = 0.5 * c.soc_contrib_gdp / 100 * gdp / (wagePerEff * effPre * cov * base);
      ee = 100 * rate / 3; er = 100 * rate * 2 / 3; contribSrc = "estimated from social contributions (World Bank)";
    } else { ee = 0; er = 0; contribSrc = "unknown — assumed tax-financed"; }
  }
  // sanity cap: pension contributions cannot exceed 70% of all social contributions (World Bank)
  let baseAdj = base;
  if (c.soc_contrib_gdp && param(iso, "contrib_base") == null && S.edits[iso]?.contrib_base == null) {
    const raw = wagePerEff * effPre * (ee + er) / 100 * base * cov, cap = 0.7 * c.soc_contrib_gdp / 100 * gdp;
    if (raw > cap) { baseAdj = base * cap / raw; contribSrc += ` · base capped at 70% of social contributions`; }
  }
  const hpc = param(iso, "health_pc") ?? (c.gdp_pc ? c.gdp_pc * 0.06 : 0);
  const gov = clamp((param(iso, "health_gov_share") ?? 50) / 100, 0, 1);
  const oop = c.health_oop_pc != null && c.health_pc ? clamp(c.health_oop_pc / c.health_pc, 0, 1 - gov) : (1 - gov) * 0.6;
  const out = {
    gdp, vaPerEff, wagePerEff, P0, cov, ee: ee / 100, er: er / 100, contribSrc, base: baseAdj,
    hk: hpc * pop / hw, gov, oop,
  };
  // average wage per worker (head count) for display
  let workers = 0;
  for (let a = 0; a < AGES; a++) workers += p.m[a] * (em.pre[a] + em.post[a]) + p.f[a] * (ef.pre[a] + ef.post[a]);
  out.avgWage = ls * gdp / workers;
  calibCache.set(key, out);
  return out;
}

const SERIES_KEYS = ["pop", "va", "contrib", "pension", "health", "prod"];
function emptyAgeArrays() {
  const o = {}; for (const k of SERIES_KEYS) o[k] = { m: new Float64Array(AGES), f: new Float64Array(AGES) }; return o;
}
function emptyTotals() {
  return { pop: 0, gdp: 0, pension: 0, contrib: 0, contribEE: 0, contribER: 0, health: 0, healthRet: 0, healthRetGov: 0,
    healthRetOop: 0, retirees: 0, beneficiaries: 0, workers: 0, contributors: 0, countries: 0 };
}

/** Run the model for one country and year; adds results into `agg` (ages) and `tot` (totals). */
function runCountry(iso, id, year, agg, tot, retOverride) {
  const cal = calibration(iso, id);
  const p = shockedPop(id, year);
  if (!cal || !p) return false;
  const R = retOverride || retAges(iso);
  const G = (1 + S.growth / 100) ** (year - BASE);
  const P = cal.P0 * (S.index === "wage" ? G : 1);
  const crate = (cal.ee + cal.er) * cal.base;
  for (const sex of ["m", "f"]) {
    const Rs = R[sex], em = empProfile(iso, sex, Rs), pp = p[sex];
    for (let a = 0; a < AGES; a++) {
      const n = pp[a]; if (!n) continue;
      const prod = cohortProd(year - a) * (S.ageProfile ? AGE_PROD[a] : 1);
      const rf = retFrac(a, Rs);
      const va = n * (em.pre[a] + em.post[a]) * prod * cal.vaPerEff * G;
      const contrib = n * em.pre[a] * prod * cal.wagePerEff * G * crate * cal.cov;
      const pension = n * rf * cal.cov * P;
      const health = n * HEALTH_REL[a] * cal.hk * G;
      if (agg) {
        agg.va[sex][a] += va; agg.contrib[sex][a] += contrib; agg.pension[sex][a] += pension;
        agg.health[sex][a] += health; agg.prod[sex][a] += n * prod;
      }
      tot.pop += n; tot.gdp += va; tot.pension += pension; tot.contrib += contrib;
      tot.contribEE += crate ? contrib * cal.ee / (cal.ee + cal.er) : 0; tot.contribER += crate ? contrib * cal.er / (cal.ee + cal.er) : 0;
      tot.health += health; tot.healthRet += health * rf; tot.healthRetGov += health * rf * cal.gov;
      tot.healthRetOop += health * rf * cal.oop;
      tot.retirees += n * rf; tot.beneficiaries += n * rf * cal.cov;
      tot.workers += n * (em.pre[a] + em.post[a]); tot.contributors += n * em.pre[a] * cal.cov;
    }
  }
  tot.countries++;
  return true;
}

// ------------------------------------------------------------------ selection resolution
function resolve() {
  const pyramidIds = [...S.sel];
  const costIds = new Set(); const noMembers = []; const bigPending = [];
  for (const id of S.sel) {
    const mem = membersOf(id);
    if (mem == null) { noMembers.push(id); continue; }
    if (mem.length > BIG_GROUP && !S.allowBig.has(id)) { bigPending.push([id, mem.length]); continue; }
    mem.forEach(m => costIds.add(m));
  }
  const cost = [...costIds].map(id => ({ id, iso: D.byId.get(id).iso3 })).filter(c => c.iso && D.econ[c.iso]?.gdp);
  return { pyramidIds, cost, noMembers, bigPending };
}

// ------------------------------------------------------------------ main update
let R0 = null;
let updateQueued = false;
function update() {
  if (updateQueued) return;
  updateQueued = true;
  requestAnimationFrame(async () => {
    updateQueued = false;
    R0 = resolve();
    const need = [...R0.pyramidIds, ...R0.cost.map(c => c.id)].filter(id => !popReady(id));
    if (need.length) {
      $("selNote").textContent = `Loading ${need.length} population file(s)…`;
      await Promise.all(need.map(loadPop));
      R0 = resolve();
    }
    render();
  });
}

function render() {
  refreshProd();
  writeHash();
  renderChips();
  drawMapSelection();
  const { pyramidIds, cost, noMembers, bigPending } = R0;
  const notes = [];
  const countrySel = S.sel.filter(id => D.byId.get(id)?.type === "Country/Area");
  if (S.sel.length > countrySel.length && countrySel.length) {
    const aggMembers = new Set(S.sel.filter(id => !countrySel.includes(id)).flatMap(id => membersOf(id) || []));
    if (countrySel.some(id => aggMembers.has(id))) notes.push("⚠ A country is also inside a selected region — it is counted twice in the pyramid.");
  }
  $("selNote").textContent = notes.join(" ");

  // ---------- pyramid data
  const year = S.year;
  const left = { m: new Float64Array(AGES), f: new Float64Array(AGES) }, leftBase = { m: new Float64Array(AGES), f: new Float64Array(AGES) };
  for (const id of pyramidIds) {
    const p = shockedPop(id, year), b = rawPop(id, year);
    if (!p) continue;
    for (let a = 0; a < AGES; a++) { left.m[a] += p.m[a]; left.f[a] += p.f[a]; leftBase.m[a] += b.m[a]; leftBase.f[a] += b.f[a]; }
  }
  const agg = emptyAgeArrays(), tot = emptyTotals();
  for (const c of cost) runCountry(c.iso, c.id, year, agg, tot);
  // un-shocked right pyramid for the outline
  let rightBase = null;
  if (S.shocks.length && S.showBase && cost.length) {
    const saved = S.shocks; S.shocks = [];
    const aggB = emptyAgeArrays(), totB = emptyTotals();
    for (const c of cost) runCountry(c.iso, c.id, year, aggB, totB);
    S.shocks = saved; rightBase = aggB[S.rightMode];
  }

  const name = selectionName();
  $("pyrTitle").textContent = `${name} — ${year}`;
  const rets = cost.length ? avgRet(cost) : null;
  drawPyramid($("pyrL"), left, S.shocks.length && S.showBase ? leftBase : null, { kind: "pop", rets });
  const rm = S.rightMode;
  const capR = {
    va: "Value added (GDP) by age / birth year", contrib: "Pension contributions paid (employee + employer)",
    pension: "Pension benefits received", health: "Health spending", prod: "Population × productivity (effective persons)",
  }[rm];
  $("capL").textContent = "Population";
  $("capR").textContent = capR;
  if (cost.length) drawPyramid($("pyrR"), agg[rm], rightBase, { kind: rm, rets });
  else drawEmpty($("pyrR"), bigPending.length ? "Large group — press “Compute costs” below." : noMembers.length ? "No economic data for this aggregate — pick countries or a geographic region." : "No economic data for this selection.");
  renderLegend();
  renderCosts(cost, tot, noMembers, bigPending);
  renderTable(cost);
  lastCsv = { left, leftBase, right: cost.length ? agg[rm] : null, rm, year };
}

function avgRet(cost) {
  let wm = 0, wf = 0, sm = 0, sf = 0;
  for (const c of cost) {
    const r = retAges(c.iso), p = rawPop(c.id, S.year);
    const n = p ? d3.sum(p.m) + d3.sum(p.f) : 1;
    sm += r.m * n; sf += r.f * n; wm += n; wf += n;
  }
  return { m: sm / wm, f: sf / wf };
}

function selectionName() {
  if (!S.sel.length) return "Nothing selected";
  const names = S.sel.map(id => D.byId.get(id)?.name || id);
  return names.length <= 3 ? names.join(" + ") : `${names.slice(0, 2).join(" + ")} + ${names.length - 2} more`;
}

// ------------------------------------------------------------------ pyramid chart
function binData(arr, bin) {
  const out = [];
  if (bin === 1) { for (let a = 0; a < AGES; a++) out.push({ a0: a, a1: a, v: arr[a] }); return out; }
  for (let a = 0; a < 100; a += 5) out.push({ a0: a, a1: a + 4, v: d3.sum(arr.slice(a, a + 5)) });
  out.push({ a0: 100, a1: 100, v: arr[100] });
  return out;
}
function unitFmt(kind, total) {
  if (S.units === "pct") return v => `${(100 * v / total).toFixed(1)}%`;
  if (kind === "pop" || kind === "prod") return v => fmtNum(v);
  return v => fmtMoney(v);
}
function drawEmpty(svg, msg) {
  const s = d3.select(svg); s.selectAll("*").remove();
  const w = svg.clientWidth, h = svg.clientHeight;
  s.append("text").attr("x", w / 2).attr("y", h / 2).attr("text-anchor", "middle").text(msg);
}
function drawPyramid(svg, data, base, { kind, rets }) {
  const s = d3.select(svg); s.selectAll("*").remove();
  const W = svg.clientWidth || 500, H = svg.clientHeight || 560;
  const margin = { t: 8, r: 46, b: 26, l: 8 }, mid = 34;
  const bin = S.bin;
  const M = binData(data.m, bin), F = binData(data.f, bin);
  const MB = base ? binData(base.m, bin) : null, FB = base ? binData(base.f, bin) : null;
  const total = d3.sum(data.m) + d3.sum(data.f) || 1;
  const conv = v => S.units === "pct" ? 100 * v / total : v;
  const totalB = base ? (d3.sum(base.m) + d3.sum(base.f) || 1) : 1;
  const convB = v => S.units === "pct" ? 100 * v / totalB : v;
  let max = d3.max([...M, ...F], d => conv(d.v)) || 1;
  if (MB) max = Math.max(max, d3.max([...MB, ...FB], d => convB(d.v)));
  max *= bin === 5 ? 1.18 : 1.05;
  const half = (W - margin.l - margin.r - mid) / 2;
  const cx = margin.l + half + mid / 2;
  const x = d3.scaleLinear().domain([0, max]).range([0, half]);
  const n = M.length;
  const y = d3.scaleBand().domain(d3.range(n)).range([H - margin.b, margin.t]).paddingInner(bin === 5 ? 0.12 : 0.08);
  const fmt = unitFmt(kind, total);
  const male = css("--male"), female = css("--female");

  // grid
  const ticks = x.ticks(4).filter(t => t > 0);
  const g = s.append("g").attr("class", "grid");
  for (const t of ticks) for (const sgn of [-1, 1]) {
    const px = sgn < 0 ? cx - mid / 2 - x(t) : cx + mid / 2 + x(t);
    g.append("line").attr("x1", px).attr("x2", px).attr("y1", margin.t).attr("y2", H - margin.b);
    s.append("text").attr("x", px).attr("y", H - 8).attr("text-anchor", "middle")
      .text(S.units === "pct" ? `${+t.toFixed(2)}%` : (kind === "pop" || kind === "prod" ? d3.format("~s")(t) : "$" + d3.format("~s")(t).replace("G", "B")));
  }
  // bars: rounded data-end, square at the baseline
  const r = Math.min(4, y.bandwidth() / 2);
  const barPath = (x0, len, yy, h, dir) => {
    if (len <= 0.5) return "";
    const rr = Math.min(r, len);
    return dir < 0
      ? `M${x0},${yy}H${x0 - len + rr}Q${x0 - len},${yy} ${x0 - len},${yy + rr}V${yy + h - rr}Q${x0 - len},${yy + h} ${x0 - len + rr},${yy + h}H${x0}Z`
      : `M${x0},${yy}H${x0 + len - rr}Q${x0 + len},${yy} ${x0 + len},${yy + rr}V${yy + h - rr}Q${x0 + len},${yy + h} ${x0 + len - rr},${yy + h}H${x0}Z`;
  };
  const bars = s.append("g");
  M.forEach((d, i) => bars.append("path").attr("d", barPath(cx - mid / 2, x(conv(d.v)), y(i), y.bandwidth(), -1)).attr("fill", male));
  F.forEach((d, i) => bars.append("path").attr("d", barPath(cx + mid / 2, x(conv(d.v)), y(i), y.bandwidth(), 1)).attr("fill", female));
  // un-shocked outline
  if (MB) {
    const ol = s.append("g");
    MB.forEach((d, i) => ol.append("rect").attr("class", "base-outline").attr("x", cx - mid / 2 - x(convB(d.v))).attr("y", y(i)).attr("width", x(convB(d.v))).attr("height", y.bandwidth()));
    FB.forEach((d, i) => ol.append("rect").attr("class", "base-outline").attr("x", cx + mid / 2).attr("y", y(i)).attr("width", x(convB(d.v))).attr("height", y.bandwidth()));
  }
  // value labels (5-year bins only)
  if (bin === 5) {
    const lab = s.append("g");
    M.forEach((d, i) => d.v > 0 && lab.append("text").attr("class", "bar-label").attr("x", cx - mid / 2 - x(conv(d.v)) - 3).attr("y", y(i) + y.bandwidth() / 2).attr("dy", "0.35em").attr("text-anchor", "end").text(fmt(d.v)));
    F.forEach((d, i) => d.v > 0 && lab.append("text").attr("class", "bar-label").attr("x", cx + mid / 2 + x(conv(d.v)) + 3).attr("y", y(i) + y.bandwidth() / 2).attr("dy", "0.35em").text(fmt(d.v)));
  }
  // age labels in the centre column, birth years at right
  const every = bin === 5 ? 1 : 10;
  const ageG = s.append("g");
  M.forEach((d, i) => {
    if (d.a0 % (bin === 5 ? 5 : 10) !== 0 || (bin === 5 && (i % every))) return;
    const label = d.a0 === 100 ? "100+" : bin === 5 ? `${d.a0}` : `${d.a0}`;
    ageG.append("text").attr("x", cx).attr("y", y(i) + y.bandwidth() / 2).attr("dy", "0.35em").attr("text-anchor", "middle").text(label);
    if (bin === 1 || i % 2 === 0) {
      s.append("text").attr("x", W - 4).attr("y", y(i) + y.bandwidth() / 2).attr("dy", "0.35em").attr("text-anchor", "end")
        .attr("class", "bar-label").text(d.a0 === 100 ? `≤${S.year - 100}` : `${S.year - d.a1}`);
    }
  });
  s.append("text").attr("x", W - 4).attr("y", H - 8).attr("text-anchor", "end").attr("class", "bar-label").text("born ↑");
  s.append("line").attr("class", "zero").attr("x1", cx - mid / 2).attr("x2", cx - mid / 2).attr("y1", margin.t).attr("y2", H - margin.b);
  s.append("line").attr("class", "zero").attr("x1", cx + mid / 2).attr("x2", cx + mid / 2).attr("y1", margin.t).attr("y2", H - margin.b);

  // retirement-age lines
  if (rets) {
    const yAge = age => {
      const i = bin === 5 ? Math.min(20, age / 5) : Math.min(100, age);
      const i0 = Math.floor(i);
      return y(i0) + y.bandwidth() - (i - i0) * y.step() + (y.step() - y.bandwidth()) / 2;
    };
    for (const [sex, x0, x1, anchor, tx] of [["m", margin.l, cx - mid / 2, "start", margin.l + 2], ["f", cx + mid / 2, W - margin.r, "end", W - margin.r - 2]]) {
      const yy = yAge(rets[sex]);
      s.append("line").attr("class", "ret-line").attr("x1", x0).attr("x2", x1).attr("y1", yy).attr("y2", yy);
      s.append("text").attr("class", "ret-text").attr("x", tx).attr("y", yy - 4).attr("text-anchor", anchor).text(`retire ${(+rets[sex].toFixed(1))}`);
    }
  }
  // hover rows
  const hov = s.append("g");
  M.forEach((d, i) => {
    hov.append("rect").attr("x", 0).attr("y", y(i) - (y.step() - y.bandwidth()) / 2).attr("width", W).attr("height", y.step())
      .attr("fill", "transparent")
      .on("mousemove", ev => {
        const f = F[i];
        const ages = d.a0 === d.a1 ? (d.a0 === 100 ? "100+" : `${d.a0}`) : `${d.a0}–${d.a1}`;
        const born = d.a0 === 100 ? `${S.year - 100} or earlier` : d.a0 === d.a1 ? `${S.year - d.a0}` : `${S.year - d.a1}–${S.year - d.a0}`;
        const absF = (kind === "pop" || kind === "prod") ? fmtNum : fmtMoney;
        let html = `<b>Age ${ages}</b> · born ${born}<div class="r"><span><i class="sw" style="background:${male}"></i>Male</span><span>${absF(d.v)} · ${(100 * d.v / total).toFixed(2)}%</span></div>
          <div class="r"><span><i class="sw" style="background:${female}"></i>Female</span><span>${absF(f.v)} · ${(100 * f.v / total).toFixed(2)}%</span></div>`;
        if (MB) {
          const dv = d.v + f.v - MB[i].v - FB[i].v;
          html += `<div class="r muted"><span>vs. no shock</span><span>${dv >= 0 ? "+" : ""}${absF(dv)}</span></div>`;
        }
        if (kind !== "pop") {
          html += `<div class="r muted"><span>Cohort productivity</span><span>×${cohortProd(S.year - Math.round((d.a0 + d.a1) / 2)).toFixed(2)}</span></div>`;
        }
        showTip(ev, html);
      })
      .on("mouseleave", hideTip);
  });
}

function renderLegend() {
  const male = css("--male"), female = css("--female");
  let h = `<span><i style="background:${male}"></i>Male</span><span><i style="background:${female}"></i>Female</span>`;
  if (S.shocks.length && S.showBase) h += `<span><i class="dash"></i>Without shocks</span>`;
  h += `<span><i class="dash" style="border-top-style:dashed"></i>Retirement age</span>`;
  $("pyrLegend").innerHTML = h;
}

// ------------------------------------------------------------------ tooltip
const tip = () => $("tooltip");
function showTip(ev, html) {
  const t = tip(); t.innerHTML = html; t.hidden = false;
  const w = t.offsetWidth, h = t.offsetHeight;
  let x = ev.clientX + 14, y = ev.clientY + 14;
  if (x + w > innerWidth - 8) x = ev.clientX - w - 14;
  if (y + h > innerHeight - 8) y = ev.clientY - h - 14;
  t.style.left = `${x}px`; t.style.top = `${y}px`;
}
function hideTip() { tip().hidden = true; }

// ------------------------------------------------------------------ cost panel
function renderCosts(cost, tot, noMembers, bigPending) {
  $("costYear").textContent = `· ${S.year}`;
  const msgs = [];
  if (bigPending.length) {
    for (const [id, n] of bigPending) msgs.push(`<b>${D.byId.get(id).name}</b> has ${n} member countries (~${Math.round(n * 0.2)} MB to load). <button class="small" data-loadbig="${id}">Compute costs</button>`);
  }
  if (noMembers.length) msgs.push(`Cost model needs countries: ${noMembers.map(id => D.byId.get(id).name).join(", ")} ha${noMembers.length > 1 ? "ve" : "s"} no member list in the source data.`);
  if (cost.length > 1) msgs.push(`Merged ${cost.length} countries: each is modelled with its own data, then summed — per-capita values are population-weighted for ${S.year}.`);
  $("costMsg").innerHTML = msgs.join("<br>");
  $("costMsg").querySelectorAll("[data-loadbig]").forEach(b => b.onclick = () => { S.allowBig.add(+b.dataset.loadbig); update(); });

  if (!cost.length) { $("tiles").innerHTML = ""; drawEmpty($("tsChart"), "Select countries to estimate costs"); drawEmpty($("raChart"), ""); $("tsLegend").innerHTML = ""; $("raLegend").innerHTML = ""; return; }
  const g = tot.gdp, pg = v => fmtPct(100 * v / g, 2);
  const subsidy = tot.pension - tot.contrib;
  const selfShare = tot.pension ? 100 * tot.contrib / tot.pension : 0;
  const c1 = css("--s1"), c2 = css("--s2"), c3 = css("--s3"), c4 = css("--s4");
  const tiles = [
    ["Population", fmtNum(tot.pop), `${fmtPct(100 * tot.retirees / tot.pop)} at/after retirement age`],
    ["Old-age dependency", `${(100 * tot.retirees / tot.workers).toFixed(0)}`, `people over retirement age per 100 workers · ${fmtNum(tot.workers)} workers`],
    ["GDP (value added)", fmtMoney(g), `${fmtMoney(g / tot.pop)} per person`],
    ["Pension spending", pg(tot.pension), `${fmtMoney(tot.pension)} · ${fmtMoney(tot.pension / tot.beneficiaries)} per pensioner/yr`],
    ["Self-paid (contributions)", `${selfShare.toFixed(0)}%`, `of pensions · ${fmtMoney(tot.contrib)} = ${pg(tot.contrib)} GDP`,
      [[tot.contribEE, c1, "employee"], [tot.contribER, c2, "employer"], [Math.max(0, subsidy), c3, "state"]]],
    [subsidy >= 0 ? "State subsidy" : "Pension surplus", pg(Math.abs(subsidy)), `${fmtMoney(Math.abs(subsidy))} · ${fmtMoney(Math.abs(subsidy) / tot.workers)} per worker/yr`],
    ["Health spending on retirees", pg(tot.healthRet), `${fmtMoney(tot.healthRet)} · ${fmtMoney(tot.healthRet / tot.retirees)} per retiree/yr`,
      [[tot.healthRetGov, c1, "government"], [tot.healthRetOop, c2, "out-of-pocket"], [tot.healthRet - tot.healthRetGov - tot.healthRetOop, c3, "other private"]]],
    ["Public cost of retirees", pg(tot.pension + tot.healthRetGov), `pensions + public health · ${fmtMoney((tot.pension + tot.healthRetGov) / tot.pop)} per resident`],
  ];
  $("tiles").innerHTML = tiles.map(([k, v, s, parts]) => {
    let bar = "";
    if (parts) {
      const sum = d3.sum(parts, p => Math.max(0, p[0])) || 1;
      bar = `<div class="bar">${parts.map(([val, col, lab]) => `<i title="${lab}: ${(100 * Math.max(0, val) / sum).toFixed(0)}%" style="flex:${Math.max(0, val)};background:${col}"></i>`).join("")}</div>
        <div class="s">${parts.map(([val, col, lab]) => `<span style="white-space:nowrap"><i class="sw" style="display:inline-block;width:8px;height:8px;border-radius:2px;background:${col}"></i> ${lab} ${(100 * Math.max(0, val) / sum).toFixed(0)}%</span>`).join(" · ")}</div>`;
    }
    return `<div class="tile"><div class="k">${k}</div><div class="v">${v}</div><div class="s">${s}</div>${bar}</div>`;
  }).join("");

  // ----- time series
  const years = d3.range(1990, 2101);
  const ts = years.map(y => {
    const t = emptyTotals();
    for (const c of cost) runCountry(c.iso, c.id, y, null, t);
    return { y, pension: 100 * t.pension / t.gdp, contrib: 100 * t.contrib / t.gdp, subsidy: 100 * (t.pension - t.contrib) / t.gdp, health: 100 * t.healthRetGov / t.gdp };
  });
  const series = [
    { k: "pension", label: "Pension spending", short: "Pensions", color: c1 },
    { k: "contrib", label: "Contributions (self-paid)", short: "Contrib.", color: c2 },
    { k: "subsidy", label: "State subsidy", short: "Subsidy", color: c3 },
    { k: "health", label: "Public health on retirees", short: "Health", color: c4 },
  ];
  lineChart($("tsChart"), $("tsLegend"), ts, "y", series, { marker: S.year, xfmt: d => d, xlabel: "Year" });

  // ----- retirement-age sensitivity
  const uniform = S.retMode === "uniform";
  const xs = uniform ? d3.range(50, 76) : d3.range(-10, 11);
  const ra = xs.map(v => {
    const t = emptyTotals();
    for (const c of cost) {
      const base = retAges(c.iso);
      const R = uniform ? { m: v, f: v } : { m: base.m0 + v, f: base.f0 + v };
      runCountry(c.iso, c.id, S.year, null, t, R);
    }
    return { x: v, pension: 100 * t.pension / t.gdp, contrib: 100 * t.contrib / t.gdp, subsidy: 100 * (t.pension - t.contrib) / t.gdp, health: 100 * t.healthRetGov / t.gdp };
  });
  lineChart($("raChart"), $("raLegend"), ra, "x", series, {
    marker: uniform ? S.retUniform : S.retShift, xfmt: v => uniform ? v : (v > 0 ? `+${v}` : v),
    xlabel: uniform ? "Retirement age" : "Years vs statutory",
  });
}

function lineChart(svg, legendEl, rows, xk, series, { marker, xfmt, xlabel }) {
  const s = d3.select(svg); s.selectAll("*").remove();
  const W = svg.clientWidth || 600, H = svg.clientHeight || 280;
  const m = { t: 10, r: 112, b: 30, l: 40 };
  const x = d3.scaleLinear().domain(d3.extent(rows, d => d[xk])).range([m.l, W - m.r]);
  const vals = rows.flatMap(r => series.map(se => r[se.k])).filter(isFinite);
  const y = d3.scaleLinear().domain([Math.min(0, d3.min(vals)), d3.max(vals) * 1.08 || 1]).nice().range([H - m.b, m.t]);
  const g = s.append("g").attr("class", "grid");
  y.ticks(5).forEach(t => {
    g.append("line").attr("x1", m.l).attr("x2", W - m.r).attr("y1", y(t)).attr("y2", y(t));
    s.append("text").attr("x", m.l - 6).attr("y", y(t)).attr("dy", "0.35em").attr("text-anchor", "end").text(`${t}%`);
  });
  if (y.domain()[0] < 0) s.append("line").attr("class", "zero").attr("x1", m.l).attr("x2", W - m.r).attr("y1", y(0)).attr("y2", y(0));
  x.ticks(Math.max(3, Math.floor((W - m.l - m.r) / 70))).forEach(t => s.append("text").attr("x", x(t)).attr("y", H - 10).attr("text-anchor", "middle").text(xfmt(t)));
  s.append("line").attr("class", "ret-line").attr("x1", x(marker)).attr("x2", x(marker)).attr("y1", m.t).attr("y2", H - m.b);
  const line = k => d3.line().x(d => x(d[xk])).y(d => y(d[k])).defined(d => isFinite(d[k]));
  // direct end labels with simple collision avoidance
  const last = rows[rows.length - 1];
  const labels = series.map(se => ({ ...se, yy: y(last[se.k]) })).sort((a, b) => a.yy - b.yy);
  for (let i = 1; i < labels.length; i++) if (labels[i].yy - labels[i - 1].yy < 13) labels[i].yy = labels[i - 1].yy + 13;
  for (const se of series) {
    s.append("path").attr("d", line(se.k)(rows)).attr("fill", "none").attr("stroke", se.color).attr("stroke-width", 2).attr("stroke-linejoin", "round").attr("stroke-linecap", "round");
  }
  for (const l of labels) {
    s.append("text").attr("x", W - m.r + 6).attr("y", l.yy).attr("dy", "0.35em").text(`${l.short} ${last[l.k].toFixed(1)}%`).style("fill", css("--text-2"));
  }
  legendEl.innerHTML = series.map(se => `<span><i class="line" style="background:${se.color}"></i>${se.label}</span>`).join("");
  // crosshair
  const cross = s.append("line").attr("class", "zero").attr("y1", m.t).attr("y2", H - m.b).style("opacity", 0);
  const dots = series.map(se => s.append("circle").attr("r", 4).attr("fill", se.color).attr("stroke", css("--surface")).attr("stroke-width", 2).style("opacity", 0));
  s.append("rect").attr("x", m.l).attr("y", m.t).attr("width", W - m.l - m.r).attr("height", H - m.t - m.b).attr("fill", "transparent")
    .on("mousemove", ev => {
      const [px] = d3.pointer(ev);
      const xv = x.invert(px);
      const d = rows.reduce((a, b) => Math.abs(b[xk] - xv) < Math.abs(a[xk] - xv) ? b : a);
      cross.attr("x1", x(d[xk])).attr("x2", x(d[xk])).style("opacity", 1);
      series.forEach((se, i) => dots[i].attr("cx", x(d[xk])).attr("cy", y(d[se.k])).style("opacity", 1));
      showTip(ev, `<b>${xlabel} ${xfmt(d[xk])}</b>` + series.map(se => `<div class="r"><span><i class="sw" style="background:${se.color}"></i>${se.label}</span><span>${d[se.k].toFixed(2)}% GDP</span></div>`).join(""));
    })
    .on("mouseleave", () => { cross.style("opacity", 0); dots.forEach(d => d.style("opacity", 0)); hideTip(); });
}

// ------------------------------------------------------------------ assumptions table
function renderTable(cost) {
  const t = $("assump");
  if (!cost.length) { t.innerHTML = `<tr><td class="muted">Select one or more countries.</td></tr>`; return; }
  const rows = cost.slice(0, 80);
  let h = `<thead><tr><th>Country</th><th title="Population in selected year">Pop.</th><th title="GDP, World Bank, current US$">GDP</th>${EDIT_FIELDS.map(([k, hd, ti]) => `<th title="${ti}">${hd}</th>`).join("")}
    <th title="Average public pension per beneficiary (derived, base year)">Avg pension</th><th title="Average gross wage per worker (derived)">Avg wage</th><th title="Contribution source">Contrib. source</th></tr></thead><tbody>`;
  for (const c of rows) {
    const e = D.econ[c.iso], cal = calibration(c.iso, c.id), p = rawPop(c.id, S.year);
    const src = e.src || {};
    const srcOf = k => ({ ret_m: src.ret_age, ret_f: src.ret_age, contrib_ee: src.contrib, contrib_er: src.contrib, health_gov_share: src.health_gov_pc }[k] || src[k] || "default assumption");
    h += `<tr><td>${D.byId.get(c.id).name}</td><td>${fmtNum(d3.sum(p.m) + d3.sum(p.f))}</td><td>${fmtMoney(e.gdp)}</td>`;
    for (const [k] of EDIT_FIELDS) {
      const edited = S.edits[c.iso]?.[k] != null && S.edits[c.iso][k] !== "";
      let v = param(c.iso, k);
      const est = v == null;
      if (est) v = { ret_m: 62, ret_f: 62, pension_coverage: 50, labour_share: 50, contrib_base: 70, health_gov_share: 50, contrib_ee: cal ? cal.ee * 100 : null, contrib_er: cal ? cal.er * 100 : null }[k];
      const disp = v == null ? "" : (+v).toFixed(k.startsWith("ret") ? 1 : k === "health_pc" ? 0 : 2).replace(/\.0+$/, "");
      h += `<td class="${est ? "est" : ""}"><input data-iso="${c.iso}" data-k="${k}" value="${disp}" title="${est ? "not in data — default/estimate" : srcOf(k)}" class="${edited ? "edited" : ""}" inputmode="decimal"></td>`;
    }
    h += `<td>${cal ? fmtMoney(cal.P0) : "–"}</td><td>${cal ? fmtMoney(cal.avgWage) : "–"}</td><td class="muted" style="text-align:left">${cal ? cal.contribSrc : ""}</td></tr>`;
  }
  if (cost.length > rows.length) h += `<tr><td class="muted" colspan="14">… and ${cost.length - rows.length} more countries</td></tr>`;
  t.innerHTML = h + "</tbody>";
  t.querySelectorAll("input").forEach(inp => inp.addEventListener("change", () => {
    const { iso, k } = inp.dataset;
    S.edits[iso] = S.edits[iso] || {};
    if (inp.value.trim() === "") delete S.edits[iso][k]; else S.edits[iso][k] = +inp.value;
    save("dp.edits", S.edits);
    update();
  }));
}

// ------------------------------------------------------------------ map
let mapSel, mapG, mapPaths;
async function initMap() {
  const topo = await getJSON("vendor/countries-50m.json");
  const features = topojson.feature(topo, topo.objects.countries).features.filter(f => f.id !== "010"); // drop Antarctica
  const svg = d3.select("#map");
  const W = $("map").clientWidth, H = $("map").clientHeight;
  const proj = d3.geoNaturalEarth1().fitExtent([[4, 4], [W - 4, H - 4]], { type: "FeatureCollection", features });
  const path = d3.geoPath(proj);
  mapSel = svg;
  mapG = svg.append("g");
  mapPaths = mapG.selectAll("path").data(features).join("path")
    .attr("class", "country").attr("d", path)
    .on("mousemove", (ev, f) => {
      const id = +f.id, loc = D.byId.get(id);
      const v = mapValue(id);
      showTip(ev, `<b>${loc?.name || f.properties.name}</b><div class="r"><span>${$("mapMetric").selectedOptions[0].text}</span><span>${v == null ? "no data" : fmtMapVal(v)}</span></div><div class="muted">double-click: open · ctrl/⌘-click: merge</div>`);
    })
    .on("mouseleave", hideTip)
    .on("click", (ev, f) => {
      const id = +f.id; if (!D.byId.has(id)) return;
      if (ev.ctrlKey || ev.metaKey || ev.shiftKey) {
        S.sel = S.sel.includes(id) ? S.sel.filter(x => x !== id) : [...S.sel, id];
        update();
      }
    })
    .on("dblclick", (ev, f) => {
      ev.preventDefault(); ev.stopPropagation();
      const id = +f.id; if (!D.byId.has(id) || ev.ctrlKey || ev.metaKey || ev.shiftKey) return;
      S.sel = [id]; update();
      document.querySelector(".layout").scrollIntoView({ behavior: "smooth", block: "start" });
    });
  const zoom = d3.zoom().scaleExtent([1, 12]).on("zoom", ev => mapG.attr("transform", ev.transform));
  svg.call(zoom).on("dblclick.zoom", null);
  colorMap();
}
function mapValue(id) {
  const k = S.mapMetric, loc = D.byId.get(id);
  if (!loc) return null;
  if (["s65", "med", "pop"].includes(k)) {
    const s = D.summary.loc[id]; if (!s) return null;
    const i = Math.round((clamp(S.year, 1950, 2100) - 1950) / 5);
    return s[k][i];
  }
  return loc.iso3 ? (k === "health_pc" || k === "pension_gdp" ? param(loc.iso3, k) : D.econ[loc.iso3]?.[k]) ?? null : null;
}
function fmtMapVal(v) {
  const k = S.mapMetric;
  return k === "pop" ? fmtNum(v) : k === "s65" || k === "pension_gdp" ? `${v.toFixed(1)}%` : k === "med" ? v.toFixed(1) : fmtMoney(v);
}
const RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"];
function colorMap() {
  if (!mapPaths) return;
  const vals = mapPaths.data().map(f => mapValue(+f.id)).filter(v => v != null && isFinite(v) && v > 0);
  const log = ["pop", "health_pc", "gdp_pc"].includes(S.mapMetric);
  const ext = log ? d3.extent(vals) : [d3.min(vals), d3.quantile(vals.sort(d3.ascending), 0.98)];
  const sc = (log ? d3.scaleSequentialLog() : d3.scaleSequential()).domain(ext).interpolator(d3.interpolateRgbBasis(RAMP)).clamp(true);
  mapPaths.attr("fill", f => { const v = mapValue(+f.id); return v == null || !(v > 0) ? css("--land") : sc(v); });
  $("mapLegend").innerHTML = `<span>${fmtMapVal(ext[0])}</span><span class="ramp" style="background:linear-gradient(90deg,${RAMP.join(",")})"></span><span>${fmtMapVal(ext[1])}${log ? " (log)" : ""}</span>
    <span class="muted">· ${["s65", "med", "pop"].includes(S.mapMetric) ? `year ${Math.round(S.year / 5) * 5}` : "latest data"} · grey = no data</span>
    <label class="check" style="margin-left:auto"><input type="checkbox" id="tapMerge" ${S.tapMerge ? "checked" : ""}> tap/click merges (touch screens)</label>`;
  $("tapMerge").onchange = e => { S.tapMerge = e.target.checked; };
}
function drawMapSelection() {
  if (!mapPaths) return;
  const set = new Set(S.sel);
  mapPaths.classed("selected", f => set.has(+f.id));
  mapPaths.filter(f => set.has(+f.id)).raise();
}

// ------------------------------------------------------------------ UI: selection
function renderChips() {
  $("chips").innerHTML = S.sel.map(id => `<span class="chip">${D.byId.get(id)?.name || id}<button data-rm="${id}" aria-label="remove">×</button></span>`).join("")
    || `<span class="muted small">Double-click a country on the map or search above.</span>`;
  $("chips").querySelectorAll("[data-rm]").forEach(b => b.onclick = () => { S.sel = S.sel.filter(x => x !== +b.dataset.rm); update(); });
}
function initSearch() {
  const inp = $("search"), list = $("searchList");
  let items = [], active = 0;
  const pick = (id, add) => { S.sel = add ? [...new Set([...S.sel, id])] : [id]; inp.value = ""; list.hidden = true; update(); };
  const draw = () => {
    list.innerHTML = items.map((l, i) => `<div data-id="${l.id}" class="${i === active ? "active" : ""}"><span>${l.name}</span><span class="t">${l.type === "Country/Area" ? "" : l.type} · Ctrl+Enter / ⌘-click adds</span></div>`).join("");
    list.hidden = !items.length;
    list.querySelectorAll("div").forEach(d => d.onmousedown = ev => { ev.preventDefault(); pick(+d.dataset.id, ev.ctrlKey || ev.metaKey); });
  };
  inp.addEventListener("input", () => {
    const q = inp.value.trim().toLowerCase();
    items = q ? D.locs.filter(l => l.name.toLowerCase().includes(q) || (l.iso3 || "").toLowerCase() === q)
      .sort((a, b) => (a.name.toLowerCase().startsWith(q) ? 0 : 1) - (b.name.toLowerCase().startsWith(q) ? 0 : 1)).slice(0, 14) : [];
    active = 0; draw();
  });
  inp.addEventListener("keydown", e => {
    if (e.key === "ArrowDown") { active = Math.min(items.length - 1, active + 1); draw(); e.preventDefault(); }
    if (e.key === "ArrowUp") { active = Math.max(0, active - 1); draw(); e.preventDefault(); }
    if (e.key === "Enter" && items[active]) pick(items[active].id, e.ctrlKey || e.metaKey);
    if (e.key === "Escape") list.hidden = true;
  });
  inp.addEventListener("blur", () => setTimeout(() => (list.hidden = true), 150));
}
function initPresets() {
  const saved = load("dp.groups", {});
  const sel = $("presetSel");
  sel.innerHTML = `<option value="">—</option><optgroup label="Built-in">${Object.keys(PRESETS).map(k => `<option value="p:${k}">${k}</option>`).join("")}</optgroup>`
    + (Object.keys(saved).length ? `<optgroup label="Saved">${Object.keys(saved).map(k => `<option value="s:${k}">${k}</option>`).join("")}</optgroup>` : "");
  sel.onchange = () => {
    const v = sel.value; if (!v) return;
    const ids = v.startsWith("p:")
      ? PRESETS[v.slice(2)].split(" ").map(iso => D.byIso.get(iso)?.id).filter(Boolean)
      : saved[v.slice(2)];
    S.sel = ids; sel.value = ""; update();
  };
}

// ------------------------------------------------------------------ UI: shocks & productivity
function renderShocks() {
  $("shockList").innerHTML = S.shocks.map((s, i) => `<div class="item"><span>${s.label ? `<b>${s.label}</b> · ` : ""}${s.year}${s.dur > 1 ? `–${s.year + s.dur - 1}` : ""}, age ${s.a0}${s.a1 !== s.a0 ? `–${s.a1}` : ""}, ${{ b: "both", m: "men", f: "women" }[s.sex]}, ${s.pct > 0 ? "+" : ""}${s.pct}%${s.dur > 1 ? "/yr" : ""}</span><button data-i="${i}" aria-label="remove">×</button></div>`).join("")
    || `<div class="muted small">No shocks.</div>`;
  $("shockList").querySelectorAll("button").forEach(b => b.onclick = () => { S.shocks.splice(+b.dataset.i, 1); renderShocks(); update(); });
}
function renderProd() {
  $("prodList").innerHTML = S.prod.map((p, i) => `<div class="prod-row">born <input type="number" data-i="${i}" data-f="b" value="${p.b}" style="width:70px"> × <input type="number" step="0.05" data-i="${i}" data-f="m" value="${p.m}" style="width:70px"><button data-del="${i}" aria-label="remove">×</button></div>`).join("");
  $("prodList").querySelectorAll("input").forEach(inp => inp.onchange = () => { S.prod[+inp.dataset.i][inp.dataset.f] = +inp.value; drawProdSpark(); update(); });
  $("prodList").querySelectorAll("[data-del]").forEach(b => b.onclick = () => { if (S.prod.length > 1) { S.prod.splice(+b.dataset.del, 1); renderProd(); update(); } });
  drawProdSpark();
}
function drawProdSpark() {
  const c = $("prodSpark"), ctx = c.getContext("2d");
  const w = c.width = c.clientWidth * devicePixelRatio, h = c.height = 60 * devicePixelRatio;
  ctx.clearRect(0, 0, w, h);
  refreshProd();
  const bs = d3.range(1900, 2101), vs = bs.map(cohortProd);
  const lo = Math.min(0.5, d3.min(vs)), hi = Math.max(1.5, d3.max(vs));
  const X = b => (b - 1900) / 200 * (w - 8) + 4, Y = v => h - 12 * devicePixelRatio - (v - lo) / (hi - lo) * (h - 18 * devicePixelRatio);
  ctx.strokeStyle = css("--grid"); ctx.lineWidth = devicePixelRatio;
  ctx.beginPath(); ctx.moveTo(4, Y(1)); ctx.lineTo(w - 4, Y(1)); ctx.stroke();
  ctx.strokeStyle = css("--accent"); ctx.lineWidth = 2 * devicePixelRatio;
  ctx.beginPath(); bs.forEach((b, i) => (i ? ctx.lineTo(X(b), Y(vs[i])) : ctx.moveTo(X(b), Y(vs[i])))); ctx.stroke();
  ctx.fillStyle = css("--muted"); ctx.font = `${10 * devicePixelRatio}px sans-serif`;
  ctx.fillText("1900", 4, h - 1); ctx.fillText("2100", w - 28 * devicePixelRatio, h - 1);
  ctx.fillText(`×${hi.toFixed(1)}`, 4, 10 * devicePixelRatio);
}

// ------------------------------------------------------------------ CSV
let lastCsv = null;
function downloadCsv() {
  if (!lastCsv) return;
  const { left, leftBase, right, rm, year } = lastCsv;
  const rows = [["age", "birth_year", "male", "female", "male_no_shock", "female_no_shock", ...(right ? [`${rm}_male`, `${rm}_female`] : [])]];
  for (let a = 0; a < AGES; a++) rows.push([a === 100 ? "100+" : a, year - a, left.m[a], left.f[a], leftBase.m[a], leftBase.f[a], ...(right ? [right.m[a], right.f[a]] : [])].map(v => typeof v === "number" ? +v.toFixed(2) : v));
  const blob = new Blob([rows.map(r => r.join(",")).join("\n")], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = `pyramid_${selectionName().replace(/[^\w]+/g, "_")}_${year}.csv`; a.click();
}

// ------------------------------------------------------------------ URL hash
function writeHash() {
  const h = `sel=${S.sel.join(",")}&y=${S.year}`;
  if (location.hash.slice(1) !== h) history.replaceState(null, "", `#${h}`);
}
function readHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  const sel = (p.get("sel") || "").split(",").map(Number).filter(id => D.byId.has(id));
  if (sel.length) S.sel = sel;
  const y = +p.get("y"); if (y >= 1950 && y <= 2100) S.year = y;
}

// ------------------------------------------------------------------ wiring
function bind() {
  const on = (id, ev, fn) => $(id).addEventListener(ev, fn);
  on("year", "input", e => { S.year = +e.target.value; $("yearOut").textContent = S.year; colorMap(); update(); });
  on("bin", "change", e => { S.bin = +e.target.value; update(); });
  on("units", "change", e => { S.units = e.target.value; update(); });
  on("rightMode", "change", e => { S.rightMode = e.target.value; update(); });
  on("showBase", "change", e => { S.showBase = e.target.checked; update(); });
  on("ageProfile", "change", e => { S.ageProfile = e.target.checked; update(); });
  on("growth", "change", e => { S.growth = +e.target.value || 0; update(); });
  on("index", "change", e => { S.index = e.target.value; update(); });
  document.querySelectorAll("input[name=retMode]").forEach(r => r.addEventListener("change", e => {
    S.retMode = e.target.value;
    const uni = S.retMode === "uniform";
    $("retLabel").textContent = uni ? "Retirement age (all countries)" : "Shift vs statutory";
    Object.assign($("ret"), uni ? { min: 50, max: 75, value: S.retUniform } : { min: -10, max: 10, value: S.retShift });
    $("retOut").textContent = uni ? S.retUniform : (S.retShift >= 0 ? `+${S.retShift}` : S.retShift);
    update();
  }));
  on("ret", "input", e => {
    const v = +e.target.value;
    if (S.retMode === "uniform") { S.retUniform = v; $("retOut").textContent = v; } else { S.retShift = v; $("retOut").textContent = v >= 0 ? `+${v}` : v; }
    update();
  });
  let timer = null;
  on("play", "click", () => {
    if (timer) { clearInterval(timer); timer = null; $("play").textContent = "▶"; return; }
    if (S.year >= 2100) S.year = 1950;
    $("play").textContent = "❚❚";
    timer = setInterval(() => {
      S.year++; $("year").value = S.year; $("yearOut").textContent = S.year; colorMap(); update();
      if (S.year >= 2100) { clearInterval(timer); timer = null; $("play").textContent = "▶"; }
    }, 140);
  });
  on("addShock", "click", () => {
    const n = id => +$(id).value;
    const a0 = clamp(Math.min(n("shA0"), n("shA1")), 0, 100), a1 = clamp(Math.max(n("shA0"), n("shA1")), 0, 100);
    S.shocks.push({ year: n("shYear"), dur: Math.max(1, n("shDur")), a0, a1, sex: $("shSex").value, pct: n("shPct") });
    renderShocks(); update();
  });
  document.querySelectorAll("[data-preset]").forEach(b => b.onclick = () => {
    const p = { ...SHOCK_PRESETS[b.dataset.preset] };
    if (p.year < S.year - 50 || p.year > 2100) p.year = BASE;
    S.shocks.push(p); renderShocks(); update();
  });
  document.querySelectorAll("[data-prod]").forEach(b => b.onclick = () => { S.prod = PROD_PRESETS[b.dataset.prod].map(p => ({ ...p })); renderProd(); update(); });
  on("addProd", "click", () => { const last = S.prod[S.prod.length - 1]; S.prod.push({ b: Math.min(2100, (last?.b ?? 2000) + 10), m: last?.m ?? 1 }); renderProd(); });
  on("clearSel", "click", () => { S.sel = []; update(); });
  on("saveGroup", "click", () => {
    if (!S.sel.length) return;
    const name = prompt("Name for this group:", selectionName()); if (!name) return;
    const g = load("dp.groups", {}); g[name] = [...S.sel]; save("dp.groups", g); initPresets();
  });
  on("resetEdits", "click", () => { S.edits = {}; save("dp.edits", S.edits); calibCache.clear(); update(); });
  on("dlCsv", "click", downloadCsv);
  on("mapMetric", "change", e => { S.mapMetric = e.target.value; colorMap(); });
  on("mapToggle", "click", () => {
    const w = $("mapWrap"); w.hidden = !w.hidden; $("mapToggle").textContent = w.hidden ? "Show map" : "Hide map";
  });
  on("themeBtn", "click", () => {
    const cur = document.documentElement.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    document.documentElement.dataset.theme = cur === "dark" ? "light" : "dark";
    save("dp.theme", document.documentElement.dataset.theme);
    colorMap(); render(); drawProdSpark();
  });
  let rt = null;
  addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => R0 && render(), 150); });
}

async function main() {
  const theme = load("dp.theme", null); if (theme) document.documentElement.dataset.theme = theme;
  const [locs, econ, summary] = await Promise.all([getJSON("data/locations.json"), getJSON("data/econ.json"), getJSON("data/summary.json")]);
  D.locs = locs; D.econ = econ; D.summary = summary;
  for (const l of locs) {
    D.byId.set(l.id, l);
    if (l.iso3 && l.type === "Country/Area") D.byIso.set(l.iso3, l);
    if (l.parent != null) { if (!D.children.has(l.parent)) D.children.set(l.parent, []); D.children.get(l.parent).push(l.id); }
  }
  S.sel = [D.byIso.get("KOR").id];
  readHash();
  $("year").value = S.year; $("yearOut").textContent = S.year;
  bind(); initSearch(); initPresets(); renderShocks(); renderProd();
  update();
  await initMap();
  // touch-friendly merge: plain click/tap toggles group membership when enabled
  mapPaths.on("click.tap", (ev, f) => {
    if (!S.tapMerge || ev.ctrlKey || ev.metaKey || ev.shiftKey) return;
    const id = +f.id; if (!D.byId.has(id)) return;
    S.sel = S.sel.includes(id) ? S.sel.filter(x => x !== id) : [...S.sel, id];
    update();
  });
  drawMapSelection();
}
main().catch(err => { console.error(err); document.body.insertAdjacentHTML("afterbegin", `<p style="color:#d03b3b;padding:12px">Failed to load data: ${err.message}. If you opened the file directly, serve the folder over HTTP (e.g. <code>python3 -m http.server -d docs</code>).</p>`); });
