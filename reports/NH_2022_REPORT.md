# New Hampshire 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state NH 2022`. 10 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

## Sources

| Item | Vintage | File (data_raw) | Retrieved | URL |
|---|---|---|---|---|
| pep | Census PEP Vintage 2022, July 1 2022 estimates | `US/co-est2022-alldata.csv` | 2026-11-23 | https://www2.census.gov/programs-surveys/popest/datasets/2020-2022/counties/totals/co-est2022-alldata.csv |
| cbsa | Census PEP Vintage 2023 CBSA file (OMB July 2023 delineations) | `US/cbsa-est2023-alldata.csv` | 2026-11-23 | https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/metro/totals/cbsa-est2023-alldata.csv |
| cenpop | 2020 Census centers of population, county | `US/CenPop2020_Mean_CO.txt` | 2026-11-23 | https://www2.census.gov/geo/docs/reference/cenpop2020/county/CenPop2020_Mean_CO.txt |
| counties | Census cartographic boundary file 2022, 1:500k | `US/cb_2022_us_county_500k.zip` | 2026-11-23 | https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip |
| bea_emp | BEA CAEMP25N (formerly CAINC25N), released 2023-11-16 | `US/bea_CAEMP25N.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAEMP25N.zip |
| bea_farm | BEA CAINC45, released 2023-11-16 | `US/bea_CAINC45.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAINC45.zip |
| bea_earn | BEA CAINC5N, file dated 2026-01-14 | `US/bea_CAINC5N.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAINC5N.zip |
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 33 | `NH/CDL_2022_33.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=33 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C13 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NH.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 1,395,231 | 1,395,231 | 0.000% |
| ACS workers by residence | 726,246 | 726,246 | 0.000% |
| ACS workers by workplace | 698,242 | 698,242 | 0.000% |
| ACS workers working out of state | 97,218 | 97,218 | 0.000% |
| BEA non-farm employment (L80) | 927,828 | 927,828 | 0.000% |
| BEA farm employment (L70) | 5,194 | 5,194 | 0.000% |
| BEA farm proprietors (L50) | 3,812 | 3,812 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | -21,854,000 | -21,854,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 48,247,000 | 48,247,000 | 0.000% |
| CoA hired farm labour expense $ | 61,934,000 | 61,933,000 | 0.002% |
| BEA non-farm earnings $ (CAINC5N L82) | 70,881,570,000 | 70,881,570,000 | 0.000% |
| ACS foreign born entered 2010+ | 24,649 | 24,649 | 0.000% |
| CoA owned acres | 369,782 | 369,782 | 0.000% |
| CoA rented-from-others acres | 47,405 | 47,405 | 0.000% |
| CoA land in farms, ha | 168,830 | 168,830 | 0.000% |
| CoA total cropland, ha | 42,612 | 42,612 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.689, median 0.742, max 0.816; BEA counts jobs, ACS counts people by main job). Sum N = 795,460 = sum HU + HA = 795,460. Farm jobs after scaling: 3,893 (BEA 5,194). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 69,214. Jobs = in-state residents working out of state = 97,218, split by the state farm share (HA = 542). Location: the 11 out-of-state counties within 1 km of the state (23017, 23031, 25009, 25011, 25017, 25027, 50005, 50009, 50017, 50025, 50027); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 55,265 ha vs Census of Agriculture cropland 42,612 ha and land in farms 168,830 ha; county ratio TF / CoA cropland 0.92 to 1.60. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 34,242 ha). County area covered by CDL pixels: 2,403,803 ha vs land area 2,319,013 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 0.83 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (76,395 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 29,852 $ per BEA farm job, 39,833 $ per farm worker; county range 28,417 to 52,753 $ per worker. State compensation per farm wage job by year: 2018 29,318 $, 2019 24,066 $, 2020 26,682 $, 2021 24,926 $, 2022 34,911 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 8,134,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (61,933,000 $ in 2022, column `hired_labor_coa_usd`) is 1.28x BEA farm compensation (48,247,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state -4,208 $, county -22,997 to 52,330 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 102,083 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 107,630,000 $ vs CAINC45 -21,854,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.886, county range 0.833 to 0.940.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 52 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 7,159 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Hillsborough); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (2); rural = the rest (7). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 109.7 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 43.9 straight-line km/h between counties (median 22.0 to 48.6 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.35).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 33001 Belknap | not published; NASS 'other (combined) counties' value = 36.5 $/acre |
| cash_rent_usd_acre | 33003 Carroll | not published; NASS 'other (combined) counties' value = 36.5 $/acre |
| cash_rent_usd_acre | 33017 Strafford | not published; NASS 'other (combined) counties' value = 36.5 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26919) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 33001 | Belknap | rural | 32,144 | 28,499 | 242 | 2,359 | 12.00M | 28,417 | -18,533 | 0.931 | 36* |
| 33003 | Carroll | rural | 24,419 | 22,906 | 224 | 2,429 | 12.23M | 40,168 | 873 | 0.940 | 36* |
| 33005 | Cheshire | rural | 38,344 | 35,380 | 377 | 5,648 | 14.45M | 30,815 | -16,416 | 0.895 | 58 |
| 33007 | Coos | rural | 14,066 | 13,001 | 253 | 7,251 | 6.91M | 46,507 | -22,997 | 0.864 | 39 |
| 33009 | Grafton | rural | 45,358 | 57,002 | 419 | 11,888 | 17.63M | 34,541 | 52,330 | 0.903 | 52 |
| 33011 | Hillsborough | core | 231,932 | 215,787 | 533 | 5,645 | 92.94M | 39,890 | -15,178 | 0.833 | 40 |
| 33013 | Merrimack | rural | 78,773 | 80,595 | 576 | 7,164 | 29.76M | 51,755 | -5,571 | 0.881 | 38 |
| 33015 | Rockingham | suburb | 171,850 | 167,939 | 626 | 4,861 | 59.31M | 36,678 | -11,673 | 0.877 | 141 |
| 33017 | Strafford | suburb | 69,543 | 59,035 | 390 | 2,884 | 21.08M | 35,821 | -4,607 | 0.914 | 36* |
| 33019 | Sullivan | rural | 19,817 | 14,206 | 252 | 5,136 | 8.90M | 52,753 | -6,443 | 0.855 | 102 |
| EXT | External (out-of-state commuting) | external | 69,214 | 96,676 | 542 | 7,695 | 26.23M | 39,833 | n/a | 0.886 | n/a |

`*` filled, see above.
