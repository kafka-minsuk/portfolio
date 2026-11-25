# Minnesota 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state MN 2022`. 87 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 27 | `MN/CDL_2022_27.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=27 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MN.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 5,717,184 | 5,717,184 | 0.000% |
| ACS workers by residence | 2,934,581 | 2,934,581 | 0.000% |
| ACS workers by workplace | 2,947,205 | 2,947,205 | 0.000% |
| ACS workers working out of state | 67,136 | 67,136 | 0.000% |
| BEA non-farm employment (L80) | 3,767,500 | 3,767,500 | 0.000% |
| BEA farm employment (L70) | 77,286 | 77,286 | 0.000% |
| BEA farm proprietors (L50) | 57,947 | 57,947 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 5,745,694,000 | 5,745,694,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 823,486,000 | 823,486,000 | 0.000% |
| CoA hired farm labour expense $ | 1,320,774,000 | 1,320,974,000 | -0.015% |
| BEA non-farm earnings $ (CAINC5N L82) | 275,212,413,000 | 275,212,413,000 | 0.000% |
| ACS foreign born entered 2010+ | 158,524 | 158,524 | 0.000% |
| CoA owned acres | 13,004,109 | 13,006,137 | -0.016% |
| CoA rented-from-others acres | 12,436,295 | 12,436,488 | -0.002% |
| CoA land in farms, ha | 10,296,265 | 10,296,265 | -0.000% |
| CoA total cropland, ha | 8,718,572 | 8,718,572 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.596, median 0.762, max 0.895; BEA counts jobs, ACS counts people by main job). Sum N = 3,014,341 = sum HU + HA = 3,014,341. Farm jobs after scaling: 58,024 (BEA 77,286). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 79,760. Jobs = in-state residents working out of state = 67,136, split by the state farm share (HA = 1,322). Location: the 33 out-of-state counties within 1 km of the state (19005, 19059, 19063, 19089, 19109, 19119, 19131, 19143, 19189, 19191, 19195, 38017, 38035, 38067, 38077, 38097, 38099, 46011, 46039, 46051, 46099, 46101, 46109, 55011, 55013, 55031, 55063, 55091, 55093, 55095, 55109, 55121, 55123); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 8,271,815 ha vs Census of Agriculture cropland 8,718,572 ha and land in farms 10,296,265 ha; county ratio TF / CoA cropland 0.10 to 1.57. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,104,035 ha). County area covered by CDL pixels: 21,856,110 ha vs land area 20,624,484 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 6.01 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (73,049 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 44,719 $ per BEA farm job, 59,564 $ per farm worker; county range 28,404 to 122,881 $ per worker. State compensation per farm wage job by year: 2018 43,617 $, 2019 42,645 $, 2020 41,751 $, 2021 40,328 $, 2022 42,582 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 152,565,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,320,974,000 $ in 2022, column `hired_labor_coa_usd`) is 1.60x BEA farm compensation (823,486,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 74,343 $, county -3,970 to 194,281 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 95,256 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 6,806,821,000 $ vs CAINC45 5,745,694,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.511, county range 0.349 to 0.935.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 185 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 6,107 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Hennepin); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (26); rural = the rest (60). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Cook); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 222.7 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 61.0 straight-line km/h between counties (median 10.2 to 65.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.22).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 27031 Cook | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 27075 Lake | state owner share |
| omega | 27123 Ramsey | state owner share |
| cash_rent_usd_acre | 27013 Blue Earth | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27015 Brown | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27031 Cook | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27043 Faribault | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27075 Lake | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27089 Marshall | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27099 Mower | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27103 Nicollet | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27123 Ramsey | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27127 Redwood | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27137 St. Louis | not published; NASS 'other (combined) counties' value = 203 $/acre |
| cash_rent_usd_acre | 27143 Sibley | not published; NASS 'other (combined) counties' value = 203 $/acre |
| owned_acres | 27075 Lake | (D) in Census of Ag; see fills above |
| owned_acres | 27123 Ramsey | (D) in Census of Ag; see fills above |
| rented_acres | 27075 Lake | (D) in Census of Ag; see fills above |
| rented_acres | 27123 Ramsey | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 27031 Cook | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 27075 Lake | (D) in Census of Ag; left null (comparison column only) |

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
| 27001 | Aitkin | rural | 5,940 | 4,847 | 323 | 13,967 | 7.54M | 34,174 | -138 | 0.742 | 20 |
| 27003 | Anoka | suburb | 190,371 | 141,059 | 442 | 7,899 | 106.36M | 62,202 | 36,305 | 0.648 | 65 |
| 27005 | Becker | rural | 16,252 | 14,568 | 942 | 98,149 | 13.61M | 55,015 | 58,360 | 0.621 | 133 |
| 27007 | Beltrami | rural | 21,007 | 20,582 | 380 | 42,974 | 14.62M | 37,657 | 23,509 | 0.752 | 41 |
| 27009 | Benton | suburb | 22,016 | 15,856 | 666 | 52,752 | 14.79M | 67,567 | 58,471 | 0.694 | 101 |
| 27011 | Big Stone | rural | 2,256 | 1,834 | 290 | 92,968 | 2.84M | 64,467 | 145,323 | 0.489 | 164 |
| 27013 | Blue Earth | suburb | 37,318 | 40,436 | 896 | 145,021 | 25.45M | 56,722 | 115,537 | 0.383 | 203* |
| 27015 | Brown | rural | 13,314 | 14,272 | 941 | 124,886 | 15.13M | 50,173 | 102,860 | 0.506 | 203* |
| 27017 | Carlton | suburb | 16,454 | 13,161 | 307 | 2,645 | 10.35M | 48,471 | -3,970 | 0.854 | 18 |
| 27019 | Carver | suburb | 58,029 | 47,700 | 670 | 47,343 | 27.23M | 46,409 | 37,862 | 0.533 | 216 |
| 27021 | Cass | rural | 12,703 | 11,090 | 338 | 18,644 | 11.42M | 48,976 | 18,331 | 0.722 | 28 |
| 27023 | Chippewa | rural | 5,806 | 5,360 | 552 | 121,145 | 6.35M | 82,078 | 92,072 | 0.354 | 224 |
| 27025 | Chisago | suburb | 29,403 | 18,616 | 615 | 27,348 | 14.40M | 54,313 | 23,052 | 0.638 | 71 |
| 27027 | Clay | suburb | 33,554 | 21,902 | 654 | 197,389 | 19.60M | 116,156 | 110,305 | 0.383 | 151 |
| 27029 | Clearwater | rural | 3,576 | 2,801 | 319 | 43,862 | 3.51M | 66,651 | 29,984 | 0.700 | 48 |
| 27031 | Cook | rural | 2,758 | 2,875 | 0 | 36 | 1.88M | 0 | n/a | 0.935 | 203* |
| 27033 | Cottonwood | rural | 5,231 | 5,263 | 549 | 136,094 | 6.72M | 70,155 | 152,897 | 0.455 | 228 |
| 27035 | Crow Wing | rural | 30,545 | 31,649 | 380 | 14,661 | 20.82M | 31,793 | 9,582 | 0.716 | 36 |
| 27037 | Dakota | suburb | 235,955 | 201,231 | 820 | 66,267 | 151.77M | 65,491 | 60,365 | 0.578 | 210 |
| 27039 | Dodge | suburb | 11,295 | 6,043 | 521 | 91,744 | 9.08M | 77,978 | 69,336 | 0.404 | 268 |
| 27041 | Douglas | rural | 19,442 | 20,184 | 722 | 79,958 | 13.81M | 39,349 | 48,649 | 0.616 | 137 |
| 27043 | Faribault | rural | 6,728 | 4,958 | 608 | 160,183 | 7.76M | 66,306 | 125,936 | 0.383 | 203* |
| 27045 | Fillmore | suburb | 10,541 | 6,364 | 1,016 | 126,805 | 11.83M | 60,746 | 50,806 | 0.558 | 214 |
| 27047 | Freeborn | rural | 14,440 | 12,694 | 883 | 146,078 | 12.46M | 59,731 | 87,568 | 0.431 | 244 |
| 27049 | Goodhue | rural | 23,597 | 21,509 | 1,281 | 116,181 | 19.32M | 67,369 | 68,949 | 0.529 | 223 |
| 27051 | Grant | rural | 2,864 | 1,872 | 359 | 105,746 | 2.91M | 90,658 | 122,090 | 0.437 | 186 |
| 27053 | Hennepin | core | 690,929 | 886,288 | 624 | 13,534 | 444.06M | 38,677 | 17,174 | 0.694 | 155 |
| 27055 | Houston | suburb | 9,853 | 5,228 | 631 | 39,480 | 9.06M | 53,848 | 39,186 | 0.715 | 207 |
| 27057 | Hubbard | rural | 9,402 | 6,696 | 281 | 19,184 | 8.10M | 63,045 | 32,102 | 0.588 | 20 |
| 27059 | Isanti | suburb | 20,699 | 12,970 | 597 | 33,227 | 11.60M | 43,405 | 3,620 | 0.613 | 65 |
| 27061 | Itasca | rural | 18,780 | 16,933 | 278 | 5,387 | 16.15M | 37,867 | -742 | 0.740 | 18 |
| 27063 | Jackson | rural | 5,193 | 4,556 | 547 | 151,708 | 6.99M | 72,525 | 125,491 | 0.450 | 231 |
| 27065 | Kanabec | rural | 7,466 | 4,432 | 406 | 19,838 | 5.65M | 42,681 | 15,761 | 0.697 | 62 |
| 27067 | Kandiyohi | rural | 21,810 | 21,865 | 1,197 | 131,379 | 18.13M | 58,252 | 68,329 | 0.455 | 218 |
| 27069 | Kittson | rural | 2,030 | 1,440 | 359 | 151,519 | 2.30M | 92,361 | 109,428 | 0.541 | 82 |
| 27071 | Koochiching | rural | 5,539 | 5,292 | 139 | 7,882 | 4.86M | 122,881 | 10,058 | 0.758 | 22 |
| 27073 | Lac qui Parle | rural | 3,142 | 2,196 | 532 | 147,424 | 5.08M | 74,779 | 112,398 | 0.464 | 181 |
| 27075 | Lake | rural | 4,850 | 4,918 | 30 | 63 | 4.00M | 60,732 | 29 | 0.511 | 203* |
| 27077 | Lake of the Woods | rural | 1,912 | 1,592 | 110 | 23,806 | 1.55M | 85,105 | 41,950 | 0.617 | 21 |
| 27079 | Le Sueur | suburb | 15,133 | 9,039 | 713 | 73,341 | 10.10M | 60,131 | 60,579 | 0.503 | 223 |
| 27081 | Lincoln | rural | 2,761 | 1,476 | 429 | 97,178 | 4.02M | 62,420 | 89,361 | 0.535 | 207 |
| 27083 | Lyon | rural | 12,595 | 13,875 | 724 | 143,571 | 13.62M | 52,163 | 145,647 | 0.396 | 232 |
| 27085 | McLeod | rural | 18,781 | 17,112 | 755 | 95,694 | 16.45M | 62,324 | 39,581 | 0.483 | 239 |
| 27087 | Mahnomen | rural | 1,963 | 1,978 | 238 | 66,018 | 2.18M | 72,314 | 102,022 | 0.560 | 136 |
| 27089 | Marshall | rural | 4,245 | 2,322 | 700 | 279,188 | 4.28M | 106,917 | 107,346 | 0.526 | 203* |
| 27091 | Martin | rural | 9,657 | 8,947 | 778 | 157,615 | 11.17M | 66,118 | 146,631 | 0.360 | 265 |
| 27093 | Meeker | rural | 11,624 | 7,612 | 800 | 104,899 | 10.83M | 78,287 | 59,984 | 0.533 | 213 |
| 27095 | Mille Lacs | suburb | 12,727 | 9,943 | 539 | 26,909 | 8.38M | 28,404 | 8,583 | 0.646 | 76 |
| 27097 | Morrison | rural | 16,347 | 11,617 | 1,567 | 91,155 | 15.34M | 43,163 | 72,085 | 0.762 | 74 |
| 27099 | Mower | rural | 19,181 | 16,211 | 882 | 153,342 | 15.72M | 56,142 | 108,532 | 0.403 | 203* |
| 27101 | Murray | rural | 3,979 | 2,570 | 529 | 146,552 | 6.10M | 67,527 | 116,166 | 0.476 | 223 |
| 27103 | Nicollet | suburb | 18,663 | 17,809 | 782 | 87,601 | 13.47M | 62,370 | 84,997 | 0.384 | 203* |
| 27105 | Nobles | rural | 10,420 | 9,912 | 800 | 158,869 | 10.99M | 62,011 | 123,463 | 0.421 | 232 |
| 27107 | Norman | rural | 3,046 | 1,773 | 480 | 185,230 | 3.09M | 77,454 | 105,795 | 0.375 | 132 |
| 27109 | Olmsted | suburb | 85,332 | 100,750 | 983 | 91,835 | 54.14M | 56,067 | 56,700 | 0.517 | 225 |
| 27111 | Otter Tail | rural | 27,776 | 22,656 | 2,076 | 220,244 | 25.71M | 62,326 | 50,583 | 0.638 | 105 |
| 27113 | Pennington | rural | 7,317 | 9,200 | 341 | 115,757 | 5.65M | 55,410 | 105,551 | 0.518 | 74 |
| 27115 | Pine | rural | 12,619 | 9,137 | 711 | 26,652 | 9.55M | 40,264 | 10,969 | 0.751 | 54 |
| 27117 | Pipestone | rural | 4,368 | 4,041 | 493 | 91,730 | 6.35M | 80,331 | 145,502 | 0.507 | 200 |
| 27119 | Polk | suburb | 14,969 | 11,694 | 1,144 | 374,775 | 13.83M | 88,615 | 95,737 | 0.432 | 124 |
| 27121 | Pope | rural | 5,730 | 4,268 | 605 | 102,854 | 5.61M | 70,065 | 69,119 | 0.529 | 157 |
| 27123 | Ramsey | suburb | 277,111 | 326,149 | 49 | 120 | 179.35M | 72,301 | 16,444 | 0.511 | 203* |
| 27125 | Red Lake | rural | 1,945 | 1,050 | 222 | 85,676 | 1.76M | 58,894 | 182,000 | 0.586 | 71 |
| 27127 | Redwood | rural | 7,246 | 6,446 | 886 | 190,660 | 9.52M | 45,095 | 124,713 | 0.392 | 203* |
| 27129 | Renville | rural | 7,014 | 5,058 | 917 | 216,161 | 10.17M | 73,407 | 126,149 | 0.374 | 247 |
| 27131 | Rice | rural | 32,398 | 28,802 | 1,063 | 73,381 | 22.10M | 47,772 | 46,577 | 0.533 | 241 |
| 27133 | Rock | suburb | 4,914 | 3,542 | 457 | 103,806 | 6.48M | 76,426 | 167,459 | 0.461 | 245 |
| 27135 | Roseau | rural | 7,760 | 7,538 | 671 | 180,765 | 6.06M | 62,121 | 78,179 | 0.608 | 64 |
| 27137 | St. Louis | suburb | 95,204 | 102,812 | 519 | 3,360 | 64.46M | 46,617 | 5,399 | 0.794 | 203* |
| 27139 | Scott | suburb | 83,336 | 65,703 | 640 | 33,817 | 45.21M | 50,773 | 35,860 | 0.450 | 212 |
| 27141 | Sherburne | suburb | 52,791 | 31,000 | 427 | 28,662 | 22.09M | 62,553 | 32,832 | 0.620 | 50 |
| 27143 | Sibley | rural | 7,742 | 4,251 | 791 | 124,121 | 8.00M | 62,938 | 83,992 | 0.474 | 203* |
| 27145 | Stearns | suburb | 82,627 | 92,489 | 3,446 | 193,489 | 59.60M | 36,239 | 54,982 | 0.688 | 147 |
| 27147 | Steele | rural | 18,758 | 21,263 | 771 | 84,473 | 16.31M | 45,947 | 92,265 | 0.519 | 242 |
| 27149 | Stevens | rural | 4,965 | 5,430 | 644 | 115,869 | 4.80M | 67,018 | 154,594 | 0.349 | 173 |
| 27151 | Swift | rural | 4,576 | 3,490 | 609 | 145,759 | 5.73M | 60,177 | 115,443 | 0.546 | 214 |
| 27153 | Todd | rural | 11,052 | 6,686 | 1,249 | 89,578 | 11.50M | 53,802 | 32,991 | 0.719 | 88 |
| 27155 | Traverse | rural | 1,569 | 1,128 | 335 | 126,380 | 2.57M | 80,697 | 194,281 | 0.385 | 186 |
| 27157 | Wabasha | suburb | 11,055 | 7,325 | 810 | 68,938 | 10.02M | 52,096 | 61,086 | 0.645 | 259 |
| 27159 | Wadena | rural | 6,104 | 6,646 | 546 | 30,390 | 5.92M | 31,217 | 31,868 | 0.699 | 32 |
| 27161 | Waseca | rural | 9,427 | 5,852 | 596 | 87,459 | 8.24M | 56,695 | 106,744 | 0.479 | 247 |
| 27163 | Washington | suburb | 139,002 | 112,123 | 556 | 17,243 | 76.05M | 101,960 | 42,178 | 0.567 | 153 |
| 27165 | Watonwan | rural | 5,196 | 4,075 | 333 | 96,538 | 5.96M | 66,088 | 146,775 | 0.401 | 238 |
| 27167 | Wilkin | rural | 3,139 | 1,654 | 317 | 165,887 | 3.54M | 95,204 | 138,072 | 0.403 | 135 |
| 27169 | Winona | rural | 27,040 | 25,887 | 1,179 | 60,111 | 20.36M | 47,455 | 48,467 | 0.631 | 226 |
| 27171 | Wright | suburb | 75,733 | 52,263 | 1,157 | 77,868 | 34.58M | 63,428 | 29,761 | 0.495 | 185 |
| 27173 | Yellow Medicine | rural | 4,644 | 3,445 | 560 | 155,120 | 6.86M | 61,418 | 94,016 | 0.472 | 199 |
| EXT | External (out-of-state commuting) | external | 79,760 | 65,814 | 1,322 | 188,428 | 54.44M | 59,564 | n/a | 0.511 | n/a |

`*` filled, see above.
