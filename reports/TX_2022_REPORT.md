# Texas 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state TX 2022`. 254 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 48 | `TX/CDL_2022_48.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=48 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R6_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C9.zip |
| ghsl_R6_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_TX.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (36 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 30,029,572 | 30,029,572 | 0.000% |
| ACS workers by residence | 13,755,352 | 13,755,352 | 0.000% |
| ACS workers by workplace | 13,739,878 | 13,739,878 | 0.000% |
| ACS workers working out of state | 137,449 | 137,449 | 0.000% |
| BEA non-farm employment (L80) | 19,357,673 | 19,357,673 | 0.000% |
| BEA farm employment (L70) | 273,763 | 273,763 | 0.000% |
| BEA farm proprietors (L50) | 221,394 | 221,394 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 3,321,702,000 | 3,321,702,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 1,219,030,000 | 1,219,030,000 | 0.000% |
| CoA hired farm labour expense $ | 1,905,897,000 | 1,941,580,000 | -1.838% |
| BEA non-farm earnings $ (CAINC5N L82) | 1,364,658,285,000 | 1,364,658,285,000 | 0.000% |
| ACS foreign born entered 2010+ | 1,440,693 | 1,440,693 | 0.000% |
| CoA owned acres | 71,411,513 | 72,031,471 | -0.861% |
| CoA rented-from-others acres | 53,121,736 | 53,439,854 | -0.595% |
| CoA land in farms, ha | 50,776,444 | 50,776,444 | 0.000% |
| CoA total cropland, ha | 11,275,306 | 11,292,197 | -0.150% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.241, median 0.659, max 2.019; BEA counts jobs, ACS counts people by main job). Sum N = 13,877,327 = sum HU + HA = 13,877,327. Farm jobs after scaling: 181,491 (BEA 273,763). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 121,975. Jobs = in-state residents working out of state = 137,449, split by the state farm share (HA = 1,816). Location: the 33 out-of-state counties within 1 km of the state (05081, 05091, 22011, 22017, 22019, 22023, 22031, 22085, 22115, 35009, 35013, 35015, 35025, 35035, 35037, 35041, 35059, 40007, 40009, 40013, 40023, 40025, 40033, 40045, 40057, 40065, 40067, 40085, 40089, 40095, 40129, 40139, 40141); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 9,708,896 ha vs Census of Agriculture cropland 11,292,197 ha and land in farms 50,776,444 ha; county ratio TF / CoA cropland 0.02 to 6.85. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 13,606,673 ha). County area covered by CDL pixels: 68,768,431 ha vs land area 67,668,556 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 27.81 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (70,497 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 29,497 $ per BEA farm job, 44,493 $ per farm worker; county range 3,440 to 203,055 $ per worker. State compensation per farm wage job by year: 2018 36,606 $, 2019 32,230 $, 2020 23,783 $, 2021 33,565 $, 2022 23,278 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 399,225,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,941,580,000 $ in 2022, column `hired_labor_coa_usd`) is 1.59x BEA farm compensation (1,219,030,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 12,133 $, county -198,991 to 409,941 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 100,650 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 8,087,239,000 $ vs CAINC45 3,321,702,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.573, county range 0.189 to 0.924.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 31 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 2,499 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 15 counties have no recent foreign born in the ACS sample (Armstrong, Borden, Briscoe, Cottle, Foard, Irion, Jim Hogg, Kenedy, Kent, Loving, McCulloch, McMullen, Motley, Roberts, Stonewall), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Harris); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (85); rural = the rest (168). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 355.1 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 71.5 straight-line km/h between counties (median 7.9 to 55.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.18).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| omega | 48007 Aransas | state owner share |
| omega | 48273 Kleberg | state owner share |
| omega | 48301 Loving | state owner share |
| cash_rent_usd_acre | 48007 Aransas | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48043 Brewster | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48103 Crane | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48105 Crockett | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48109 Culberson | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48127 Dimmit | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48135 Ector | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48137 Edwards | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48141 El Paso | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48163 Frio | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48165 Gaines | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48169 Garza | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48183 Gregg | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48189 Hale | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48199 Hardin | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48205 Hartley | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48227 Howard | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48229 Hudspeth | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48235 Irion | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48243 Jeff Davis | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48247 Jim Hogg | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48261 Kenedy | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48267 Kimble | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48269 King | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48271 Kinney | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48293 Limestone | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48301 Loving | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48309 McLennan | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48311 McMullen | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48315 Marion | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48323 Maverick | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48329 Midland | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48335 Mitchell | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48351 Newton | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48359 Oldham | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48371 Pecos | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48377 Presidio | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48385 Real | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48389 Reeves | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48395 Robertson | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48417 Shackelford | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48431 Sterling | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48433 Stonewall | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48443 Terrell | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48461 Upton | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48465 Val Verde | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48473 Waller | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48475 Ward | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48479 Webb | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48495 Winkler | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48497 Wise | not published; NASS 'other (combined) counties' value = 26 $/acre |
| cash_rent_usd_acre | 48507 Zavala | not published; NASS 'other (combined) counties' value = 26 $/acre |
| owned_acres | 48007 Aransas | (D) in Census of Ag; see fills above |
| owned_acres | 48273 Kleberg | (D) in Census of Ag; see fills above |
| owned_acres | 48301 Loving | (D) in Census of Ag; see fills above |
| rented_acres | 48007 Aransas | (D) in Census of Ag; see fills above |
| rented_acres | 48273 Kleberg | (D) in Census of Ag; see fills above |
| rented_acres | 48301 Loving | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 48301 Loving | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 48313 Madison | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 48475 Ward | (D) in Census of Ag; left null (comparison column only) |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26914) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 48001 | Anderson | rural | 19,753 | 17,926 | 1,295 | 7,204 | 16.28M | 47,019 | -35 | 0.777 | 26 |
| 48003 | Andrews | rural | 9,009 | 7,985 | 158 | 16,472 | 7.99M | 23,670 | 32,357 | 0.350 | 22 |
| 48005 | Angelina | rural | 36,669 | 34,860 | 671 | 321 | 29.04M | 46,491 | 38,676 | 0.827 | 12 |
| 48007 | Aransas | suburb | 8,833 | 7,299 | 70 | 2,403 | 10.44M | 11,086 | -14,179 | 0.574 | 26* |
| 48009 | Archer | suburb | 4,016 | 1,652 | 252 | 47,093 | 4.67M | 62,402 | 35,699 | 0.608 | 32 |
| 48011 | Armstrong | suburb | 815 | 390 | 122 | 49,980 | 0.91M | 48,560 | 5,529 | 0.563 | 26 |
| 48013 | Atascosa | suburb | 20,318 | 14,950 | 1,397 | 21,892 | 12.97M | 48,421 | -10,845 | 0.675 | 19 |
| 48015 | Austin | suburb | 14,424 | 10,117 | 1,090 | 17,516 | 10.65M | 63,088 | -18,875 | 0.642 | 20 |
| 48017 | Bailey | rural | 2,813 | 1,847 | 475 | 87,869 | 3.89M | 58,573 | 104,261 | 0.771 | 30 |
| 48019 | Bandera | suburb | 8,952 | 4,057 | 494 | 1,755 | 7.70M | 48,100 | -5,724 | 0.724 | 20 |
| 48021 | Bastrop | suburb | 44,714 | 25,032 | 1,363 | 16,189 | 16.94M | 30,993 | -9,904 | 0.634 | 15 |
| 48023 | Baylor | rural | 1,466 | 1,245 | 176 | 60,372 | 2.75M | 57,026 | 62,307 | 0.564 | 28 |
| 48025 | Bee | rural | 9,981 | 8,576 | 785 | 31,728 | 9.56M | 42,123 | -1,937 | 0.613 | 35 |
| 48027 | Bell | suburb | 168,459 | 166,733 | 1,910 | 75,715 | 104.28M | 28,671 | -4,360 | 0.460 | 45 |
| 48029 | Bexar | suburb | 960,800 | 995,319 | 2,029 | 23,026 | 546.95M | 45,927 | -629 | 0.639 | 26 |
| 48031 | Blanco | rural | 5,329 | 4,342 | 540 | 1,449 | 4.79M | 61,376 | -12,339 | 0.615 | 20 |
| 48033 | Borden | rural | 267 | 279 | 62 | 28,225 | 0.38M | 98,374 | -43,890 | 0.569 | 28 |
| 48035 | Bosque | suburb | 7,486 | 3,874 | 796 | 17,444 | 7.26M | 64,284 | -11,141 | 0.798 | 24 |
| 48037 | Bowie | suburb | 37,867 | 41,884 | 1,217 | 17,808 | 35.16M | 30,723 | -720 | 0.792 | 27 |
| 48039 | Brazoria | suburb | 171,722 | 125,134 | 2,089 | 63,074 | 102.83M | 55,396 | -10,772 | 0.490 | 16 |
| 48041 | Brazos | suburb | 112,581 | 117,500 | 1,080 | 12,755 | 68.23M | 43,641 | 356 | 0.429 | 20 |
| 48043 | Brewster | rural | 4,694 | 4,004 | 158 | 861 | 6.17M | 56,111 | 2,380 | 0.447 | 26* |
| 48045 | Briscoe | rural | 496 | 320 | 153 | 48,971 | 0.86M | 45,232 | 34,591 | 0.401 | 20 |
| 48047 | Brooks | rural | 2,951 | 2,136 | 293 | 2,567 | 2.37M | 37,694 | -214 | 0.877 | 14 |
| 48049 | Brown | rural | 16,839 | 15,933 | 1,414 | 26,257 | 16.73M | 37,217 | -11,932 | 0.636 | 14 |
| 48051 | Burleson | suburb | 7,492 | 4,518 | 840 | 25,248 | 8.17M | 50,476 | -11,252 | 0.613 | 36 |
| 48053 | Burnet | rural | 22,760 | 19,856 | 980 | 2,920 | 17.59M | 33,500 | -21,648 | 0.458 | 14 |
| 48055 | Caldwell | suburb | 20,060 | 11,027 | 1,017 | 16,942 | 10.25M | 33,606 | -7,144 | 0.565 | 29 |
| 48057 | Calhoun | rural | 9,608 | 15,193 | 292 | 31,948 | 16.24M | 40,923 | 18,082 | 0.283 | 45 |
| 48059 | Callahan | suburb | 6,157 | 2,613 | 451 | 28,418 | 5.35M | 50,337 | -11,810 | 0.648 | 14 |
| 48061 | Cameron | suburb | 166,691 | 158,416 | 1,440 | 105,555 | 110.35M | 38,292 | -1,323 | 0.370 | 44 |
| 48063 | Camp | rural | 5,171 | 3,074 | 371 | 898 | 5.45M | 74,322 | 49,615 | 0.700 | 22 |
| 48065 | Carson | suburb | 2,820 | 2,896 | 175 | 100,345 | 3.74M | 89,656 | -38,565 | 0.556 | 32 |
| 48067 | Cass | rural | 10,886 | 7,384 | 634 | 1,869 | 9.37M | 60,512 | 25,767 | 0.769 | 14 |
| 48069 | Castro | rural | 3,364 | 2,270 | 871 | 152,153 | 4.39M | 73,871 | 272,231 | 0.678 | 33 |
| 48071 | Chambers | suburb | 21,825 | 19,015 | 502 | 28,133 | 22.25M | 53,353 | -573 | 0.435 | 16 |
| 48073 | Cherokee | rural | 19,699 | 14,932 | 1,338 | 5,318 | 16.09M | 66,362 | 16,576 | 0.650 | 22 |
| 48075 | Childress | rural | 2,840 | 2,519 | 268 | 47,232 | 2.92M | 42,458 | 8,096 | 0.666 | 20 |
| 48077 | Clay | suburb | 4,745 | 1,437 | 370 | 41,673 | 5.38M | 90,103 | -9,184 | 0.718 | 26 |
| 48079 | Cochran | suburb | 1,036 | 535 | 204 | 87,056 | 1.45M | 71,260 | 2,990 | 0.573 | 46 |
| 48081 | Coke | rural | 1,325 | 660 | 199 | 12,298 | 2.47M | 85,826 | -17,905 | 0.683 | 18 |
| 48083 | Coleman | rural | 3,361 | 1,967 | 469 | 52,854 | 5.82M | 58,853 | -9,690 | 0.584 | 18 |
| 48085 | Collin | suburb | 559,680 | 540,525 | 1,558 | 47,162 | 288.86M | 30,899 | -21,718 | 0.446 | 28 |
| 48087 | Collingsworth | rural | 1,218 | 860 | 271 | 55,766 | 1.68M | 50,262 | -41,660 | 0.609 | 20 |
| 48089 | Colorado | rural | 8,769 | 6,866 | 956 | 58,459 | 8.52M | 56,320 | -23,380 | 0.628 | 40 |
| 48091 | Comal | suburb | 76,950 | 76,610 | 743 | 3,072 | 45.14M | 34,387 | -10,195 | 0.651 | 8 |
| 48093 | Comanche | rural | 6,042 | 4,091 | 1,087 | 59,190 | 7.65M | 50,620 | 31,011 | 0.683 | 22 |
| 48095 | Concho | rural | 992 | 992 | 325 | 46,633 | 1.78M | 43,718 | 16,906 | 0.379 | 35 |
| 48097 | Cooke | rural | 19,886 | 15,266 | 1,234 | 36,455 | 15.77M | 34,906 | -20,181 | 0.573 | 20 |
| 48099 | Coryell | suburb | 33,899 | 22,120 | 1,230 | 28,340 | 21.64M | 29,303 | -15,040 | 0.545 | 26 |
| 48101 | Cottle | rural | 713 | 454 | 121 | 34,153 | 0.93M | 60,098 | 53,691 | 0.581 | 28 |
| 48103 | Crane | rural | 2,237 | 2,159 | 34 | 266 | 3.53M | 22,255 | 50,323 | 0.290 | 26* |
| 48105 | Crockett | rural | 1,558 | 1,287 | 186 | 513 | 3.18M | 39,833 | -8,514 | 0.322 | 26* |
| 48107 | Crosby | suburb | 2,335 | 978 | 309 | 122,505 | 2.18M | 69,002 | -13,305 | 0.530 | 29 |
| 48109 | Culberson | rural | 911 | 1,068 | 85 | 7,009 | 2.32M | 61,682 | -37,943 | 0.340 | 26* |
| 48111 | Dallam | rural | 3,814 | 3,455 | 485 | 152,787 | 4.68M | 56,369 | 167,582 | 0.632 | 23 |
| 48113 | Dallas | suburb | 1,292,835 | 1,598,401 | 692 | 13,064 | 932.85M | 59,427 | 8,390 | 0.436 | 14 |
| 48115 | Dawson | rural | 4,205 | 3,760 | 481 | 158,603 | 5.08M | 47,337 | 61,982 | 0.430 | 52 |
| 48117 | Deaf Smith | rural | 8,286 | 7,605 | 970 | 175,196 | 9.89M | 54,949 | 349,818 | 0.667 | 28 |
| 48119 | Delta | rural | 2,279 | 722 | 227 | 24,693 | 2.24M | 44,890 | 14,246 | 0.572 | 34 |
| 48121 | Denton | suburb | 492,599 | 356,182 | 2,371 | 39,061 | 219.85M | 47,670 | 1,803 | 0.510 | 20 |
| 48123 | DeWitt | rural | 7,490 | 6,287 | 972 | 12,741 | 10.31M | 45,784 | -24,176 | 0.676 | 18 |
| 48125 | Dickens | rural | 589 | 329 | 157 | 27,309 | 1.11M | 55,962 | -12,755 | 0.718 | 18 |
| 48127 | Dimmit | rural | 2,352 | 4,327 | 304 | 4,488 | 4.81M | 70,536 | -6,304 | 0.739 | 26* |
| 48129 | Donley | rural | 1,383 | 913 | 240 | 23,720 | 1.88M | 63,852 | 10,323 | 0.494 | 21 |
| 48131 | Duval | rural | 3,590 | 2,203 | 647 | 7,998 | 5.42M | 47,708 | -11,801 | 0.897 | 14 |
| 48133 | Eastland | rural | 7,573 | 6,788 | 838 | 32,323 | 10.74M | 34,218 | -20,856 | 0.622 | 18 |
| 48135 | Ector | suburb | 73,281 | 73,154 | 188 | 311 | 93.85M | 34,921 | 1,795 | 0.573 | 26* |
| 48137 | Edwards | rural | 716 | 451 | 229 | 565 | 2.04M | 52,510 | -5,305 | 0.669 | 26* |
| 48139 | Ellis | suburb | 97,761 | 68,837 | 1,617 | 79,621 | 58.16M | 36,110 | -24,128 | 0.469 | 28 |
| 48141 | El Paso | suburb | 377,646 | 371,377 | 776 | 20,050 | 421.30M | 32,299 | -7,529 | 0.189 | 26* |
| 48143 | Erath | rural | 20,446 | 17,197 | 1,762 | 34,583 | 18.75M | 51,162 | 57,887 | 0.749 | 17 |
| 48145 | Falls | suburb | 6,200 | 3,837 | 875 | 102,295 | 5.90M | 31,385 | -10,634 | 0.569 | 34 |
| 48147 | Fannin | rural | 14,759 | 9,049 | 1,635 | 73,875 | 12.44M | 34,070 | -16,599 | 0.677 | 28 |
| 48149 | Fayette | rural | 10,737 | 9,320 | 1,677 | 24,027 | 13.70M | 41,366 | -19,670 | 0.630 | 18 |
| 48151 | Fisher | rural | 1,793 | 965 | 452 | 83,685 | 1.64M | 44,552 | 4,146 | 0.579 | 27 |
| 48153 | Floyd | rural | 2,187 | 1,206 | 421 | 149,191 | 3.35M | 75,665 | 14,686 | 0.303 | 24 |
| 48155 | Foard | rural | 500 | 397 | 141 | 41,047 | 0.67M | 57,630 | 60,172 | 0.639 | 18 |
| 48157 | Fort Bend | suburb | 393,884 | 245,889 | 879 | 57,055 | 159.38M | 61,544 | -8,901 | 0.283 | 50 |
| 48159 | Franklin | rural | 4,489 | 3,827 | 384 | 3,379 | 4.78M | 38,320 | 175,383 | 0.609 | 32 |
| 48161 | Freestone | rural | 7,065 | 4,469 | 886 | 3,697 | 8.51M | 41,134 | 8,909 | 0.751 | 18 |
| 48163 | Frio | rural | 6,830 | 6,796 | 693 | 39,265 | 5.62M | 59,460 | 11,460 | 0.681 | 26* |
| 48165 | Gaines | rural | 8,472 | 7,586 | 576 | 204,640 | 9.10M | 65,895 | 65,689 | 0.666 | 26* |
| 48167 | Galveston | suburb | 164,431 | 129,731 | 449 | 8,891 | 116.58M | 22,324 | -16,099 | 0.489 | 36 |
| 48169 | Garza | suburb | 1,616 | 1,372 | 156 | 29,238 | 1.90M | 58,154 | -21,333 | 0.595 | 26* |
| 48171 | Gillespie | rural | 12,087 | 12,406 | 1,104 | 11,089 | 12.88M | 41,249 | -14,937 | 0.599 | 9 |
| 48173 | Glasscock | rural | 455 | 806 | 192 | 54,528 | 1.74M | 43,209 | -101,737 | 0.517 | 31 |
| 48175 | Goliad | suburb | 2,875 | 1,268 | 532 | 9,594 | 3.10M | 53,783 | -15,782 | 0.705 | 24 |
| 48177 | Gonzales | rural | 8,636 | 6,601 | 1,508 | 16,041 | 11.35M | 46,638 | 121,588 | 0.624 | 18 |
| 48179 | Gray | rural | 8,829 | 8,043 | 361 | 52,194 | 12.26M | 60,441 | 60,532 | 0.343 | 22 |
| 48181 | Grayson | suburb | 63,791 | 56,512 | 1,975 | 59,778 | 44.11M | 36,917 | -17,716 | 0.395 | 18 |
| 48183 | Gregg | suburb | 56,334 | 73,898 | 362 | 314 | 57.81M | 29,942 | -14,258 | 0.887 | 26* |
| 48185 | Grimes | rural | 11,335 | 6,785 | 921 | 4,766 | 10.21M | 56,794 | -13,288 | 0.798 | 14 |
| 48187 | Guadalupe | suburb | 83,268 | 53,277 | 1,635 | 34,184 | 43.12M | 30,581 | -2,659 | 0.661 | 26 |
| 48189 | Hale | rural | 13,458 | 11,227 | 1,057 | 180,697 | 16.13M | 51,084 | 87,077 | 0.526 | 26* |
| 48191 | Hall | rural | 1,155 | 691 | 239 | 60,944 | 1.95M | 50,927 | -14,260 | 0.593 | 26 |
| 48193 | Hamilton | rural | 3,312 | 2,813 | 670 | 25,652 | 4.49M | 45,126 | -5,468 | 0.711 | 14 |
| 48195 | Hansford | rural | 2,429 | 1,874 | 343 | 129,299 | 3.33M | 73,714 | 239,287 | 0.416 | 37 |
| 48197 | Hardeman | rural | 1,802 | 1,278 | 250 | 55,801 | 2.14M | 40,727 | 45,371 | 0.654 | 18 |
| 48199 | Hardin | suburb | 23,503 | 13,171 | 403 | 1,168 | 16.47M | 36,386 | -22,511 | 0.924 | 26* |
| 48201 | Harris | core | 2,239,156 | 2,532,064 | 1,822 | 11,504 | 1,403.60M | 43,465 | 77 | 0.796 | 14 |
| 48203 | Harrison | suburb | 30,667 | 25,434 | 909 | 1,127 | 25.29M | 29,667 | -9,687 | 0.780 | 13 |
| 48205 | Hartley | rural | 1,695 | 1,698 | 554 | 131,546 | 3.13M | 77,290 | 243,524 | 0.710 | 26* |
| 48207 | Haskell | rural | 2,265 | 1,724 | 319 | 131,098 | 2.69M | 60,770 | 29,092 | 0.503 | 29 |
| 48209 | Hays | suburb | 124,248 | 91,892 | 989 | 7,516 | 45.62M | 43,031 | -7,405 | 0.654 | 30 |
| 48211 | Hemphill | rural | 1,546 | 1,555 | 189 | 10,314 | 2.97M | 38,431 | 105,157 | 0.538 | 9 |
| 48213 | Henderson | rural | 33,007 | 23,720 | 1,466 | 8,016 | 24.03M | 36,567 | -10,628 | 0.643 | 18 |
| 48215 | Hidalgo | suburb | 332,795 | 307,993 | 2,666 | 134,106 | 212.67M | 46,716 | 13,702 | 0.563 | 50 |
| 48217 | Hill | rural | 15,366 | 10,199 | 1,118 | 93,659 | 11.96M | 47,816 | -1,733 | 0.419 | 40 |
| 48219 | Hockley | suburb | 9,554 | 7,799 | 585 | 142,291 | 9.41M | 51,126 | 3,032 | 0.492 | 42 |
| 48221 | Hood | rural | 26,263 | 18,553 | 762 | 3,840 | 17.95M | 45,124 | -12,629 | 0.725 | 22 |
| 48223 | Hopkins | rural | 16,779 | 13,735 | 1,593 | 21,122 | 15.97M | 42,981 | 76,656 | 0.709 | 18 |
| 48225 | Houston | rural | 7,676 | 5,915 | 848 | 10,438 | 8.38M | 57,012 | -1,823 | 0.712 | 12 |
| 48227 | Howard | rural | 14,167 | 14,097 | 428 | 69,584 | 13.95M | 36,596 | 14,578 | 0.434 | 26* |
| 48229 | Hudspeth | suburb | 966 | 1,545 | 255 | 23,213 | 1.61M | 32,278 | 19,677 | 0.450 | 26* |
| 48231 | Hunt | suburb | 44,966 | 35,006 | 3,053 | 35,167 | 33.33M | 32,766 | -15,165 | 0.622 | 22 |
| 48233 | Hutchinson | rural | 8,999 | 9,328 | 269 | 45,688 | 13.73M | 37,107 | -49,910 | 0.366 | 22 |
| 48235 | Irion | suburb | 689 | 721 | 115 | 2,395 | 1.32M | 39,263 | 25,970 | 0.470 | 26* |
| 48237 | Jack | rural | 3,060 | 2,044 | 369 | 9,632 | 4.73M | 46,707 | -19,218 | 0.511 | 16 |
| 48239 | Jackson | rural | 5,890 | 5,351 | 612 | 76,528 | 7.08M | 47,716 | -20,215 | 0.407 | 56 |
| 48241 | Jasper | rural | 12,091 | 9,896 | 603 | 321 | 12.36M | 38,242 | -14,555 | 0.841 | 18 |
| 48243 | Jeff Davis | rural | 700 | 782 | 98 | 340 | 1.97M | 43,899 | 7,366 | 0.677 | 26* |
| 48245 | Jefferson | suburb | 103,041 | 128,245 | 659 | 25,915 | 141.52M | 43,694 | -12,540 | 0.341 | 28 |
| 48247 | Jim Hogg | rural | 2,042 | 1,709 | 264 | 806 | 2.08M | 33,371 | -11,581 | 0.860 | 26* |
| 48249 | Jim Wells | rural | 14,790 | 13,510 | 765 | 46,841 | 13.96M | 47,406 | 23,077 | 0.535 | 32 |
| 48251 | Johnson | suburb | 85,387 | 57,671 | 1,923 | 31,070 | 47.08M | 35,418 | -11,387 | 0.612 | 25 |
| 48253 | Jones | suburb | 6,338 | 3,905 | 606 | 124,495 | 6.12M | 40,378 | 10,636 | 0.566 | 22 |
| 48255 | Karnes | rural | 4,804 | 7,818 | 1,161 | 24,526 | 6.22M | 33,953 | -18,932 | 0.539 | 20 |
| 48257 | Kaufman | suburb | 71,908 | 43,847 | 1,927 | 21,320 | 37.77M | 36,109 | -11,604 | 0.624 | 18 |
| 48259 | Kendall | suburb | 21,045 | 21,563 | 863 | 2,012 | 12.95M | 39,530 | -13,662 | 0.576 | 14 |
| 48261 | Kenedy | rural | 46 | 276 | 67 | 4,835 | 0.54M | 64,611 | 25,648 | 0.747 | 26* |
| 48263 | Kent | rural | 187 | 149 | 49 | 13,091 | 0.72M | 63,030 | 20,118 | 0.579 | 12 |
| 48265 | Kerr | rural | 22,844 | 21,706 | 774 | 1,890 | 21.12M | 36,051 | -10,657 | 0.809 | 20 |
| 48267 | Kimble | rural | 2,089 | 1,626 | 417 | 2,218 | 3.29M | 42,217 | -7,543 | 0.788 | 26* |
| 48269 | King | rural | 85 | 81 | 44 | 8,865 | 0.26M | 53,317 | 179,081 | 0.844 | 26* |
| 48271 | Kinney | rural | 1,314 | 1,219 | 226 | 4,995 | 1.66M | 26,353 | -9,585 | 0.631 | 26* |
| 48273 | Kleberg | rural | 13,086 | 12,392 | 343 | 44,227 | 11.37M | 32,835 | 27,895 | 0.574 | 45 |
| 48275 | Knox | rural | 1,394 | 1,276 | 229 | 86,678 | 1.65M | 34,597 | 43,200 | 0.498 | 30 |
| 48277 | Lamar | rural | 22,572 | 23,178 | 1,393 | 62,395 | 21.33M | 34,258 | -7,070 | 0.726 | 19 |
| 48279 | Lamb | rural | 5,456 | 3,240 | 883 | 150,164 | 6.79M | 60,297 | 146,988 | 0.625 | 50 |
| 48281 | Lampasas | suburb | 8,762 | 5,417 | 583 | 8,024 | 7.31M | 34,124 | -25,463 | 0.588 | 22 |
| 48283 | La Salle | rural | 2,207 | 4,392 | 551 | 5,360 | 3.93M | 25,578 | -16,910 | 0.780 | 15 |
| 48285 | Lavaca | rural | 9,147 | 6,273 | 1,571 | 22,978 | 9.87M | 35,778 | -12,714 | 0.525 | 18 |
| 48287 | Lee | rural | 7,672 | 5,549 | 1,073 | 11,673 | 6.82M | 46,382 | -5,984 | 0.609 | 11 |
| 48289 | Leon | rural | 6,183 | 4,721 | 1,153 | 5,651 | 9.00M | 45,627 | 27,008 | 0.670 | 14 |
| 48291 | Liberty | suburb | 32,970 | 20,394 | 885 | 23,334 | 20.31M | 45,802 | -20,236 | 0.659 | 24 |
| 48293 | Limestone | rural | 8,100 | 6,322 | 865 | 26,770 | 8.87M | 35,840 | -2,570 | 0.749 | 26* |
| 48295 | Lipscomb | rural | 1,344 | 884 | 169 | 29,871 | 1.78M | 117,360 | 46,183 | 0.556 | 22 |
| 48297 | Live Oak | rural | 4,000 | 3,830 | 605 | 22,004 | 6.93M | 29,567 | -16,434 | 0.619 | 11 |
| 48299 | Llano | rural | 8,055 | 5,718 | 404 | 3,012 | 11.08M | 54,917 | -19,603 | 0.754 | 8 |
| 48301 | Loving | rural | 39 | 804 | 52 | 66 | 0.30M | 3,440 | 2,615 | 0.574 | 26* |
| 48303 | Lubbock | suburb | 151,356 | 154,472 | 1,044 | 159,837 | 130.30M | 51,497 | -4,268 | 0.454 | 38 |
| 48305 | Lynn | suburb | 2,461 | 1,147 | 268 | 170,514 | 1.98M | 87,138 | -16,000 | 0.446 | 46 |
| 48307 | McCulloch | rural | 3,189 | 2,500 | 400 | 36,292 | 5.24M | 36,240 | -14,453 | 0.773 | 11 |
| 48309 | McLennan | suburb | 117,951 | 122,863 | 2,442 | 82,658 | 77.60M | 32,086 | -4,008 | 0.480 | 26* |
| 48311 | McMullen | rural | 247 | 553 | 183 | 2,074 | 1.62M | 58,987 | -33,100 | 0.737 | 26* |
| 48313 | Madison | rural | 4,698 | 3,757 | 643 | 3,106 | 4.92M | 46,036 | 9,502 | 0.503 | 20 |
| 48315 | Marion | rural | 3,364 | 1,912 | 128 | 388 | 3.01M | 46,624 | 4,332 | 0.914 | 26* |
| 48317 | Martin | suburb | 2,176 | 2,704 | 340 | 95,854 | 2.07M | 42,379 | -24,318 | 0.605 | 30 |
| 48319 | Mason | rural | 1,629 | 990 | 263 | 4,990 | 2.74M | 91,365 | -7,652 | 0.569 | 8 |
| 48321 | Matagorda | rural | 14,742 | 13,837 | 914 | 86,443 | 12.80M | 53,497 | 3,323 | 0.476 | 44 |
| 48323 | Maverick | suburb | 22,296 | 18,354 | 266 | 3,736 | 14.42M | 54,085 | 17,989 | 0.488 | 26* |
| 48325 | Medina | suburb | 21,776 | 13,414 | 1,402 | 49,803 | 12.52M | 43,704 | -4,664 | 0.591 | 28 |
| 48327 | Menard | rural | 671 | 416 | 142 | 3,471 | 1.47M | 63,282 | -12,908 | 0.590 | 13 |
| 48329 | Midland | suburb | 85,072 | 113,706 | 478 | 18,005 | 94.00M | 57,386 | 3,414 | 0.556 | 26* |
| 48331 | Milam | rural | 10,580 | 5,462 | 1,192 | 63,127 | 10.77M | 53,793 | 5,254 | 0.576 | 34 |
| 48333 | Mills | rural | 2,012 | 1,375 | 561 | 14,842 | 3.47M | 57,078 | -10,326 | 0.690 | 11 |
| 48335 | Mitchell | rural | 3,745 | 2,222 | 355 | 51,532 | 3.27M | 43,840 | -5,818 | 0.331 | 26* |
| 48337 | Montague | rural | 8,196 | 5,232 | 782 | 18,604 | 9.55M | 47,623 | -20,491 | 0.656 | 18 |
| 48339 | Montgomery | suburb | 297,162 | 247,595 | 1,125 | 1,300 | 153.60M | 38,438 | -11,690 | 0.710 | 19 |
| 48341 | Moore | rural | 9,653 | 10,080 | 420 | 98,364 | 10.71M | 56,653 | 409,941 | 0.373 | 34 |
| 48343 | Morris | rural | 4,953 | 3,515 | 310 | 1,008 | 5.69M | 33,718 | 80,570 | 0.791 | 12 |
| 48345 | Motley | rural | 562 | 378 | 148 | 23,505 | 0.71M | 46,199 | 10,564 | 0.660 | 20 |
| 48347 | Nacogdoches | rural | 27,800 | 25,773 | 1,035 | 632 | 20.50M | 42,838 | 182,668 | 0.705 | 22 |
| 48349 | Navarro | rural | 22,195 | 17,601 | 1,808 | 41,781 | 20.75M | 35,692 | -10,824 | 0.737 | 28 |
| 48351 | Newton | rural | 4,221 | 1,576 | 264 | 331 | 3.64M | 26,000 | -17,149 | 0.859 | 26* |
| 48353 | Nolan | rural | 6,187 | 6,652 | 386 | 39,086 | 8.25M | 44,340 | -11,143 | 0.491 | 14 |
| 48355 | Nueces | suburb | 160,375 | 169,292 | 724 | 137,563 | 130.96M | 47,112 | -29,526 | 0.403 | 69 |
| 48357 | Ochiltree | rural | 4,804 | 4,823 | 522 | 129,856 | 5.95M | 65,304 | 199,641 | 0.413 | 26 |
| 48359 | Oldham | suburb | 874 | 783 | 147 | 28,803 | 1.22M | 69,183 | 171,626 | 0.744 | 26* |
| 48361 | Orange | suburb | 37,696 | 25,443 | 489 | 1,027 | 33.56M | 31,098 | -17,340 | 0.657 | 24 |
| 48363 | Palo Pinto | rural | 11,985 | 8,319 | 839 | 8,630 | 14.97M | 59,427 | -9,876 | 0.602 | 18 |
| 48365 | Panola | rural | 9,529 | 8,417 | 740 | 564 | 9.88M | 31,802 | 66,937 | 0.787 | 18 |
| 48367 | Parker | suburb | 71,963 | 45,383 | 2,644 | 6,209 | 42.95M | 45,550 | -16,823 | 0.775 | 22 |
| 48369 | Parmer | rural | 4,677 | 5,175 | 1,020 | 160,744 | 5.16M | 53,484 | 215,425 | 0.518 | 32 |
| 48371 | Pecos | rural | 5,976 | 5,856 | 352 | 12,450 | 8.92M | 51,167 | -24,422 | 0.578 | 26* |
| 48373 | Polk | rural | 17,662 | 15,334 | 524 | 365 | 11.86M | 17,349 | -17,390 | 0.738 | 22 |
| 48375 | Potter | suburb | 49,483 | 79,014 | 221 | 11,571 | 54.73M | 38,479 | 12,708 | 0.295 | 12 |
| 48377 | Presidio | rural | 2,449 | 2,532 | 180 | 576 | 6.77M | 175,233 | 115,326 | 0.492 | 26* |
| 48379 | Rains | rural | 5,019 | 2,378 | 376 | 2,832 | 3.96M | 50,338 | -3,234 | 0.619 | 24 |
| 48381 | Randall | suburb | 72,342 | 41,315 | 670 | 72,536 | 44.49M | 66,886 | 109,524 | 0.610 | 18 |
| 48383 | Reagan | rural | 1,566 | 2,734 | 183 | 27,343 | 2.88M | 33,199 | 11,959 | 0.463 | 38 |
| 48385 | Real | rural | 744 | 764 | 107 | 261 | 1.97M | 54,318 | -18,935 | 0.740 | 26* |
| 48387 | Red River | rural | 4,303 | 2,023 | 534 | 22,046 | 5.85M | 52,503 | 4,546 | 0.781 | 31 |
| 48389 | Reeves | rural | 6,255 | 13,649 | 528 | 9,529 | 8.77M | 21,305 | 8,206 | 0.364 | 26* |
| 48391 | Refugio | rural | 2,557 | 1,862 | 182 | 39,759 | 2.81M | 67,998 | 9,941 | 0.368 | 54 |
| 48393 | Roberts | rural | 398 | 201 | 55 | 11,788 | 0.51M | 60,921 | 9,117 | 0.630 | 10 |
| 48395 | Robertson | suburb | 6,617 | 4,523 | 961 | 24,596 | 7.99M | 48,323 | 23,381 | 0.569 | 26* |
| 48397 | Rockwall | suburb | 56,151 | 42,641 | 297 | 5,520 | 31.72M | 17,707 | -6,792 | 0.458 | 15 |
| 48399 | Runnels | rural | 4,404 | 2,809 | 548 | 99,931 | 6.10M | 58,442 | 12,505 | 0.555 | 27 |
| 48401 | Rusk | suburb | 21,072 | 13,273 | 889 | 997 | 16.69M | 65,208 | 44,911 | 0.658 | 15 |
| 48403 | Sabine | rural | 3,029 | 2,327 | 118 | 90 | 3.79M | 51,667 | 21,960 | 0.872 | 16 |
| 48405 | San Augustine | rural | 2,585 | 2,199 | 260 | 121 | 3.46M | 24,883 | 120,869 | 0.777 | 12 |
| 48407 | San Jacinto | suburb | 10,378 | 3,459 | 404 | 418 | 5.66M | 45,572 | -18,519 | 0.734 | 18 |
| 48409 | San Patricio | suburb | 28,393 | 23,631 | 668 | 103,794 | 26.07M | 40,444 | 3,629 | 0.245 | 70 |
| 48411 | San Saba | rural | 2,312 | 1,487 | 446 | 20,779 | 3.40M | 57,670 | -15,160 | 0.653 | 12 |
| 48413 | Schleicher | rural | 1,058 | 728 | 206 | 11,364 | 1.88M | 53,707 | -9,162 | 0.523 | 26 |
| 48415 | Scurry | rural | 6,876 | 6,919 | 541 | 63,105 | 8.67M | 52,483 | -2,537 | 0.493 | 30 |
| 48417 | Shackelford | rural | 1,483 | 1,364 | 128 | 16,191 | 2.14M | 57,051 | -11,554 | 0.378 | 26* |
| 48419 | Shelby | rural | 10,047 | 8,638 | 896 | 332 | 11.63M | 46,623 | 280,164 | 0.536 | 20 |
| 48421 | Sherman | rural | 1,116 | 714 | 278 | 130,142 | 1.75M | 82,985 | 356,689 | 0.607 | 34 |
| 48423 | Smith | suburb | 107,599 | 116,257 | 2,316 | 2,536 | 88.84M | 34,494 | -1,909 | 0.805 | 13 |
| 48425 | Somervell | rural | 4,543 | 4,988 | 300 | 1,238 | 3.77M | 28,545 | 25,006 | 0.399 | 15 |
| 48427 | Starr | rural | 23,333 | 19,864 | 1,074 | 38,482 | 13.45M | 28,850 | 1,081 | 0.730 | 40 |
| 48429 | Stephens | rural | 3,815 | 3,516 | 304 | 12,130 | 5.70M | 45,207 | -27,969 | 0.720 | 12 |
| 48431 | Sterling | rural | 575 | 546 | 84 | 2,843 | 1.28M | 43,536 | 14,231 | 0.312 | 26* |
| 48433 | Stonewall | rural | 664 | 587 | 192 | 27,243 | 0.81M | 203,055 | 4,120 | 0.813 | 26* |
| 48435 | Sutton | rural | 1,421 | 1,257 | 185 | 1,141 | 2.82M | 49,705 | -3,135 | 0.727 | 12 |
| 48437 | Swisher | rural | 2,610 | 1,735 | 449 | 123,303 | 3.93M | 92,344 | 331,283 | 0.609 | 32 |
| 48439 | Tarrant | suburb | 1,050,372 | 1,072,531 | 1,061 | 5,638 | 640.39M | 46,754 | 789 | 0.800 | 11 |
| 48441 | Taylor | suburb | 70,258 | 74,461 | 898 | 55,080 | 57.73M | 37,203 | -14,284 | 0.578 | 16 |
| 48443 | Terrell | rural | 364 | 279 | 63 | 342 | 1.07M | 50,813 | -5,868 | 0.425 | 26* |
| 48445 | Terry | rural | 4,957 | 4,104 | 837 | 157,867 | 5.62M | 36,809 | 47,742 | 0.508 | 38 |
| 48447 | Throckmorton | rural | 717 | 582 | 186 | 37,099 | 1.01M | 53,934 | -4,064 | 0.448 | 17 |
| 48449 | Titus | rural | 13,191 | 16,331 | 600 | 2,327 | 12.71M | 34,459 | 148,803 | 0.796 | 16 |
| 48451 | Tom Green | suburb | 57,290 | 56,207 | 1,002 | 85,950 | 48.63M | 40,488 | 14,519 | 0.565 | 39 |
| 48453 | Travis | suburb | 725,645 | 867,590 | 905 | 24,617 | 331.22M | 50,243 | -4,367 | 0.482 | 22 |
| 48455 | Trinity | rural | 4,849 | 2,648 | 348 | 475 | 4.55M | 17,598 | -15,486 | 0.799 | 12 |
| 48457 | Tyler | rural | 6,255 | 4,123 | 518 | 170 | 5.79M | 50,284 | -12,697 | 0.845 | 32 |
| 48459 | Upshur | suburb | 16,377 | 8,136 | 893 | 1,530 | 10.86M | 43,163 | -1,300 | 0.741 | 16 |
| 48461 | Upton | rural | 1,320 | 2,010 | 77 | 14,069 | 2.62M | 51,913 | -52,872 | 0.426 | 26* |
| 48463 | Uvalde | rural | 9,661 | 9,353 | 562 | 47,260 | 11.55M | 44,607 | 102 | 0.682 | 18 |
| 48465 | Val Verde | rural | 21,131 | 19,689 | 365 | 954 | 19.51M | 26,327 | -10,188 | 0.562 | 26* |
| 48467 | Van Zandt | rural | 24,887 | 13,439 | 1,979 | 5,385 | 17.86M | 47,389 | 1,156 | 0.703 | 23 |
| 48469 | Victoria | suburb | 41,154 | 40,334 | 1,173 | 40,074 | 36.08M | 32,617 | -4,985 | 0.370 | 46 |
| 48471 | Walker | rural | 28,340 | 30,623 | 1,405 | 2,572 | 15.28M | 46,811 | -5,205 | 0.720 | 16 |
| 48473 | Waller | suburb | 24,146 | 24,260 | 1,745 | 17,784 | 12.07M | 42,042 | -2,025 | 0.430 | 26* |
| 48475 | Ward | rural | 5,042 | 5,779 | 87 | 428 | 6.91M | 16,214 | -198,991 | 0.434 | 26* |
| 48477 | Washington | rural | 16,369 | 15,886 | 1,821 | 12,107 | 15.02M | 33,797 | -17,441 | 0.756 | 16 |
| 48479 | Webb | suburb | 110,657 | 107,997 | 589 | 1,494 | 87.39M | 37,872 | -3,089 | 0.549 | 26* |
| 48481 | Wharton | rural | 17,908 | 14,396 | 1,997 | 166,095 | 13.39M | 45,188 | -602 | 0.408 | 52 |
| 48483 | Wheeler | rural | 2,269 | 1,914 | 390 | 31,779 | 3.46M | 65,456 | 3,246 | 0.539 | 11 |
| 48485 | Wichita | suburb | 62,261 | 66,237 | 542 | 53,537 | 54.11M | 47,589 | -9,334 | 0.603 | 34 |
| 48487 | Wilbarger | rural | 5,436 | 5,706 | 365 | 100,071 | 7.42M | 58,406 | 2,809 | 0.746 | 26 |
| 48489 | Willacy | rural | 7,939 | 5,968 | 458 | 79,453 | 4.92M | 34,463 | 11,499 | 0.474 | 70 |
| 48491 | Williamson | suburb | 321,072 | 259,801 | 1,919 | 85,543 | 134.35M | 35,052 | -3,079 | 0.539 | 40 |
| 48493 | Wilson | suburb | 23,328 | 11,762 | 1,661 | 24,256 | 9.97M | 36,081 | -10,028 | 0.690 | 15 |
| 48495 | Winkler | rural | 3,380 | 5,629 | 81 | 627 | 4.99M | 35,744 | -106,212 | 0.544 | 26* |
| 48497 | Wise | suburb | 33,718 | 23,852 | 2,018 | 19,795 | 22.79M | 37,945 | -23,195 | 0.629 | 26* |
| 48499 | Wood | rural | 16,925 | 12,033 | 977 | 4,606 | 15.56M | 37,700 | 45,739 | 0.745 | 19 |
| 48501 | Yoakum | rural | 3,273 | 3,272 | 375 | 90,764 | 4.05M | 54,182 | 17,417 | 0.467 | 20 |
| 48503 | Young | rural | 8,135 | 7,614 | 490 | 38,381 | 11.12M | 52,861 | -14,654 | 0.478 | 12 |
| 48505 | Zapata | rural | 4,669 | 4,011 | 424 | 1,783 | 5.95M | 23,399 | -12,067 | 0.677 | 38 |
| 48507 | Zavala | rural | 3,612 | 2,159 | 289 | 29,650 | 4.69M | 51,781 | -13,179 | 0.619 | 26* |
| EXT | External (out-of-state commuting) | external | 121,975 | 135,633 | 1,816 | 97,124 | 82.20M | 44,493 | n/a | 0.573 | n/a |

`*` filled, see above.
