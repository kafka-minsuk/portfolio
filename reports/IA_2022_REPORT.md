# Iowa 2022 county data: validation report

Built 2026-11-23 by `python -m urqse.data.build_state IA 2022`. 99 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

## Sources

| Item | Vintage | File (data_raw) | Retrieved | URL |
|---|---|---|---|---|
| pep | Census PEP Vintage 2022, July 1 2022 estimates | `co-est2022-alldata.csv` | 2026-11-23 | https://www2.census.gov/programs-surveys/popest/datasets/2020-2022/counties/totals/co-est2022-alldata.csv |
| cbsa | Census PEP Vintage 2023 CBSA file (OMB July 2023 delineations) | `cbsa-est2023-alldata.csv` | 2026-11-23 | https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/metro/totals/cbsa-est2023-alldata.csv |
| cenpop | 2020 Census centers of population, county | `CenPop2020_Mean_CO.txt` | 2026-11-23 | https://www2.census.gov/geo/docs/reference/cenpop2020/county/CenPop2020_Mean_CO.txt |
| counties | Census cartographic boundary file 2022, 1:500k | `cb_2022_us_county_500k.zip` | 2026-11-23 | https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip |
| bea_emp | BEA CAEMP25N (formerly CAINC25N), released 2023-11-16 | `bea_CAEMP25N.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAEMP25N.zip |
| bea_farm | BEA CAINC45, released 2023-11-16 | `bea_CAINC45.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAINC45.zip |
| bea_earn | BEA CAINC5N, file dated 2026-01-14 | `bea_CAINC5N.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAINC5N.zip |
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 19 | `CDL_2022_19.tif` | 2026-11-23 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=19 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_IA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-23 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 3,200,517 | 3,200,517 | 0.000% |
| ACS workers by residence | 1,598,658 | 1,598,658 | 0.000% |
| ACS workers by workplace | 1,600,078 | 1,600,078 | 0.000% |
| ACS workers working out of state | 71,194 | 71,194 | 0.000% |
| BEA non-farm employment (L80) | 2,024,343 | 2,024,343 | 0.000% |
| BEA farm employment (L70) | 89,652 | 89,652 | 0.000% |
| BEA farm proprietors (L50) | 68,612 | 68,612 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 9,844,856,000 | 9,844,856,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 881,933,000 | 881,933,000 | 0.000% |
| CoA hired farm labour expense $ | 1,222,260,000 | 1,222,261,000 | -0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 126,773,282,000 | 126,773,282,000 | 0.000% |
| ACS foreign born entered 2010+ | 70,687 | 70,687 | 0.000% |
| CoA owned acres | 15,043,032 | 15,043,032 | 0.000% |
| CoA rented-from-others acres | 14,935,133 | 14,935,133 | 0.000% |
| CoA land in farms, ha | 12,131,733 | 12,131,733 | 0.000% |
| CoA total cropland, ha | 10,473,911 | 10,473,911 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.553, median 0.728, max 0.914; BEA counts jobs, ACS counts people by main job). Sum N = 1,671,272 = sum HU + HA = 1,671,272. Farm jobs after scaling: 65,173 (BEA 89,652). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 72,614. Jobs = in-state residents working out of state = 71,194, split by the state farm share (HA = 2,900). Location: the 39 out-of-state counties within 1 km of the state (17015, 17067, 17071, 17085, 17131, 17161, 17195, 27043, 27045, 27047, 27055, 27063, 27091, 27099, 27105, 27133, 29005, 29045, 29081, 29129, 29147, 29171, 29197, 29199, 29227, 31021, 31025, 31043, 31055, 31131, 31153, 31173, 31177, 46083, 46099, 46127, 55023, 55043, 55123); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 9,419,745 ha vs Census of Agriculture cropland 10,473,911 ha and land in farms 12,131,733 ha; county ratio TF / CoA cropland 0.52 to 1.37. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 2,550,124 ha). County area covered by CDL pixels: 14,574,448 ha vs land area 14,465,960 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 4.52 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (62,624 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 44,801 $ per BEA farm job, 61,627 $ per farm worker; county range 35,839 to 92,864 $ per worker. State compensation per farm wage job by year: 2018 44,761 $, 2019 41,384 $, 2020 37,368 $, 2021 42,025 $, 2022 41,917 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 151,305,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,222,261,000 $ in 2022, column `hired_labor_coa_usd`) is 1.39x BEA farm compensation (881,933,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 109,812 $, county 11,462 to 219,654 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 82,594 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 11,050,464,000 $ vs CAINC45 9,844,856,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.502, county range 0.332 to 0.764.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 256 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 9,253 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (Cherokee, Monroe, Wayne), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Polk); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (21); rural = the rest (77). `# VERIFY` one core for a multi-metro state.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 202.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.1 straight-line km/h between counties (median 16.9 to 27.0 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.28).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 19007 Appanoose | not published; NASS 'other (combined) counties' value = 248 $/acre |
| cash_rent_usd_acre | 19081 Hancock | not published; NASS 'other (combined) counties' value = 248 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines). Census of Agriculture tenure and value cells are all published.

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual for Iowa.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 19001 | Adair | rural | 3,573 | 2,754 | 519 | 93,529 | 4.75M | 76,917 | 74,459 | 0.605 | 208 |
| 19003 | Adams | rural | 1,730 | 1,052 | 289 | 59,262 | 2.78M | 66,857 | 97,739 | 0.542 | 230 |
| 19005 | Allamakee | rural | 6,758 | 4,478 | 708 | 44,004 | 9.06M | 63,643 | 84,707 | 0.681 | 238 |
| 19007 | Appanoose | rural | 4,916 | 3,889 | 399 | 31,097 | 6.28M | 75,376 | 14,143 | 0.726 | 248* |
| 19009 | Audubon | rural | 2,806 | 1,626 | 464 | 87,112 | 3.74M | 76,337 | 175,583 | 0.476 | 282 |
| 19011 | Benton | suburb | 13,111 | 6,312 | 783 | 140,840 | 11.55M | 60,221 | 128,465 | 0.404 | 270 |
| 19013 | Black Hawk | suburb | 65,260 | 74,604 | 746 | 97,076 | 64.18M | 67,353 | 97,144 | 0.452 | 290 |
| 19015 | Boone | suburb | 14,054 | 10,820 | 802 | 107,284 | 13.62M | 45,116 | 69,071 | 0.415 | 254 |
| 19017 | Bremer | suburb | 12,544 | 9,879 | 674 | 78,011 | 10.83M | 53,751 | 83,443 | 0.489 | 287 |
| 19019 | Buchanan | rural | 10,291 | 6,796 | 781 | 113,932 | 10.19M | 60,799 | 129,774 | 0.494 | 253 |
| 19021 | Buena Vista | rural | 10,171 | 10,328 | 690 | 124,199 | 11.45M | 64,073 | 193,254 | 0.465 | 276 |
| 19023 | Butler | rural | 6,733 | 3,388 | 642 | 109,195 | 7.79M | 88,011 | 101,042 | 0.475 | 274 |
| 19025 | Calhoun | rural | 4,196 | 2,696 | 483 | 126,608 | 6.11M | 77,028 | 183,685 | 0.458 | 272 |
| 19027 | Carroll | rural | 10,600 | 10,818 | 799 | 122,424 | 12.22M | 66,561 | 179,699 | 0.535 | 275 |
| 19029 | Cass | rural | 6,486 | 6,118 | 552 | 103,637 | 7.29M | 62,926 | 96,888 | 0.530 | 217 |
| 19031 | Cedar | rural | 9,612 | 4,940 | 589 | 110,527 | 9.42M | 74,562 | 118,069 | 0.384 | 271 |
| 19033 | Cerro Gordo | rural | 21,675 | 23,816 | 585 | 111,861 | 21.90M | 39,920 | 96,644 | 0.408 | 232 |
| 19035 | Cherokee | rural | 5,847 | 4,899 | 604 | 114,794 | 7.68M | 57,206 | 147,806 | 0.462 | 278 |
| 19037 | Chickasaw | rural | 6,088 | 5,232 | 744 | 96,524 | 7.69M | 64,727 | 99,413 | 0.486 | 257 |
| 19039 | Clarke | rural | 4,416 | 4,228 | 475 | 30,114 | 4.62M | 69,464 | 32,860 | 0.764 | 174 |
| 19041 | Clay | rural | 8,259 | 8,288 | 527 | 111,175 | 8.86M | 92,864 | 155,561 | 0.430 | 268 |
| 19043 | Clayton | rural | 8,523 | 6,191 | 1,068 | 82,368 | 9.86M | 67,040 | 90,235 | 0.684 | 254 |
| 19045 | Clinton | rural | 21,251 | 19,658 | 911 | 124,937 | 23.12M | 50,033 | 90,935 | 0.491 | 275 |
| 19047 | Crawford | rural | 7,703 | 6,451 | 745 | 143,745 | 8.04M | 64,949 | 156,234 | 0.433 | 275 |
| 19049 | Dallas | suburb | 54,746 | 44,255 | 693 | 95,236 | 29.09M | 80,295 | 87,475 | 0.469 | 258 |
| 19051 | Davis | rural | 4,002 | 2,605 | 640 | 38,983 | 4.87M | 41,402 | 22,115 | 0.727 | 154 |
| 19053 | Decatur | rural | 3,437 | 2,279 | 426 | 31,459 | 3.65M | 60,525 | 23,444 | 0.706 | 161 |
| 19055 | Delaware | rural | 9,504 | 7,445 | 1,135 | 105,253 | 10.93M | 45,340 | 119,778 | 0.685 | 270 |
| 19057 | Des Moines | rural | 18,215 | 20,532 | 470 | 55,743 | 20.49M | 45,087 | 75,757 | 0.565 | 220 |
| 19059 | Dickinson | rural | 9,231 | 9,197 | 278 | 71,153 | 9.53M | 75,673 | 183,002 | 0.421 | 225 |
| 19061 | Dubuque | suburb | 50,680 | 56,254 | 1,158 | 76,643 | 42.06M | 35,839 | 91,046 | 0.634 | 274 |
| 19063 | Emmet | rural | 4,843 | 3,537 | 383 | 81,333 | 5.45M | 66,772 | 122,533 | 0.471 | 225 |
| 19065 | Fayette | rural | 9,082 | 7,141 | 1,008 | 123,317 | 11.05M | 60,856 | 89,308 | 0.553 | 253 |
| 19067 | Floyd | rural | 7,256 | 5,776 | 679 | 96,915 | 8.61M | 54,662 | 117,215 | 0.438 | 233 |
| 19069 | Franklin | rural | 4,670 | 3,520 | 590 | 125,602 | 6.22M | 65,362 | 153,620 | 0.377 | 260 |
| 19071 | Fremont | rural | 3,089 | 2,027 | 296 | 92,077 | 3.00M | 91,102 | 101,731 | 0.364 | 237 |
| 19073 | Greene | rural | 4,337 | 3,171 | 522 | 119,577 | 6.07M | 67,263 | 117,310 | 0.423 | 254 |
| 19075 | Grundy | suburb | 6,159 | 3,651 | 474 | 113,511 | 7.08M | 75,743 | 130,535 | 0.354 | 304 |
| 19077 | Guthrie | suburb | 5,221 | 3,253 | 533 | 85,113 | 5.99M | 82,789 | 116,081 | 0.559 | 222 |
| 19079 | Hamilton | rural | 7,201 | 4,919 | 647 | 124,138 | 9.10M | 81,341 | 219,654 | 0.353 | 279 |
| 19081 | Hancock | rural | 5,556 | 4,851 | 626 | 124,392 | 8.61M | 79,341 | 148,733 | 0.368 | 248* |
| 19083 | Hardin | rural | 8,199 | 7,063 | 796 | 114,463 | 10.30M | 54,390 | 177,511 | 0.404 | 256 |
| 19085 | Harrison | suburb | 7,301 | 4,059 | 533 | 125,368 | 6.37M | 62,415 | 106,633 | 0.542 | 245 |
| 19087 | Henry | rural | 9,653 | 9,487 | 694 | 59,944 | 9.72M | 45,555 | 82,403 | 0.611 | 234 |
| 19089 | Howard | rural | 4,560 | 3,715 | 643 | 91,073 | 7.09M | 68,207 | 116,505 | 0.504 | 235 |
| 19091 | Humboldt | rural | 4,706 | 4,025 | 402 | 96,144 | 5.83M | 45,426 | 158,904 | 0.396 | 262 |
| 19093 | Ida | rural | 3,435 | 3,645 | 479 | 93,064 | 4.91M | 62,141 | 141,771 | 0.368 | 292 |
| 19095 | Iowa | rural | 8,302 | 8,467 | 711 | 91,914 | 9.37M | 67,542 | 89,159 | 0.554 | 266 |
| 19097 | Jackson | rural | 9,135 | 6,432 | 829 | 66,537 | 9.92M | 50,796 | 64,994 | 0.586 | 242 |
| 19099 | Jasper | suburb | 18,050 | 11,236 | 837 | 128,928 | 17.65M | 67,347 | 99,310 | 0.533 | 247 |
| 19101 | Jefferson | rural | 7,486 | 7,849 | 445 | 54,664 | 8.26M | 38,724 | 65,966 | 0.576 | 243 |
| 19103 | Johnson | suburb | 82,604 | 89,705 | 1,007 | 85,211 | 49.52M | 51,934 | 63,036 | 0.546 | 249 |
| 19105 | Jones | suburb | 9,730 | 5,960 | 672 | 92,708 | 9.28M | 62,727 | 79,158 | 0.568 | 260 |
| 19107 | Keokuk | rural | 4,501 | 2,337 | 608 | 88,077 | 6.41M | 59,000 | 83,247 | 0.680 | 226 |
| 19109 | Kossuth | rural | 6,915 | 6,240 | 898 | 213,052 | 11.31M | 63,869 | 147,017 | 0.436 | 269 |
| 19111 | Lee | rural | 14,867 | 15,251 | 724 | 57,331 | 17.12M | 41,742 | 38,811 | 0.629 | 206 |
| 19113 | Linn | suburb | 119,071 | 127,777 | 1,074 | 103,386 | 91.23M | 64,566 | 63,253 | 0.505 | 265 |
| 19115 | Louisa | rural | 5,341 | 3,782 | 445 | 60,058 | 5.26M | 62,177 | 129,582 | 0.543 | 229 |
| 19117 | Lucas | rural | 4,024 | 3,447 | 424 | 28,426 | 4.97M | 42,968 | 11,462 | 0.713 | 169 |
| 19119 | Lyon | rural | 5,790 | 4,039 | 848 | 124,482 | 8.30M | 72,008 | 177,699 | 0.459 | 269 |
| 19121 | Madison | suburb | 8,899 | 5,102 | 687 | 59,033 | 6.71M | 80,067 | 39,160 | 0.650 | 208 |
| 19123 | Mahaska | rural | 11,000 | 8,212 | 768 | 93,190 | 14.12M | 50,681 | 78,331 | 0.604 | 239 |
| 19125 | Marion | rural | 16,435 | 18,263 | 740 | 59,972 | 14.97M | 50,079 | 35,020 | 0.622 | 193 |
| 19127 | Marshall | rural | 19,134 | 17,877 | 828 | 109,806 | 16.29M | 54,901 | 93,064 | 0.444 | 264 |
| 19129 | Mills | suburb | 6,839 | 3,647 | 342 | 78,418 | 5.66M | 61,460 | 90,920 | 0.407 | 255 |
| 19131 | Mitchell | rural | 5,611 | 4,261 | 640 | 96,749 | 8.03M | 56,093 | 114,846 | 0.463 | 250 |
| 19133 | Monona | rural | 4,057 | 2,903 | 415 | 124,644 | 4.68M | 62,569 | 180,438 | 0.430 | 258 |
| 19135 | Monroe | rural | 3,579 | 3,016 | 364 | 23,669 | 5.48M | 49,551 | 26,870 | 0.700 | 176 |
| 19137 | Montgomery | rural | 4,722 | 4,096 | 418 | 75,533 | 5.68M | 74,602 | 75,036 | 0.491 | 217 |
| 19139 | Muscatine | rural | 20,877 | 21,708 | 582 | 67,095 | 21.37M | 58,669 | 76,601 | 0.549 | 264 |
| 19141 | O'Brien | rural | 6,811 | 5,679 | 578 | 126,126 | 10.22M | 80,944 | 194,898 | 0.426 | 286 |
| 19143 | Osceola | rural | 3,035 | 2,080 | 441 | 88,903 | 5.65M | 70,177 | 155,048 | 0.408 | 241 |
| 19145 | Page | rural | 6,772 | 6,485 | 638 | 92,110 | 8.01M | 51,562 | 116,621 | 0.531 | 220 |
| 19147 | Palo Alto | rural | 4,401 | 3,368 | 613 | 118,799 | 5.89M | 61,922 | 166,449 | 0.392 | 245 |
| 19149 | Plymouth | rural | 13,441 | 11,179 | 988 | 174,728 | 14.50M | 68,021 | 176,085 | 0.487 | 271 |
| 19151 | Pocahontas | rural | 3,283 | 2,636 | 493 | 131,679 | 5.06M | 75,209 | 173,338 | 0.332 | 266 |
| 19153 | Polk | core | 257,254 | 295,013 | 561 | 59,181 | 221.20M | 70,843 | 53,552 | 0.393 | 254 |
| 19155 | Pottawattamie | suburb | 45,090 | 39,135 | 885 | 180,251 | 41.26M | 64,123 | 95,409 | 0.435 | 255 |
| 19157 | Poweshiek | rural | 8,988 | 10,147 | 784 | 107,483 | 11.51M | 47,784 | 89,595 | 0.505 | 238 |
| 19159 | Ringgold | rural | 2,269 | 1,448 | 454 | 46,524 | 3.07M | 64,390 | 78,785 | 0.633 | 204 |
| 19161 | Sac | rural | 4,875 | 2,853 | 634 | 124,689 | 7.71M | 77,888 | 174,558 | 0.426 | 270 |
| 19163 | Scott | suburb | 85,855 | 90,330 | 583 | 71,512 | 77.55M | 70,525 | 83,247 | 0.444 | 266 |
| 19165 | Shelby | rural | 5,912 | 5,507 | 657 | 127,665 | 5.92M | 54,019 | 145,361 | 0.457 | 262 |
| 19167 | Sioux | rural | 18,709 | 19,366 | 1,528 | 166,445 | 21.88M | 67,641 | 177,705 | 0.442 | 295 |
| 19169 | Story | suburb | 51,376 | 54,845 | 819 | 110,802 | 32.16M | 59,928 | 82,678 | 0.451 | 266 |
| 19171 | Tama | rural | 8,090 | 5,535 | 774 | 128,670 | 8.64M | 65,902 | 117,980 | 0.498 | 265 |
| 19173 | Taylor | rural | 2,856 | 2,084 | 522 | 69,645 | 3.28M | 48,018 | 94,214 | 0.516 | 205 |
| 19175 | Union | rural | 5,485 | 5,746 | 499 | 47,006 | 7.16M | 48,563 | 54,116 | 0.553 | 216 |
| 19177 | Van Buren | rural | 2,918 | 2,081 | 486 | 39,781 | 3.60M | 67,204 | 40,145 | 0.667 | 168 |
| 19179 | Wapello | rural | 16,045 | 16,433 | 554 | 44,629 | 18.81M | 51,443 | 35,899 | 0.655 | 231 |
| 19181 | Warren | suburb | 26,985 | 13,946 | 797 | 53,327 | 15.33M | 65,245 | 28,555 | 0.526 | 207 |
| 19183 | Washington | suburb | 11,443 | 9,182 | 833 | 86,360 | 11.47M | 60,175 | 165,792 | 0.574 | 237 |
| 19185 | Wayne | rural | 2,827 | 2,195 | 462 | 53,280 | 3.64M | 54,250 | 39,998 | 0.627 | 164 |
| 19187 | Webster | rural | 17,470 | 18,102 | 809 | 142,918 | 19.76M | 53,085 | 165,773 | 0.414 | 263 |
| 19189 | Winnebago | rural | 5,338 | 5,137 | 626 | 82,810 | 5.41M | 78,661 | 125,106 | 0.473 | 263 |
| 19191 | Winneshiek | rural | 10,797 | 9,977 | 1,211 | 94,844 | 11.61M | 51,469 | 65,595 | 0.636 | 237 |
| 19193 | Woodbury | suburb | 52,032 | 49,261 | 777 | 154,897 | 42.46M | 69,367 | 131,328 | 0.432 | 261 |
| 19195 | Worth | rural | 3,906 | 2,215 | 393 | 81,513 | 3.96M | 61,506 | 109,510 | 0.441 | 218 |
| 19197 | Wright | rural | 5,740 | 5,664 | 785 | 125,534 | 9.52M | 50,422 | 204,341 | 0.364 | 278 |
| EXT | External (out-of-state commuting) | external | 72,614 | 68,294 | 2,900 | 419,123 | 68.45M | 61,627 | n/a | 0.502 | n/a |

`*` filled, see above.
