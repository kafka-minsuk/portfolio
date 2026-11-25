# Massachusetts 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state MA 2022`. 14 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 25 | `MA/CDL_2022_25.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=25 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| ghsl_R4_C13 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip |
| ghsl_R5_C13 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C13.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C13.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 6,981,974 | 6,981,974 | 0.000% |
| ACS workers by residence | 3,595,260 | 3,595,260 | 0.000% |
| ACS workers by workplace | 3,675,551 | 3,675,551 | 0.000% |
| ACS workers working out of state | 121,610 | 121,610 | 0.000% |
| BEA non-farm employment (L80) | 4,991,682 | 4,991,682 | 0.000% |
| BEA farm employment (L70) | 10,562 | 10,562 | 0.000% |
| BEA farm proprietors (L50) | 6,128 | 6,128 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 164,923,000 | 164,923,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 160,345,000 | 160,345,000 | 0.000% |
| CoA hired farm labour expense $ | 203,795,000 | 203,793,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 445,920,370,000 | 445,920,370,000 | 0.000% |
| ACS foreign born entered 2010+ | 420,303 | 420,303 | 0.000% |
| CoA owned acres | 396,020 | 396,020 | 0.000% |
| CoA rented-from-others acres | 68,431 | 68,431 | 0.000% |
| CoA land in farms, ha | 187,957 | 187,957 | 0.000% |
| CoA total cropland, ha | 64,592 | 64,592 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.580, median 0.735, max 0.770; BEA counts jobs, ACS counts people by main job). Sum N = 3,797,161 = sum HU + HA = 3,797,161. Farm jobs after scaling: 7,831 (BEA 10,562). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 201,901. Jobs = in-state residents working out of state = 121,610, split by the state farm share (HA = 259). Location: the 14 out-of-state counties within 1 km of the state (09110, 09150, 09160, 33005, 33011, 33015, 36021, 36027, 36083, 44001, 44005, 44007, 50003, 50025); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 81,661 ha vs Census of Agriculture cropland 64,592 ha and land in farms 187,957 ha; county ratio TF / CoA cropland 0.56 to 3.17. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 35,144 ha). County area covered by CDL pixels: 2,120,884 ha vs land area 2,020,434 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 4.96 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (89,333 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 27,352 $ per BEA farm job, 36,892 $ per farm worker; county range 23,506 to 66,196 $ per worker. State compensation per farm wage job by year: 2018 30,596 $, 2019 25,744 $, 2020 28,608 $, 2021 27,097 $, 2022 36,163 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 25,707,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (203,793,000 $ in 2022, column `hired_labor_coa_usd`) is 1.27x BEA farm compensation (160,345,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 15,615 $, county 4,080 to 35,425 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 121,580 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 295,633,000 $ vs CAINC45 164,923,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.853, county range 0.731 to 0.966.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 88 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 13,831 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Middlesex); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (10); rural = the rest (3). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 2 counties have no BEA farm jobs (Nantucket, Suffolk); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 135.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 49.5 straight-line km/h between counties (median 6.9 to 39.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.29).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 25019 Nantucket | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 25025 Suffolk | 0 farm jobs: no farm sector in the model (spec §3.11) |
| cash_rent_usd_acre | 25001 Barnstable | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25003 Berkshire | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25007 Dukes | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25009 Essex | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25013 Hampden | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25019 Nantucket | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25021 Norfolk | not published; NASS 'other (combined) counties' value = 75.5 $/acre |
| cash_rent_usd_acre | 25025 Suffolk | not published; NASS 'other (combined) counties' value = 75.5 $/acre |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26919) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25001 | Barnstable | suburb | 111,344 | 106,980 | 226 | 619 | 89.17M | 34,670 | 9,555 | 0.780 | 76* |
| 25003 | Berkshire | suburb | 62,128 | 62,433 | 446 | 12,470 | 30.38M | 28,678 | 4,080 | 0.863 | 76* |
| 25005 | Bristol | suburb | 285,132 | 235,807 | 752 | 7,371 | 160.43M | 37,358 | 7,155 | 0.782 | 84 |
| 25007 | Dukes | rural | 10,084 | 10,424 | 71 | 617 | 7.93M | 33,357 | 9,618 | 0.897 | 76* |
| 25009 | Essex | suburb | 412,030 | 341,149 | 438 | 3,990 | 176.80M | 33,447 | 16,248 | 0.731 | 76* |
| 25011 | Franklin | rural | 35,365 | 28,320 | 703 | 11,951 | 17.55M | 27,758 | 9,012 | 0.855 | 113 |
| 25013 | Hampden | suburb | 209,900 | 210,590 | 566 | 5,451 | 137.42M | 27,550 | 13,149 | 0.851 | 76* |
| 25015 | Hampshire | suburb | 75,077 | 73,837 | 594 | 10,811 | 31.33M | 26,513 | 9,629 | 0.846 | 118 |
| 25017 | Middlesex | core | 881,099 | 959,645 | 1,485 | 4,142 | 378.76M | 66,196 | 35,425 | 0.829 | 68 |
| 25019 | Nantucket | rural | 7,418 | 8,180 | 0 | 96 | 5.67M | 0 | n/a | 0.874 | 76* |
| 25021 | Norfolk | suburb | 379,344 | 369,661 | 421 | 1,515 | 193.72M | 29,270 | 19,997 | 0.921 | 76* |
| 25023 | Plymouth | suburb | 268,672 | 219,078 | 692 | 8,101 | 129.12M | 40,338 | 12,220 | 0.895 | 81 |
| 25025 | Suffolk | suburb | 424,949 | 660,953 | 0 | 76 | 144.98M | 0 | n/a | 0.966 | 76* |
| 25027 | Worcester | suburb | 432,718 | 380,664 | 1,436 | 14,451 | 149.40M | 23,506 | 11,117 | 0.868 | 44 |
| EXT | External (out-of-state commuting) | external | 201,901 | 121,351 | 259 | 2,702 | 92.81M | 36,892 | n/a | 0.853 | n/a |

`*` filled, see above.
