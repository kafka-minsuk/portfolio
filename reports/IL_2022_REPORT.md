# Illinois 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state IL 2022`. 102 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 17 | `IL/CDL_2022_17.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=17 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_IL.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 12,582,032 | 12,582,032 | 0.000% |
| ACS workers by residence | 6,171,891 | 6,171,891 | 0.000% |
| ACS workers by workplace | 6,156,211 | 6,156,211 | 0.000% |
| ACS workers working out of state | 206,540 | 206,540 | 0.000% |
| BEA non-farm employment (L80) | 8,021,071 | 8,021,071 | 0.000% |
| BEA farm employment (L70) | 73,287 | 73,287 | 0.000% |
| BEA farm proprietors (L50) | 57,681 | 57,681 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 9,030,011,000 | 9,030,011,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 723,862,000 | 723,862,000 | 0.000% |
| CoA hired farm labour expense $ | 932,744,000 | 932,742,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 605,857,488,000 | 605,857,488,000 | 0.000% |
| ACS foreign born entered 2010+ | 396,398 | 396,398 | 0.000% |
| CoA owned acres | 11,607,971 | 11,607,971 | 0.000% |
| CoA rented-from-others acres | 14,684,070 | 14,684,070 | 0.000% |
| CoA land in farms, ha | 10,640,011 | 10,640,011 | 0.000% |
| CoA total cropland, ha | 9,272,902 | 9,272,902 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.483, median 0.787, max 0.963; BEA counts jobs, ACS counts people by main job). Sum N = 6,362,751 = sum HU + HA = 6,362,751. Farm jobs after scaling: 57,445 (BEA 73,287). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 190,860. Jobs = in-state residents working out of state = 206,540, split by the state farm share (HA = 1,927). Location: the 44 out-of-state counties within 1 km of the state (18007, 18051, 18083, 18089, 18111, 18129, 18153, 18165, 18167, 18171, 19045, 19057, 19061, 19097, 19111, 19115, 19139, 19163, 21007, 21055, 21139, 21145, 21225, 29031, 29045, 29099, 29111, 29113, 29127, 29133, 29157, 29163, 29173, 29183, 29186, 29189, 29201, 29510, 55043, 55045, 55059, 55065, 55105, 55127); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 8,791,090 ha vs Census of Agriculture cropland 9,272,902 ha and land in farms 10,640,011 ha; county ratio TF / CoA cropland 0.38 to 22.46. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,341,955 ha). County area covered by CDL pixels: 14,591,577 ha vs land area 14,377,852 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 13.82 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (75,533 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 41,056 $ per BEA farm job, 52,378 $ per farm worker; county range 16,205 to 311,913 $ per worker. State compensation per farm wage job by year: 2018 34,820 $, 2019 38,119 $, 2020 37,389 $, 2021 38,788 $, 2022 46,384 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 83,143,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (932,742,000 $ in 2022, column `hired_labor_coa_usd`) is 1.29x BEA farm compensation (723,862,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 123,214 $, county 6,685 to 610,245 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 99,341 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 8,853,964,000 $ vs CAINC45 9,030,011,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.442, county range 0.206 to 0.922.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 243 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 8,420 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (Hardin, Massac, Scott), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Cook); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (36); rural = the rest (65). `# VERIFY` one core for a multi-metro state.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 209.1 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 60.3 straight-line km/h between counties (median 10.6 to 28.7 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.25).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 17019 Champaign | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17037 DeKalb | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17043 DuPage | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17049 Effingham | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17069 Hardin | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17105 Livingston | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17113 McLean | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17135 Montgomery | not published; NASS 'other (combined) counties' value = 273 $/acre |
| cash_rent_usd_acre | 17167 Sangamon | not published; NASS 'other (combined) counties' value = 273 $/acre |

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
| 17001 | Adams | rural | 32,863 | 34,374 | 979 | 115,404 | 41.64M | 33,872 | 114,067 | 0.614 | 178 |
| 17003 | Alexander | suburb | 1,797 | 1,001 | 101 | 20,098 | 2.57M | 51,009 | 89,738 | 0.514 | 176 |
| 17005 | Bond | suburb | 6,913 | 5,074 | 465 | 59,884 | 5.69M | 39,765 | 66,943 | 0.546 | 197 |
| 17007 | Boone | suburb | 25,158 | 16,794 | 403 | 50,957 | 20.44M | 52,594 | 48,881 | 0.309 | 263 |
| 17009 | Brown | rural | 2,368 | 4,219 | 296 | 28,714 | 3.02M | 55,826 | 51,666 | 0.696 | 206 |
| 17011 | Bureau | rural | 15,611 | 11,568 | 1,088 | 173,978 | 15.36M | 63,688 | 24,674 | 0.402 | 292 |
| 17013 | Calhoun | suburb | 1,746 | 684 | 205 | 14,891 | 1.66M | 101,949 | 59,980 | 0.674 | 200 |
| 17015 | Carroll | rural | 6,722 | 5,083 | 540 | 73,174 | 8.13M | 51,403 | 139,950 | 0.510 | 285 |
| 17017 | Cass | rural | 5,760 | 4,818 | 340 | 59,238 | 5.25M | 44,289 | 157,468 | 0.490 | 250 |
| 17019 | Champaign | suburb | 98,994 | 107,572 | 1,012 | 213,991 | 73.55M | 49,006 | 212,647 | 0.318 | 273* |
| 17021 | Christian | rural | 14,557 | 11,319 | 659 | 148,634 | 15.61M | 46,382 | 213,692 | 0.372 | 308 |
| 17023 | Clark | rural | 7,074 | 4,700 | 447 | 75,727 | 7.22M | 56,392 | 126,674 | 0.476 | 228 |
| 17025 | Clay | rural | 5,711 | 5,202 | 577 | 72,346 | 6.66M | 68,243 | 71,484 | 0.548 | 159 |
| 17027 | Clinton | suburb | 18,038 | 12,345 | 758 | 80,985 | 15.32M | 56,548 | 81,236 | 0.555 | 196 |
| 17029 | Coles | rural | 22,724 | 23,424 | 483 | 93,886 | 20.95M | 56,382 | 132,880 | 0.413 | 293 |
| 17031 | Cook | core | 2,547,260 | 2,679,149 | 166 | 3,955 | 1,531.62M | 37,654 | 38,035 | 0.260 | 118 |
| 17033 | Crawford | rural | 8,191 | 8,333 | 495 | 68,596 | 10.69M | 39,906 | 89,422 | 0.393 | 183 |
| 17035 | Cumberland | rural | 5,403 | 2,825 | 460 | 55,678 | 4.16M | 75,390 | 610,245 | 0.496 | 205 |
| 17037 | DeKalb | suburb | 50,485 | 41,347 | 862 | 135,493 | 35.88M | 48,689 | 139,513 | 0.284 | 273* |
| 17039 | De Witt | rural | 7,552 | 5,991 | 429 | 81,794 | 8.06M | 67,074 | 190,196 | 0.334 | 296 |
| 17041 | Douglas | rural | 9,387 | 7,791 | 484 | 91,874 | 9.37M | 56,447 | 164,855 | 0.293 | 298 |
| 17043 | DuPage | suburb | 480,623 | 583,336 | 81 | 1,900 | 417.50M | 64,980 | 13,482 | 0.922 | 273* |
| 17045 | Edgar | rural | 7,409 | 6,981 | 541 | 127,960 | 8.96M | 49,285 | 138,104 | 0.367 | 280 |
| 17047 | Edwards | rural | 2,655 | 1,962 | 273 | 37,429 | 3.27M | 17,662 | 95,223 | 0.437 | 148 |
| 17049 | Effingham | rural | 17,381 | 21,845 | 853 | 72,373 | 17.29M | 45,755 | 79,729 | 0.532 | 273* |
| 17051 | Fayette | rural | 8,886 | 6,045 | 839 | 102,587 | 8.97M | 59,529 | 82,662 | 0.471 | 172 |
| 17053 | Ford | suburb | 6,338 | 4,897 | 361 | 112,024 | 9.81M | 60,196 | 208,107 | 0.334 | 263 |
| 17055 | Franklin | rural | 15,486 | 9,657 | 444 | 47,159 | 15.06M | 52,673 | 86,928 | 0.608 | 126 |
| 17057 | Fulton | rural | 14,264 | 9,076 | 685 | 105,064 | 12.48M | 52,743 | 114,638 | 0.585 | 257 |
| 17059 | Gallatin | rural | 2,074 | 823 | 133 | 53,113 | 2.83M | 91,618 | 202,858 | 0.461 | 171 |
| 17061 | Greene | rural | 5,447 | 2,691 | 490 | 85,147 | 5.10M | 52,720 | 169,512 | 0.529 | 249 |
| 17063 | Grundy | suburb | 26,321 | 23,214 | 320 | 78,487 | 25.72M | 52,076 | 210,912 | 0.391 | 246 |
| 17065 | Hamilton | rural | 3,243 | 1,696 | 328 | 65,164 | 4.03M | 84,679 | 83,254 | 0.463 | 145 |
| 17067 | Hancock | rural | 8,112 | 4,378 | 718 | 127,733 | 9.69M | 69,239 | 146,967 | 0.526 | 265 |
| 17069 | Hardin | rural | 1,210 | 569 | 62 | 3,002 | 1.51M | 70,702 | 62,844 | 0.849 | 273* |
| 17071 | Henderson | rural | 2,896 | 1,017 | 214 | 62,623 | 3.30M | 77,249 | 213,356 | 0.528 | 259 |
| 17073 | Henry | suburb | 23,067 | 14,776 | 993 | 166,519 | 21.03M | 47,203 | 139,675 | 0.445 | 263 |
| 17075 | Iroquois | rural | 12,171 | 7,497 | 997 | 249,214 | 15.24M | 57,742 | 188,739 | 0.401 | 205 |
| 17077 | Jackson | rural | 22,448 | 24,061 | 489 | 47,946 | 20.61M | 75,603 | 42,963 | 0.549 | 154 |
| 17079 | Jasper | rural | 4,584 | 2,607 | 587 | 85,764 | 5.85M | 54,560 | 88,449 | 0.471 | 186 |
| 17081 | Jefferson | rural | 15,993 | 20,044 | 775 | 59,683 | 14.75M | 33,367 | 38,401 | 0.639 | 136 |
| 17083 | Jersey | suburb | 10,053 | 6,098 | 382 | 45,627 | 7.81M | 55,983 | 71,567 | 0.590 | 201 |
| 17085 | Jo Daviess | rural | 10,721 | 7,727 | 635 | 53,925 | 10.51M | 53,979 | 44,012 | 0.576 | 237 |
| 17087 | Johnson | rural | 4,316 | 2,577 | 366 | 10,787 | 3.74M | 66,728 | 13,559 | 0.810 | 52 |
| 17089 | Kane | suburb | 263,420 | 233,546 | 833 | 57,039 | 187.23M | 49,592 | 22,988 | 0.284 | 265 |
| 17091 | Kankakee | suburb | 49,040 | 45,427 | 875 | 135,223 | 46.48M | 51,572 | 107,306 | 0.341 | 230 |
| 17093 | Kendall | suburb | 68,047 | 39,682 | 357 | 56,831 | 38.98M | 54,453 | 79,000 | 0.319 | 261 |
| 17095 | Knox | rural | 20,421 | 19,352 | 746 | 115,867 | 20.22M | 57,541 | 170,537 | 0.434 | 265 |
| 17097 | Lake | suburb | 360,255 | 371,539 | 414 | 8,568 | 240.04M | 54,864 | 23,481 | 0.549 | 112 |
| 17099 | LaSalle | rural | 51,386 | 44,284 | 1,258 | 224,375 | 49.83M | 54,067 | 143,619 | 0.357 | 256 |
| 17101 | Lawrence | rural | 5,958 | 4,361 | 339 | 62,974 | 5.83M | 41,216 | 165,750 | 0.387 | 204 |
| 17103 | Lee | rural | 15,132 | 14,543 | 723 | 152,696 | 15.36M | 52,720 | 141,949 | 0.388 | 280 |
| 17105 | Livingston | rural | 16,394 | 15,835 | 1,238 | 237,188 | 21.12M | 44,162 | 234,404 | 0.368 | 273* |
| 17107 | Logan | rural | 12,076 | 9,859 | 693 | 134,580 | 12.04M | 43,423 | 204,947 | 0.254 | 319 |
| 17109 | McDonough | rural | 12,596 | 12,828 | 664 | 103,652 | 12.65M | 40,290 | 170,796 | 0.407 | 281 |
| 17111 | McHenry | suburb | 162,822 | 121,136 | 896 | 67,446 | 103.75M | 50,939 | 21,316 | 0.354 | 217 |
| 17113 | McLean | suburb | 84,210 | 86,997 | 1,087 | 252,767 | 61.14M | 49,309 | 225,922 | 0.309 | 273* |
| 17115 | Macon | suburb | 44,302 | 48,488 | 479 | 113,593 | 55.79M | 47,624 | 191,183 | 0.279 | 311 |
| 17117 | Macoupin | suburb | 19,857 | 10,986 | 819 | 136,813 | 18.15M | 51,772 | 94,568 | 0.462 | 265 |
| 17119 | Madison | suburb | 127,321 | 110,459 | 927 | 87,713 | 108.49M | 40,022 | 54,949 | 0.421 | 204 |
| 17121 | Marion | rural | 16,031 | 14,016 | 791 | 71,569 | 16.80M | 47,717 | 51,467 | 0.570 | 171 |
| 17123 | Marshall | suburb | 5,110 | 3,158 | 317 | 73,137 | 5.28M | 48,058 | 178,720 | 0.357 | 259 |
| 17125 | Mason | rural | 5,716 | 3,620 | 403 | 101,730 | 6.32M | 73,270 | 235,389 | 0.424 | 247 |
| 17127 | Massac | suburb | 5,704 | 3,741 | 322 | 23,424 | 6.87M | 41,024 | 42,739 | 0.587 | 114 |
| 17129 | Menard | suburb | 5,863 | 2,174 | 240 | 58,527 | 3.94M | 67,315 | 159,941 | 0.346 | 279 |
| 17131 | Mercer | suburb | 7,255 | 3,492 | 465 | 100,254 | 6.67M | 65,498 | 224,013 | 0.488 | 250 |
| 17133 | Monroe | suburb | 18,632 | 9,928 | 398 | 51,747 | 10.11M | 59,706 | 58,160 | 0.420 | 156 |
| 17135 | Montgomery | rural | 11,366 | 9,859 | 853 | 126,498 | 12.15M | 42,934 | 117,510 | 0.452 | 273* |
| 17137 | Morgan | rural | 14,173 | 14,246 | 566 | 101,401 | 16.79M | 56,904 | 147,177 | 0.472 | 230 |
| 17139 | Moultrie | rural | 6,511 | 5,242 | 387 | 69,015 | 6.51M | 72,449 | 171,657 | 0.284 | 331 |
| 17141 | Ogle | rural | 24,422 | 16,556 | 807 | 141,179 | 22.62M | 54,960 | 103,484 | 0.409 | 254 |
| 17143 | Peoria | suburb | 80,437 | 96,407 | 615 | 80,161 | 70.02M | 59,205 | 100,414 | 0.502 | 236 |
| 17145 | Perry | rural | 7,830 | 5,607 | 465 | 55,524 | 7.97M | 32,593 | 51,966 | 0.538 | 144 |
| 17147 | Piatt | suburb | 8,230 | 4,181 | 292 | 98,517 | 6.39M | 68,002 | 276,709 | 0.206 | 331 |
| 17149 | Pike | rural | 6,292 | 4,325 | 744 | 110,120 | 7.31M | 55,781 | 110,484 | 0.641 | 208 |
| 17151 | Pope | rural | 1,263 | 523 | 156 | 8,647 | 1.76M | 16,205 | 6,685 | 0.719 | 92 |
| 17153 | Pulaski | rural | 1,690 | 1,530 | 165 | 23,337 | 2.12M | 62,584 | 87,784 | 0.403 | 144 |
| 17155 | Putnam | rural | 2,598 | 1,562 | 115 | 24,384 | 3.53M | 311,913 | 192,583 | 0.484 | 226 |
| 17157 | Randolph | rural | 12,228 | 12,536 | 652 | 68,786 | 11.95M | 41,767 | 71,486 | 0.480 | 149 |
| 17159 | Richland | rural | 7,529 | 7,028 | 402 | 62,016 | 8.50M | 52,272 | 148,143 | 0.351 | 182 |
| 17161 | Rock Island | suburb | 65,172 | 73,657 | 471 | 49,715 | 62.53M | 57,581 | 91,038 | 0.592 | 208 |
| 17163 | St. Clair | suburb | 121,312 | 107,066 | 632 | 82,091 | 90.78M | 44,960 | 87,069 | 0.383 | 191 |
| 17165 | Saline | rural | 9,695 | 8,750 | 338 | 43,266 | 10.39M | 40,419 | 77,269 | 0.551 | 134 |
| 17167 | Sangamon | suburb | 91,961 | 103,411 | 890 | 153,968 | 81.76M | 52,179 | 200,376 | 0.345 | 273* |
| 17169 | Schuyler | rural | 2,946 | 2,061 | 437 | 46,718 | 3.35M | 30,899 | 99,266 | 0.615 | 217 |
| 17171 | Scott | rural | 2,187 | 1,160 | 252 | 40,942 | 2.08M | 55,275 | 142,382 | 0.558 | 240 |
| 17173 | Shelby | rural | 10,097 | 5,775 | 884 | 137,388 | 11.17M | 49,451 | 114,088 | 0.504 | 218 |
| 17175 | Stark | suburb | 2,384 | 1,493 | 216 | 62,870 | 2.66M | 67,454 | 233,575 | 0.382 | 268 |
| 17177 | Stephenson | rural | 20,106 | 18,826 | 1,003 | 101,039 | 19.88M | 50,289 | 72,775 | 0.490 | 274 |
| 17179 | Tazewell | suburb | 60,929 | 55,006 | 752 | 112,577 | 47.36M | 51,465 | 150,712 | 0.388 | 280 |
| 17181 | Union | rural | 6,750 | 5,582 | 507 | 17,696 | 6.49M | 53,104 | 35,262 | 0.683 | 127 |
| 17183 | Vermilion | rural | 29,995 | 28,708 | 780 | 175,468 | 32.23M | 41,689 | 187,181 | 0.319 | 228 |
| 17185 | Wabash | rural | 4,981 | 3,473 | 151 | 41,451 | 4.96M | 59,791 | 121,544 | 0.372 | 169 |
| 17187 | Warren | rural | 7,485 | 6,173 | 488 | 107,998 | 7.65M | 52,607 | 285,957 | 0.391 | 266 |
| 17189 | Washington | rural | 6,716 | 6,678 | 596 | 100,896 | 8.55M | 53,021 | 64,563 | 0.433 | 172 |
| 17191 | Wayne | rural | 7,059 | 4,441 | 797 | 113,594 | 7.67M | 36,358 | 90,689 | 0.520 | 149 |
| 17193 | White | rural | 5,884 | 4,878 | 437 | 85,692 | 6.65M | 57,938 | 153,847 | 0.413 | 163 |
| 17195 | Whiteside | rural | 26,038 | 22,193 | 841 | 132,153 | 21.96M | 59,012 | 128,961 | 0.452 | 276 |
| 17197 | Will | suburb | 352,432 | 299,717 | 782 | 86,307 | 298.60M | 46,389 | 65,217 | 0.291 | 204 |
| 17199 | Williamson | rural | 29,817 | 31,057 | 498 | 20,567 | 28.12M | 34,727 | 20,685 | 0.598 | 88 |
| 17201 | Winnebago | suburb | 127,395 | 130,545 | 608 | 61,531 | 121.69M | 43,629 | 49,270 | 0.474 | 239 |
| 17203 | Woodford | suburb | 18,421 | 11,879 | 764 | 99,330 | 12.10M | 60,168 | 130,875 | 0.458 | 273 |
| EXT | External (out-of-state commuting) | external | 190,860 | 204,613 | 1,927 | 294,940 | 142.48M | 52,378 | n/a | 0.442 | n/a |

`*` filled, see above.
