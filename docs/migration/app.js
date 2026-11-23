// Urban–rural migration simulator: controls, model runs (Pyodide worker or ?fixture), rendering.
// All model math lives in Python (urqse.api). This file only draws the JSON the model returns.
const d3 = window.d3;
const $ = id => document.getElementById(id);
const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const FIXTURE = new URLSearchParams(location.search).has("fixture");
const TOL = 1e-8;

const DEFAULT_SCENARIO = {
  params: { alpha: 0.75, beta: 0.8, lam: 6.8, kappa_lam: 0.08, mu: 0.5, theta_T: 0.40, lam_R: 3.0, nu: 2.0, eta: 0.0,
            price_rent_ratio: 36.0, epsilon: 0.10, varsigma: 0.5, land_income_in_choice: false },
  shocks: { core_productivity_pct: 10.0, farm_tfp_pct: 0.0, travel_cut_pct: 0.0, travel_cut_scope: "into_core",
            immigration_per_period: 0.0, periods: 60 },
};

// ------------------------------------------------------------------ formatting
const MINUS = "−";
const signed = (v, d = 1) => v == null || !isFinite(v) ? "—" : (v > 0 ? "+" : v < 0 ? MINUS : "") + Math.abs(v).toFixed(d);
const pct = (v, d = 1) => v == null || !isFinite(v) ? "—" : signed(v, d) + "%";
const int = d3.format(",.0f");
const sci = v => v == null || !isFinite(v) ? "—" : v === 0 ? "0" : v.toExponential(1).replace("-", MINUS);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// ------------------------------------------------------------------ controls (one table drives the form)
const SHOCK_CTL = [
  { key: "core_productivity_pct", label: "Core productivity shock", min: -20, max: 30, step: 1, fmt: v => pct(v, 0), help: "Non-farm productivity in the core city." },
  { key: "farm_tfp_pct", label: "Farm productivity shock", min: -20, max: 30, step: 1, fmt: v => pct(v, 0), help: "Total factor productivity on every farm." },
  { key: "travel_cut_pct", label: "Travel-time cut", min: 0, max: 50, step: 1, fmt: v => pct(v, 0),
    choice: { key: "travel_cut_scope", options: [["into_core", "Links into the core"], ["all", "All links"]] } },
  { key: "immigration_per_period", label: "International immigrants per period", input: "number", min: 0, step: 100, fmt: int, help: "New arrivals settle like residents do." },
  { key: "periods", label: "Periods", min: 10, max: 200, step: 5, fmt: int, help: "Length of the adjustment path." },
];
const PARAM_CTL = [
  { key: "theta_T", label: "Land share in farming θ_T", min: 0.05, max: 0.7, step: 0.01, fmt: v => v.toFixed(2), help: "Higher means more diminishing returns to farm labour." },
  { key: "lam_R", label: "Residence elasticity λ_R", min: 0.5, max: 10, step: 0.1, fmt: v => v.toFixed(1), help: "How strongly residents respond to living standards." },
  { key: "mu", label: "Floor-space supply elasticity μ", min: 0, max: 3, step: 0.05, fmt: v => v.toFixed(2) },
  { key: "nu", label: "Migration friction ν", min: 0.2, max: 6, step: 0.1, fmt: v => v.toFixed(1), help: "Higher means people relocate more slowly." },
  { key: "eta", label: "Openness to the rest of the country η", min: 0, max: 5, step: 0.1, fmt: v => v.toFixed(1), help: "0 = closed region (the v1 setting)." },
  { key: "epsilon", label: "Consolidation target ε", min: 0.01, max: 0.5, step: 0.01, fmt: v => "+" + Math.round(v * 100) + "%", help: "Stop when farmland per farm worker rises this much." },
  { key: "price_rent_ratio", label: "Farmland price / rent ratio", min: 10, max: 60, step: 1, fmt: v => v.toFixed(0) },
  { key: "varsigma", label: "Landlord income kept in county ς", min: 0, max: 1, step: 0.05, fmt: v => Math.round(v * 100) + "%" },
  { key: "land_income_in_choice", label: "Land income affects where people live", check: true, help: "Off by default: land income is portable wealth." },
];

