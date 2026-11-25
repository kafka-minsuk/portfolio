# South Carolina 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state SC 2022`. 46 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 45 | `SC/CDL_2022_45.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=45 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| ghsl_R6_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_SC.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 5,282,634 | 5,282,634 | 0.000% |
| ACS workers by residence | 2,344,150 | 2,344,150 | 0.000% |
| ACS workers by workplace | 2,303,480 | 2,303,480 | 0.000% |
| ACS workers working out of state | 121,724 | 121,724 | 0.000% |
| BEA non-farm employment (L80) | 3,039,624 | 3,039,624 | 0.000% |
| BEA farm employment (L70) | 27,503 | 27,503 | 0.000% |
| BEA farm proprietors (L50) | 20,958 | 20,958 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 206,486,000 | 206,486,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 132,491,000 | 132,491,000 | 0.000% |
| CoA hired farm labour expense $ | 274,519,000 | 274,519,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 177,616,888,000 | 177,616,888,000 | 0.000% |
| ACS foreign born entered 2010+ | 86,925 | 86,925 | 0.000% |
| CoA owned acres | 3,265,059 | 3,265,059 | 0.000% |
| CoA rented-from-others acres | 1,288,863 | 1,288,863 | 0.000% |
| CoA land in farms, ha | 1,842,907 | 1,842,907 | -0.000% |
| CoA total cropland, ha | 789,208 | 789,208 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.611, median 0.749, max 0.881; BEA counts jobs, ACS counts people by main job). Sum N = 2,425,204 = sum HU + HA = 2,425,204. Farm jobs after scaling: 20,837 (BEA 27,503). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 81,054. Jobs = in-state residents working out of state = 121,724, split by the state farm share (HA = 1,101). Location: the 29 out-of-state counties within 1 km of the state (13033, 13051, 13073, 13103, 13105, 13119, 13137, 13147, 13181, 13241, 13245, 13251, 13257, 37007, 37019, 37045, 37047, 37071, 37089, 37099, 37113, 37119, 37149, 37153, 37155, 37161, 37165, 37175, 37179); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 751,790 ha vs Census of Agriculture cropland 789,208 ha and land in farms 1,842,907 ha; county ratio TF / CoA cropland 0.15 to 1.82. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 622,165 ha). County area covered by CDL pixels: 8,057,235 ha vs land area 7,786,606 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 5.05 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (58,434 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 21,629 $ per BEA farm job, 28,549 $ per farm worker; county range 9,079 to 87,963 $ per worker. State compensation per farm wage job by year: 2018 22,561 $, 2019 21,191 $, 2020 19,656 $, 2021 24,362 $, 2022 20,243 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 78,770,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (274,519,000 $ in 2022, column `hired_labor_coa_usd`) is 2.07x BEA farm compensation (132,491,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 7,508 $, county -27,604 to 74,346 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 77,812 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 663,471,000 $ vs CAINC45 206,486,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.717, county range 0.419 to 0.965.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 48 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 4,355 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Greenville); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (25); rural = the rest (20). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 150.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 59.2 straight-line km/h between counties (median 16.1 to 28.6 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.22).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 45013 Beaufort | not published; NASS 'other (combined) counties' value = 82.5 $/acre |
| cash_rent_usd_acre | 45051 Horry | not published; NASS 'other (combined) counties' value = 82.5 $/acre |
| cash_rent_usd_acre | 45053 Jasper | not published; NASS 'other (combined) counties' value = 82.5 $/acre |
| cash_rent_usd_acre | 45055 Kershaw | not published; NASS 'other (combined) counties' value = 82.5 $/acre |
| cash_rent_usd_acre | 45065 McCormick | not published; NASS 'other (combined) counties' value = 82.5 $/acre |
| cash_rent_usd_acre | 45079 Richland | not published; NASS 'other (combined) counties' value = 82.5 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

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
| 45001 | Abbeville | rural | 9,815 | 5,897 | 371 | 3,847 | 6.79M | 13,759 | -4,405 | 0.852 | 12 |
| 45003 | Aiken | suburb | 73,609 | 66,518 | 863 | 20,869 | 56.57M | 19,579 | -12,699 | 0.835 | 36 |
| 45005 | Allendale | rural | 2,606 | 1,989 | 123 | 16,884 | 2.94M | 44,629 | 11,224 | 0.882 | 29 |
| 45007 | Anderson | suburb | 91,484 | 75,577 | 1,071 | 9,774 | 60.99M | 19,878 | -5,805 | 0.716 | 19 |
| 45009 | Bamberg | rural | 4,756 | 3,482 | 312 | 18,269 | 3.80M | 20,654 | -412 | 0.669 | 34 |
| 45011 | Barnwell | rural | 8,688 | 6,510 | 362 | 15,565 | 7.02M | 21,912 | -5,910 | 0.679 | 32 |
| 45013 | Beaufort | suburb | 84,685 | 88,804 | 176 | 607 | 43.31M | 51,708 | 942 | 0.923 | 82* |
| 45015 | Berkeley | suburb | 113,737 | 80,173 | 300 | 7,633 | 63.95M | 17,014 | -509 | 0.965 | 26 |
| 45017 | Calhoun | suburb | 6,093 | 4,208 | 306 | 24,309 | 6.75M | 24,358 | -9,525 | 0.737 | 50 |
| 45019 | Charleston | suburb | 210,569 | 278,281 | 333 | 1,953 | 153.82M | 33,327 | 12,589 | 0.875 | 26 |
| 45021 | Cherokee | rural | 23,919 | 20,425 | 351 | 3,144 | 13.13M | 26,085 | 19,811 | 0.761 | 39 |
| 45023 | Chester | suburb | 13,438 | 9,572 | 346 | 4,271 | 9.32M | 20,088 | -4,753 | 0.822 | 22 |
| 45025 | Chesterfield | rural | 17,675 | 15,357 | 566 | 21,166 | 14.00M | 32,179 | 35,609 | 0.819 | 58 |
| 45027 | Clarendon | rural | 10,781 | 7,121 | 429 | 42,310 | 9.31M | 20,434 | 7,129 | 0.465 | 47 |
| 45029 | Colleton | rural | 15,466 | 12,260 | 434 | 15,580 | 10.38M | 33,018 | -3,608 | 0.880 | 41 |
| 45031 | Darlington | suburb | 25,776 | 22,152 | 394 | 49,357 | 22.58M | 32,361 | 9,437 | 0.540 | 44 |
| 45033 | Dillon | rural | 11,149 | 9,832 | 275 | 33,668 | 10.54M | 27,770 | -490 | 0.419 | 55 |
| 45035 | Dorchester | suburb | 77,259 | 47,639 | 368 | 12,651 | 42.01M | 20,176 | -4,343 | 0.658 | 44 |
| 45037 | Edgefield | suburb | 11,020 | 6,866 | 384 | 6,766 | 5.54M | 35,275 | 39,823 | 0.822 | 14 |
| 45039 | Fairfield | suburb | 9,136 | 5,862 | 148 | 1,452 | 5.98M | 20,957 | 10,294 | 0.861 | 10 |
| 45041 | Florence | suburb | 59,787 | 68,126 | 476 | 48,822 | 52.65M | 26,630 | 16,417 | 0.462 | 45 |
| 45043 | Georgetown | rural | 25,553 | 24,672 | 166 | 5,010 | 26.50M | 31,473 | 15,447 | 0.821 | 40 |
| 45045 | Greenville | core | 257,265 | 288,170 | 719 | 2,288 | 189.88M | 33,065 | -1,309 | 0.867 | 28 |
| 45047 | Greenwood | rural | 28,878 | 30,699 | 385 | 2,345 | 21.91M | 9,079 | 8,286 | 0.822 | 13 |
| 45049 | Hampton | rural | 7,180 | 5,395 | 274 | 20,981 | 5.84M | 26,821 | -23,490 | 0.737 | 39 |
| 45051 | Horry | suburb | 152,128 | 154,094 | 738 | 48,686 | 142.44M | 31,754 | -27,604 | 0.561 | 82* |
| 45053 | Jasper | suburb | 11,940 | 10,186 | 115 | 4,987 | 6.44M | 30,332 | 10,601 | 0.945 | 82* |
| 45055 | Kershaw | suburb | 28,936 | 19,444 | 365 | 7,707 | 21.15M | 28,444 | 74,346 | 0.771 | 82* |
| 45057 | Lancaster | suburb | 43,090 | 34,335 | 459 | 4,437 | 21.90M | 11,149 | 24,861 | 0.746 | 24 |
| 45059 | Laurens | suburb | 28,596 | 22,870 | 645 | 8,100 | 18.29M | 20,429 | 8,748 | 0.835 | 18 |
| 45061 | Lee | rural | 5,504 | 3,445 | 266 | 38,204 | 5.30M | 35,631 | 25,146 | 0.518 | 51 |
| 45063 | Lexington | suburb | 142,954 | 133,791 | 903 | 12,851 | 93.87M | 87,963 | 32,696 | 0.775 | 30 |
| 45065 | McCormick | rural | 3,174 | 2,033 | 61 | 399 | 2.47M | 20,819 | 12,511 | 0.903 | 82* |
| 45067 | Marion | rural | 10,681 | 7,263 | 195 | 23,062 | 10.27M | 32,537 | -3,714 | 0.558 | 55 |
| 45069 | Marlboro | rural | 8,693 | 6,758 | 231 | 31,891 | 7.86M | 31,249 | 53,320 | 0.547 | 60 |
| 45071 | Newberry | rural | 16,467 | 15,094 | 481 | 7,285 | 14.41M | 29,090 | 17,120 | 0.797 | 32 |
| 45073 | Oconee | rural | 31,671 | 28,047 | 669 | 2,090 | 22.42M | 19,558 | 9,530 | 0.808 | 24 |
| 45075 | Orangeburg | rural | 31,563 | 28,927 | 894 | 64,260 | 29.96M | 42,214 | 5,464 | 0.601 | 48 |
| 45077 | Pickens | suburb | 58,591 | 48,576 | 617 | 780 | 32.38M | 26,138 | -9,220 | 0.845 | 22 |
| 45079 | Richland | suburb | 202,979 | 233,147 | 363 | 9,172 | 174.00M | 21,407 | 2,175 | 0.753 | 82* |
| 45081 | Saluda | suburb | 7,725 | 4,904 | 594 | 6,750 | 6.47M | 25,120 | 15,443 | 0.809 | 23 |
| 45083 | Spartanburg | suburb | 151,753 | 159,929 | 1,003 | 4,803 | 108.24M | 18,792 | 900 | 0.761 | 14 |
| 45085 | Sumter | suburb | 45,080 | 44,957 | 532 | 37,047 | 35.10M | 34,840 | 33,405 | 0.659 | 47 |
| 45087 | Union | suburb | 10,591 | 8,312 | 197 | 1,589 | 7.91M | 22,274 | 538 | 0.799 | 12 |
| 45089 | Williamsburg | rural | 11,755 | 9,256 | 640 | 41,305 | 9.01M | 25,205 | -8,929 | 0.623 | 38 |
| 45091 | York | suburb | 139,955 | 121,692 | 933 | 6,867 | 66.51M | 25,322 | 10,095 | 0.803 | 42 |
| EXT | External (out-of-state commuting) | external | 81,054 | 120,623 | 1,101 | 39,727 | 58.15M | 28,549 | n/a | 0.717 | n/a |

`*` filled, see above.
