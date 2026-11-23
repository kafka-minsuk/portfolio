# Prompts to paste into Claude Code (one per session/milestone)

Setup first: create the repo, put `CLAUDE.md` at the root, the spec at `docs/URQSE_model_spec.md`, and `urqse.py` + `test_urqse.py` in `reference/`.

---

## M1 — Package the core + new decisions (synthetic data only)

> Read CLAUDE.md and docs/URQSE_model_spec.md (especially §3, §5, §12). Port reference/urqse.py into the src/urqse package layout in CLAUDE.md, and move the reference tests into tests/. Keep them passing unchanged in behaviour.
> Then implement spec §12:
> 1. `land.py`: owner share ω_n per county, operator income, landlord income routing (ς local share), the `land_income_in_choice` flag (default False), and farmland asset prices along a path (PV + Gordon terminal, i−g calibrated from a price/rent ratio).
> 2. `immigration.py`: exogenous I_t path allocated by residence logit × gateway weights g_n. Set η=0 everywhere.
> 3. `dynamics.py`: a consolidation stop rule object (target ratio, ε, rural-county mask) returning the stop period and the reason.
> Add tests: population conservation with immigration; operator income = V/H when ω=1; land income not entering choice changes nothing in allocations when the flag is False; the stop rule fires on a synthetic urban-productivity shock; the asset-price constant-rent case.
> Before coding, show me a short plan and any spec ambiguities. Don't touch the app yet.

## M2 — Iowa data build (offline)

> Implement src/urqse/data/build_state.py for Iowa (2022 base year). Produce data/IA/2022/county.parquet with the schema in schema.py: N (ACS/PEP), HU, HA (BEA CAINC25N farm and non-farm jobs incl. proprietors), wA_obs (BEA CAINC45), TF (USDA Cropland Data Layer zonal stats), L (GHSL building volume), ω (Census of Agriculture tenure), cash rents and land values (NASS), and a travel-time matrix (OSM, r5py or OSRM). Add an external zone so jobs = resident workers. Write a validation report (markdown) with sources, vintages and coverage gaps. Mark anything uncertain `# VERIFY`. Download scripts must be idempotent and cache raw files.

## M3 — Calibration on real data

> Run the inversion (spec §5) on Iowa. Report the fit, the ξ_A map, and the cash-rent over-identification test (model ρ vs NASS cash rents). Estimate θ_T by county from rent shares and compare it with the 0.40 default. Estimate κλ by PPML on LODES OD flows. Save the calibrated fundamentals and a snapshot test.

## M4 — Streamlit app v1

> Build app/streamlit_app.py: state map (pydeck choropleth), calibration report tab, scenario builder (core productivity shock, travel-time cut on selected links, immigration path, consolidation target), results tab (long-run Δ maps, path animation with the stop marker, farmland price paths, stayer vs leaver wealth), and a diagnostics tab (convergence contract, sensitivity over λ_R, θ_T, μ). Cache solves on a hash of params + scenario. No model math in the app.

## M5 — Fast counterfactuals

> Implement exact hat algebra for the static model and check that it equals the level solve on 5 random scenarios. Add the optional JAX Newton fallback with a test where Anderson is forced to stall.
