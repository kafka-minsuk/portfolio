// Runs the URQSE Python model (docs/py/urqse.zip) under Pyodide, off the main thread.
// Protocol: in {id, type: "run", scenario} | {id, type: "default", region}
//           out {type: "status", stage, text} | {id, ok: true, result} | {id, ok: false, error}
// A real region's document (data/{region}.json, shape in urqse.api) is fetched once and kept in Python.
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
importScripts(PYODIDE + "pyodide.js");

const status = (stage, text) => postMessage({ type: "status", stage, text });

const ready = (async () => {
  status("runtime", "Downloading the Python runtime…");
  const py = await loadPyodide({ indexURL: PYODIDE });
  status("numpy", "Loading NumPy…");
  await py.loadPackage("numpy");
  status("model", "Loading the model package…");
  const res = await fetch(new URL("../py/urqse.zip", self.location.href));
  if (!res.ok) throw new Error(`Model package py/urqse.zip not found (HTTP ${res.status}).`);
  py.unpackArchive(await res.arrayBuffer(), "zip");
  py.runPython(`
import json, urqse.api
_docs = {}
def _to_json(obj):
    return obj if isinstance(obj, str) else json.dumps(obj, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
def _load(name, text): _docs[name] = json.loads(text)
def _run(s):
    sc = json.loads(s)
    return _to_json(urqse.api.run(sc, _docs.get(sc.get("region"))))
def _default(name): return _to_json(urqse.api.default_scenario(_docs.get(name)))
`);
  status("ready", "Model ready.");
  return py;
})();
ready.catch(err => status("error", String(err.message || err)));

const loaded = new Map();  // region -> Promise, so concurrent calls fetch once
function loadRegion(py, region) {
  if (!region || region === "synthetic") return null;
  if (!/^[A-Z]{2}_\d{4}$/.test(region)) throw new Error(`Unknown region ${region}`);
  if (!loaded.has(region)) loaded.set(region, (async () => {
    const res = await fetch(new URL(`data/${region}.json`, self.location.href));
    if (!res.ok) throw new Error(`Region data data/${region}.json not found (HTTP ${res.status}).`);
    py.globals.get("_load")(region, await res.text());
  })().catch(err => { loaded.delete(region); throw err; }));
  return loaded.get(region);
}

self.onmessage = async ({ data: { id, type, scenario, region } }) => {
  try {
    const py = await ready;
    await loadRegion(py, type === "run" ? scenario.region : region);
    const out = type === "run" ? py.globals.get("_run")(JSON.stringify(scenario)) : py.globals.get("_default")(region ?? "synthetic");
    postMessage({ id, ok: true, result: JSON.parse(out) });
  } catch (err) {
    postMessage({ id, ok: false, error: String(err.message || err) });
  }
};