const S = { scenario: structuredClone(DEFAULT_SCENARIO), result: null, view: "long", metric: "dN_pct", period: 0, autoRun: false };

function controlHTML(c, group) {
  const id = `${group}-${c.key}`;
  if (c.check) return `<div class="ctl check"><label><input type="checkbox" id="${id}" data-group="${group}" data-key="${c.key}"> <span>${c.label}${c.help ? `<div class="help">${c.help}</div>` : ""}</span></label></div>`;
  const field = c.input === "number"
    ? `<input type="number" id="${id}" min="${c.min}" step="${c.step}" data-group="${group}" data-key="${c.key}">`
    : `<input type="range" id="${id}" min="${c.min}" max="${c.max}" step="${c.step}" data-group="${group}" data-key="${c.key}">`;
  const choice = c.choice ? `<div class="opts">${c.choice.options.map(([v, l]) =>
    `<label><input type="radio" name="${c.choice.key}" value="${v}" data-group="${group}" data-key="${c.choice.key}"> ${l}</label>`).join("")}</div>` : "";
  return `<div class="ctl"><div class="top"><label for="${id}">${c.label}</label>${c.input === "number" ? "" : `<output id="${id}-out"></output>`}</div>${field}${choice}${c.help ? `<div class="help">${c.help}</div>` : ""}</div>`;
}

function buildControls() {
  $("shockCtl").innerHTML = SHOCK_CTL.map(c => controlHTML(c, "shocks")).join("");
  $("paramCtl").innerHTML = PARAM_CTL.map(c => controlHTML(c, "params")).join("");
  $("controls").addEventListener("input", e => {
    const { group, key } = e.target.dataset;
    if (!group) return;
    const v = e.target.type === "checkbox" ? e.target.checked : e.target.type === "radio" ? e.target.value : Number(e.target.value);
    S.scenario[group][key] = v;
    syncOutputs();
    if (S.autoRun) scheduleRun();
  });
}

function syncControls() {
  for (const [group, list] of [["shocks", SHOCK_CTL], ["params", PARAM_CTL]]) for (const c of list) {
    const el = $(`${group}-${c.key}`), v = S.scenario[group][c.key];
    if (c.check) el.checked = !!v; else el.value = v;
    if (c.choice) for (const r of document.getElementsByName(c.choice.key)) r.checked = r.value === S.scenario[group][c.choice.key];
  }
  syncOutputs();
}

function syncOutputs() {
  for (const [group, list] of [["shocks", SHOCK_CTL], ["params", PARAM_CTL]]) for (const c of list) {
    const out = $(`${group}-${c.key}-out`);
    if (out) out.textContent = c.fmt(S.scenario[group][c.key]);
  }
}

// ------------------------------------------------------------------ backends
function workerBackend(onStage) {
  const worker = new Worker("migration/worker.js");
  const waits = new Map();
  let seq = 0;
  const failAll = msg => { for (const w of waits.values()) w.reject(new Error(msg)); waits.clear(); };
  worker.onmessage = ({ data }) => {
    if (data.type === "status") return onStage(data);
    const w = waits.get(data.id);
    waits.delete(data.id);
    data.ok ? w.resolve(data.result) : w.reject(new Error(data.error));
  };
  worker.onerror = e => {
    const msg = e.message || "The model worker failed to start. Check your connection: the Python runtime loads from cdn.jsdelivr.net.";
    onStage({ stage: "error", text: msg });
    failAll(msg);
  };
  const call = (type, scenario) => new Promise((resolve, reject) => {
    const id = ++seq;
    waits.set(id, { resolve, reject });
    worker.postMessage({ id, type, scenario });
  });
  return { run: sc => call("run", sc), defaults: () => call("default") };
}

function fixtureBackend() {
  const fixture = fetch("migration/sample_result.json").then(r => r.json());
  return { run: () => fixture, defaults: async () => structuredClone(DEFAULT_SCENARIO) };
}

