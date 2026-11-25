# Indiana 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state IN 2022`. 92 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 18 | `IN/CDL_2022_18.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=18 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_IN.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 6,833,037 | 6,833,037 | 0.000% |
| ACS workers by residence | 3,222,821 | 3,222,821 | 0.000% |
| ACS workers by workplace | 3,169,941 | 3,169,941 | 0.000% |
| ACS workers working out of state | 168,247 | 168,247 | 0.000% |
| BEA non-farm employment (L80) | 4,083,338 | 4,083,338 | 0.000% |
| BEA farm employment (L70) | 57,327 | 57,327 | 0.000% |
| BEA farm proprietors (L50) | 47,575 | 47,575 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 4,285,150,000 | 4,285,150,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 449,507,000 | 449,507,000 | 0.000% |
| CoA hired farm labour expense $ | 741,451,000 | 741,445,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 273,540,840,000 | 273,540,840,000 | 0.000% |
| ACS foreign born entered 2010+ | 140,196 | 140,196 | 0.000% |
| CoA owned acres | 6,974,236 | 6,974,236 | 0.000% |
| CoA rented-from-others acres | 7,628,004 | 7,628,004 | 0.000% |
| CoA land in farms, ha | 5,909,317 | 5,909,317 | -0.000% |
| CoA total cropland, ha | 5,071,414 | 5,071,414 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.635, median 0.786, max 0.941; BEA counts jobs, ACS counts people by main job). Sum N = 3,338,188 = sum HU + HA = 3,338,188. Farm jobs after scaling: 44,338 (BEA 57,327). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 115,367. Jobs = in-state residents working out of state = 168,247, split by the state farm share (HA = 2,353). Location: the 41 out-of-state counties within 1 km of the state (17023, 17031, 17033, 17045, 17047, 17059, 17075, 17091, 17101, 17183, 17185, 17193, 17197, 21015, 21027, 21029, 21041, 21059, 21077, 21091, 21093, 21101, 21111, 21163, 21185, 21223, 21225, 26021, 26023, 26027, 26059, 26149, 39017, 39037, 39039, 39061, 39107, 39125, 39135, 39161, 39171); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 4,757,668 ha vs Census of Agriculture cropland 5,071,414 ha and land in farms 5,909,317 ha; county ratio TF / CoA cropland 0.43 to 1.31. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 924,226 ha). County area covered by CDL pixels: 9,372,424 ha vs land area 9,278,861 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 8.15 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (66,990 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 39,531 $ per BEA farm job, 51,112 $ per farm worker; county range 27,878 to 106,677 $ per worker. State compensation per farm wage job by year: 2018 35,376 $, 2019 36,198 $, 2020 35,939 $, 2021 35,591 $, 2022 46,094 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 82,420,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (741,445,000 $ in 2022, column `hired_labor_coa_usd`) is 1.65x BEA farm compensation (449,507,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 74,749 $, county -497 to 298,555 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 87,516 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 4,527,959,000 $ vs CAINC45 4,285,150,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.478, county range 0.250 to 0.828.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 209 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 8,259 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 2 counties have no recent foreign born in the ACS sample (Crawford, Pike), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Marion); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (43); rural = the rest (48). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 169.4 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 57.9 straight-line km/h between counties (median 8.1 to 22.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.24).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 18001 Adams | not published; NASS 'other (combined) counties' value = 205 $/acre |
| cash_rent_usd_acre | 18043 Floyd | not published; NASS 'other (combined) counties' value = 205 $/acre |
| cash_rent_usd_acre | 18051 Gibson | not published; NASS 'other (combined) counties' value = 205 $/acre |

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
| 18001 | Adams | rural | 15,265 | 13,812 | 975 | 65,031 | 16.85M | 51,636 | 90,927 | 0.467 | 205* |
| 18003 | Allen | suburb | 186,470 | 195,010 | 1,159 | 82,168 | 147.28M | 47,216 | 42,124 | 0.397 | 190 |
| 18005 | Bartholomew | suburb | 40,397 | 48,977 | 435 | 51,123 | 31.27M | 55,764 | 74,964 | 0.432 | 195 |
| 18007 | Benton | suburb | 3,944 | 2,107 | 296 | 95,632 | 5.09M | 75,745 | 158,159 | 0.348 | 265 |
| 18009 | Blackford | rural | 4,852 | 2,981 | 190 | 31,959 | 5.70M | 57,895 | 75,252 | 0.354 | 220 |
| 18011 | Boone | suburb | 36,583 | 35,603 | 405 | 80,022 | 27.24M | 68,591 | 54,034 | 0.356 | 253 |
| 18013 | Brown | suburb | 7,134 | 3,566 | 98 | 1,903 | 3.47M | 75,959 | -497 | 0.761 | 127 |
| 18015 | Carroll | suburb | 9,486 | 5,295 | 353 | 72,699 | 7.48M | 48,613 | 113,401 | 0.462 | 250 |
| 18017 | Cass | rural | 17,896 | 15,210 | 545 | 75,145 | 15.69M | 53,727 | 74,693 | 0.479 | 234 |
| 18019 | Clark | suburb | 61,188 | 55,144 | 356 | 18,373 | 50.67M | 50,856 | 40,417 | 0.554 | 149 |
| 18021 | Clay | suburb | 11,606 | 6,772 | 353 | 48,988 | 9.75M | 48,503 | 50,111 | 0.398 | 199 |
| 18023 | Clinton | rural | 15,322 | 11,615 | 503 | 86,510 | 12.72M | 59,065 | 90,525 | 0.372 | 247 |
| 18025 | Crawford | rural | 4,279 | 2,655 | 275 | 4,554 | 3.59M | 30,535 | 2,958 | 0.828 | 78 |
| 18027 | Daviess | rural | 14,983 | 11,664 | 836 | 65,158 | 15.23M | 57,313 | 149,068 | 0.506 | 232 |
| 18029 | Dearborn | suburb | 25,312 | 15,465 | 367 | 7,051 | 14.57M | 51,285 | 704 | 0.821 | 135 |
| 18031 | Decatur | rural | 13,135 | 14,603 | 519 | 63,195 | 14.52M | 52,688 | 64,213 | 0.532 | 213 |
| 18033 | DeKalb | rural | 21,137 | 22,288 | 652 | 52,774 | 20.97M | 42,790 | 32,762 | 0.550 | 152 |
| 18035 | Delaware | suburb | 51,601 | 50,483 | 511 | 64,189 | 40.27M | 41,742 | 40,384 | 0.396 | 215 |
| 18037 | Dubois | rural | 22,578 | 28,094 | 648 | 40,810 | 22.72M | 53,549 | 145,739 | 0.623 | 177 |
| 18039 | Elkhart | suburb | 97,136 | 126,732 | 1,190 | 51,471 | 104.13M | 42,123 | 124,483 | 0.554 | 170 |
| 18041 | Fayette | rural | 10,093 | 6,938 | 260 | 29,200 | 9.36M | 40,324 | 37,123 | 0.451 | 193 |
| 18043 | Floyd | suburb | 38,923 | 32,554 | 173 | 2,491 | 25.91M | 50,439 | 269 | 0.693 | 205* |
| 18045 | Fountain | rural | 7,531 | 4,918 | 311 | 69,123 | 6.50M | 52,312 | 88,700 | 0.382 | 255 |
| 18047 | Franklin | suburb | 11,370 | 5,902 | 496 | 29,482 | 8.46M | 52,311 | 34,362 | 0.647 | 157 |
| 18049 | Fulton | rural | 8,674 | 6,073 | 431 | 69,693 | 8.55M | 53,069 | 76,629 | 0.500 | 204 |
| 18051 | Gibson | rural | 15,614 | 22,762 | 567 | 80,949 | 12.78M | 59,972 | 84,979 | 0.420 | 205* |
| 18053 | Grant | rural | 28,661 | 28,518 | 376 | 75,287 | 29.69M | 54,749 | 86,709 | 0.497 | 201 |
| 18055 | Greene | rural | 13,253 | 7,402 | 612 | 42,414 | 9.73M | 37,014 | 63,121 | 0.507 | 185 |
| 18057 | Hamilton | suburb | 184,368 | 161,287 | 427 | 46,773 | 127.59M | 42,011 | 56,880 | 0.444 | 245 |
| 18059 | Hancock | suburb | 41,586 | 30,969 | 462 | 53,655 | 24.73M | 44,589 | 45,282 | 0.312 | 245 |
| 18061 | Harrison | suburb | 18,035 | 11,430 | 666 | 23,013 | 12.20M | 43,498 | 33,707 | 0.616 | 120 |
| 18063 | Hendricks | suburb | 91,969 | 81,904 | 494 | 56,837 | 61.59M | 58,320 | 35,016 | 0.386 | 231 |
| 18065 | Henry | rural | 20,169 | 14,162 | 544 | 68,138 | 16.73M | 51,583 | 52,975 | 0.401 | 210 |
| 18067 | Howard | suburb | 36,245 | 39,237 | 378 | 53,659 | 37.08M | 59,209 | 66,718 | 0.437 | 220 |
| 18069 | Huntington | rural | 17,611 | 14,333 | 514 | 67,261 | 17.58M | 48,126 | 73,540 | 0.441 | 197 |
| 18071 | Jackson | rural | 22,017 | 22,801 | 649 | 54,556 | 18.58M | 56,736 | 73,021 | 0.561 | 175 |
| 18073 | Jasper | suburb | 14,923 | 11,336 | 611 | 109,482 | 14.44M | 66,619 | 165,470 | 0.359 | 215 |
| 18075 | Jay | rural | 8,776 | 7,365 | 694 | 74,094 | 10.31M | 28,620 | 298,555 | 0.617 | 200 |
| 18077 | Jefferson | rural | 14,833 | 13,747 | 465 | 22,679 | 12.40M | 32,393 | 2,390 | 0.741 | 150 |
| 18079 | Jennings | rural | 12,758 | 8,611 | 421 | 34,539 | 9.59M | 55,362 | 56,303 | 0.554 | 193 |
| 18081 | Johnson | suburb | 81,130 | 63,116 | 404 | 38,952 | 50.19M | 49,760 | 21,300 | 0.313 | 212 |
| 18083 | Knox | rural | 17,699 | 18,514 | 520 | 95,519 | 15.05M | 44,468 | 140,038 | 0.422 | 225 |
| 18085 | Kosciusko | rural | 39,179 | 39,346 | 1,074 | 82,610 | 30.68M | 59,060 | 120,682 | 0.422 | 190 |
| 18087 | LaGrange | rural | 17,471 | 15,521 | 1,487 | 45,202 | 16.84M | 62,307 | 85,898 | 0.702 | 163 |
| 18089 | Lake | suburb | 221,831 | 201,237 | 315 | 45,187 | 231.35M | 49,364 | 47,667 | 0.400 | 193 |
| 18091 | LaPorte | suburb | 48,913 | 40,949 | 606 | 88,333 | 40.73M | 63,018 | 79,927 | 0.464 | 178 |
| 18093 | Lawrence | rural | 21,016 | 15,685 | 572 | 19,063 | 17.67M | 50,432 | 21,622 | 0.705 | 143 |
| 18095 | Madison | suburb | 58,438 | 44,647 | 611 | 76,901 | 48.58M | 50,389 | 41,208 | 0.377 | 226 |
| 18097 | Marion | core | 474,526 | 585,664 | 215 | 6,022 | 429.57M | 48,127 | 25,306 | 0.427 | 179 |
| 18099 | Marshall | rural | 21,335 | 19,889 | 710 | 71,732 | 18.25M | 46,530 | 86,258 | 0.468 | 177 |
| 18101 | Martin | rural | 4,688 | 7,836 | 215 | 13,523 | 5.21M | 31,447 | 124,019 | 0.682 | 176 |
| 18103 | Miami | rural | 15,136 | 10,250 | 554 | 66,509 | 14.43M | 33,962 | 88,605 | 0.446 | 188 |
| 18105 | Monroe | suburb | 68,299 | 76,018 | 327 | 5,408 | 43.21M | 37,394 | 1,332 | 0.798 | 112 |
| 18107 | Montgomery | rural | 17,939 | 16,895 | 598 | 96,664 | 17.32M | 53,068 | 79,446 | 0.506 | 260 |
| 18109 | Morgan | suburb | 34,416 | 19,791 | 459 | 34,949 | 18.52M | 42,314 | 40,622 | 0.488 | 193 |
| 18111 | Newton | suburb | 5,738 | 2,898 | 309 | 75,837 | 5.47M | 106,677 | 155,845 | 0.356 | 223 |
| 18113 | Noble | rural | 22,483 | 18,456 | 923 | 56,363 | 16.67M | 56,614 | 66,569 | 0.603 | 170 |
| 18115 | Ohio | suburb | 2,741 | 1,262 | 117 | 2,232 | 1.92M | 73,481 | 2,974 | 0.708 | 105 |
| 18117 | Orange | rural | 9,211 | 7,607 | 370 | 19,343 | 7.78M | 55,691 | 84,932 | 0.730 | 181 |
| 18119 | Owen | suburb | 9,810 | 5,914 | 365 | 19,429 | 5.47M | 27,878 | 19,202 | 0.673 | 170 |
| 18121 | Parke | rural | 6,270 | 3,664 | 364 | 50,553 | 5.66M | 53,408 | 45,588 | 0.528 | 208 |
| 18123 | Perry | rural | 8,372 | 6,907 | 327 | 10,137 | 7.92M | 30,247 | 57,647 | 0.739 | 92 |
| 18125 | Pike | rural | 5,430 | 2,953 | 226 | 29,653 | 4.03M | 33,310 | 64,111 | 0.558 | 170 |
| 18127 | Porter | suburb | 81,856 | 69,030 | 359 | 49,267 | 65.62M | 46,928 | 50,400 | 0.499 | 186 |
| 18129 | Posey | suburb | 12,131 | 9,547 | 383 | 67,483 | 13.43M | 34,797 | 104,557 | 0.250 | 211 |
| 18131 | Pulaski | rural | 5,849 | 4,529 | 467 | 84,781 | 6.00M | 75,619 | 111,690 | 0.387 | 215 |
| 18133 | Putnam | rural | 15,990 | 13,148 | 596 | 56,193 | 10.27M | 44,385 | 27,120 | 0.485 | 210 |
| 18135 | Randolph | rural | 10,613 | 7,309 | 529 | 91,019 | 11.20M | 83,652 | 90,196 | 0.526 | 198 |
| 18137 | Ripley | rural | 14,452 | 12,525 | 713 | 40,728 | 12.00M | 40,212 | 34,288 | 0.555 | 168 |
| 18139 | Rush | rural | 7,343 | 5,286 | 452 | 85,029 | 8.70M | 56,282 | 85,547 | 0.505 | 227 |
| 18141 | St. Joseph | suburb | 128,488 | 129,616 | 539 | 54,073 | 99.63M | 54,637 | 49,642 | 0.497 | 173 |
| 18143 | Scott | rural | 10,567 | 8,883 | 251 | 12,965 | 8.24M | 43,382 | 11,761 | 0.570 | 140 |
| 18145 | Shelby | suburb | 21,541 | 19,336 | 456 | 79,141 | 18.01M | 59,559 | 81,032 | 0.435 | 215 |
| 18147 | Spencer | rural | 9,652 | 6,990 | 432 | 48,580 | 10.77M | 59,187 | 71,030 | 0.568 | 158 |
| 18149 | Starke | rural | 9,336 | 4,645 | 344 | 43,712 | 7.01M | 47,454 | 61,047 | 0.556 | 155 |
| 18151 | Steuben | rural | 16,098 | 15,501 | 354 | 33,424 | 13.91M | 42,027 | 32,886 | 0.488 | 156 |
| 18153 | Sullivan | suburb | 8,694 | 6,553 | 373 | 58,696 | 7.57M | 48,005 | 73,564 | 0.453 | 190 |
| 18155 | Switzerland | rural | 4,361 | 2,025 | 249 | 5,366 | 3.43M | 55,345 | 6,994 | 0.803 | 123 |
| 18157 | Tippecanoe | suburb | 88,935 | 101,876 | 614 | 79,748 | 62.91M | 51,054 | 47,571 | 0.382 | 222 |
| 18159 | Tipton | suburb | 7,268 | 6,084 | 360 | 58,034 | 7.26M | 57,692 | 83,628 | 0.493 | 274 |
| 18161 | Union | rural | 3,533 | 1,442 | 144 | 25,798 | 2.92M | 34,270 | 57,888 | 0.557 | 208 |
| 18163 | Vanderburgh | suburb | 87,736 | 104,842 | 192 | 23,319 | 80.87M | 42,996 | 49,203 | 0.396 | 206 |
| 18165 | Vermillion | suburb | 6,710 | 4,466 | 214 | 35,721 | 7.25M | 44,090 | 42,774 | 0.470 | 232 |
| 18167 | Vigo | suburb | 47,887 | 55,341 | 427 | 42,996 | 44.09M | 33,785 | 37,844 | 0.476 | 179 |
| 18169 | Wabash | rural | 14,096 | 12,866 | 609 | 71,420 | 16.53M | 58,499 | 56,720 | 0.511 | 196 |
| 18171 | Warren | suburb | 3,978 | 2,268 | 336 | 68,359 | 3.43M | 58,394 | 128,058 | 0.413 | 247 |
| 18173 | Warrick | suburb | 31,207 | 21,876 | 287 | 31,502 | 23.52M | 44,665 | 38,542 | 0.436 | 165 |
| 18175 | Washington | suburb | 12,768 | 6,759 | 557 | 40,837 | 9.75M | 55,287 | 134,522 | 0.669 | 142 |
| 18177 | Wayne | rural | 29,789 | 31,645 | 608 | 57,033 | 27.93M | 55,022 | 56,796 | 0.547 | 188 |
| 18179 | Wells | suburb | 14,158 | 11,463 | 523 | 75,682 | 12.27M | 39,901 | 86,240 | 0.364 | 236 |
| 18181 | White | rural | 11,067 | 10,224 | 564 | 109,042 | 11.66M | 65,917 | 100,589 | 0.349 | 235 |
| 18183 | Whitley | suburb | 16,934 | 14,187 | 518 | 55,514 | 15.73M | 36,808 | 56,718 | 0.548 | 177 |
| EXT | External (out-of-state commuting) | external | 115,367 | 165,894 | 2,353 | 252,517 | 97.28M | 51,112 | n/a | 0.478 | n/a |

`*` filled, see above.
