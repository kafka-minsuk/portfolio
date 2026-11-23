// Runs the URQSE Python model (docs/py/urqse.zip) under Pyodide, off the main thread.
// Protocol: in {id, type: "run", scenario} | {id, type: "default"}
//           out {type: "status", stage, text} | {id, ok: true, result} | {id, ok: false, error}
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
def _to_json(obj):
    return obj if isinstance(obj, str) else json.dumps(obj, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
def _run(s): return _to_json(urqse.api.run(json.loads(s)))
def _default(): return _to_json(urqse.api.default_scenario())
`);
  status("ready", "Model ready.");
  return py;
})();
ready.catch(err => status("error", String(err.message || err)));

self.onmessage = async ({ data: { id, type, scenario } }) => {
  try {
    const py = await ready;
    const out = type === "run" ? py.globals.get("_run")(JSON.stringify(scenario)) : py.globals.get("_default")();
    postMessage({ id, ok: true, result: JSON.parse(out) });
  } catch (err) {
    postMessage({ id, ok: false, error: String(err.message || err) });
  }
};
