# Mississippi 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state MS 2022`. 82 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 28 | `MS/CDL_2022_28.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=28 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R6_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip |
| ghsl_R6_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MS.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 2,940,057 | 2,940,057 | 0.000% |
| ACS workers by residence | 1,232,826 | 1,232,826 | 0.000% |
| ACS workers by workplace | 1,178,501 | 1,178,501 | 0.000% |
| ACS workers working out of state | 106,139 | 106,139 | 0.000% |
| BEA non-farm employment (L80) | 1,636,047 | 1,636,047 | 0.000% |
| BEA farm employment (L70) | 38,095 | 38,095 | 0.000% |
| BEA farm proprietors (L50) | 29,112 | 29,112 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 1,202,431,000 | 1,202,431,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 179,469,000 | 179,469,000 | 0.000% |
| CoA hired farm labour expense $ | 338,053,000 | 338,051,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 82,371,976,000 | 82,371,976,000 | 0.000% |
| ACS foreign born entered 2010+ | 24,728 | 24,728 | 0.000% |
| CoA owned acres | 6,325,747 | 6,325,747 | 0.000% |
| CoA rented-from-others acres | 3,925,750 | 3,925,750 | 0.000% |
| CoA land in farms, ha | 4,148,634 | 4,148,634 | 0.000% |
| CoA total cropland, ha | 2,078,196 | 2,078,196 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.337, median 0.671, max 0.803; BEA counts jobs, ACS counts people by main job). Sum N = 1,284,640 = sum HU + HA = 1,284,640. Farm jobs after scaling: 25,395 (BEA 38,095). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 51,814. Jobs = in-state residents working out of state = 106,139, split by the state farm share (HA = 2,287). Location: the 30 out-of-state counties within 1 km of the state (01023, 01033, 01059, 01075, 01077, 01093, 01097, 01107, 01119, 01129, 05017, 05035, 05041, 05077, 05107, 22029, 22035, 22037, 22065, 22091, 22103, 22105, 22107, 22117, 22125, 47047, 47069, 47071, 47109, 47157); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,704,386 ha vs Census of Agriculture cropland 2,078,196 ha and land in farms 4,148,634 ha; county ratio TF / CoA cropland 0.04 to 1.47. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,560,337 ha). County area covered by CDL pixels: 12,347,212 ha vs land area 12,153,393 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 2.94 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (50,348 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 19,538 $ per BEA farm job, 29,309 $ per farm worker; county range 10,063 to 99,168 $ per worker. State compensation per farm wage job by year: 2018 21,228 $, 2019 20,245 $, 2020 18,186 $, 2021 18,910 $, 2022 19,979 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 48,217,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (338,051,000 $ in 2022, column `hired_labor_coa_usd`) is 1.88x BEA farm compensation (179,469,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 31,564 $, county -72,482 to 224,240 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 71,435 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,022,485,000 $ vs CAINC45 1,202,431,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.617, county range 0.162 to 0.941.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 92 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,369 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 12 counties have no recent foreign born in the ACS sample (Attala, Carroll, Choctaw, Issaquena, Jasper, Jefferson Davis, Montgomery, Noxubee, Sharkey, Tunica, Wilkinson, Yalobusha), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Hinds); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (19); rural = the rest (62). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 192.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 60.5 straight-line km/h between counties (median 16.7 to 25.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.23).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 28001 Adams | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28007 Attala | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28035 Forrest | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28041 Greene | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28043 Grenada | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28045 Hancock | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28047 Harrison | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28059 Jackson | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28071 Lafayette | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28077 Lawrence | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28111 Perry | not published; NASS 'other (combined) counties' value = 64.5 $/acre |
| cash_rent_usd_acre | 28149 Warren | not published; NASS 'other (combined) counties' value = 64.5 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26916) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 28001 | Adams | rural | 9,965 | 10,525 | 120 | 5,789 | 9.15M | 29,769 | 3,083 | 0.690 | 64* |
| 28003 | Alcorn | rural | 14,245 | 13,786 | 306 | 10,170 | 10.97M | 33,513 | -2,963 | 0.693 | 58 |
| 28005 | Amite | rural | 3,724 | 1,785 | 240 | 698 | 3.95M | 33,349 | 76,368 | 0.898 | 28 |
| 28007 | Attala | rural | 6,886 | 4,652 | 277 | 6,079 | 5.00M | 23,372 | 7,617 | 0.918 | 64* |
| 28009 | Benton | suburb | 3,225 | 1,200 | 153 | 10,322 | 2.04M | 34,672 | 1,106 | 0.744 | 58 |
| 28011 | Bolivar | rural | 10,635 | 10,236 | 495 | 169,504 | 11.16M | 35,131 | 83,386 | 0.302 | 106 |
| 28013 | Calhoun | rural | 5,599 | 3,367 | 595 | 27,435 | 4.14M | 31,686 | -3,864 | 0.593 | 123 |
| 28015 | Carroll | rural | 3,525 | 1,224 | 195 | 14,994 | 2.35M | 53,233 | -21,103 | 0.672 | 50 |
| 28017 | Chickasaw | rural | 6,566 | 5,204 | 377 | 25,959 | 5.49M | 36,263 | 54,539 | 0.665 | 110 |
| 28019 | Choctaw | rural | 3,131 | 2,148 | 143 | 1,646 | 2.24M | 12,971 | 16,879 | 0.941 | 34 |
| 28021 | Claiborne | rural | 2,466 | 2,774 | 137 | 4,450 | 2.19M | 24,707 | -23,326 | 0.855 | 94 |
| 28023 | Clarke | rural | 5,980 | 2,791 | 165 | 1,493 | 5.31M | 20,681 | 58,021 | 0.811 | 17 |
| 28025 | Clay | rural | 6,979 | 6,554 | 278 | 9,517 | 8.14M | 99,168 | 29,259 | 0.759 | 25 |
| 28027 | Coahoma | rural | 7,411 | 6,940 | 349 | 99,185 | 8.70M | 39,007 | -30,146 | 0.335 | 138 |
| 28029 | Copiah | suburb | 10,527 | 6,306 | 292 | 2,164 | 6.77M | 39,216 | 23,862 | 0.858 | 42 |
| 28031 | Covington | rural | 7,108 | 5,227 | 326 | 3,368 | 6.45M | 34,645 | 160,461 | 0.759 | 52 |
| 28033 | DeSoto | suburb | 92,131 | 70,498 | 301 | 25,993 | 54.29M | 30,618 | 4,678 | 0.476 | 88 |
| 28035 | Forrest | suburb | 35,362 | 43,546 | 249 | 1,458 | 30.49M | 19,950 | -10,530 | 0.876 | 64* |
| 28037 | Franklin | rural | 2,529 | 1,292 | 83 | 670 | 2.12M | 15,404 | 5,643 | 0.849 | 20 |
| 28039 | George | rural | 8,328 | 4,598 | 370 | 4,490 | 5.54M | 20,248 | -7,057 | 0.736 | 48 |
| 28041 | Greene | rural | 3,214 | 1,902 | 222 | 545 | 3.52M | 23,049 | -1,383 | 0.912 | 64* |
| 28043 | Grenada | rural | 8,902 | 9,566 | 193 | 9,580 | 6.61M | 23,108 | -11,118 | 0.768 | 64* |
| 28045 | Hancock | suburb | 20,582 | 18,592 | 165 | 224 | 20.00M | 14,054 | -25,459 | 0.890 | 64* |
| 28047 | Harrison | suburb | 91,384 | 105,331 | 245 | 73 | 82.36M | 13,029 | -11,466 | 0.908 | 64* |
| 28049 | Hinds | core | 96,567 | 112,492 | 618 | 12,049 | 79.71M | 26,555 | -4,044 | 0.696 | 64 |
| 28051 | Holmes | suburb | 5,279 | 2,915 | 285 | 40,127 | 3.61M | 37,811 | -72,482 | 0.591 | 117 |
| 28053 | Humphreys | rural | 2,518 | 1,751 | 234 | 72,771 | 2.51M | 41,419 | 1,386 | 0.345 | 139 |
| 28055 | Issaquena | rural | 174 | 97 | 52 | 40,948 | 0.50M | 66,428 | 7,292 | 0.430 | 130 |
| 28057 | Itawamba | rural | 10,630 | 6,444 | 269 | 8,288 | 7.22M | 29,616 | 8,171 | 0.712 | 50 |
| 28059 | Jackson | suburb | 61,439 | 52,893 | 286 | 1,413 | 54.76M | 25,284 | -5,872 | 0.812 | 64* |
| 28061 | Jasper | rural | 6,314 | 3,794 | 237 | 618 | 5.76M | 30,788 | 193,777 | 0.893 | 14 |
| 28063 | Jefferson | rural | 2,102 | 1,506 | 188 | 3,881 | 1.76M | 19,637 | 15,855 | 0.708 | 56 |
| 28065 | Jefferson Davis | rural | 4,431 | 2,175 | 239 | 1,452 | 3.38M | 11,831 | 53,189 | 0.882 | 22 |
| 28067 | Jones | rural | 27,751 | 29,175 | 666 | 1,406 | 24.68M | 16,394 | 93,389 | 0.860 | 24 |
| 28069 | Kemper | rural | 3,192 | 1,773 | 206 | 617 | 3.11M | 38,544 | -12,224 | 0.841 | 18 |
| 28071 | Lafayette | rural | 24,693 | 26,847 | 270 | 7,682 | 14.27M | 24,995 | -8,805 | 0.864 | 64* |
| 28073 | Lamar | suburb | 29,912 | 24,024 | 290 | 961 | 16.57M | 16,404 | 36,115 | 0.867 | 42 |
| 28075 | Lauderdale | rural | 29,647 | 33,769 | 244 | 310 | 30.67M | 22,893 | 742 | 0.924 | 19 |
| 28077 | Lawrence | rural | 4,037 | 2,616 | 223 | 2,061 | 4.28M | 25,720 | 114,308 | 0.805 | 64* |
| 28079 | Leake | rural | 8,014 | 5,563 | 473 | 3,050 | 7.42M | 34,386 | 183,311 | 0.867 | 24 |
| 28081 | Lee | rural | 38,045 | 50,415 | 317 | 25,181 | 32.09M | 41,794 | 8,812 | 0.404 | 86 |
| 28083 | Leflore | rural | 10,240 | 12,452 | 386 | 99,984 | 9.99M | 44,902 | 15,486 | 0.335 | 117 |
| 28085 | Lincoln | rural | 13,497 | 12,433 | 335 | 896 | 11.75M | 27,393 | 47,242 | 0.832 | 18 |
| 28087 | Lowndes | rural | 24,604 | 27,845 | 279 | 17,148 | 27.39M | 32,086 | 14,396 | 0.594 | 53 |
| 28089 | Madison | suburb | 53,113 | 59,452 | 418 | 15,138 | 31.73M | 27,688 | -5,946 | 0.756 | 88 |
| 28091 | Marion | rural | 8,800 | 8,749 | 380 | 1,379 | 8.26M | 18,331 | 73,201 | 0.814 | 35 |
| 28093 | Marshall | suburb | 13,832 | 9,989 | 321 | 16,621 | 9.37M | 39,334 | -12,847 | 0.614 | 62 |
| 28095 | Monroe | rural | 13,500 | 10,157 | 431 | 31,808 | 14.45M | 29,809 | 5,834 | 0.702 | 73 |
| 28097 | Montgomery | rural | 3,384 | 2,397 | 187 | 7,769 | 2.50M | 31,191 | 2,987 | 0.784 | 128 |
| 28099 | Neshoba | rural | 10,776 | 10,756 | 467 | 1,118 | 8.96M | 19,878 | 146,277 | 0.801 | 16 |
| 28101 | Newton | rural | 8,429 | 5,567 | 373 | 3,097 | 6.70M | 19,883 | 90,348 | 0.832 | 20 |
| 28103 | Noxubee | rural | 3,788 | 2,286 | 290 | 32,250 | 4.27M | 37,724 | -1,901 | 0.633 | 88 |
| 28105 | Oktibbeha | rural | 21,814 | 21,637 | 260 | 3,229 | 15.80M | 21,880 | -17,338 | 0.818 | 20 |
| 28107 | Panola | rural | 11,587 | 9,789 | 440 | 37,478 | 8.01M | 31,997 | -15,347 | 0.655 | 96 |
| 28109 | Pearl River | rural | 22,433 | 13,444 | 482 | 1,521 | 14.99M | 19,479 | -17,962 | 0.866 | 28 |
| 28111 | Perry | suburb | 3,972 | 2,766 | 208 | 1,567 | 4.55M | 25,931 | 25,577 | 0.913 | 64* |
| 28113 | Pike | rural | 14,632 | 15,722 | 363 | 910 | 13.00M | 23,811 | 9,429 | 0.827 | 26 |
| 28115 | Pontotoc | rural | 13,607 | 11,346 | 506 | 18,401 | 9.97M | 29,788 | -5,375 | 0.679 | 72 |
| 28117 | Prentiss | rural | 10,261 | 8,208 | 318 | 13,255 | 7.29M | 21,215 | 5,528 | 0.720 | 44 |
| 28119 | Quitman | rural | 2,126 | 998 | 224 | 69,339 | 1.68M | 35,068 | 2,184 | 0.544 | 106 |
| 28121 | Rankin | suburb | 76,431 | 70,188 | 448 | 5,698 | 40.73M | 24,149 | 77,309 | 0.710 | 54 |
| 28123 | Scott | suburb | 11,275 | 13,082 | 638 | 4,055 | 8.99M | 26,600 | 87,323 | 0.826 | 50 |
| 28125 | Sharkey | rural | 1,474 | 1,061 | 190 | 57,566 | 1.29M | 35,532 | 19,792 | 0.201 | 108 |
| 28127 | Simpson | suburb | 10,225 | 7,444 | 389 | 1,647 | 7.56M | 26,562 | 95,500 | 0.604 | 28 |
| 28129 | Smith | rural | 5,298 | 2,772 | 362 | 1,333 | 6.68M | 24,035 | 158,290 | 0.808 | 22 |
| 28131 | Stone | suburb | 6,656 | 4,918 | 186 | 1,030 | 4.94M | 47,584 | -14,004 | 0.796 | 36 |
| 28133 | Sunflower | rural | 8,599 | 8,083 | 559 | 143,919 | 8.02M | 32,012 | 47,425 | 0.313 | 118 |
| 28135 | Tallahatchie | rural | 4,407 | 2,911 | 429 | 85,403 | 2.68M | 32,139 | 56,393 | 0.488 | 112 |
| 28137 | Tate | suburb | 11,725 | 6,257 | 360 | 18,975 | 6.32M | 31,997 | -4,007 | 0.657 | 86 |
| 28139 | Tippah | rural | 9,100 | 7,128 | 413 | 10,128 | 6.40M | 27,639 | -3,154 | 0.806 | 68 |
| 28141 | Tishomingo | rural | 7,399 | 6,448 | 179 | 3,292 | 7.60M | 10,063 | -14,077 | 0.881 | 22 |
| 28143 | Tunica | suburb | 3,954 | 4,863 | 224 | 81,143 | 3.36M | 46,726 | 37,704 | 0.162 | 106 |
| 28145 | Union | rural | 12,007 | 12,181 | 443 | 15,527 | 9.16M | 15,869 | -8,379 | 0.721 | 62 |
| 28147 | Walthall | rural | 4,834 | 2,324 | 301 | 2,321 | 4.37M | 28,304 | 37,481 | 0.834 | 38 |
| 28149 | Warren | rural | 19,159 | 20,150 | 163 | 16,554 | 15.00M | 34,345 | 6,126 | 0.619 | 64* |
| 28151 | Washington | rural | 16,403 | 15,618 | 445 | 135,572 | 17.04M | 29,559 | 5,294 | 0.336 | 135 |
| 28153 | Wayne | rural | 7,398 | 5,558 | 326 | 1,261 | 8.09M | 46,612 | 224,240 | 0.871 | 25 |
| 28155 | Webster | rural | 3,990 | 1,904 | 191 | 7,906 | 2.53M | 21,857 | -9,910 | 0.678 | 117 |
| 28157 | Wilkinson | rural | 2,773 | 1,846 | 124 | 1,362 | 2.26M | 12,780 | -953 | 0.888 | 37 |
| 28159 | Winston | rural | 6,340 | 4,953 | 283 | 3,322 | 5.28M | 19,410 | 64,885 | 0.850 | 32 |
| 28161 | Yalobusha | rural | 4,991 | 2,861 | 206 | 7,353 | 2.85M | 27,765 | -6,972 | 0.711 | 135 |
| 28163 | Yazoo | suburb | 8,844 | 6,267 | 498 | 67,489 | 6.69M | 35,686 | -480 | 0.527 | 110 |
| EXT | External (out-of-state commuting) | external | 51,814 | 103,852 | 2,287 | 153,502 | 41.18M | 29,309 | n/a | 0.617 | n/a |

`*` filled, see above.
