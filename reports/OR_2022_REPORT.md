# Oregon 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state OR 2022`. 36 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 41 | `OR/CDL_2022_41.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=41 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C8.zip |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_OR.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 4,240,137 | 4,240,137 | 0.000% |
| ACS workers by residence | 2,007,255 | 2,007,255 | 0.000% |
| ACS workers by workplace | 2,052,434 | 2,052,434 | 0.000% |
| ACS workers working out of state | 39,413 | 39,413 | 0.000% |
| BEA non-farm employment (L80) | 2,600,941 | 2,600,941 | 0.000% |
| BEA farm employment (L70) | 57,344 | 57,344 | 0.000% |
| BEA farm proprietors (L50) | 34,490 | 34,490 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 1,600,328,000 | 1,600,328,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 1,113,846,000 | 1,113,846,000 | 0.000% |
| CoA hired farm labour expense $ | 1,321,301,000 | 1,321,299,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 189,360,525,000 | 189,360,525,000 | 0.000% |
| ACS foreign born entered 2010+ | 102,553 | 102,553 | 0.000% |
| CoA owned acres | 10,792,684 | 10,792,684 | 0.000% |
| CoA rented-from-others acres | 4,503,095 | 4,503,095 | 0.000% |
| CoA land in farms, ha | 6,189,982 | 6,189,982 | 0.000% |
| CoA total cropland, ha | 1,763,995 | 1,763,995 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.588, median 0.754, max 0.909; BEA counts jobs, ACS counts people by main job). Sum N = 2,091,847 = sum HU + HA = 2,091,847. Farm jobs after scaling: 43,513 (BEA 57,344). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 84,592. Jobs = in-state residents working out of state = 39,413, split by the state farm share (HA = 836). Location: the 24 out-of-state counties within 1 km of the state (06015, 06049, 06093, 16003, 16027, 16049, 16069, 16073, 16075, 16087, 32007, 32013, 32031, 53003, 53005, 53011, 53013, 53015, 53023, 53039, 53049, 53059, 53069, 53071); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,444,578 ha vs Census of Agriculture cropland 1,763,995 ha and land in farms 6,189,982 ha; county ratio TF / CoA cropland 0.08 to 1.58. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 3,875,395 ha). County area covered by CDL pixels: 25,133,462 ha vs land area 24,863,032 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 4.76 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (72,805 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 42,068 $ per BEA farm job, 55,441 $ per farm worker; county range 35,588 to 204,898 $ per worker. State compensation per farm wage job by year: 2018 33,239 $, 2019 30,935 $, 2020 42,314 $, 2021 36,642 $, 2022 48,737 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 323,340,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,321,299,000 $ in 2022, column `hired_labor_coa_usd`) is 1.19x BEA farm compensation (1,113,846,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 27,908 $, county -9,185 to 143,767 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 94,260 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,905,755,000 $ vs CAINC45 1,600,328,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.706, county range 0.506 to 0.898.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 101 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,693 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Multnomah); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (14); rural = the rest (21). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 297.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 51.3 straight-line km/h between counties (median 20.4 to 98.7 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.33).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 41001 Baker | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41007 Clatsop | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41013 Crook | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41017 Deschutes | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41023 Grant | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41027 Hood River | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41031 Jefferson | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41033 Josephine | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41035 Klamath | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41037 Lake | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41045 Malheur | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41055 Sherman | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41063 Wallowa | not published; NASS 'other (combined) counties' value = 40.5 $/acre |
| cash_rent_usd_acre | 41069 Wheeler | not published; NASS 'other (combined) counties' value = 40.5 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26910) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 41001 | Baker | rural | 6,136 | 5,773 | 590 | 45,772 | 8.72M | 52,026 | 27,563 | 0.669 | 40* |
| 41003 | Benton | suburb | 45,707 | 47,538 | 1,185 | 20,160 | 26.00M | 55,507 | 17,637 | 0.584 | 111 |
| 41005 | Clackamas | suburb | 202,643 | 169,501 | 4,195 | 14,897 | 152.77M | 58,269 | 23,543 | 0.748 | 156 |
| 41007 | Clatsop | rural | 18,276 | 18,965 | 173 | 215 | 14.30M | 37,266 | -464 | 0.700 | 40* |
| 41009 | Columbia | suburb | 23,814 | 12,773 | 570 | 1,722 | 16.79M | 204,898 | 13,322 | 0.789 | 139 |
| 41011 | Coos | rural | 25,253 | 23,756 | 617 | 565 | 28.08M | 46,423 | 22,706 | 0.805 | 88 |
| 41013 | Crook | suburb | 11,025 | 9,047 | 560 | 14,327 | 11.81M | 44,035 | 11,383 | 0.775 | 40* |
| 41015 | Curry | rural | 8,625 | 8,017 | 201 | 386 | 11.16M | 58,524 | 14,581 | 0.639 | 40 |
| 41017 | Deschutes | suburb | 96,606 | 97,384 | 1,105 | 7,089 | 78.52M | 43,355 | -9,185 | 0.809 | 40* |
| 41019 | Douglas | rural | 42,065 | 39,186 | 1,721 | 9,376 | 46.30M | 53,769 | 5,272 | 0.717 | 38 |
| 41021 | Gilliam | rural | 777 | 949 | 182 | 92,717 | 1.71M | 72,852 | 89,811 | 0.744 | 51 |
| 41023 | Grant | rural | 2,883 | 2,568 | 338 | 11,079 | 3.15M | 51,284 | 13,836 | 0.714 | 40* |
| 41025 | Harney | rural | 3,124 | 2,603 | 520 | 43,321 | 4.25M | 52,701 | 50,471 | 0.823 | 33 |
| 41027 | Hood River | rural | 12,605 | 12,859 | 1,079 | 7,278 | 7.90M | 57,049 | 24,447 | 0.832 | 40* |
| 41029 | Jackson | suburb | 97,138 | 95,824 | 1,778 | 6,941 | 86.88M | 48,032 | 3,395 | 0.739 | 41 |
| 41031 | Jefferson | suburb | 9,917 | 7,470 | 584 | 26,224 | 8.46M | 51,932 | 34,187 | 0.840 | 40* |
| 41033 | Josephine | suburb | 32,841 | 32,203 | 642 | 879 | 35.81M | 35,588 | 1,195 | 0.884 | 40* |
| 41035 | Klamath | rural | 26,823 | 25,288 | 1,191 | 64,900 | 30.44M | 65,418 | 54,995 | 0.648 | 40* |
| 41037 | Lake | rural | 3,037 | 2,766 | 438 | 42,553 | 4.07M | 59,991 | 58,870 | 0.718 | 40* |
| 41039 | Lane | suburb | 178,879 | 176,983 | 2,875 | 18,200 | 140.76M | 53,930 | 16,013 | 0.626 | 83 |
| 41041 | Lincoln | rural | 19,621 | 19,282 | 310 | 561 | 14.81M | 50,926 | 2,659 | 0.898 | 51 |
| 41043 | Linn | suburb | 56,684 | 48,386 | 2,523 | 58,153 | 49.04M | 47,275 | 20,601 | 0.533 | 138 |
| 41045 | Malheur | rural | 11,394 | 12,172 | 1,431 | 99,286 | 15.00M | 52,020 | 39,801 | 0.797 | 40* |
| 41047 | Marion | suburb | 155,647 | 150,822 | 4,519 | 72,781 | 118.35M | 58,694 | 42,205 | 0.562 | 147 |
| 41049 | Morrow | rural | 4,900 | 5,940 | 819 | 159,104 | 5.80M | 83,246 | 143,767 | 0.616 | 37 |
| 41051 | Multnomah | core | 438,555 | 528,708 | 979 | 3,798 | 303.72M | 50,164 | 34,624 | 0.725 | 135 |
| 41053 | Polk | suburb | 39,897 | 25,316 | 1,506 | 40,577 | 27.97M | 44,387 | 11,219 | 0.621 | 134 |
| 41055 | Sherman | rural | 789 | 992 | 214 | 97,132 | 1.20M | 54,690 | 106,375 | 0.506 | 40* |
| 41057 | Tillamook | rural | 10,750 | 10,070 | 476 | 1,559 | 10.63M | 54,162 | 50,069 | 0.824 | 193 |
| 41059 | Umatilla | rural | 33,310 | 28,131 | 2,262 | 250,621 | 29.69M | 53,104 | 44,704 | 0.550 | 76 |
| 41061 | Union | rural | 11,304 | 10,591 | 771 | 61,550 | 12.29M | 51,938 | 14,328 | 0.731 | 97 |
| 41063 | Wallowa | rural | 3,284 | 2,919 | 386 | 31,307 | 3.75M | 50,165 | 20,180 | 0.687 | 40* |
| 41065 | Wasco | rural | 11,567 | 10,111 | 909 | 68,440 | 11.80M | 71,047 | 26,111 | 0.803 | 60 |
| 41067 | Washington | suburb | 312,020 | 324,676 | 2,785 | 27,670 | 224.50M | 49,376 | 28,523 | 0.618 | 145 |
| 41069 | Wheeler | rural | 484 | 350 | 112 | 3,651 | 0.82M | 67,309 | 12,539 | 0.757 | 40* |
| 41071 | Yamhill | suburb | 48,875 | 39,002 | 2,967 | 39,789 | 39.70M | 47,118 | 26,073 | 0.617 | 201 |
| EXT | External (out-of-state commuting) | external | 84,592 | 38,577 | 836 | 27,740 | 66.88M | 55,441 | n/a | 0.706 | n/a |

`*` filled, see above.
