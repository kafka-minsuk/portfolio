# Georgia 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state GA 2022`. 159 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 13 | `GA/CDL_2022_13.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=13 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R6_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_GA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (16 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 10,912,876 | 10,912,876 | 0.000% |
| ACS workers by residence | 5,010,799 | 5,010,799 | 0.000% |
| ACS workers by workplace | 5,011,862 | 5,011,862 | 0.000% |
| ACS workers working out of state | 129,637 | 129,637 | 0.000% |
| BEA non-farm employment (L80) | 6,914,446 | 6,914,446 | 0.000% |
| BEA farm employment (L70) | 57,015 | 57,015 | 0.000% |
| BEA farm proprietors (L50) | 34,525 | 34,525 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 3,145,316,000 | 3,145,316,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 445,721,000 | 445,721,000 | 0.000% |
| CoA hired farm labour expense $ | 680,489,000 | 691,014,000 | -1.523% |
| BEA non-farm earnings $ (CAINC5N L82) | 440,973,179,000 | 440,973,179,000 | 0.000% |
| ACS foreign born entered 2010+ | 333,394 | 333,394 | 0.000% |
| CoA owned acres | 7,224,087 | 7,296,571 | -0.993% |
| CoA rented-from-others acres | 2,617,647 | 2,642,742 | -0.950% |
| CoA land in farms, ha | 4,022,297 | 4,022,297 | 0.000% |
| CoA total cropland, ha | 1,830,671 | 1,830,688 | -0.001% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.370, median 0.720, max 1.164; BEA counts jobs, ACS counts people by main job). Sum N = 5,141,499 = sum HU + HA = 5,141,499. Farm jobs after scaling: 41,125 (BEA 57,015). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 130,700. Jobs = in-state residents working out of state = 129,637, split by the state farm share (HA = 1,064). Location: the 38 out-of-state counties within 1 km of the state (01005, 01017, 01019, 01029, 01049, 01067, 01069, 01071, 01081, 01111, 01113, 12003, 12023, 12039, 12047, 12063, 12065, 12073, 12079, 12089, 37039, 37043, 37099, 37113, 45001, 45003, 45005, 45007, 45011, 45037, 45049, 45053, 45065, 45073, 47011, 47065, 47115, 47139); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,869,512 ha vs Census of Agriculture cropland 1,830,688 ha and land in farms 4,022,297 ha; county ratio TF / CoA cropland 0.05 to 4.66. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,226,746 ha). County area covered by CDL pixels: 15,257,055 ha vs land area 14,948,627 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 10.29 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (63,776 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 21,644 $ per BEA farm job, 30,007 $ per farm worker; county range 2,231 to 74,277 $ per worker. State compensation per farm wage job by year: 2018 22,926 $, 2019 20,251 $, 2020 19,410 $, 2021 23,032 $, 2022 19,819 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 211,062,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (691,014,000 $ in 2022, column `hired_labor_coa_usd`) is 1.55x BEA farm compensation (445,721,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 55,166 $, county -127,222 to 243,919 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 88,714 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 3,374,525,000 $ vs CAINC45 3,145,316,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.734, county range 0.469 to 1.000.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 74 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 4,270 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 8 counties have no recent foreign born in the ACS sample (Crisp, Glascock, Heard, Oglethorpe, Quitman, Talbot, Taliaferro, Treutlen), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Fulton); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (73); rural = the rest (85). `# VERIFY` one core for a multi-metro state.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 193.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 60.6 straight-line km/h between counties (median 9.1 to 24.9 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.20).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| rented_acres | 13053 Chattahoochee | land in farms minus the other tenure (Census of Ag identity) |
| rented_acres | 13063 Clayton | land in farms minus the other tenure (Census of Ag identity) |
| rented_acres | 13215 Muscogee | land in farms minus the other tenure (Census of Ag identity) |
| omega | 13039 Camden | state owner share |
| omega | 13089 DeKalb | state owner share |
| omega | 13179 Liberty | state owner share |
| omega | 13191 McIntosh | state owner share |
| omega | 13239 Quitman | state owner share |
| omega | 13309 Wheeler | state owner share |
| cash_rent_usd_acre | 13009 Baldwin | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13021 Bibb | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13025 Brantley | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13029 Bryan | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13039 Camden | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13045 Carroll | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13049 Charlton | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13051 Chatham | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13053 Chattahoochee | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13059 Clarke | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13061 Clay | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13063 Clayton | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13065 Clinch | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13067 Cobb | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13073 Columbia | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13089 DeKalb | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13095 Dougherty | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13097 Douglas | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13101 Echols | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13109 Evans | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13111 Fannin | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13113 Fayette | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13117 Forsyth | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13121 Fulton | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13127 Glynn | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13131 Grady | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13133 Greene | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13135 Gwinnett | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13145 Harris | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13149 Heard | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13151 Henry | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13159 Jasper | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13171 Lamar | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13177 Lee | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13179 Liberty | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13181 Lincoln | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13191 McIntosh | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13215 Muscogee | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13223 Paulding | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13239 Quitman | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13241 Rabun | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13245 Richmond | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13247 Rockdale | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13249 Schley | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13255 Spalding | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13259 Stewart | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13265 Taliaferro | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13271 Telfair | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13281 Towns | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13283 Treutlen | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13301 Warren | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| cash_rent_usd_acre | 13309 Wheeler | not published; NASS 'other (combined) counties' value = 51.5 $/acre |
| owned_acres | 13039 Camden | (D) in Census of Ag; see fills above |
| owned_acres | 13089 DeKalb | (D) in Census of Ag; see fills above |
| owned_acres | 13179 Liberty | (D) in Census of Ag; see fills above |
| owned_acres | 13191 McIntosh | (D) in Census of Ag; see fills above |
| owned_acres | 13239 Quitman | (D) in Census of Ag; see fills above |
| owned_acres | 13309 Wheeler | (D) in Census of Ag; see fills above |
| rented_acres | 13039 Camden | (D) in Census of Ag; see fills above |
| rented_acres | 13089 DeKalb | (D) in Census of Ag; see fills above |
| rented_acres | 13179 Liberty | (D) in Census of Ag; see fills above |
| rented_acres | 13191 McIntosh | (D) in Census of Ag; see fills above |
| rented_acres | 13239 Quitman | (D) in Census of Ag; see fills above |
| rented_acres | 13309 Wheeler | (D) in Census of Ag; see fills above |
| farm_comp_per_ws_job | 13053 Chattahoochee | 2018: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 13053 Chattahoochee | 2019: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 13053 Chattahoochee | 2020: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 13053 Chattahoochee | 2021: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 13053 Chattahoochee | 2022: compensation (D) or no farm wage jobs; state value |
| hired_labor_coa_usd | 13053 Chattahoochee | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 13089 DeKalb | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 13125 Glascock | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 13179 Liberty | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 13215 Muscogee | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 13239 Quitman | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 13269 Taylor | (D) in Census of Ag; left null (comparison column only) |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26917) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 13001 | Appling | rural | 7,195 | 6,718 | 494 | 29,119 | 8.36M | 31,718 | 111,997 | 0.689 | 90 |
| 13003 | Atkinson | rural | 3,523 | 2,827 | 261 | 19,522 | 2.81M | 19,437 | 97,434 | 0.696 | 115 |
| 13005 | Bacon | rural | 4,213 | 3,414 | 318 | 21,655 | 3.79M | 34,053 | 66,672 | 0.792 | 92 |
| 13007 | Baker | rural | 875 | 405 | 136 | 34,023 | 1.31M | 51,471 | 58,521 | 0.757 | 90 |
| 13009 | Baldwin | rural | 16,374 | 15,222 | 69 | 1,681 | 11.47M | 15,676 | -13,463 | 0.850 | 52* |
| 13011 | Banks | rural | 8,321 | 4,478 | 373 | 1,711 | 5.35M | 25,068 | 142,359 | 0.832 | 26 |
| 13013 | Barrow | suburb | 40,978 | 24,340 | 218 | 1,402 | 18.42M | 33,610 | -7,305 | 0.776 | 35 |
| 13015 | Bartow | suburb | 51,272 | 47,037 | 430 | 5,239 | 31.39M | 26,266 | 38,368 | 0.782 | 36 |
| 13017 | Ben Hill | rural | 7,099 | 6,759 | 256 | 15,418 | 6.88M | 20,070 | 20,645 | 0.879 | 96 |
| 13019 | Berrien | rural | 7,206 | 4,298 | 394 | 36,949 | 5.77M | 37,691 | 28,835 | 0.734 | 106 |
| 13021 | Bibb | suburb | 63,811 | 83,950 | 90 | 2,171 | 71.48M | 11,619 | 5,992 | 0.961 | 52* |
| 13023 | Bleckley | rural | 4,963 | 2,448 | 150 | 17,850 | 3.22M | 22,565 | 25,947 | 0.874 | 60 |
| 13025 | Brantley | suburb | 6,865 | 2,206 | 112 | 4,377 | 3.90M | 55,895 | -2,383 | 0.814 | 52* |
| 13027 | Brooks | suburb | 6,521 | 3,307 | 403 | 39,767 | 4.79M | 41,645 | 60,213 | 0.734 | 96 |
| 13029 | Bryan | suburb | 21,534 | 10,954 | 51 | 1,974 | 9.85M | 30,890 | 24,699 | 0.802 | 52* |
| 13031 | Bulloch | rural | 34,969 | 30,274 | 491 | 43,260 | 17.40M | 29,743 | 14,664 | 0.580 | 68 |
| 13033 | Burke | suburb | 10,318 | 13,255 | 514 | 52,965 | 7.72M | 29,304 | 68,097 | 0.722 | 37 |
| 13035 | Butts | suburb | 10,025 | 7,736 | 92 | 1,012 | 4.56M | 28,802 | 13,299 | 0.920 | 25 |
| 13037 | Calhoun | rural | 1,574 | 1,229 | 216 | 26,298 | 1.55M | 32,682 | 66,326 | 0.707 | 55 |
| 13039 | Camden | rural | 25,574 | 22,581 | 54 | 77 | 13.43M | 19,210 | -1,567 | 0.734 | 52* |
| 13043 | Candler | rural | 4,429 | 3,349 | 175 | 14,301 | 3.63M | 32,747 | 41,642 | 0.793 | 54 |
| 13045 | Carroll | suburb | 54,488 | 47,455 | 807 | 1,005 | 26.69M | 22,179 | 75,035 | 0.809 | 52* |
| 13047 | Catoosa | suburb | 32,259 | 18,312 | 211 | 632 | 20.18M | 31,386 | 34,128 | 0.850 | 26 |
| 13049 | Charlton | rural | 4,961 | 2,707 | 90 | 1,023 | 2.69M | 14,356 | 12,822 | 0.808 | 52* |
| 13051 | Chatham | suburb | 143,265 | 181,560 | 52 | 176 | 151.41M | 14,937 | 56,136 | 0.929 | 52* |
| 13053 | Chattahoochee | suburb | 5,719 | 14,793 | 7 | 560 | 3.44M | 28,655 | -127,222 | 1.000 | 52* |
| 13055 | Chattooga | rural | 8,879 | 6,049 | 226 | 2,541 | 6.53M | 24,797 | 56,390 | 0.836 | 37 |
| 13057 | Cherokee | suburb | 139,111 | 93,731 | 372 | 490 | 51.54M | 26,268 | 13,257 | 0.748 | 46 |
| 13059 | Clarke | suburb | 62,244 | 78,884 | 159 | 750 | 36.55M | 49,412 | 39,068 | 0.923 | 52* |
| 13061 | Clay | rural | 1,101 | 636 | 62 | 11,267 | 0.86M | 67,004 | 3,438 | 0.738 | 52* |
| 13063 | Clayton | suburb | 134,762 | 121,242 | 19 | 73 | 102.50M | 2,951 | -25,067 | 1.000 | 52* |
| 13065 | Clinch | rural | 2,512 | 2,231 | 97 | 4,061 | 2.04M | 68,869 | 59,027 | 0.967 | 52* |
| 13067 | Cobb | suburb | 401,114 | 397,840 | 115 | 28 | 276.99M | 44,772 | 13,331 | 0.933 | 52* |
| 13069 | Coffee | rural | 17,589 | 18,404 | 666 | 43,816 | 14.37M | 32,090 | 62,830 | 0.679 | 92 |
| 13071 | Colquitt | rural | 19,065 | 15,766 | 1,072 | 56,216 | 15.07M | 31,853 | 70,966 | 0.558 | 119 |
| 13073 | Columbia | suburb | 75,125 | 47,844 | 150 | 675 | 44.30M | 25,122 | -250 | 0.797 | 52* |
| 13075 | Cook | rural | 7,706 | 5,628 | 401 | 23,179 | 6.12M | 25,681 | 17,179 | 0.605 | 100 |
| 13077 | Coweta | suburb | 72,084 | 51,857 | 318 | 716 | 28.15M | 31,702 | 5,029 | 0.890 | 24 |
| 13079 | Crawford | suburb | 4,844 | 1,747 | 311 | 5,153 | 2.72M | 27,556 | 69,247 | 0.812 | 39 |
| 13081 | Crisp | rural | 8,315 | 9,005 | 279 | 31,814 | 10.56M | 39,165 | 22,981 | 0.558 | 78 |
| 13083 | Dade | suburb | 6,928 | 4,489 | 149 | 500 | 4.73M | 20,126 | 60,163 | 0.872 | 24 |
| 13085 | Dawson | suburb | 13,367 | 11,732 | 177 | 378 | 5.48M | 17,083 | 117,906 | 0.744 | 36 |
| 13087 | Decatur | rural | 10,902 | 9,549 | 509 | 51,320 | 9.15M | 41,421 | 55,006 | 0.702 | 91 |
| 13089 | DeKalb | suburb | 378,641 | 356,335 | 27 | 86 | 280.69M | 12,196 | -1,974 | 0.734 | 52* |
| 13091 | Dodge | rural | 7,620 | 5,162 | 304 | 22,817 | 4.87M | 28,131 | 18,160 | 0.899 | 52 |
| 13093 | Dooly | rural | 3,902 | 4,043 | 363 | 50,317 | 3.27M | 25,397 | 91,076 | 0.596 | 76 |
| 13095 | Dougherty | suburb | 32,937 | 46,038 | 178 | 18,040 | 47.85M | 47,359 | 27,454 | 0.862 | 52* |
| 13097 | Douglas | suburb | 69,337 | 53,902 | 78 | 104 | 34.30M | 22,378 | 3,000 | 0.623 | 52* |
| 13099 | Early | rural | 4,220 | 3,862 | 298 | 48,289 | 4.57M | 39,038 | 13,742 | 0.731 | 76 |
| 13101 | Echols | suburb | 1,901 | 891 | 81 | 2,427 | 0.80M | 34,715 | -44,986 | 0.555 | 52* |
| 13103 | Effingham | suburb | 30,689 | 14,799 | 164 | 9,164 | 15.81M | 23,881 | 29,391 | 0.708 | 34 |
| 13105 | Elbert | rural | 8,440 | 6,746 | 329 | 4,573 | 8.98M | 26,998 | 71,950 | 0.787 | 19 |
| 13107 | Emanuel | rural | 8,865 | 6,394 | 288 | 23,212 | 6.47M | 47,030 | 10,946 | 0.844 | 59 |
| 13109 | Evans | rural | 4,262 | 4,766 | 209 | 6,954 | 2.76M | 36,932 | 37,567 | 0.812 | 52* |
| 13111 | Fannin | rural | 9,711 | 9,955 | 183 | 1,113 | 5.58M | 27,734 | 46,179 | 0.883 | 52* |
| 13113 | Fayette | suburb | 54,097 | 55,046 | 126 | 187 | 32.20M | 30,329 | 5,150 | 0.902 | 52* |
| 13115 | Floyd | suburb | 42,651 | 43,033 | 456 | 4,995 | 31.29M | 30,606 | 25,403 | 0.803 | 41 |
| 13117 | Forsyth | suburb | 128,130 | 112,854 | 288 | 536 | 59.63M | 19,107 | 44,762 | 0.704 | 52* |
| 13119 | Franklin | rural | 9,404 | 8,509 | 868 | 3,621 | 8.95M | 12,229 | 124,508 | 0.745 | 26 |
| 13121 | Fulton | core | 551,789 | 913,610 | 243 | 213 | 426.95M | 18,889 | -6,557 | 0.946 | 52* |
| 13123 | Gilmer | rural | 13,217 | 9,392 | 308 | 1,179 | 6.66M | 19,950 | 243,919 | 0.834 | 40 |
| 13125 | Glascock | rural | 1,286 | 308 | 46 | 2,958 | 0.83M | 16,844 | -10,587 | 0.643 | 21 |
| 13127 | Glynn | suburb | 36,929 | 43,697 | 68 | 57 | 41.52M | 15,547 | -1,889 | 0.900 | 52* |
| 13129 | Gordon | rural | 26,088 | 26,678 | 646 | 5,425 | 19.71M | 27,019 | 145,659 | 0.671 | 35 |
| 13131 | Grady | rural | 10,600 | 5,983 | 607 | 33,400 | 7.79M | 34,451 | 38,396 | 0.793 | 52* |
| 13133 | Greene | rural | 7,261 | 8,595 | 224 | 2,472 | 5.03M | 23,340 | 111,458 | 0.753 | 52* |
| 13135 | Gwinnett | suburb | 464,985 | 420,742 | 177 | 352 | 325.92M | 27,806 | 11,861 | 0.861 | 52* |
| 13137 | Habersham | rural | 20,660 | 16,644 | 433 | 923 | 9.54M | 23,341 | 128,328 | 0.679 | 38 |
| 13139 | Hall | suburb | 97,489 | 99,174 | 600 | 1,818 | 51.95M | 29,313 | 41,639 | 0.813 | 32 |
| 13141 | Hancock | rural | 2,445 | 1,673 | 95 | 1,570 | 2.21M | 18,180 | 17,914 | 0.917 | 24 |
| 13143 | Haralson | suburb | 13,781 | 10,713 | 290 | 473 | 7.27M | 11,266 | 60,140 | 0.857 | 20 |
| 13145 | Harris | suburb | 15,595 | 6,551 | 158 | 177 | 5.76M | 21,089 | -2,761 | 0.875 | 52* |
| 13147 | Hart | rural | 10,998 | 8,210 | 674 | 5,569 | 11.53M | 14,133 | 89,789 | 0.733 | 28 |
| 13149 | Heard | suburb | 4,470 | 2,142 | 118 | 397 | 4.31M | 28,575 | 91,497 | 0.814 | 52* |
| 13151 | Henry | suburb | 115,681 | 86,618 | 199 | 1,121 | 51.65M | 21,779 | 4,706 | 0.815 | 52* |
| 13153 | Houston | suburb | 78,041 | 76,443 | 228 | 17,400 | 55.24M | 22,313 | 14,828 | 0.789 | 58 |
| 13155 | Irwin | rural | 3,897 | 1,963 | 334 | 37,559 | 2.91M | 42,264 | 32,071 | 0.728 | 105 |
| 13157 | Jackson | rural | 36,440 | 36,388 | 607 | 3,705 | 19.72M | 42,530 | 69,570 | 0.684 | 22 |
| 13159 | Jasper | suburb | 6,326 | 2,969 | 161 | 2,278 | 2.97M | 34,114 | 8,465 | 0.915 | 52* |
| 13161 | Jeff Davis | rural | 5,757 | 4,709 | 161 | 18,221 | 4.71M | 38,435 | 21,394 | 0.547 | 96 |
| 13163 | Jefferson | rural | 6,165 | 4,804 | 301 | 30,540 | 4.59M | 35,597 | 48,196 | 0.718 | 36 |
| 13165 | Jenkins | rural | 2,859 | 2,564 | 291 | 20,486 | 2.57M | 26,364 | 38,629 | 0.824 | 55 |
| 13167 | Johnson | rural | 3,175 | 1,796 | 190 | 10,278 | 2.17M | 17,860 | -20,749 | 0.816 | 43 |
| 13169 | Jones | suburb | 12,627 | 5,928 | 137 | 1,390 | 6.06M | 27,539 | 1,046 | 0.808 | 24 |
| 13171 | Lamar | rural | 7,952 | 5,515 | 247 | 2,577 | 3.43M | 22,880 | 66,944 | 0.701 | 52* |
| 13173 | Lanier | suburb | 3,781 | 2,214 | 113 | 10,284 | 1.98M | 45,147 | -11,278 | 0.739 | 80 |
| 13175 | Laurens | rural | 19,037 | 19,042 | 483 | 27,646 | 16.23M | 33,214 | 25,809 | 0.828 | 40 |
| 13177 | Lee | suburb | 15,619 | 5,931 | 161 | 34,489 | 8.10M | 62,307 | 59,379 | 0.711 | 52* |
| 13179 | Liberty | suburb | 29,627 | 33,678 | 33 | 498 | 24.20M | 34,401 | -15,698 | 0.734 | 52* |
| 13181 | Lincoln | suburb | 3,162 | 1,446 | 85 | 1,015 | 2.24M | 27,906 | 9,173 | 0.626 | 52* |
| 13183 | Long | suburb | 7,445 | 2,226 | 54 | 1,583 | 2.81M | 30,923 | 73,347 | 0.757 | 37 |
| 13185 | Lowndes | suburb | 52,388 | 58,087 | 394 | 17,225 | 38.99M | 25,932 | 13,413 | 0.739 | 84 |
| 13187 | Lumpkin | suburb | 15,172 | 10,760 | 204 | 492 | 5.68M | 31,228 | 33,798 | 0.776 | 26 |
| 13189 | McDuffie | suburb | 9,457 | 8,933 | 426 | 2,145 | 6.65M | 42,256 | 26,719 | 0.814 | 24 |
| 13191 | McIntosh | suburb | 4,519 | 2,645 | 50 | 50 | 2.77M | 55,261 | 7,111 | 0.734 | 52* |
| 13193 | Macon | rural | 3,533 | 3,203 | 413 | 32,081 | 4.21M | 31,204 | 175,719 | 0.606 | 64 |
| 13195 | Madison | suburb | 12,960 | 5,049 | 503 | 4,737 | 6.83M | 22,881 | 139,199 | 0.780 | 24 |
| 13197 | Marion | suburb | 2,806 | 1,243 | 139 | 8,403 | 1.74M | 29,780 | 12,650 | 0.846 | 41 |
| 13199 | Meriwether | suburb | 7,732 | 4,375 | 182 | 1,365 | 4.38M | 50,901 | 4,896 | 0.853 | 36 |
| 13201 | Miller | rural | 2,382 | 1,952 | 222 | 41,367 | 2.57M | 35,018 | 54,781 | 0.499 | 81 |
| 13205 | Mitchell | rural | 7,509 | 6,943 | 642 | 66,348 | 8.48M | 32,910 | 98,173 | 0.605 | 79 |
| 13207 | Monroe | suburb | 12,742 | 10,344 | 181 | 2,345 | 7.28M | 27,247 | 69,746 | 0.761 | 46 |
| 13209 | Montgomery | rural | 3,395 | 1,357 | 125 | 7,846 | 1.95M | 34,070 | 27,988 | 0.889 | 67 |
| 13211 | Morgan | suburb | 9,658 | 8,983 | 522 | 6,922 | 5.87M | 27,129 | 27,454 | 0.753 | 32 |
| 13213 | Murray | suburb | 17,719 | 9,567 | 264 | 2,711 | 10.27M | 36,509 | 193,742 | 0.829 | 36 |
| 13215 | Muscogee | suburb | 88,082 | 109,174 | 18 | 144 | 82.60M | 2,231 | -47,591 | 1.000 | 52* |
| 13217 | Newton | suburb | 52,493 | 33,817 | 225 | 2,136 | 23.24M | 15,011 | -2,771 | 0.748 | 26 |
| 13219 | Oconee | suburb | 20,456 | 19,148 | 401 | 2,622 | 8.01M | 34,859 | 23,673 | 0.898 | 26 |
| 13221 | Oglethorpe | suburb | 6,959 | 2,091 | 310 | 4,757 | 4.57M | 50,758 | 112,247 | 0.826 | 30 |
| 13223 | Paulding | suburb | 82,606 | 41,567 | 95 | 159 | 20.35M | 11,087 | 8,912 | 0.881 | 52* |
| 13225 | Peach | suburb | 11,644 | 10,807 | 354 | 10,017 | 7.47M | 26,024 | 45,695 | 0.796 | 76 |
| 13227 | Pickens | suburb | 15,293 | 11,532 | 219 | 485 | 5.85M | 23,984 | 88,957 | 0.594 | 25 |
| 13229 | Pierce | rural | 8,446 | 4,847 | 310 | 19,921 | 5.65M | 26,742 | 15,057 | 0.684 | 105 |
| 13231 | Pike | suburb | 8,480 | 4,090 | 196 | 1,462 | 3.33M | 46,292 | 12,346 | 0.838 | 44 |
| 13233 | Polk | rural | 17,896 | 14,053 | 300 | 2,234 | 10.30M | 23,313 | 60,737 | 0.660 | 42 |
| 13235 | Pulaski | rural | 3,555 | 2,443 | 394 | 23,514 | 3.16M | 20,587 | 30,950 | 0.745 | 114 |
| 13237 | Putnam | rural | 9,295 | 7,045 | 231 | 2,868 | 6.28M | 40,098 | 15,334 | 0.624 | 38 |
| 13239 | Quitman | rural | 525 | 363 | 21 | 1,487 | 0.63M | 21,129 | -2,694 | 0.734 | 52* |
| 13241 | Rabun | rural | 6,735 | 6,994 | 117 | 447 | 3.93M | 43,899 | 4,600 | 0.765 | 52* |
| 13243 | Randolph | rural | 2,390 | 2,030 | 181 | 25,221 | 2.15M | 48,843 | 22,423 | 0.734 | 46 |
| 13245 | Richmond | suburb | 91,150 | 129,382 | 114 | 3,466 | 81.28M | 11,196 | 3,493 | 0.912 | 52* |
| 13247 | Rockdale | suburb | 42,514 | 41,236 | 116 | 215 | 24.50M | 6,995 | 1,614 | 0.566 | 52* |
| 13249 | Schley | rural | 1,857 | 1,031 | 58 | 5,517 | 1.37M | 35,131 | 84,385 | 0.881 | 52* |
| 13251 | Screven | rural | 5,799 | 3,797 | 305 | 34,487 | 3.59M | 32,822 | 1,198 | 0.699 | 49 |
| 13253 | Seminole | rural | 3,239 | 2,511 | 193 | 35,001 | 3.38M | 38,800 | 74,644 | 0.469 | 83 |
| 13255 | Spalding | suburb | 27,798 | 24,322 | 183 | 1,112 | 14.25M | 21,015 | 3,815 | 0.834 | 52* |
| 13257 | Stephens | rural | 11,191 | 10,183 | 270 | 458 | 7.31M | 21,864 | 101,391 | 0.649 | 30 |
| 13259 | Stewart | suburb | 1,450 | 1,075 | 53 | 7,348 | 0.94M | 33,814 | 46,887 | 0.823 | 52* |
| 13261 | Sumter | rural | 11,843 | 12,348 | 519 | 44,037 | 9.41M | 31,516 | 77,000 | 0.761 | 56 |
| 13263 | Talbot | suburb | 2,420 | 658 | 34 | 578 | 1.61M | 31,771 | 18,857 | 0.942 | 23 |
| 13265 | Taliaferro | rural | 670 | 409 | 82 | 656 | 0.70M | 10,531 | 104,711 | 0.891 | 52* |
| 13267 | Tattnall | rural | 7,609 | 5,726 | 606 | 22,030 | 6.53M | 74,277 | 161,994 | 0.767 | 66 |
| 13269 | Taylor | rural | 2,827 | 1,662 | 178 | 11,435 | 2.32M | 28,219 | 30,173 | 0.750 | 56 |
| 13271 | Telfair | rural | 3,676 | 3,702 | 287 | 16,025 | 3.73M | 16,693 | 29,865 | 0.722 | 52* |
| 13273 | Terrell | suburb | 3,275 | 2,300 | 205 | 31,360 | 3.29M | 38,657 | 32,401 | 0.655 | 76 |
| 13275 | Thomas | rural | 20,528 | 23,516 | 550 | 33,559 | 16.07M | 31,276 | 14,618 | 0.753 | 110 |
| 13277 | Tift | rural | 17,682 | 24,481 | 395 | 27,048 | 17.44M | 30,706 | 24,126 | 0.633 | 103 |
| 13279 | Toombs | rural | 9,940 | 11,734 | 289 | 16,227 | 8.02M | 56,845 | 47,328 | 0.785 | 49 |
| 13281 | Towns | rural | 4,510 | 3,453 | 70 | 580 | 3.13M | 40,287 | -16,105 | 0.648 | 52* |
| 13283 | Treutlen | rural | 2,163 | 1,076 | 95 | 4,821 | 1.46M | 26,194 | 17,994 | 0.797 | 52* |
| 13285 | Troup | rural | 30,516 | 36,891 | 151 | 227 | 22.53M | 13,737 | -4,440 | 0.904 | 20 |
| 13287 | Turner | rural | 3,301 | 2,292 | 211 | 28,772 | 2.94M | 33,691 | 53,528 | 0.629 | 96 |
| 13289 | Twiggs | suburb | 2,727 | 2,334 | 85 | 5,920 | 2.53M | 19,759 | -1,372 | 0.776 | 62 |
| 13291 | Union | rural | 9,400 | 9,557 | 208 | 1,984 | 5.54M | 13,115 | 29,763 | 0.697 | 58 |
| 13293 | Upson | rural | 11,247 | 8,774 | 273 | 1,268 | 7.88M | 34,043 | 71,534 | 0.905 | 49 |
| 13295 | Walker | suburb | 29,901 | 17,825 | 471 | 3,535 | 19.85M | 23,801 | 94,103 | 0.707 | 26 |
| 13297 | Walton | suburb | 45,662 | 30,134 | 362 | 4,136 | 21.77M | 33,924 | 4,832 | 0.636 | 34 |
| 13299 | Ware | rural | 12,933 | 17,374 | 323 | 11,691 | 16.06M | 26,600 | 28,073 | 0.740 | 89 |
| 13301 | Warren | rural | 1,993 | 1,286 | 74 | 3,578 | 1.97M | 29,860 | -1,831 | 0.766 | 52* |
| 13303 | Washington | rural | 7,422 | 7,807 | 379 | 15,541 | 6.94M | 15,870 | -3,373 | 0.811 | 25 |
| 13305 | Wayne | rural | 10,946 | 10,337 | 254 | 14,407 | 9.84M | 24,208 | 23,656 | 0.697 | 55 |
| 13307 | Webster | rural | 958 | 388 | 62 | 11,088 | 0.66M | 27,443 | 12,168 | 0.609 | 58 |
| 13309 | Wheeler | rural | 2,736 | 1,406 | 92 | 7,613 | 1.31M | 34,507 | 45,091 | 0.734 | 52* |
| 13311 | White | rural | 12,478 | 9,513 | 267 | 1,048 | 6.09M | 16,926 | 92,152 | 0.783 | 41 |
| 13313 | Whitfield | suburb | 47,067 | 57,253 | 342 | 1,013 | 36.84M | 19,857 | 71,705 | 0.696 | 22 |
| 13315 | Wilcox | rural | 2,847 | 1,283 | 258 | 27,320 | 2.77M | 36,039 | 103,687 | 0.698 | 92 |
| 13317 | Wilkes | rural | 3,867 | 2,452 | 280 | 3,551 | 3.72M | 20,442 | 181,979 | 0.715 | 25 |
| 13319 | Wilkinson | rural | 3,231 | 3,001 | 65 | 2,815 | 3.62M | 34,951 | 9,308 | 0.949 | 18 |
| 13321 | Worth | suburb | 8,629 | 3,858 | 469 | 54,894 | 5.09M | 31,236 | 27,123 | 0.695 | 118 |
| EXT | External (out-of-state commuting) | external | 130,700 | 128,573 | 1,064 | 48,357 | 89.45M | 30,007 | n/a | 0.734 | n/a |

`*` filled, see above.
