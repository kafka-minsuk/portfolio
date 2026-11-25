# North Carolina 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state NC 2022`. 100 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 37 | `NC/CDL_2022_37.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=37 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NC.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 10,698,973 | 10,698,973 | 0.000% |
| ACS workers by residence | 4,919,645 | 4,919,645 | 0.000% |
| ACS workers by workplace | 4,919,314 | 4,919,314 | 0.000% |
| ACS workers working out of state | 120,401 | 120,401 | 0.000% |
| BEA non-farm employment (L80) | 6,539,081 | 6,539,081 | 0.000% |
| BEA farm employment (L70) | 62,960 | 62,960 | 0.000% |
| BEA farm proprietors (L50) | 37,553 | 37,553 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 3,414,661,000 | 3,414,661,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 964,299,000 | 964,299,000 | 0.000% |
| CoA hired farm labour expense $ | 896,049,000 | 932,713,000 | -3.931% |
| BEA non-farm earnings $ (CAINC5N L82) | 434,172,617,000 | 434,172,617,000 | 0.000% |
| ACS foreign born entered 2010+ | 270,128 | 270,128 | 0.000% |
| CoA owned acres | 4,765,347 | 4,824,594 | -1.228% |
| CoA rented-from-others acres | 3,297,909 | 3,303,542 | -0.171% |
| CoA land in farms, ha | 3,289,340 | 3,289,340 | 0.000% |
| CoA total cropland, ha | 1,975,131 | 1,975,131 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.438, median 0.753, max 1.029; BEA counts jobs, ACS counts people by main job). Sum N = 5,039,715 = sum HU + HA = 5,039,715. Farm jobs after scaling: 46,845 (BEA 62,960). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 120,070. Jobs = in-state residents working out of state = 120,401, split by the state farm share (HA = 1,147). Location: the 38 out-of-state counties within 1 km of the state (13111, 13241, 13281, 13291, 45021, 45025, 45033, 45045, 45051, 45057, 45069, 45073, 45077, 45083, 45091, 47009, 47019, 47029, 47059, 47091, 47123, 47139, 47155, 47171, 51025, 51035, 51077, 51081, 51083, 51089, 51117, 51141, 51143, 51175, 51550, 51590, 51800, 51810); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,918,314 ha vs Census of Agriculture cropland 1,975,131 ha and land in farms 3,289,340 ha; county ratio TF / CoA cropland 0.07 to 184.12. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 921,065 ha). County area covered by CDL pixels: 12,854,356 ha vs land area 12,593,559 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 9.90 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (66,397 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 32,791 $ per BEA farm job, 44,072 $ per farm worker; county range 7,849 to 286,510 $ per worker. State compensation per farm wage job by year: 2018 29,405 $, 2019 26,617 $, 2020 32,435 $, 2021 30,498 $, 2022 37,954 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 238,823,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (932,713,000 $ in 2022, column `hired_labor_coa_usd`) is 0.97x BEA farm compensation (964,299,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 54,235 $, county -108,826 to 297,818 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 89,107 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 4,383,040,000 $ vs CAINC45 3,414,661,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.591, county range 0.240 to 0.939.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 99 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 5,482 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (Chowan, Gates, Hyde), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Mecklenburg); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (44); rural = the rest (55). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Dare); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 211.0 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 62.9 straight-line km/h between counties (median 10.5 to 24.7 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.20).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 37055 Dare | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 37031 Carteret | state owner share |
| omega | 37173 Swain | state owner share |
| cash_rent_usd_acre | 37027 Caldwell | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37043 Clay | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37055 Dare | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37075 Graham | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37113 Macon | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37119 Mecklenburg | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37129 New Hanover | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37149 Polk | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37153 Richmond | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37155 Robeson | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37165 Scotland | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37173 Swain | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 37187 Washington | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| owned_acres | 37031 Carteret | (D) in Census of Ag; see fills above |
| owned_acres | 37173 Swain | (D) in Census of Ag; see fills above |
| rented_acres | 37031 Carteret | (D) in Census of Ag; see fills above |
| rented_acres | 37173 Swain | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 37075 Graham | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 37119 Mecklenburg | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 37175 Transylvania | (D) in Census of Ag; left null (comparison column only) |

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
| 37001 | Alamance | suburb | 80,839 | 67,979 | 524 | 9,461 | 58.72M | 31,625 | -4,904 | 0.759 | 41 |
| 37003 | Alexander | suburb | 15,849 | 9,839 | 468 | 3,996 | 10.34M | 29,363 | 127,335 | 0.704 | 50 |
| 37005 | Alleghany | rural | 4,345 | 3,167 | 449 | 5,993 | 3.94M | 33,430 | 1,702 | 0.718 | 100 |
| 37007 | Anson | suburb | 8,565 | 6,177 | 343 | 15,219 | 8.89M | 43,219 | 297,818 | 0.812 | 80 |
| 37009 | Ashe | rural | 11,435 | 9,173 | 870 | 3,962 | 6.47M | 48,164 | -18,151 | 0.758 | 78 |
| 37011 | Avery | rural | 6,209 | 7,174 | 429 | 359 | 4.75M | 34,180 | -4,462 | 0.807 | 70 |
| 37013 | Beaufort | rural | 19,091 | 16,861 | 360 | 55,322 | 16.11M | 55,730 | 47,006 | 0.401 | 117 |
| 37015 | Bertie | rural | 6,177 | 3,842 | 259 | 40,182 | 6.17M | 77,224 | 181,897 | 0.481 | 132 |
| 37017 | Bladen | rural | 10,567 | 11,016 | 502 | 42,894 | 12.14M | 57,429 | 134,379 | 0.840 | 88 |
| 37019 | Brunswick | suburb | 55,354 | 42,281 | 220 | 13,998 | 53.45M | 68,946 | 22,060 | 0.620 | 72 |
| 37021 | Buncombe | suburb | 130,073 | 151,298 | 1,341 | 1,340 | 70.57M | 22,301 | 11,224 | 0.823 | 44 |
| 37023 | Burke | suburb | 38,812 | 32,076 | 496 | 2,517 | 21.71M | 29,370 | 32,868 | 0.795 | 34 |
| 37025 | Cabarrus | suburb | 111,840 | 94,884 | 449 | 7,985 | 60.89M | 41,415 | 32,103 | 0.652 | 67 |
| 37027 | Caldwell | suburb | 35,284 | 26,135 | 310 | 2,274 | 21.58M | 32,584 | 59,878 | 0.742 | 76* |
| 37029 | Camden | suburb | 4,860 | 1,717 | 75 | 21,499 | 2.17M | 78,067 | 31,339 | 0.240 | 112 |
| 37031 | Carteret | rural | 30,080 | 27,887 | 127 | 20,900 | 35.16M | 48,824 | -8,022 | 0.594 | 76 |
| 37033 | Caswell | rural | 9,225 | 3,680 | 406 | 8,507 | 6.00M | 34,551 | 9,586 | 0.807 | 36 |
| 37035 | Catawba | suburb | 74,280 | 88,807 | 596 | 7,457 | 55.04M | 38,493 | 32,072 | 0.668 | 53 |
| 37037 | Chatham | suburb | 34,963 | 24,126 | 899 | 6,353 | 19.73M | 43,168 | 36,675 | 0.770 | 40 |
| 37039 | Cherokee | rural | 11,047 | 10,511 | 223 | 1,297 | 5.90M | 79,268 | 25,696 | 0.708 | 72 |
| 37041 | Chowan | rural | 5,623 | 5,391 | 188 | 18,524 | 4.71M | 54,019 | 27,473 | 0.468 | 110 |
| 37043 | Clay | rural | 4,364 | 3,544 | 129 | 645 | 2.70M | 25,197 | -108,826 | 0.633 | 76* |
| 37045 | Cleveland | rural | 42,455 | 37,137 | 780 | 13,151 | 25.26M | 29,195 | 57,330 | 0.634 | 40 |
| 37047 | Columbus | rural | 18,489 | 14,146 | 535 | 59,520 | 19.09M | 53,815 | 50,706 | 0.536 | 90 |
| 37049 | Craven | rural | 44,932 | 47,826 | 248 | 26,639 | 40.55M | 47,888 | 46,543 | 0.585 | 88 |
| 37051 | Cumberland | suburb | 153,731 | 176,908 | 427 | 29,024 | 117.88M | 42,123 | 58,387 | 0.688 | 100 |
| 37053 | Currituck | suburb | 14,296 | 7,122 | 98 | 17,406 | 8.70M | 25,529 | 4,632 | 0.284 | 92 |
| 37055 | Dare | rural | 18,731 | 20,373 | 0 | 1,863 | 25.10M | 0 | n/a | 0.609 | 76* |
| 37057 | Davidson | suburb | 75,568 | 49,011 | 686 | 11,020 | 53.26M | 39,622 | 12,297 | 0.779 | 47 |
| 37059 | Davie | suburb | 19,362 | 14,610 | 402 | 9,002 | 10.50M | 40,874 | 7,030 | 0.654 | 61 |
| 37061 | Duplin | rural | 21,072 | 16,711 | 1,181 | 73,566 | 23.35M | 56,180 | 206,810 | 0.565 | 92 |
| 37063 | Durham | suburb | 168,520 | 212,991 | 181 | 2,129 | 101.31M | 51,355 | 25,953 | 0.848 | 34 |
| 37065 | Edgecombe | suburb | 20,021 | 16,543 | 509 | 50,895 | 17.47M | 50,963 | 80,730 | 0.370 | 108 |
| 37067 | Forsyth | suburb | 175,739 | 193,146 | 460 | 4,965 | 135.88M | 59,908 | 7,250 | 0.688 | 62 |
| 37069 | Franklin | suburb | 32,053 | 15,438 | 493 | 19,920 | 12.84M | 64,017 | 24,565 | 0.587 | 74 |
| 37071 | Gaston | suburb | 106,701 | 84,847 | 366 | 3,837 | 60.01M | 35,678 | 21,218 | 0.714 | 30 |
| 37073 | Gates | suburb | 4,479 | 1,568 | 182 | 19,170 | 2.96M | 21,126 | 106,298 | 0.454 | 94 |
| 37075 | Graham | rural | 3,048 | 2,224 | 86 | 95 | 1.90M | 7,849 | 1,333 | 0.939 | 76* |
| 37077 | Granville | rural | 26,260 | 20,786 | 430 | 13,563 | 15.13M | 35,641 | 4,419 | 0.726 | 60 |
| 37079 | Greene | rural | 8,021 | 4,166 | 294 | 32,949 | 5.77M | 61,685 | 55,741 | 0.386 | 107 |
| 37081 | Guilford | suburb | 257,749 | 304,491 | 834 | 11,412 | 233.50M | 30,987 | -565 | 0.750 | 32 |
| 37083 | Halifax | rural | 17,869 | 16,205 | 346 | 52,048 | 17.94M | 50,204 | 53,042 | 0.507 | 114 |
| 37085 | Harnett | rural | 57,835 | 30,360 | 592 | 30,922 | 29.84M | 69,145 | 59,397 | 0.469 | 109 |
| 37087 | Haywood | rural | 27,174 | 21,492 | 436 | 1,175 | 16.62M | 27,640 | 1,063 | 0.702 | 64 |
| 37089 | Henderson | suburb | 53,627 | 46,480 | 527 | 5,376 | 28.92M | 78,604 | 30,425 | 0.638 | 105 |
| 37091 | Hertford | rural | 8,435 | 9,471 | 188 | 22,746 | 8.34M | 50,663 | 76,651 | 0.616 | 106 |
| 37093 | Hoke | suburb | 21,569 | 10,152 | 400 | 17,201 | 9.84M | 31,939 | 59,835 | 0.700 | 66 |
| 37095 | Hyde | rural | 1,325 | 1,243 | 190 | 36,516 | 3.20M | 100,336 | 1,915 | 0.491 | 175 |
| 37097 | Iredell | suburb | 90,895 | 87,794 | 979 | 20,195 | 49.04M | 41,356 | 26,130 | 0.599 | 70 |
| 37099 | Jackson | rural | 18,158 | 19,991 | 237 | 388 | 7.95M | 33,151 | 3,353 | 0.707 | 70 |
| 37101 | Johnston | suburb | 106,454 | 64,899 | 1,090 | 53,239 | 46.14M | 48,052 | 13,803 | 0.511 | 110 |
| 37103 | Jones | rural | 3,815 | 1,231 | 130 | 24,634 | 3.70M | 88,051 | 131,717 | 0.463 | 84 |
| 37105 | Lee | rural | 28,339 | 29,659 | 236 | 4,665 | 15.54M | 43,349 | 52,052 | 0.704 | 96 |
| 37107 | Lenoir | rural | 22,131 | 23,803 | 559 | 40,520 | 24.61M | 49,567 | 77,390 | 0.451 | 105 |
| 37109 | Lincoln | suburb | 41,524 | 30,171 | 435 | 8,069 | 22.15M | 30,350 | 20,135 | 0.699 | 40 |
| 37111 | McDowell | rural | 18,297 | 17,780 | 329 | 933 | 11.03M | 45,998 | 25,200 | 0.832 | 50 |
| 37113 | Macon | rural | 15,362 | 14,421 | 248 | 772 | 8.79M | 20,204 | 11,159 | 0.803 | 76* |
| 37115 | Madison | suburb | 9,348 | 5,408 | 398 | 283 | 5.07M | 56,433 | -9,863 | 0.866 | 60 |
| 37117 | Martin | rural | 8,885 | 6,454 | 333 | 35,031 | 9.06M | 64,185 | 708 | 0.487 | 108 |
| 37119 | Mecklenburg | core | 590,774 | 736,268 | 243 | 1,555 | 358.11M | 286,510 | 127,827 | 0.833 | 76* |
| 37121 | Mitchell | rural | 6,316 | 5,463 | 221 | 275 | 3.93M | 18,276 | -8,507 | 0.732 | 60 |
| 37123 | Montgomery | rural | 10,716 | 8,945 | 288 | 4,278 | 8.87M | 40,204 | 148,331 | 0.798 | 36 |
| 37125 | Moore | suburb | 44,256 | 42,121 | 567 | 7,478 | 25.23M | 42,124 | 92,116 | 0.850 | 58 |
| 37127 | Nash | suburb | 42,444 | 41,841 | 683 | 38,839 | 34.38M | 40,379 | 20,358 | 0.501 | 107 |
| 37129 | New Hanover | suburb | 115,016 | 138,431 | 150 | 1,422 | 116.31M | 18,584 | 42,030 | 0.895 | 76* |
| 37131 | Northampton | rural | 6,529 | 4,830 | 283 | 44,836 | 6.53M | 60,872 | 77,468 | 0.489 | 107 |
| 37133 | Onslow | suburb | 104,468 | 103,022 | 346 | 23,661 | 53.13M | 39,872 | 184,129 | 0.623 | 92 |
| 37135 | Orange | suburb | 69,679 | 82,988 | 526 | 8,008 | 30.81M | 45,005 | 15,368 | 0.745 | 33 |
| 37137 | Pamlico | rural | 4,402 | 3,862 | 75 | 14,461 | 4.15M | 66,931 | 30,877 | 0.531 | 86 |
| 37139 | Pasquotank | rural | 18,395 | 17,908 | 156 | 31,359 | 10.53M | 41,337 | 15,635 | 0.259 | 124 |
| 37141 | Pender | suburb | 27,872 | 17,189 | 372 | 22,618 | 16.38M | 66,608 | 94,770 | 0.568 | 74 |
| 37143 | Perquimans | rural | 5,011 | 2,839 | 179 | 31,294 | 3.65M | 47,546 | 87,745 | 0.310 | 94 |
| 37145 | Person | suburb | 18,393 | 12,639 | 470 | 12,673 | 13.01M | 35,974 | -5,936 | 0.604 | 54 |
| 37147 | Pitt | suburb | 80,221 | 83,915 | 583 | 60,217 | 58.33M | 56,872 | 55,996 | 0.442 | 108 |
| 37149 | Polk | rural | 8,355 | 7,030 | 227 | 1,287 | 4.11M | 37,327 | 11,946 | 0.875 | 76* |
| 37151 | Randolph | suburb | 65,475 | 49,217 | 1,112 | 14,747 | 46.79M | 42,039 | 74,790 | 0.751 | 52 |
| 37153 | Richmond | rural | 17,681 | 14,293 | 273 | 7,697 | 17.23M | 31,784 | 220,285 | 0.869 | 76* |
| 37155 | Robeson | rural | 43,118 | 40,123 | 863 | 92,938 | 38.55M | 43,355 | 116,415 | 0.540 | 76* |
| 37157 | Rockingham | suburb | 38,800 | 28,049 | 646 | 11,416 | 31.32M | 41,084 | 7,399 | 0.655 | 34 |
| 37159 | Rowan | suburb | 65,043 | 55,311 | 912 | 17,839 | 43.35M | 37,686 | 22,450 | 0.611 | 64 |
| 37161 | Rutherford | rural | 26,021 | 20,315 | 402 | 4,437 | 17.19M | 27,197 | 42,225 | 0.793 | 34 |
| 37163 | Sampson | rural | 24,170 | 17,696 | 2,124 | 89,339 | 24.84M | 42,844 | 78,942 | 0.566 | 113 |
| 37165 | Scotland | rural | 12,134 | 12,734 | 182 | 16,343 | 10.24M | 37,151 | 251,616 | 0.693 | 76* |
| 37167 | Stanly | rural | 28,124 | 21,724 | 487 | 20,995 | 20.94M | 54,672 | 57,462 | 0.624 | 80 |
| 37169 | Stokes | suburb | 19,243 | 8,994 | 673 | 7,388 | 12.31M | 15,538 | 8,060 | 0.790 | 68 |
| 37171 | Surry | rural | 31,099 | 29,650 | 1,142 | 18,374 | 22.02M | 27,901 | 51,610 | 0.708 | 84 |
| 37173 | Swain | rural | 5,620 | 5,807 | 44 | 110 | 3.06M | 102,224 | 12,309 | 0.594 | 76* |
| 37175 | Transylvania | rural | 13,645 | 12,532 | 206 | 1,574 | 8.17M | 67,634 | 11,664 | 0.758 | 88 |
| 37177 | Tyrrell | rural | 1,176 | 1,468 | 191 | 25,375 | 1.18M | 25,140 | 65,237 | 0.376 | 179 |
| 37179 | Union | suburb | 119,069 | 89,242 | 1,170 | 43,066 | 63.10M | 38,681 | 128,627 | 0.597 | 92 |
| 37181 | Vance | rural | 17,668 | 15,599 | 215 | 7,850 | 13.33M | 41,281 | -39,335 | 0.600 | 52 |
| 37183 | Wake | suburb | 591,910 | 650,726 | 744 | 15,128 | 322.77M | 48,549 | 33,829 | 0.650 | 82 |
| 37185 | Warren | rural | 6,896 | 4,593 | 255 | 10,825 | 4.83M | 38,852 | -10,307 | 0.657 | 46 |
| 37187 | Washington | rural | 3,906 | 3,203 | 238 | 37,267 | 3.70M | 32,468 | 2,555 | 0.296 | 76* |
| 37189 | Watauga | rural | 25,360 | 28,253 | 442 | 1,941 | 12.24M | 33,365 | -2,636 | 0.658 | 40 |
| 37191 | Wayne | suburb | 52,846 | 51,077 | 998 | 58,721 | 44.75M | 47,676 | 135,205 | 0.428 | 120 |
| 37193 | Wilkes | rural | 28,177 | 23,150 | 839 | 9,123 | 20.39M | 30,270 | 152,369 | 0.691 | 54 |
| 37195 | Wilson | rural | 34,109 | 37,374 | 776 | 35,918 | 39.61M | 59,112 | 21,156 | 0.393 | 135 |
| 37197 | Yadkin | suburb | 16,725 | 12,082 | 749 | 19,662 | 10.18M | 34,945 | 50,746 | 0.516 | 60 |
| 37199 | Yancey | rural | 7,632 | 5,342 | 286 | 455 | 4.21M | 22,697 | 3,051 | 0.716 | 42 |
| EXT | External (out-of-state commuting) | external | 120,070 | 119,254 | 1,147 | 46,951 | 80.52M | 44,072 | n/a | 0.591 | n/a |

`*` filled, see above.
