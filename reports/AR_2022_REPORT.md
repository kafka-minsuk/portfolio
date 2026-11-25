# Arkansas 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state AR 2022`. 75 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 05 | `AR/CDL_2022_05.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=05 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R6_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_AR.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 3,045,637 | 3,045,637 | 0.000% |
| ACS workers by residence | 1,304,084 | 1,304,084 | 0.000% |
| ACS workers by workplace | 1,303,407 | 1,303,407 | 0.000% |
| ACS workers working out of state | 43,534 | 43,534 | 0.000% |
| BEA non-farm employment (L80) | 1,702,946 | 1,702,946 | 0.000% |
| BEA farm employment (L70) | 52,590 | 52,590 | 0.000% |
| BEA farm proprietors (L50) | 37,615 | 37,615 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,721,020,000 | 2,721,020,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 306,287,000 | 306,287,000 | 0.000% |
| CoA hired farm labour expense $ | 496,747,000 | 496,745,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 95,179,956,000 | 95,179,956,000 | 0.000% |
| ACS foreign born entered 2010+ | 44,645 | 44,645 | 0.000% |
| CoA owned acres | 6,967,030 | 6,967,030 | 0.000% |
| CoA rented-from-others acres | 6,755,495 | 6,755,495 | 0.000% |
| CoA land in farms, ha | 5,553,309 | 5,553,309 | 0.000% |
| CoA total cropland, ha | 3,213,407 | 3,213,407 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.467, median 0.732, max 0.906; BEA counts jobs, ACS counts people by main job). Sum N = 1,346,941 = sum HU + HA = 1,346,941. Farm jobs after scaling: 38,179 (BEA 52,590). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 42,857. Jobs = in-state residents working out of state = 43,534, split by the state farm share (HA = 1,275). Location: the 36 out-of-state counties within 1 km of the state (22015, 22017, 22027, 22035, 22067, 22111, 22119, 22123, 28011, 28027, 28033, 28055, 28143, 28151, 29009, 29023, 29069, 29091, 29119, 29149, 29153, 29155, 29181, 29209, 29213, 40001, 40041, 40079, 40089, 40135, 47045, 47097, 47157, 47167, 48037, 48067); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 2,743,587 ha vs Census of Agriculture cropland 3,213,407 ha and land in farms 5,553,309 ha; county ratio TF / CoA cropland 0.00 to 1.32. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 2,051,966 ha). County area covered by CDL pixels: 13,778,115 ha vs land area 13,466,074 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 3.41 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (55,891 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 19,337 $ per BEA farm job, 26,636 $ per farm worker; county range 6,633 to 53,337 $ per worker. State compensation per farm wage job by year: 2018 21,189 $, 2019 19,590 $, 2020 17,864 $, 2021 18,777 $, 2022 20,453 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 64,878,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (496,745,000 $ in 2022, column `hired_labor_coa_usd`) is 1.62x BEA farm compensation (306,287,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 51,740 $, county -24,444 to 231,213 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 75,228 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 3,422,888,000 $ vs CAINC45 2,721,020,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.508, county range 0.129 to 0.904.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 46 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,921 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 6 counties have no recent foreign born in the ACS sample (Cleburne, Dallas, Fulton, Nevada, Newton, Woodruff), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Pulaski); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (16); rural = the rest (58). `# VERIFY` one core for a multi-metro state.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 196.7 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.6 straight-line km/h between counties (median 19.8 to 27.7 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.29).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 05001 Arkansas | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05003 Ashley | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05021 Clay | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05025 Cleveland | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05027 Columbia | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05103 Ouachita | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05111 Poinsett | not published; NASS 'other (combined) counties' value = 86 $/acre |
| cash_rent_usd_acre | 05147 Woodruff | not published; NASS 'other (combined) counties' value = 86 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26915) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 05001 | Arkansas | rural | 7,222 | 9,033 | 601 | 140,665 | 9.34M | 35,478 | 57,326 | 0.345 | 86* |
| 05003 | Ashley | rural | 6,525 | 5,860 | 351 | 51,455 | 7.31M | 42,128 | 59,929 | 0.358 | 86* |
| 05005 | Baxter | rural | 15,129 | 17,143 | 389 | 53 | 16.94M | 24,526 | 2,319 | 0.690 | 25 |
| 05007 | Benton | suburb | 141,682 | 143,770 | 1,780 | 601 | 81.10M | 25,206 | 87,315 | 0.745 | 35 |
| 05009 | Boone | rural | 15,850 | 15,489 | 981 | 677 | 15.37M | 15,715 | 4,099 | 0.763 | 40 |
| 05011 | Bradley | rural | 3,691 | 3,319 | 125 | 234 | 4.74M | 53,337 | 80,610 | 0.904 | 12 |
| 05013 | Calhoun | rural | 1,643 | 2,415 | 60 | 220 | 2.00M | 17,278 | 9,500 | 0.850 | 14 |
| 05015 | Carroll | rural | 11,683 | 11,384 | 953 | 424 | 10.97M | 24,631 | 57,480 | 0.754 | 32 |
| 05017 | Chicot | rural | 3,224 | 2,664 | 438 | 114,618 | 3.50M | 38,851 | 60,327 | 0.381 | 93 |
| 05019 | Clark | rural | 9,777 | 9,167 | 279 | 6,309 | 9.22M | 17,346 | -4,227 | 0.796 | 15 |
| 05021 | Clay | rural | 6,194 | 3,763 | 752 | 108,903 | 7.20M | 25,091 | 44,751 | 0.332 | 86* |
| 05023 | Cleburne | rural | 9,354 | 7,230 | 527 | 272 | 9.06M | 32,115 | 12,540 | 0.718 | 20 |
| 05025 | Cleveland | rural | 2,886 | 804 | 105 | 85 | 2.88M | 36,456 | 231,213 | 0.856 | 86* |
| 05027 | Columbia | rural | 9,137 | 8,423 | 264 | 98 | 10.59M | 17,331 | 45,094 | 0.860 | 86* |
| 05029 | Conway | rural | 8,867 | 6,389 | 545 | 11,982 | 9.01M | 24,669 | 99,195 | 0.725 | 21 |
| 05031 | Craighead | suburb | 50,201 | 54,475 | 634 | 127,927 | 34.43M | 28,166 | 24,967 | 0.175 | 56 |
| 05033 | Crawford | suburb | 24,303 | 16,994 | 635 | 8,374 | 18.81M | 29,012 | 3,631 | 0.708 | 34 |
| 05035 | Crittenden | suburb | 19,881 | 17,929 | 457 | 125,005 | 21.29M | 26,920 | 93,081 | 0.143 | 90 |
| 05037 | Cross | rural | 6,934 | 4,969 | 421 | 118,700 | 5.82M | 33,622 | 25,127 | 0.193 | 107 |
| 05039 | Dallas | rural | 2,617 | 2,949 | 72 | 280 | 2.36M | 10,512 | 15,235 | 0.826 | 13 |
| 05041 | Desha | rural | 4,027 | 4,075 | 426 | 114,113 | 4.97M | 36,178 | 130,095 | 0.237 | 86 |
| 05043 | Drew | rural | 6,993 | 6,912 | 320 | 30,892 | 5.39M | 25,861 | 87,451 | 0.502 | 18 |
| 05045 | Faulkner | suburb | 58,110 | 45,886 | 849 | 6,889 | 40.11M | 23,904 | -19,130 | 0.728 | 22 |
| 05047 | Franklin | rural | 6,644 | 4,707 | 575 | 2,125 | 6.99M | 25,407 | 34,954 | 0.698 | 16 |
| 05049 | Fulton | rural | 4,212 | 2,253 | 442 | 55 | 3.97M | 33,428 | -23,802 | 0.702 | 30 |
| 05051 | Garland | suburb | 41,090 | 42,491 | 305 | 69 | 38.92M | 24,003 | 1,485 | 0.877 | 10 |
| 05053 | Grant | suburb | 7,695 | 4,977 | 207 | 315 | 4.55M | 32,216 | -12,061 | 0.785 | 26 |
| 05055 | Greene | rural | 19,536 | 16,971 | 723 | 85,176 | 15.87M | 28,772 | 27,102 | 0.267 | 61 |
| 05057 | Hempstead | rural | 7,626 | 7,535 | 628 | 1,810 | 9.93M | 30,657 | 68,273 | 0.770 | 24 |
| 05059 | Hot Spring | rural | 12,758 | 8,177 | 365 | 1,516 | 10.76M | 18,962 | 8,479 | 0.710 | 20 |
| 05061 | Howard | rural | 5,285 | 6,554 | 535 | 1,259 | 7.61M | 24,616 | 161,006 | 0.813 | 33 |
| 05063 | Independence | rural | 15,894 | 17,860 | 805 | 28,232 | 14.99M | 25,525 | 81,823 | 0.670 | 48 |
| 05065 | Izard | rural | 4,112 | 2,544 | 359 | 181 | 4.60M | 28,586 | 14,625 | 0.740 | 20 |
| 05067 | Jackson | rural | 5,825 | 5,075 | 512 | 119,809 | 5.90M | 34,998 | 123,764 | 0.239 | 101 |
| 05069 | Jefferson | rural | 24,926 | 25,798 | 475 | 106,525 | 28.19M | 35,581 | 99,715 | 0.353 | 65 |
| 05071 | Johnson | rural | 9,860 | 9,002 | 523 | 2,245 | 8.26M | 24,942 | 53,626 | 0.737 | 36 |
| 05073 | Lafayette | rural | 2,313 | 1,265 | 253 | 18,883 | 2.92M | 24,623 | 109,028 | 0.413 | 62 |
| 05075 | Lawrence | rural | 6,312 | 4,697 | 576 | 78,775 | 6.15M | 25,343 | 55,678 | 0.353 | 73 |
| 05077 | Lee | rural | 2,514 | 1,832 | 327 | 111,401 | 2.93M | 40,542 | 39,024 | 0.258 | 68 |
| 05079 | Lincoln | rural | 3,550 | 2,726 | 453 | 62,723 | 3.52M | 32,605 | 63,005 | 0.351 | 32 |
| 05081 | Little River | suburb | 5,008 | 3,314 | 364 | 12,043 | 6.01M | 22,321 | 62,922 | 0.734 | 44 |
| 05083 | Logan | rural | 9,042 | 6,685 | 879 | 4,826 | 8.75M | 14,605 | 71,784 | 0.669 | 40 |
| 05085 | Lonoke | suburb | 34,314 | 15,648 | 814 | 108,672 | 19.57M | 38,171 | 10,431 | 0.402 | 41 |
| 05087 | Madison | suburb | 6,891 | 3,880 | 790 | 671 | 6.65M | 24,202 | 79,585 | 0.773 | 44 |
| 05089 | Marion | rural | 5,824 | 4,598 | 380 | 175 | 5.68M | 21,688 | -8,565 | 0.816 | 24 |
| 05091 | Miller | suburb | 15,949 | 11,555 | 360 | 26,005 | 15.25M | 24,513 | 4,512 | 0.436 | 54 |
| 05093 | Mississippi | rural | 16,253 | 18,914 | 735 | 197,696 | 23.89M | 29,715 | 78,647 | 0.129 | 99 |
| 05095 | Monroe | rural | 2,286 | 1,916 | 304 | 83,035 | 2.78M | 34,627 | 27,689 | 0.263 | 92 |
| 05097 | Montgomery | rural | 3,222 | 1,700 | 314 | 524 | 3.53M | 16,850 | 3,333 | 0.735 | 18 |
| 05099 | Nevada | rural | 3,117 | 2,375 | 258 | 349 | 3.35M | 23,547 | 62,904 | 0.729 | 12 |
| 05101 | Newton | rural | 2,785 | 1,185 | 332 | 743 | 2.29M | 21,395 | -4,606 | 0.821 | 22 |
| 05103 | Ouachita | rural | 8,345 | 6,765 | 113 | 470 | 7.76M | 8,206 | 17,537 | 0.904 | 86* |
| 05105 | Perry | suburb | 3,749 | 1,256 | 223 | 5,020 | 3.06M | 29,193 | 55,983 | 0.687 | 12 |
| 05107 | Phillips | rural | 5,529 | 5,093 | 460 | 131,508 | 7.28M | 32,063 | 69,642 | 0.205 | 101 |
| 05109 | Pike | rural | 4,210 | 2,711 | 265 | 755 | 4.44M | 23,884 | 71,137 | 0.830 | 22 |
| 05111 | Poinsett | suburb | 9,114 | 6,065 | 573 | 150,768 | 7.85M | 32,383 | 78,276 | 0.190 | 86* |
| 05113 | Polk | rural | 7,479 | 6,984 | 656 | 1,312 | 8.42M | 17,985 | 84,801 | 0.823 | 29 |
| 05115 | Pope | rural | 26,768 | 27,280 | 796 | 5,700 | 25.66M | 21,999 | 55,047 | 0.616 | 16 |
| 05117 | Prairie | rural | 3,540 | 1,672 | 460 | 93,770 | 3.09M | 33,696 | 41,339 | 0.379 | 38 |
| 05119 | Pulaski | core | 186,769 | 256,031 | 333 | 19,969 | 182.40M | 30,746 | 18,640 | 0.699 | 32 |
| 05121 | Randolph | rural | 6,962 | 6,283 | 567 | 36,654 | 7.75M | 27,712 | 43,798 | 0.587 | 22 |
| 05123 | St. Francis | rural | 7,810 | 7,304 | 409 | 109,907 | 6.91M | 36,986 | 45,088 | 0.245 | 99 |
| 05125 | Saline | suburb | 58,391 | 33,999 | 288 | 197 | 34.21M | 6,633 | -6,035 | 0.719 | 18 |
| 05127 | Scott | rural | 4,047 | 2,768 | 403 | 761 | 5.44M | 27,535 | 89,939 | 0.796 | 16 |
| 05129 | Searcy | rural | 2,844 | 1,569 | 301 | 314 | 2.81M | 29,936 | -19,924 | 0.792 | 22 |
| 05131 | Sebastian | suburb | 56,890 | 70,965 | 593 | 2,841 | 59.65M | 29,269 | 61,489 | 0.685 | 16 |
| 05133 | Sevier | rural | 6,683 | 5,075 | 437 | 661 | 6.03M | 17,075 | 213,767 | 0.780 | 34 |
| 05135 | Sharp | rural | 6,216 | 4,151 | 448 | 152 | 5.44M | 27,523 | 122,504 | 0.731 | 22 |
| 05137 | Stone | rural | 3,856 | 2,952 | 353 | 683 | 4.12M | 18,631 | 27,391 | 0.739 | 20 |
| 05139 | Union | rural | 15,967 | 17,707 | 207 | 161 | 21.93M | 24,566 | 15,025 | 0.791 | 30 |
| 05141 | Van Buren | rural | 5,364 | 4,616 | 417 | 106 | 5.17M | 19,687 | -24,444 | 0.776 | 22 |
| 05143 | Washington | suburb | 119,440 | 121,370 | 1,885 | 781 | 81.40M | 27,973 | 58,369 | 0.751 | 42 |
| 05145 | White | rural | 31,811 | 27,091 | 1,397 | 44,035 | 27.44M | 24,834 | 9,593 | 0.710 | 25 |
| 05147 | Woodruff | rural | 2,625 | 1,802 | 331 | 105,129 | 2.86M | 31,476 | 104,129 | 0.277 | 86* |
| 05149 | Yell | rural | 8,902 | 6,443 | 707 | 7,318 | 7.96M | 18,222 | 109,291 | 0.708 | 15 |
| EXT | External (out-of-state commuting) | external | 42,857 | 42,259 | 1,275 | 91,636 | 37.31M | 26,636 | n/a | 0.508 | n/a |

`*` filled, see above.
