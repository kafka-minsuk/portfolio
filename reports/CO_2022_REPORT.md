# Colorado 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state CO 2022`. 64 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 08 | `CO/CDL_2022_08.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=08 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_CO.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 5,839,926 | 5,839,926 | 0.000% |
| ACS workers by residence | 3,006,848 | 3,006,848 | 0.000% |
| ACS workers by workplace | 3,002,991 | 3,002,991 | 0.000% |
| ACS workers working out of state | 28,362 | 28,362 | 0.000% |
| BEA non-farm employment (L80) | 4,138,718 | 4,138,718 | 0.000% |
| BEA farm employment (L70) | 49,226 | 49,226 | 0.000% |
| BEA farm proprietors (L50) | 34,941 | 34,941 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 619,333,000 | 619,333,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 610,855,000 | 610,855,000 | 0.000% |
| CoA hired farm labour expense $ | 667,380,000 | 675,083,000 | -1.141% |
| BEA non-farm earnings $ (CAINC5N L82) | 317,704,874,000 | 317,704,874,000 | 0.000% |
| ACS foreign born entered 2010+ | 148,842 | 148,842 | 0.000% |
| CoA owned acres | 20,334,391 | 20,345,526 | -0.055% |
| CoA rented-from-others acres | 9,864,755 | 9,868,373 | -0.037% |
| CoA land in farms, ha | 12,226,150 | 12,227,131 | -0.008% |
| CoA total cropland, ha | 4,239,683 | 4,240,751 | -0.025% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.444, median 0.694, max 0.941; BEA counts jobs, ACS counts people by main job). Sum N = 3,031,353 = sum HU + HA = 3,031,353. Farm jobs after scaling: 33,895 (BEA 49,226). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 24,505. Jobs = in-state residents working out of state = 28,362, split by the state farm share (HA = 320). Location: the 29 out-of-state counties within 1 km of the state (04001, 20023, 20071, 20075, 20129, 20181, 20187, 20199, 31029, 31033, 31049, 31057, 31101, 31105, 31135, 35007, 35039, 35045, 35055, 35059, 40025, 49009, 49019, 49037, 49047, 56001, 56007, 56021, 56037); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 3,599,892 ha vs Census of Agriculture cropland 4,240,751 ha and land in farms 12,227,131 ha; county ratio TF / CoA cropland 0.01 to 1.59. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 7,366,294 ha). County area covered by CDL pixels: 26,959,993 ha vs land area 26,841,874 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 5.87 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (76,764 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 46,844 $ per BEA farm job, 68,032 $ per farm worker; county range 21,916 to 201,075 $ per worker. State compensation per farm wage job by year: 2018 45,959 $, 2019 34,427 $, 2020 46,024 $, 2021 54,913 $, 2022 42,762 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 84,026,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (675,083,000 $ in 2022, column `hired_labor_coa_usd`) is 1.11x BEA farm compensation (610,855,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 12,581 $, county -23,634 to 64,421 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 107,004 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,427,632,000 $ vs CAINC45 619,333,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.673, county range 0.445 to 1.000.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 34 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 2,401 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 4 counties have no recent foreign born in the ACS sample (Dolores, Hinsdale, Huerfano, Jackson), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Denver); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (16); rural = the rest (47). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 4 counties have no BEA farm jobs (Clear Creek, Gilpin, Lake, San Juan); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 281.8 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 51.8 straight-line km/h between counties (median 5.6 to 67.2 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.39).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 08019 Clear Creek | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 08047 Gilpin | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 08065 Lake | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 08111 San Juan | 0 farm jobs: no farm sector in the model (spec §3.11) |
| rented_acres | 08079 Mineral | land in farms minus the other tenure (Census of Ag identity) |
| omega | 08014 Broomfield | state owner share |
| omega | 08019 Clear Creek | state owner share |
| omega | 08031 Denver | state owner share |
| omega | 08047 Gilpin | state owner share |
| omega | 08111 San Juan | state owner share |
| cash_rent_usd_acre | 08011 Bent | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08014 Broomfield | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08015 Chaffee | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08019 Clear Creek | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08023 Costilla | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08025 Crowley | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08027 Custer | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08031 Denver | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08033 Dolores | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08035 Douglas | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08037 Eagle | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08039 Elbert | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08041 El Paso | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08043 Fremont | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08045 Garfield | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08047 Gilpin | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08049 Grand | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08051 Gunnison | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08053 Hinsdale | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08055 Huerfano | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08057 Jackson | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08059 Jefferson | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08065 Lake | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08071 Las Animas | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08077 Mesa | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08079 Mineral | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08081 Moffat | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08083 Montezuma | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08085 Montrose | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08089 Otero | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08091 Ouray | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08093 Park | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08097 Pitkin | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08099 Prowers | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08101 Pueblo | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08103 Rio Blanco | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08105 Rio Grande | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08107 Routt | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08109 Saguache | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08111 San Juan | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08113 San Miguel | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08117 Summit | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 08119 Teller | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| owned_acres | 08019 Clear Creek | (D) in Census of Ag; see fills above |
| owned_acres | 08047 Gilpin | (D) in Census of Ag; see fills above |
| rented_acres | 08014 Broomfield | (D) in Census of Ag; see fills above |
| rented_acres | 08019 Clear Creek | (D) in Census of Ag; see fills above |
| rented_acres | 08031 Denver | (D) in Census of Ag; see fills above |
| rented_acres | 08047 Gilpin | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 08025 Crowley | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 08065 Lake | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 08071 Las Animas | (D) in Census of Ag; left null (comparison column only) |

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
| 08001 | Adams | suburb | 271,582 | 222,594 | 884 | 183,384 | 181.52M | 95,538 | 22,877 | 0.461 | 22 |
| 08003 | Alamosa | rural | 7,632 | 8,025 | 454 | 29,739 | 7.55M | 62,312 | 9,296 | 0.613 | 21 |
| 08005 | Arapahoe | suburb | 349,283 | 328,603 | 595 | 75,683 | 201.90M | 86,162 | 4,033 | 0.698 | 16 |
| 08007 | Archuleta | rural | 5,858 | 5,454 | 238 | 1,227 | 5.82M | 89,134 | -7,621 | 0.720 | 14 |
| 08009 | Baca | rural | 1,468 | 1,019 | 500 | 240,596 | 2.38M | 88,878 | 9,281 | 0.730 | 30 |
| 08011 | Bent | rural | 1,674 | 1,159 | 362 | 35,347 | 2.30M | 60,779 | 15,149 | 0.740 | 26* |
| 08013 | Boulder | suburb | 175,188 | 211,609 | 866 | 15,057 | 112.92M | 47,264 | 7,705 | 0.644 | 29 |
| 08014 | Broomfield | suburb | 41,490 | 45,535 | 27 | 1,800 | 23.69M | 21,916 | -12,829 | 0.673 | 26* |
| 08015 | Chaffee | rural | 8,649 | 8,651 | 182 | 3,628 | 8.59M | 85,873 | 16,470 | 0.738 | 26* |
| 08017 | Cheyenne | rural | 878 | 982 | 390 | 198,479 | 1.57M | 61,809 | -5,537 | 0.663 | 33 |
| 08019 | Clear Creek | suburb | 5,360 | 4,387 | 0 | 21 | 1.10M | 0 | n/a | 0.673 | 26* |
| 08021 | Conejos | rural | 2,946 | 1,576 | 408 | 36,538 | 3.29M | 74,230 | 14,009 | 0.816 | 20 |
| 08023 | Costilla | rural | 1,129 | 644 | 167 | 16,916 | 1.41M | 118,228 | -7,449 | 0.937 | 26* |
| 08025 | Crowley | rural | 1,567 | 800 | 202 | 5,874 | 1.27M | 82,807 | 13,611 | 0.886 | 26* |
| 08027 | Custer | rural | 2,029 | 1,537 | 135 | 8,313 | 2.27M | 69,068 | 454 | 0.644 | 26* |
| 08029 | Delta | rural | 11,981 | 9,152 | 969 | 30,695 | 14.70M | 69,306 | 5,782 | 0.783 | 21 |
| 08031 | Denver | core | 409,324 | 550,309 | 16 | 5,102 | 246.90M | 64,405 | 6,000 | 0.673 | 26* |
| 08033 | Dolores | rural | 1,043 | 628 | 191 | 23,773 | 0.97M | 77,385 | 806 | 0.773 | 26* |
| 08035 | Douglas | suburb | 195,197 | 166,031 | 934 | 1,920 | 86.52M | 37,799 | 2,334 | 0.829 | 26* |
| 08037 | Eagle | rural | 31,408 | 29,701 | 143 | 4,813 | 12.81M | 106,115 | 14,530 | 0.705 | 26* |
| 08039 | Elbert | suburb | 13,823 | 5,299 | 767 | 58,660 | 6.78M | 66,169 | -23,634 | 0.691 | 26* |
| 08041 | El Paso | suburb | 368,980 | 364,229 | 1,084 | 8,241 | 226.19M | 51,082 | -4,150 | 0.582 | 26* |
| 08043 | Fremont | rural | 16,657 | 15,302 | 714 | 3,459 | 19.70M | 41,516 | 495 | 0.740 | 26* |
| 08045 | Garfield | rural | 33,232 | 28,791 | 613 | 21,200 | 16.69M | 52,847 | 994 | 0.563 | 26* |
| 08047 | Gilpin | suburb | 3,557 | 5,378 | 0 | 4 | 0.98M | 0 | n/a | 0.673 | 26* |
| 08049 | Grand | rural | 8,728 | 8,302 | 200 | 635 | 5.01M | 54,937 | 15,128 | 0.617 | 26* |
| 08051 | Gunnison | rural | 9,984 | 10,083 | 221 | 3,003 | 6.40M | 63,570 | -2,975 | 0.690 | 26* |
| 08053 | Hinsdale | rural | 408 | 388 | 25 | 121 | 0.56M | 38,060 | -17,725 | 0.857 | 26* |
| 08055 | Huerfano | rural | 2,498 | 2,139 | 350 | 4,628 | 3.50M | 35,866 | -5,065 | 0.668 | 26* |
| 08057 | Jackson | rural | 660 | 613 | 103 | 312 | 0.80M | 64,330 | 32,497 | 0.765 | 26* |
| 08059 | Jefferson | suburb | 317,312 | 276,428 | 541 | 435 | 227.61M | 39,004 | 9,292 | 0.668 | 26* |
| 08061 | Kiowa | rural | 624 | 351 | 233 | 196,778 | 1.01M | 169,401 | 17,776 | 0.701 | 24 |
| 08063 | Kit Carson | rural | 3,444 | 2,737 | 656 | 320,874 | 4.74M | 80,738 | -1,516 | 0.584 | 41 |
| 08065 | Lake | rural | 4,390 | 3,216 | 0 | 17 | 1.47M | 0 | n/a | 0.765 | 26* |
| 08067 | La Plata | rural | 28,762 | 29,386 | 920 | 15,695 | 18.11M | 54,684 | -9,136 | 0.887 | 18 |
| 08069 | Larimer | suburb | 189,742 | 189,628 | 1,574 | 28,486 | 111.16M | 61,720 | 11,952 | 0.598 | 40 |
| 08071 | Las Animas | rural | 5,703 | 5,126 | 506 | 11,117 | 7.18M | 44,914 | 2,928 | 0.761 | 26* |
| 08073 | Lincoln | rural | 2,169 | 1,995 | 376 | 168,436 | 2.83M | 74,872 | 2,337 | 0.572 | 22 |
| 08075 | Logan | rural | 10,183 | 8,775 | 946 | 183,228 | 9.50M | 67,714 | 2,729 | 0.562 | 36 |
| 08077 | Mesa | suburb | 72,651 | 69,953 | 2,053 | 30,572 | 75.69M | 53,503 | 2,964 | 0.752 | 26* |
| 08079 | Mineral | rural | 413 | 422 | 8 | 68 | 0.58M | 201,075 | 28,444 | 1.000 | 26* |
| 08081 | Moffat | rural | 6,062 | 4,018 | 359 | 33,835 | 5.77M | 44,556 | -474 | 0.777 | 26* |
| 08083 | Montezuma | rural | 10,741 | 9,533 | 877 | 34,029 | 8.74M | 66,289 | -5,160 | 0.917 | 26* |
| 08085 | Montrose | rural | 18,297 | 16,443 | 938 | 37,656 | 17.77M | 74,146 | 3,302 | 0.689 | 26* |
| 08087 | Morgan | rural | 13,360 | 11,879 | 1,048 | 109,801 | 11.77M | 79,798 | 42,924 | 0.758 | 36 |
| 08089 | Otero | rural | 7,033 | 6,669 | 599 | 29,129 | 8.79M | 52,914 | 8,611 | 0.673 | 26* |
| 08091 | Ouray | rural | 2,167 | 1,935 | 70 | 2,291 | 1.98M | 116,438 | 17,510 | 0.831 | 26* |
| 08093 | Park | suburb | 8,580 | 4,719 | 148 | 194 | 3.78M | 44,172 | -6,043 | 0.614 | 26* |
| 08095 | Phillips | rural | 2,055 | 1,683 | 337 | 141,307 | 2.67M | 84,123 | 8,429 | 0.445 | 46 |
| 08097 | Pitkin | rural | 10,314 | 18,214 | 80 | 1,695 | 6.42M | 65,118 | -14,164 | 0.933 | 26* |
| 08099 | Prowers | rural | 5,353 | 4,446 | 578 | 170,248 | 6.52M | 77,821 | 17,216 | 0.656 | 26* |
| 08101 | Pueblo | suburb | 69,850 | 67,792 | 892 | 15,437 | 73.09M | 44,697 | 666 | 0.715 | 26* |
| 08103 | Rio Blanco | rural | 2,852 | 2,928 | 311 | 12,618 | 3.27M | 45,674 | 1,798 | 0.640 | 26* |
| 08105 | Rio Grande | rural | 4,989 | 4,573 | 434 | 36,865 | 6.59M | 90,375 | 31,330 | 0.716 | 26* |
| 08107 | Routt | rural | 13,686 | 14,369 | 538 | 14,139 | 10.59M | 62,797 | -215 | 0.661 | 26* |
| 08109 | Saguache | rural | 2,660 | 2,110 | 371 | 31,862 | 3.17M | 83,435 | 12,291 | 0.706 | 26* |
| 08111 | San Juan | rural | 372 | 543 | 0 | 49 | 0.19M | 0 | n/a | 0.673 | 26* |
| 08113 | San Miguel | rural | 4,897 | 6,209 | 112 | 6,445 | 1.71M | 44,503 | -2,293 | 0.737 | 26* |
| 08115 | Sedgwick | rural | 1,062 | 776 | 287 | 85,132 | 1.42M | 65,325 | -2,737 | 0.470 | 44 |
| 08117 | Summit | rural | 18,644 | 21,607 | 52 | 36 | 8.09M | 50,058 | -11,587 | 0.834 | 26* |
| 08119 | Teller | suburb | 11,249 | 8,479 | 97 | 150 | 6.05M | 35,542 | -14,500 | 0.479 | 26* |
| 08121 | Washington | rural | 2,247 | 1,132 | 592 | 336,944 | 3.08M | 89,634 | 8,491 | 0.611 | 36 |
| 08123 | Weld | suburb | 166,155 | 128,393 | 4,657 | 289,446 | 91.48M | 80,386 | 64,421 | 0.699 | 28 |
| 08125 | Yuma | rural | 4,617 | 3,709 | 965 | 235,713 | 6.12M | 98,674 | 2,701 | 0.511 | 44 |
| EXT | External (out-of-state commuting) | external | 24,505 | 28,042 | 320 | 33,999 | 15.93M | 68,032 | n/a | 0.673 | n/a |

`*` filled, see above.
