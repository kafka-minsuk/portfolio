# Oklahoma 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state OK 2022`. 77 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 40 | `OK/CDL_2022_40.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=40 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_OK.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 4,019,800 | 4,019,800 | 0.000% |
| ACS workers by residence | 1,790,757 | 1,790,757 | 0.000% |
| ACS workers by workplace | 1,779,817 | 1,779,817 | 0.000% |
| ACS workers working out of state | 43,133 | 43,133 | 0.000% |
| BEA non-farm employment (L80) | 2,329,224 | 2,329,224 | 0.000% |
| BEA farm employment (L70) | 83,662 | 83,662 | 0.000% |
| BEA farm proprietors (L50) | 70,293 | 70,293 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 559,726,000 | 559,726,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 312,961,000 | 312,961,000 | 0.000% |
| CoA hired farm labour expense $ | 441,548,000 | 441,546,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 154,619,724,000 | 154,619,724,000 | 0.000% |
| ACS foreign born entered 2010+ | 73,495 | 73,495 | 0.000% |
| CoA owned acres | 20,046,054 | 20,046,054 | 0.000% |
| CoA rented-from-others acres | 12,851,509 | 12,851,509 | 0.000% |
| CoA land in farms, ha | 13,313,171 | 13,313,171 | 0.000% |
| CoA total cropland, ha | 4,407,942 | 4,407,942 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.500, median 0.697, max 0.834; BEA counts jobs, ACS counts people by main job). Sum N = 1,822,950 = sum HU + HA = 1,822,950. Farm jobs after scaling: 58,019 (BEA 83,662). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 32,193. Jobs = in-state residents working out of state = 43,133, split by the state farm share (HA = 1,406). Location: the 46 out-of-state counties within 1 km of the state (05007, 05033, 05081, 05113, 05127, 05131, 05133, 05143, 08009, 20007, 20019, 20021, 20025, 20033, 20035, 20077, 20099, 20119, 20125, 20129, 20175, 20189, 20191, 29119, 29145, 35059, 48037, 48075, 48077, 48087, 48097, 48111, 48147, 48181, 48195, 48197, 48211, 48277, 48295, 48337, 48357, 48387, 48421, 48483, 48485, 48487); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 3,446,460 ha vs Census of Agriculture cropland 4,407,942 ha and land in farms 13,313,171 ha; county ratio TF / CoA cropland 0.02 to 1.35. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 7,618,220 ha). County area covered by CDL pixels: 18,103,721 ha vs land area 17,766,468 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 4.66 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (66,383 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 31,979 $ per BEA farm job, 46,113 $ per farm worker; county range 24,252 to 120,953 $ per worker. State compensation per farm wage job by year: 2018 34,949 $, 2019 31,453 $, 2020 23,640 $, 2021 34,398 $, 2022 23,409 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 82,366,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (441,546,000 $ in 2022, column `hired_labor_coa_usd`) is 1.41x BEA farm compensation (312,961,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 6,690 $, county -90,296 to 186,182 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 89,801 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,601,305,000 $ vs CAINC45 559,726,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.609, county range 0.433 to 0.841.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 33 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 2,192 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 2 counties have no recent foreign born in the ACS sample (Cimarron, Cotton), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Oklahoma); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (17); rural = the rest (59). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 198.6 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 64.6 straight-line km/h between counties (median 15.0 to 36.9 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.24).

## Suppressed cells and fills

None.

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
| 40001 | Adair | rural | 7,067 | 4,836 | 846 | 516 | 6.36M | 52,687 | 44,521 | 0.820 | 26 |
| 40003 | Alfalfa | rural | 2,078 | 1,421 | 451 | 130,239 | 3.22M | 56,069 | 10,340 | 0.507 | 48 |
| 40005 | Atoka | rural | 4,937 | 3,060 | 616 | 3,752 | 4.96M | 39,298 | -17,736 | 0.839 | 18 |
| 40007 | Beaver | rural | 2,309 | 1,310 | 597 | 107,986 | 3.44M | 49,109 | 85,841 | 0.501 | 15 |
| 40009 | Beckham | rural | 8,281 | 8,178 | 621 | 52,227 | 11.01M | 64,088 | -16,774 | 0.624 | 21 |
| 40011 | Blaine | rural | 3,028 | 2,696 | 500 | 109,927 | 5.25M | 73,837 | -16,408 | 0.537 | 36 |
| 40013 | Bryan | rural | 19,983 | 19,109 | 1,045 | 18,312 | 15.78M | 44,317 | -12,190 | 0.704 | 15 |
| 40015 | Caddo | rural | 10,624 | 7,197 | 1,055 | 113,827 | 11.46M | 71,300 | -5,798 | 0.585 | 36 |
| 40017 | Canadian | suburb | 78,324 | 46,378 | 1,062 | 100,176 | 42.98M | 37,188 | -1,491 | 0.479 | 37 |
| 40019 | Carter | rural | 21,047 | 22,269 | 922 | 8,236 | 25.95M | 43,420 | -18,291 | 0.723 | 16 |
| 40021 | Cherokee | rural | 20,118 | 15,304 | 1,759 | 505 | 14.80M | 42,968 | 9,356 | 0.753 | 31 |
| 40023 | Choctaw | rural | 5,454 | 4,243 | 661 | 5,147 | 5.78M | 38,504 | -18,817 | 0.775 | 28 |
| 40025 | Cimarron | rural | 1,082 | 696 | 335 | 148,748 | 1.73M | 120,953 | 94,340 | 0.503 | 26 |
| 40027 | Cleveland | suburb | 147,489 | 104,374 | 756 | 8,038 | 84.50M | 56,769 | -19,874 | 0.678 | 23 |
| 40029 | Coal | rural | 1,959 | 1,192 | 336 | 3,489 | 2.94M | 53,186 | 11,631 | 0.753 | 18 |
| 40031 | Comanche | suburb | 53,915 | 54,378 | 913 | 43,610 | 41.23M | 32,785 | -3,290 | 0.517 | 30 |
| 40033 | Cotton | suburb | 2,353 | 1,615 | 336 | 76,052 | 3.02M | 42,477 | -12,672 | 0.469 | 34 |
| 40035 | Craig | rural | 5,246 | 4,607 | 867 | 11,514 | 6.88M | 58,528 | 10,601 | 0.629 | 32 |
| 40037 | Creek | suburb | 30,846 | 19,541 | 1,122 | 2,388 | 27.51M | 33,519 | -18,771 | 0.830 | 14 |
| 40039 | Custer | rural | 14,054 | 14,034 | 728 | 97,791 | 13.87M | 56,155 | -1,894 | 0.527 | 42 |
| 40041 | Delaware | rural | 15,849 | 11,044 | 966 | 4,607 | 13.83M | 41,614 | 82,615 | 0.793 | 40 |
| 40043 | Dewey | rural | 1,836 | 1,561 | 378 | 58,994 | 2.80M | 47,694 | -16,838 | 0.629 | 32 |
| 40045 | Ellis | rural | 1,559 | 985 | 361 | 36,681 | 2.62M | 74,385 | 52,041 | 0.527 | 18 |
| 40047 | Garfield | suburb | 28,409 | 27,680 | 828 | 168,122 | 29.98M | 48,887 | -1,656 | 0.451 | 44 |
| 40049 | Garvin | rural | 10,699 | 9,754 | 1,047 | 23,496 | 12.62M | 44,247 | -14,261 | 0.648 | 20 |
| 40051 | Grady | suburb | 24,743 | 15,966 | 1,432 | 62,637 | 20.99M | 38,454 | 2,325 | 0.637 | 44 |
| 40053 | Grant | rural | 1,798 | 1,228 | 427 | 169,187 | 3.26M | 77,337 | 2,557 | 0.443 | 41 |
| 40055 | Greer | rural | 1,926 | 984 | 339 | 50,464 | 2.87M | 52,074 | 17,030 | 0.547 | 22 |
| 40057 | Harmon | rural | 1,069 | 577 | 234 | 46,310 | 1.47M | 57,862 | 31,762 | 0.525 | 22 |
| 40059 | Harper | rural | 1,403 | 777 | 284 | 53,038 | 2.03M | 87,338 | 99,046 | 0.571 | 15 |
| 40061 | Haskell | rural | 4,404 | 2,955 | 530 | 1,693 | 5.32M | 51,044 | 51,705 | 0.731 | 24 |
| 40063 | Hughes | rural | 4,260 | 2,737 | 733 | 5,474 | 5.85M | 41,934 | 137,886 | 0.808 | 16 |
| 40065 | Jackson | rural | 11,658 | 11,574 | 651 | 118,397 | 10.27M | 39,237 | -1,136 | 0.433 | 32 |
| 40067 | Jefferson | rural | 2,048 | 1,082 | 268 | 35,587 | 2.50M | 64,899 | 10,064 | 0.685 | 27 |
| 40069 | Johnston | rural | 3,736 | 2,947 | 460 | 4,779 | 4.01M | 27,728 | -11,993 | 0.729 | 14 |
| 40071 | Kay | rural | 18,612 | 18,121 | 795 | 131,292 | 23.76M | 33,273 | -4,846 | 0.503 | 48 |
| 40073 | Kingfisher | rural | 6,850 | 7,290 | 771 | 139,610 | 7.04M | 52,441 | 11,839 | 0.505 | 36 |
| 40075 | Kiowa | rural | 3,253 | 2,100 | 476 | 128,358 | 5.11M | 66,721 | 32,178 | 0.471 | 33 |
| 40077 | Latimer | rural | 3,509 | 2,769 | 484 | 828 | 4.35M | 39,569 | -1,985 | 0.780 | 16 |
| 40079 | Le Flore | rural | 18,627 | 13,370 | 1,392 | 11,352 | 16.85M | 40,809 | 60,376 | 0.768 | 19 |
| 40081 | Lincoln | suburb | 14,320 | 7,681 | 1,251 | 9,450 | 12.81M | 41,167 | -21,494 | 0.676 | 26 |
| 40083 | Logan | suburb | 22,183 | 10,508 | 755 | 43,726 | 13.09M | 70,823 | -16,077 | 0.558 | 30 |
| 40085 | Love | rural | 4,203 | 5,601 | 507 | 8,699 | 4.29M | 31,931 | -19,346 | 0.697 | 21 |
| 40087 | McClain | suburb | 20,149 | 11,505 | 811 | 22,851 | 12.59M | 51,093 | -9,776 | 0.688 | 52 |
| 40089 | McCurtain | rural | 12,201 | 11,933 | 1,172 | 10,577 | 13.36M | 35,687 | 40,793 | 0.841 | 20 |
| 40091 | McIntosh | rural | 6,183 | 4,493 | 644 | 3,911 | 8.35M | 30,714 | -11,266 | 0.748 | 21 |
| 40093 | Major | rural | 3,387 | 2,127 | 572 | 91,336 | 4.24M | 50,006 | 5,778 | 0.484 | 30 |
| 40095 | Marshall | rural | 5,890 | 4,528 | 350 | 3,430 | 7.96M | 38,523 | -19,584 | 0.723 | 16 |
| 40097 | Mayes | rural | 16,439 | 14,266 | 1,267 | 10,207 | 18.42M | 50,374 | 4,387 | 0.746 | 33 |
| 40099 | Murray | rural | 5,893 | 5,154 | 373 | 3,055 | 6.28M | 64,403 | -9,361 | 0.705 | 32 |
| 40101 | Muskogee | rural | 25,734 | 27,457 | 1,230 | 16,293 | 29.47M | 36,684 | -11,356 | 0.681 | 28 |
| 40103 | Noble | rural | 4,712 | 4,680 | 578 | 69,928 | 5.53M | 50,843 | -4,074 | 0.526 | 34 |
| 40105 | Nowata | rural | 3,905 | 1,968 | 525 | 6,438 | 3.66M | 54,280 | -11,943 | 0.781 | 20 |
| 40107 | Okfuskee | rural | 3,780 | 1,963 | 524 | 3,824 | 4.09M | 34,898 | -18,785 | 0.719 | 22 |
| 40109 | Oklahoma | core | 381,419 | 494,439 | 886 | 11,718 | 324.67M | 40,389 | -9,893 | 0.731 | 36 |
| 40111 | Okmulgee | suburb | 14,677 | 10,730 | 1,036 | 8,508 | 13.91M | 24,252 | -10,063 | 0.706 | 18 |
| 40113 | Osage | suburb | 18,825 | 9,723 | 991 | 18,396 | 16.34M | 48,506 | 5,743 | 0.546 | 20 |
| 40115 | Ottawa | rural | 12,105 | 11,300 | 868 | 20,792 | 12.17M | 53,285 | 37,912 | 0.698 | 41 |
| 40117 | Pawnee | suburb | 6,520 | 3,281 | 455 | 11,967 | 5.24M | 52,773 | -21,953 | 0.555 | 23 |
| 40119 | Payne | rural | 36,655 | 37,040 | 1,077 | 16,809 | 30.62M | 37,725 | -14,548 | 0.616 | 24 |
| 40121 | Pittsburg | rural | 16,848 | 16,205 | 1,280 | 3,901 | 23.21M | 30,431 | -12,046 | 0.785 | 14 |
| 40123 | Pontotoc | rural | 17,006 | 18,069 | 897 | 2,415 | 17.99M | 38,865 | -10,751 | 0.799 | 17 |
| 40125 | Pottawatomie | rural | 29,303 | 23,793 | 1,152 | 9,913 | 23.45M | 30,746 | -15,586 | 0.806 | 24 |
| 40127 | Pushmataha | rural | 3,588 | 2,546 | 453 | 309 | 3.99M | 32,353 | -14,846 | 0.706 | 28 |
| 40129 | Roger Mills | rural | 1,469 | 855 | 353 | 35,094 | 2.32M | 56,869 | -11,492 | 0.667 | 30 |
| 40131 | Rogers | suburb | 45,762 | 30,649 | 1,208 | 7,938 | 30.51M | 44,170 | -14,585 | 0.742 | 26 |
| 40133 | Seminole | rural | 8,453 | 7,338 | 703 | 2,300 | 8.61M | 57,837 | -9,347 | 0.716 | 18 |
| 40135 | Sequoyah | suburb | 15,212 | 10,195 | 883 | 8,083 | 12.04M | 42,922 | -3,109 | 0.764 | 16 |
| 40137 | Stephens | rural | 17,283 | 15,769 | 966 | 22,735 | 19.35M | 25,235 | -15,416 | 0.611 | 16 |
| 40139 | Texas | rural | 10,085 | 8,427 | 1,310 | 213,549 | 11.63M | 59,499 | 186,182 | 0.615 | 20 |
| 40141 | Tillman | rural | 2,709 | 1,625 | 460 | 135,788 | 3.77M | 50,702 | -34,311 | 0.496 | 33 |
| 40143 | Tulsa | suburb | 318,243 | 382,181 | 828 | 5,396 | 277.09M | 49,412 | -275 | 0.643 | 24 |
| 40145 | Wagoner | suburb | 38,272 | 14,756 | 781 | 26,681 | 20.39M | 41,378 | -5,549 | 0.621 | 26 |
| 40147 | Washington | rural | 22,900 | 21,936 | 608 | 7,213 | 19.83M | 54,251 | -15,198 | 0.441 | 9 |
| 40149 | Washita | rural | 4,710 | 2,257 | 574 | 143,033 | 5.76M | 56,716 | -14,048 | 0.468 | 37 |
| 40151 | Woods | rural | 4,044 | 3,831 | 572 | 86,130 | 5.37M | 43,675 | 9,170 | 0.515 | 28 |
| 40153 | Woodward | rural | 9,248 | 9,053 | 732 | 50,683 | 11.66M | 46,149 | -90,296 | 0.612 | 23 |
| EXT | External (out-of-state commuting) | external | 32,193 | 41,727 | 1,406 | 83,523 | 27.94M | 46,113 | n/a | 0.609 | n/a |

`*` filled, see above.