// ------------------------------------------------------------------ running
let backend, runTimer = null, busy = false, queued = null;
const setStatus = (text, err = false) => { $("status").textContent = text; $("status").classList.toggle("err", err); };

function scheduleRun() { clearTimeout(runTimer); runTimer = setTimeout(requestRun, 450); }
function requestRun() { clearTimeout(runTimer); queued = structuredClone(S.scenario); if (!busy) pump(); }

async function pump() {
  busy = true;
  $("runBtn").disabled = true;
  while (queued) {
    const sc = queued;
    queued = null;
    setStatus("Solving…");
    const t0 = performance.now();
    try {
      const res = await backend.run(sc);
      if (queued) continue;  // a newer scenario is waiting; skip drawing a stale one
      S.result = res;
      S.period = Math.min(S.period, res.path.t.length - 1);
      showResult();
      const secs = ((performance.now() - t0) / 1000).toFixed(1);
      setStatus(FIXTURE ? "Sample results (?fixture). The controls do not change them." : `Solved in ${secs} s. Changes re-run automatically.`);
      S.autoRun = !FIXTURE;
    } catch (err) {
      showError(err.message);
    }
  }
  busy = false;
  $("runBtn").disabled = false;
}

function showError(msg) {
  setStatus("The model run failed.", true);
  $("loading").hidden = true;
  $("errorCard").hidden = false;
  $("errorMsg").textContent = msg;
}

function onStage({ stage, text }) {
  if (stage === "error") return showError(text);
  setStatus(text);
  const order = ["runtime", "numpy", "model", "run"];
  const at = order.indexOf(stage === "ready" ? "run" : stage);
  for (const li of $("steps").children) {
    const i = order.indexOf(li.dataset.stage);
    li.classList.toggle("done", i < at);
    li.classList.toggle("active", i === at);
  }
}

// ------------------------------------------------------------------ convergence gate
function diagnose(r) {
  const solveOk = s => !!s && s.converged === true && s.residual_inf <= TOL;
  const pathOk = r.path.all_converged === true && r.path.worst_residual <= TOL;
  return { ok: solveOk(r.calibration.solve) && solveOk(r.long_run.solve) && pathOk, solveOk, pathOk };
}

function showResult() {
  const r = S.result, dx = diagnose(r);
  $("loading").hidden = true;
  $("errorCard").hidden = true;
  $("diagCard").hidden = false;
  $("gate").hidden = dx.ok;
  $("output").hidden = !dx.ok;
  drawDiagnostics(r, dx);
  if (dx.ok) render();
}

// ------------------------------------------------------------------ tiles
const TILES = [
  ["Rural residents", r => r.long_run.totals.rural_residents_pct, "residents of rural counties"],
  ["Farmland per farm worker", r => r.long_run.totals.land_per_farm_worker_pct, "rural counties"],
  ["Farm wage", r => r.long_run.totals.farm_wage_pct, "rural counties"],
  ["Farmland rent", r => r.long_run.totals.farmland_rent_pct, "per hectare"],
  ["Core floor rent", r => r.long_run.totals.core_rent_pct, "core city"],
  ["Region population", r => r.long_run.totals.region_pop_pct, "all counties"],
  ["Welfare", r => r.long_run.welfare_pct, "expected utility, residents"],
  ["Farm households that stay", r => r.wealth.stayer_pct, "wealth change"],
  ["Farm households that leave", r => r.wealth.leaver_pct, "wealth change"],
];

function drawTiles(r) {
  $("tiles").innerHTML = TILES.map(([k, get, sub]) => {
    const v = get(r);
    return `<div class="tile"><div class="k">${k}</div><div class="v${Math.abs(v) < 0.05 ? " neutral" : ""}">${pct(v)}</div><div class="s">${sub}</div></div>`;
  }).join("");
  const sh = S.scenario.shocks;
  const parts = [];
  if (sh.core_productivity_pct) parts.push(`core productivity ${pct(sh.core_productivity_pct, 0)}`);
  if (sh.farm_tfp_pct) parts.push(`farm productivity ${pct(sh.farm_tfp_pct, 0)}`);
  if (sh.travel_cut_pct) parts.push(`travel time ${pct(-sh.travel_cut_pct, 0)} (${sh.travel_cut_scope === "all" ? "all links" : "links into the core"})`);
  if (sh.immigration_per_period) parts.push(`${int(sh.immigration_per_period)} immigrants per period`);
  $("scenarioLine").textContent = FIXTURE ? "Sample results" : parts.length ? "Shock: " + parts.join(", ") : "No shock";
}

