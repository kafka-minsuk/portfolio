# Wyoming 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state WY 2022`. 23 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 56 | `WY/CDL_2022_56.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=56 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_WY.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 581,381 | 581,381 | 0.000% |
| ACS workers by residence | 284,555 | 284,555 | 0.000% |
| ACS workers by workplace | 290,191 | 290,191 | 0.000% |
| ACS workers working out of state | 7,982 | 7,982 | 0.000% |
| BEA non-farm employment (L80) | 422,281 | 422,281 | 0.000% |
| BEA farm employment (L70) | 14,283 | 14,283 | 0.000% |
| BEA farm proprietors (L50) | 10,455 | 10,455 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 395,347,000 | 395,347,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 167,241,000 | 167,241,000 | 0.000% |
| CoA hired farm labour expense $ | 155,369,000 | 155,367,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 25,023,859,000 | 25,023,859,000 | 0.000% |
| ACS foreign born entered 2010+ | 5,130 | 5,130 | 0.000% |
| CoA owned acres | 19,056,540 | 19,056,540 | 0.000% |
| CoA rented-from-others acres | 9,719,781 | 9,719,781 | 0.000% |
| CoA land in farms, ha | 11,645,364 | 11,645,364 | -0.000% |
| CoA total cropland, ha | 941,341 | 941,341 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.482, median 0.670, max 0.812; BEA counts jobs, ACS counts people by main job). Sum N = 298,173 = sum HU + HA = 298,173. Farm jobs after scaling: 9,607 (BEA 14,283). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 13,618. Jobs = in-state residents working out of state = 7,982, split by the state farm share (HA = 264). Location: the 28 out-of-state counties within 1 km of the state (08057, 08069, 08081, 08107, 08123, 16007, 16019, 16029, 16043, 16081, 30003, 30009, 30011, 30031, 30067, 30075, 31007, 31105, 31157, 31165, 46019, 46033, 46047, 46081, 46103, 49009, 49033, 49043); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,009,983 ha vs Census of Agriculture cropland 941,341 ha and land in farms 11,645,364 ha; county ratio TF / CoA cropland 0.26 to 1.96. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 5,015,422 ha). County area covered by CDL pixels: 25,332,424 ha vs land area 25,145,871 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 0.67 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (59,259 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 44,325 $ per BEA farm job, 65,900 $ per farm worker; county range 42,550 to 175,649 $ per worker. State compensation per farm wage job by year: 2018 42,430 $, 2019 30,176 $, 2020 45,982 $, 2021 55,581 $, 2022 43,689 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 19,929,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (155,367,000 $ in 2022, column `hired_labor_coa_usd`) is 0.93x BEA farm compensation (167,241,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 27,680 $, county 4,864 to 58,811 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 89,185 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 455,106,000 $ vs CAINC45 395,347,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.662, county range 0.519 to 0.833.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 17 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 1,261 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 2 counties have no recent foreign born in the ACS sample (Hot Springs, Niobrara), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Laramie); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (1); rural = the rest (21). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 305.2 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.2 straight-line km/h between counties (median 38.7 to 88.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.35).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 56001 Albany | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56003 Big Horn | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56005 Campbell | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56009 Converse | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56017 Hot Springs | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56019 Johnson | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56025 Natrona | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56027 Niobrara | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56029 Park | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56031 Platte | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56037 Sweetwater | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56039 Teton | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56041 Uinta | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56043 Washakie | not published; NASS 'other (combined) counties' value = 13.5 $/acre |
| cash_rent_usd_acre | 56045 Weston | not published; NASS 'other (combined) counties' value = 13.5 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26913) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 56001 | Albany | rural | 20,511 | 19,893 | 445 | 29,110 | 10.61M | 68,120 | 19,176 | 0.833 | 14* |
| 56003 | Big Horn | rural | 4,868 | 4,410 | 570 | 55,903 | 5.44M | 61,087 | 26,721 | 0.578 | 14* |
| 56005 | Campbell | rural | 23,900 | 25,355 | 698 | 74,317 | 19.11M | 44,001 | 18,747 | 0.585 | 14* |
| 56007 | Carbon | rural | 6,516 | 6,140 | 307 | 19,475 | 6.70M | 63,721 | 37,734 | 0.622 | 17 |
| 56009 | Converse | rural | 6,843 | 6,257 | 387 | 26,397 | 5.26M | 69,555 | 20,935 | 0.810 | 14* |
| 56011 | Crook | rural | 3,398 | 2,689 | 349 | 96,095 | 3.44M | 67,107 | 25,102 | 0.584 | 16 |
| 56013 | Fremont | rural | 16,314 | 14,903 | 989 | 60,620 | 15.45M | 65,259 | 33,160 | 0.666 | 13 |
| 56015 | Goshen | rural | 5,734 | 4,569 | 680 | 92,708 | 6.69M | 56,542 | 22,126 | 0.704 | 18 |
| 56017 | Hot Springs | rural | 2,008 | 1,915 | 129 | 8,370 | 2.30M | 80,021 | 4,864 | 0.752 | 14* |
| 56019 | Johnson | rural | 3,948 | 3,789 | 280 | 28,864 | 3.79M | 91,540 | 24,734 | 0.592 | 14* |
| 56021 | Laramie | core | 50,613 | 51,584 | 888 | 125,384 | 34.01M | 82,037 | 20,553 | 0.702 | 25 |
| 56023 | Lincoln | rural | 9,577 | 8,082 | 457 | 34,905 | 5.69M | 48,710 | 22,425 | 0.689 | 20 |
| 56025 | Natrona | suburb | 40,190 | 39,751 | 342 | 13,678 | 33.63M | 49,848 | 15,760 | 0.576 | 14* |
| 56027 | Niobrara | rural | 1,083 | 1,040 | 208 | 30,612 | 1.38M | 56,881 | 28,411 | 0.667 | 14* |
| 56029 | Park | rural | 14,351 | 13,697 | 696 | 51,002 | 13.79M | 78,386 | 46,741 | 0.829 | 14* |
| 56031 | Platte | rural | 3,494 | 3,361 | 419 | 52,989 | 5.25M | 58,013 | 52,706 | 0.714 | 14* |
| 56033 | Sheridan | rural | 15,372 | 14,149 | 417 | 49,190 | 12.61M | 87,021 | 12,492 | 0.747 | 21 |
| 56035 | Sublette | rural | 4,365 | 3,990 | 304 | 54,626 | 3.65M | 66,540 | 47,130 | 0.797 | 16 |
| 56037 | Sweetwater | rural | 20,668 | 21,558 | 227 | 14,030 | 14.48M | 49,232 | 58,811 | 0.519 | 14* |
| 56039 | Teton | rural | 14,567 | 19,084 | 102 | 2,344 | 5.17M | 175,649 | 36,787 | 0.522 | 14* |
| 56041 | Uinta | rural | 9,468 | 8,239 | 271 | 38,747 | 6.84M | 42,550 | 15,770 | 0.591 | 14* |
| 56043 | Washakie | rural | 3,828 | 3,685 | 237 | 21,332 | 3.29M | 61,038 | 40,672 | 0.736 | 14* |
| 56045 | Weston | rural | 2,939 | 2,446 | 203 | 29,286 | 3.53M | 68,189 | 6,670 | 0.592 | 14* |
| EXT | External (out-of-state commuting) | external | 13,618 | 7,718 | 264 | 27,781 | 10.63M | 65,900 | n/a | 0.662 | n/a |

`*` filled, see above.
