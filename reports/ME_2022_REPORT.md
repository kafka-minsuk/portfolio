# Maine 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state ME 2022`. 16 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 23 | `ME/CDL_2022_23.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=23 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C13 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_ME.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 1,385,340 | 1,385,340 | 0.000% |
| ACS workers by residence | 670,170 | 670,170 | 0.000% |
| ACS workers by workplace | 659,445 | 659,445 | 0.000% |
| ACS workers working out of state | 23,362 | 23,362 | 0.000% |
| BEA non-farm employment (L80) | 866,670 | 866,670 | 0.000% |
| BEA farm employment (L70) | 10,656 | 10,656 | 0.000% |
| BEA farm proprietors (L50) | 6,898 | 6,898 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 307,756,000 | 307,756,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 133,202,000 | 133,202,000 | 0.000% |
| CoA hired farm labour expense $ | 150,587,000 | 150,585,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 53,862,271,000 | 53,862,271,000 | 0.000% |
| ACS foreign born entered 2010+ | 17,647 | 17,647 | 0.000% |
| CoA owned acres | 1,034,043 | 1,034,043 | 0.000% |
| CoA rented-from-others acres | 191,003 | 191,003 | 0.000% |
| CoA land in farms, ha | 495,759 | 495,759 | 0.000% |
| CoA total cropland, ha | 180,238 | 180,238 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.672, median 0.761, max 0.810; BEA counts jobs, ACS counts people by main job). Sum N = 682,807 = sum HU + HA = 682,807. Farm jobs after scaling: 8,093 (BEA 10,656). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 12,637. Jobs = in-state residents working out of state = 23,362, split by the state farm share (HA = 287). Location: the 4 out-of-state counties within 1 km of the state (33003, 33007, 33015, 33017); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 255,977 ha vs Census of Agriculture cropland 180,238 ha and land in farms 495,759 ha; county ratio TF / CoA cropland 1.06 to 1.99. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 110,262 ha). County area covered by CDL pixels: 8,488,548 ha vs land area 7,988,817 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 0.99 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (62,149 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 29,461 $ per BEA farm job, 38,790 $ per farm worker; county range 23,916 to 74,467 $ per worker. State compensation per farm wage job by year: 2018 29,680 $, 2019 24,496 $, 2020 27,047 $, 2021 25,368 $, 2022 35,445 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 19,368,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (150,585,000 $ in 2022, column `hired_labor_coa_usd`) is 1.13x BEA farm compensation (133,202,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 28,881 $, county 7,717 to 83,314 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 82,693 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 304,418,000 $ vs CAINC45 307,756,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.844, county range 0.763 to 0.935.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 60 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,729 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Cumberland); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (4); rural = the rest (11). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 140.8 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 47.1 straight-line km/h between counties (median 17.0 to 87.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.33).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 23007 Franklin | not published; NASS 'other (combined) counties' value = 57 $/acre |
| cash_rent_usd_acre | 23013 Knox | not published; NASS 'other (combined) counties' value = 57 $/acre |
| cash_rent_usd_acre | 23021 Piscataquis | not published; NASS 'other (combined) counties' value = 57 $/acre |
| cash_rent_usd_acre | 23023 Sagadahoc | not published; NASS 'other (combined) counties' value = 57 $/acre |
| cash_rent_usd_acre | 23029 Washington | not published; NASS 'other (combined) counties' value = 57 $/acre |

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
| 23001 | Androscoggin | suburb | 54,700 | 49,908 | 467 | 10,055 | 27.75M | 40,216 | 83,314 | 0.894 | 56 |
| 23003 | Aroostook | rural | 28,276 | 26,804 | 1,250 | 90,553 | 19.01M | 39,190 | 66,395 | 0.788 | 86 |
| 23005 | Cumberland | core | 164,899 | 191,620 | 703 | 9,215 | 72.49M | 43,203 | 11,568 | 0.846 | 94 |
| 23007 | Franklin | rural | 13,669 | 11,897 | 307 | 7,071 | 7.91M | 23,916 | 8,805 | 0.909 | 57* |
| 23009 | Hancock | rural | 27,161 | 25,202 | 336 | 8,044 | 14.99M | 56,526 | 20,658 | 0.874 | 125 |
| 23011 | Kennebec | rural | 59,235 | 62,513 | 606 | 17,842 | 28.55M | 31,557 | 18,244 | 0.795 | 37 |
| 23013 | Knox | rural | 18,931 | 20,184 | 239 | 3,834 | 10.93M | 30,868 | 28,979 | 0.806 | 57* |
| 23015 | Lincoln | rural | 16,466 | 13,556 | 281 | 3,470 | 9.15M | 31,254 | 24,875 | 0.872 | 44 |
| 23017 | Oxford | rural | 25,576 | 20,542 | 483 | 11,251 | 13.20M | 29,894 | 19,673 | 0.900 | 37 |
| 23019 | Penobscot | suburb | 72,207 | 75,578 | 625 | 25,077 | 36.08M | 36,652 | 12,139 | 0.861 | 42 |
| 23021 | Piscataquis | rural | 6,957 | 6,484 | 169 | 6,947 | 4.37M | 35,507 | 9,210 | 0.891 | 57* |
| 23023 | Sagadahoc | suburb | 18,551 | 16,309 | 206 | 2,163 | 9.79M | 36,302 | 7,717 | 0.881 | 57* |
| 23025 | Somerset | rural | 22,146 | 18,194 | 738 | 20,691 | 15.60M | 38,661 | 29,176 | 0.763 | 24 |
| 23027 | Waldo | rural | 18,015 | 13,591 | 475 | 11,946 | 8.90M | 27,943 | 8,811 | 0.847 | 24 |
| 23029 | Washington | rural | 12,356 | 11,735 | 523 | 18,442 | 8.30M | 74,467 | 37,659 | 0.935 | 57* |
| 23031 | York | suburb | 111,025 | 87,235 | 685 | 9,376 | 41.36M | 32,956 | 11,160 | 0.905 | 34 |
| EXT | External (out-of-state commuting) | external | 12,637 | 23,075 | 287 | 9,068 | 6.19M | 38,790 | n/a | 0.844 | n/a |

`*` filled, see above.