// ------------------------------------------------------------------ map
const METRICS = [
  ["dN_pct", "Residents"], ["HA_pct", "Farm jobs"], ["wA_pct", "Farm wage"], ["rho_pct", "Farmland rent"], ["r_pct", "Floor rent"],
];
const KIND_LABEL = { core: "Core city", suburb: "Suburb", rural: "Rural" };
const tip = $("tooltip");
function showTip(html, ev) {
  tip.innerHTML = html;
  tip.hidden = false;
  const w = tip.offsetWidth, h = tip.offsetHeight;
  let x = ev.clientX + 14, y = ev.clientY + 14;
  if (x + w > innerWidth - 8) x = ev.clientX - w - 14;
  if (y + h > innerHeight - 8) y = ev.clientY - h - 14;
  tip.style.left = Math.max(8, x) + "px";
  tip.style.top = Math.max(8, y) + "px";
}
const hideTip = () => { tip.hidden = true; };

function divergingScale(maxAbs) {
  const m = maxAbs > 0 ? maxAbs : 1;
  const interp = d3.piecewise(d3.interpolateLab, [css("--div-neg"), css("--div-mid"), css("--div-pos")]);
  return d3.scaleDiverging(interp).domain([-m, 0, m]).clamp(true);
}

function mapValues(r) {
  const n0 = r.path.N[0];
  if (S.view === "path") {
    const row = r.path.N[S.period];
    return { values: row.map((v, i) => (v / n0[i] - 1) * 100), sizes: row,
             maxAbs: d3.max(r.path.N, row => d3.max(row, (v, i) => Math.abs(v / n0[i] - 1) * 100)), label: `Residents, period ${r.path.t[S.period]} vs start` };
  }
  const vals = r.long_run[S.metric];
  return { values: vals, sizes: r.long_run.N, maxAbs: d3.max(vals, Math.abs), label: `${METRICS.find(m => m[0] === S.metric)[1]}, long run vs start` };
}

function drawMap(r) {
  const svg = d3.select("#map"), node = svg.node();
  const W = node.clientWidth, H = node.clientHeight;
  svg.attr("viewBox", `0 0 ${W} ${H}`).selectAll("*").remove();
  const C = r.counties, mv = mapValues(r), color = divergingScale(mv.maxAbs);
  const maxN = d3.max([...r.path.N, r.long_run.N], row => d3.max(row));
  const rMax = Math.max(14, Math.min(28, Math.min(W, H) / 18));
  const rad = d3.scaleSqrt().domain([0, maxN]).range([0, rMax]);
  const pad = rMax + 8;
  const xs = d3.extent(C, c => c.x), ys = d3.extent(C, c => c.y);
  const k = Math.min((W - 2 * pad) / (xs[1] - xs[0] || 1), (H - 2 * pad) / (ys[1] - ys[0] || 1));
  const cx = W / 2 - k * (xs[0] + xs[1]) / 2, cy = H / 2 + k * (ys[0] + ys[1]) / 2;
  const px = c => cx + k * c.x, py = c => cy - k * c.y;

  const order = d3.range(C.length).sort((a, b) => mv.sizes[b] - mv.sizes[a]);  // small circles on top
  const g = svg.append("g");
  const stroke = { core: [css("--core-ring"), 2.5, null], suburb: [css("--core-ring"), 1.5, "3 2"], rural: [css("--surface"), 1.5, null] };
  g.selectAll("circle.county").data(order).join("circle")
    .attr("class", "county")
    .attr("cx", i => px(C[i])).attr("cy", i => py(C[i]))
    .attr("r", i => Math.max(3, rad(mv.sizes[i])))
    .attr("fill", i => color(mv.values[i]))
    .attr("stroke", i => stroke[C[i].kind][0]).attr("stroke-width", i => stroke[C[i].kind][1])
    .attr("stroke-dasharray", i => stroke[C[i].kind][2]);
  // generous invisible hit targets
  g.selectAll("circle.hit").data(order).join("circle")
    .attr("class", "hit").attr("fill", "transparent")
    .attr("cx", i => px(C[i])).attr("cy", i => py(C[i]))
    .attr("r", i => Math.max(11, rad(mv.sizes[i])))
    .on("mousemove", (ev, i) => showTip(countyTip(r, i), ev))
    .on("mouseleave", hideTip);
  for (const i of d3.range(C.length).filter(i => C[i].kind === "core")) {
    g.append("text").attr("class", "label").attr("x", px(C[i])).attr("y", py(C[i]) - Math.max(3, rad(mv.sizes[i])) - 6)
      .attr("text-anchor", "middle").text(C[i].name);
  }
  // scale bar
  const km = [10, 20, 25, 50, 100].find(v => v * k > 60) || 100;
  const sb = svg.append("g").attr("transform", `translate(14,${H - 16})`);
  sb.append("line").attr("x2", km * k).attr("stroke", css("--text-2")).attr("stroke-width", 1.5);
  sb.append("text").attr("y", -5).text(`${km} km`);

  drawMapLegend(color, mv);
}

function drawMapLegend(color, mv) {
  const m = color.domain()[2];
  const stops = d3.range(0, 1.0001, 0.1).map(t => color(-m + 2 * m * t)).join(",");
  const ring = (kind) => {
    const s = { core: `stroke="var(--core-ring)" stroke-width="2.5"`, suburb: `stroke="var(--core-ring)" stroke-width="1.5" stroke-dasharray="3 2"`, rural: `stroke="var(--border)" stroke-width="1"` }[kind];
    return `<span><svg width="16" height="16"><circle cx="8" cy="8" r="6" fill="var(--div-mid)" ${s}/></svg> ${KIND_LABEL[kind]}</span>`;
  };
  $("mapLegend").innerHTML =
    `<span class="ramp"><b>${esc(mv.label)}</b></span>
     <span class="ramp">${pct(-m, m < 10 ? 1 : 0)} <i style="background:linear-gradient(90deg,${stops})"></i> ${pct(m, m < 10 ? 1 : 0)}</span>
     <span class="kinds">${ring("core")}${ring("suburb")}${ring("rural")}</span>
     <span>Circle area = residents</span>`;
}

function countyTip(r, i) {
  const c = r.counties[i], L = r.long_run;
  const row = (k, v) => `<div class="r"><span>${k}</span><b>${v}</b></div>`;
  let html = `<b>${esc(c.name)}</b> <span class="muted">· ${KIND_LABEL[c.kind] || c.kind}</span>`;
  if (S.view === "path") {
    const n = r.path.N[S.period][i];
    html += row(`Residents at period ${r.path.t[S.period]}`, `${int(n)} (${pct((n / r.path.N[0][i] - 1) * 100)})`);
  }
  html += row("Residents, start → long run", `${int(c.N0)} → ${int(L.N[i])}`)
    + row("Residents", pct(L.dN_pct[i])) + row("Farm jobs", pct(L.HA_pct[i])) + row("Farm wage", pct(L.wA_pct[i]))
    + row("Farmland rent", pct(L.rho_pct[i])) + row("Floor rent", pct(L.r_pct[i]))
    + row("Farmland", int(c.TF)) + row("Owner-operated share", Math.round(c.omega * 100) + "%");
  return html;
}

function drawTable(r) {
  const L = r.long_run;
  const head = ["County", "Type", "Residents", "Long run", "Residents Δ", "Farm jobs Δ", "Farm wage Δ", "Farmland rent Δ", "Floor rent Δ", "Owner share"];
  $("countyTable").innerHTML = `<thead><tr>${head.map(h => `<th>${h}</th>`).join("")}</tr></thead><tbody>${r.counties.map((c, i) =>
    `<tr><td>${esc(c.name)}</td><td>${KIND_LABEL[c.kind] || c.kind}</td><td>${int(c.N0)}</td><td>${int(L.N[i])}</td><td>${pct(L.dN_pct[i])}</td><td>${pct(L.HA_pct[i])}</td><td>${pct(L.wA_pct[i])}</td><td>${pct(L.rho_pct[i])}</td><td>${pct(L.r_pct[i])}</td><td>${Math.round(c.omega * 100)}%</td></tr>`).join("")}</tbody>`;
}

// ------------------------------------------------------------------ line charts (single y axis each)
function lineChart(sel, { t, series, refs = [], vlines = [], yFmt, tipFmt = yFmt }) {
  const svg = d3.select(sel), node = svg.node();
  const W = node.clientWidth, H = node.clientHeight;
  const direct = series.length > 1;
  const M = { t: 12, r: direct ? 92 : 16, b: 28, l: 48 };
  svg.attr("viewBox", `0 0 ${W} ${H}`).selectAll("*").remove();
  const x = d3.scaleLinear().domain(d3.extent(t)).range([M.l, W - M.r]);
  const all = [...series.flatMap(s => s.values), ...refs.map(r => r.y)];
  let [lo, hi] = d3.extent(all);
  const span = hi - lo || Math.abs(hi) * 0.02 || 0.01;
  const y = d3.scaleLinear().domain([lo - span * 0.08, hi + span * 0.08]).nice().range([H - M.b, M.t]);

  svg.append("g").attr("class", "grid").attr("transform", `translate(${M.l},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(-(W - M.l - M.r)).tickFormat("")).call(g => g.select(".domain").remove());
  svg.append("g").attr("class", "axis").attr("transform", `translate(0,${H - M.b})`).call(d3.axisBottom(x).ticks(Math.min(8, W / 70)).tickSizeOuter(0));
  svg.append("g").attr("class", "axis").attr("transform", `translate(${M.l},0)`).call(d3.axisLeft(y).ticks(5).tickFormat(yFmt).tickSizeOuter(0))
    .call(g => g.select(".domain").remove());

  for (const r of refs) {
    svg.append("line").attr("class", "ref").attr("x1", M.l).attr("x2", W - M.r).attr("y1", y(r.y)).attr("y2", y(r.y));
    svg.append("text").attr("class", "direct").attr("x", M.l + 6).attr("y", y(r.y) - 5).text(r.label);
  }
  for (const v of vlines) {
    svg.append("line").attr("class", v.cls).attr("x1", x(v.x)).attr("x2", x(v.x)).attr("y1", M.t).attr("y2", H - M.b);
    if (v.label) svg.append("text").attr("class", "direct").attr("x", x(v.x) + (x(v.x) > W * 0.7 ? -5 : 5)).attr("y", M.t + 12)
      .attr("text-anchor", x(v.x) > W * 0.7 ? "end" : "start").text(v.label);
  }
  const line = vals => d3.line().x((_, i) => x(t[i])).y(v => y(v))(vals);
  for (const s of series) {
    svg.append("path").attr("class", "series").attr("stroke", s.color).attr("d", line(s.values));
    if (direct) svg.append("text").attr("class", "direct").attr("x", W - M.r + 6).attr("y", y(s.values.at(-1)) + 4).text(s.name);
  }

  // hover layer: crosshair + per-series dots + tooltip; click picks a period for the map
  const cursor = svg.append("line").attr("class", "cursor").attr("y1", M.t).attr("y2", H - M.b).style("display", "none");
  const dots = series.map(s => svg.append("circle").attr("class", "dot").attr("r", 4).attr("fill", s.color).style("display", "none"));
  const idxAt = ev => d3.bisectCenter(t, x.invert(d3.pointer(ev, node)[0]));
  svg.append("rect").attr("x", M.l).attr("y", M.t).attr("width", W - M.l - M.r).attr("height", H - M.t - M.b)
    .attr("fill", "transparent").style("cursor", "crosshair")
    .on("mousemove", ev => {
      const i = idxAt(ev);
      cursor.style("display", null).attr("x1", x(t[i])).attr("x2", x(t[i]));
      dots.forEach((d, k) => d.style("display", null).attr("cx", x(t[i])).attr("cy", y(series[k].values[i])));
      showTip(`<b>Period ${t[i]}</b>` + series.map(s => `<div class="r"><span><i class="sw" style="background:${s.color}"></i>${s.name}</span><b>${tipFmt(s.values[i])}</b></div>`).join(""), ev);
    })
    .on("mouseleave", () => { cursor.style("display", "none"); dots.forEach(d => d.style("display", "none")); hideTip(); })
    .on("click", ev => setPeriod(idxAt(ev)));
}

const legendHTML = items => items.map(([kind, color, label]) =>
  `<span><i class="${kind}" style="background:${color}"></i>${label}</span>`).join("");

const STOP_TEXT = {
  consolidation: p => `Consolidation target reached at period ${p}`,
  steady_state: p => `Steady state at period ${p}, before the consolidation target`,
  horizon: p => `Reached the horizon at period ${p} without consolidating`,
};

function drawPath(r) {
  const P = r.path, t = P.t, stop = P.stop || {};
  const scrub = S.view === "path" ? [{ x: t[S.period], cls: "scrubline" }] : [];
  const stopV = stop.period != null ? [{ x: stop.period, cls: "stop", label: `stop · t=${stop.period}` }] : [];
  $("stopLine").textContent = stop.period != null ? STOP_TEXT[stop.reason]?.(stop.period) ?? `Stopped at period ${stop.period}` : "The path did not stop";
  const c1 = css("--s1"), c2 = css("--s2");
  $("lpwLegend").innerHTML = legendHTML([["line", c1, "Farmland per farm worker"], ["dash", "", `Target ${P.target_ratio.toFixed(2)} (1 + ε)`], ["line", css("--text"), "Stop"]]);
  lineChart("#lpwChart", { t, series: [{ name: "Land per worker", values: P.land_per_worker_ratio, color: c1 }],
    refs: [{ y: P.target_ratio, label: `target ${P.target_ratio.toFixed(2)}` }], vlines: [...stopV, ...scrub], yFmt: d3.format(".2f"), tipFmt: d3.format(".3f") });
  lineChart("#ruralChart", { t, series: [{ name: "Rural share", values: P.rural_share.map(v => v * 100), color: c1 }],
    vlines: [...stopV, ...scrub], yFmt: d3.format(".1f"), tipFmt: v => v.toFixed(2) + "%" });
  $("priceLegend").innerHTML = legendHTML([["line", c1, "Farmland price"], ["line", c2, "Urban floor rent"]]);
  lineChart("#priceChart", { t, series: [{ name: "Farmland price", values: P.farmland_price_index, color: c1 }, { name: "Urban rent", values: P.urban_rent_index, color: c2 }],
    vlines: [...stopV, ...scrub], yFmt: d3.format(".2f"), tipFmt: d3.format(".3f") });
}

// ------------------------------------------------------------------ diagnostics
function drawDiagnostics(r, dx) {
  $("badge").className = "badge " + (dx.ok ? "ok" : "bad");
  $("badge").textContent = dx.ok ? "✓ Converged" : "✕ Not converged";
  const row = (k, v, ok) => `<div class="r"><span>${k}</span><span${ok == null ? "" : ` class="flag ${ok ? "ok" : "bad"}"`}>${v}</span></div>`;
  const solveBox = (title, s) => `<div class="box"><h3>${title}</h3>${row("Converged", s.converged ? "yes" : "no", dx.solveOk(s))}
    ${row("Residual (max)", sci(s.residual_inf), s.residual_inf <= TOL)}${row("Iterations", s.iterations)}${row("Method", esc(s.method))}</div>`;
  const E = r.calibration.max_rel_error;
  let html = solveBox("Calibration solve", r.calibration.solve) + solveBox("Long-run solve", r.long_run.solve)
    + `<div class="box"><h3>Adjustment path</h3>${row("All periods converged", r.path.all_converged ? "yes" : "no", r.path.all_converged)}
       ${row("Worst residual", sci(r.path.worst_residual), r.path.worst_residual <= TOL)}
       ${row("Stop", r.path.stop?.reason ? esc(r.path.stop.reason.replace("_", " ")) : "—")}</div>`
    + `<div class="box"><h3>Calibration fit (max relative error)</h3>${row("Non-farm jobs H_U", sci(E.HU))}${row("Farm jobs H_A", sci(E.HA))}
       ${row("Farm wage w_A", sci(E.wA))}${row("Residents N", sci(E.N))}</div>`;
  const A = r.analytic;
  if (A) {
    const gap = A.x_closed_form ? Math.abs(A.x_solver / A.x_closed_form - 1) * 100 : NaN;
    html += `<div class="box"><h3>Two-location check (§4)</h3>${row("Welfare shock s", A.s.toFixed(4))}
      ${row("x / s, closed form", (A.x_closed_form / A.s).toFixed(3))}${row("x / s, solver", (A.x_solver / A.s).toFixed(3))}
      ${row("Gap", isFinite(gap) ? gap.toFixed(2) + "%" : "—", isFinite(gap) ? gap < 0.2 : null)}</div>`;
  }
  $("diag").innerHTML = html;
}

// ------------------------------------------------------------------ view state
function render() {
  const r = S.result;
  if (!r || $("output").hidden) return;
  drawTiles(r);
  drawMap(r);
  drawPath(r);
  drawTable(r);
  $("scrub").max = r.path.t.length - 1;
  $("scrub").value = S.period;
  $("scrubOut").textContent = `t = ${r.path.t[S.period]}`;
}

function setView(view) {
  S.view = view;
  for (const b of document.querySelectorAll(".seg button")) b.classList.toggle("on", b.dataset.view === view);
  $("scrubRow").hidden = view !== "path";
  $("metricWrap").hidden = view === "path";
  render();
}

function setPeriod(i) {
  S.period = i;
  if (S.view !== "path") return setView("path");
  render();
}

let playTimer = null;
function togglePlay() {
  if (playTimer) { clearInterval(playTimer); playTimer = null; $("playBtn").textContent = "▶"; return; }
  const last = S.result.path.t.length - 1;
  if (S.period >= last) S.period = 0;
  $("playBtn").textContent = "❚❚";
  playTimer = setInterval(() => {
    if (S.period >= last) return togglePlay();
    setPeriod(S.period + 1);
  }, 90);
}

function wireView() {
  $("metric").innerHTML = METRICS.map(([k, l]) => `<option value="${k}">${l}</option>`).join("");
  $("metric").addEventListener("change", e => { S.metric = e.target.value; render(); });
  for (const b of document.querySelectorAll(".seg button")) b.addEventListener("click", () => setView(b.dataset.view));
  $("scrub").addEventListener("input", e => setPeriod(Number(e.target.value)));
  $("playBtn").addEventListener("click", togglePlay);
  $("runBtn").addEventListener("click", requestRun);
  $("resetBtn").addEventListener("click", async () => {
    S.scenario = await backend.defaults();
    syncControls();
    requestRun();
  });
  $("themeBtn").addEventListener("click", () => {
    const root = document.documentElement;
    const cur = root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    root.dataset.theme = cur === "dark" ? "light" : "dark";
    try { localStorage.setItem("dp.theme", JSON.stringify(root.dataset.theme)); } catch { /* storage unavailable */ }
    render();
  });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", render);
  let rt = null;
  addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(render, 150); });
}

async function main() {
  buildControls();
  syncControls();
  wireView();
  if (FIXTURE) {
    backend = fixtureBackend();
  } else {
    $("loading").hidden = false;
    setStatus("Starting the model…");
    backend = workerBackend(onStage);
    try {
      const d = await backend.defaults();
      S.scenario = { params: { ...DEFAULT_SCENARIO.params, ...d.params }, shocks: { ...DEFAULT_SCENARIO.shocks, ...d.shocks } };
      syncControls();
    } catch (err) {
      return showError(err.message);
    }
    onStage({ stage: "run", text: "Solving the first scenario…" });
  }
  requestRun();
}

main();
