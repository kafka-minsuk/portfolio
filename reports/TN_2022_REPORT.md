# Tennessee 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state TN 2022`. 95 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 47 | `TN/CDL_2022_47.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=47 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_TN.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 7,051,339 | 7,051,339 | 0.000% |
| ACS workers by residence | 3,213,248 | 3,213,248 | 0.000% |
| ACS workers by workplace | 3,261,510 | 3,261,510 | 0.000% |
| ACS workers working out of state | 109,695 | 109,695 | 0.000% |
| BEA non-farm employment (L80) | 4,431,214 | 4,431,214 | 0.000% |
| BEA farm employment (L70) | 75,180 | 75,180 | 0.000% |
| BEA farm proprietors (L50) | 63,657 | 63,657 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 284,285,000 | 284,285,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 289,337,000 | 289,337,000 | 0.000% |
| CoA hired farm labour expense $ | 390,334,000 | 390,331,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 303,332,656,000 | 303,332,656,000 | 0.000% |
| ACS foreign born entered 2010+ | 136,488 | 136,488 | 0.000% |
| CoA owned acres | 7,033,136 | 7,033,136 | 0.000% |
| CoA rented-from-others acres | 3,699,815 | 3,699,815 | 0.000% |
| CoA land in farms, ha | 4,343,471 | 4,343,471 | 0.000% |
| CoA total cropland, ha | 2,134,309 | 2,134,309 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.477, median 0.720, max 0.856; BEA counts jobs, ACS counts people by main job). Sum N = 3,371,205 = sum HU + HA = 3,371,205. Farm jobs after scaling: 53,899 (BEA 75,180). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 157,957. Jobs = in-state residents working out of state = 109,695, split by the state farm share (HA = 1,813). Location: the 52 out-of-state counties within 1 km of the state (01071, 01077, 01083, 01089, 05035, 05093, 13047, 13083, 13111, 13213, 13295, 13313, 21003, 21013, 21035, 21047, 21053, 21057, 21075, 21083, 21105, 21141, 21147, 21171, 21213, 21219, 21221, 21231, 21235, 28003, 28009, 28033, 28093, 28139, 28141, 29143, 29155, 37009, 37011, 37039, 37075, 37087, 37115, 37121, 37173, 37189, 37199, 51077, 51105, 51169, 51191, 51520); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,534,631 ha vs Census of Agriculture cropland 2,134,309 ha and land in farms 4,343,471 ha; county ratio TF / CoA cropland 0.15 to 1.34. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,890,658 ha). County area covered by CDL pixels: 10,911,243 ha vs land area 10,679,237 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 7.03 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (68,454 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 20,130 $ per BEA farm job, 28,078 $ per farm worker; county range 6,048 to 86,742 $ per worker. State compensation per farm wage job by year: 2018 22,033 $, 2019 18,680 $, 2020 19,841 $, 2021 18,462 $, 2022 25,110 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 77,752,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (390,331,000 $ in 2022, column `hired_labor_coa_usd`) is 1.35x BEA farm compensation (289,337,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 3,781 $, county -45,067 to 82,078 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 94,567 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 719,400,000 $ vs CAINC45 284,285,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.655, county range 0.281 to 0.893.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 111 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 5,156 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (Benton, Decatur, Van Buren), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Davidson); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (43); rural = the rest (51). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 199.4 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 61.3 straight-line km/h between counties (median 8.8 to 22.6 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.25).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 47037 Davidson | not published; NASS 'other (combined) counties' value = 72.5 $/acre |
| cash_rent_usd_acre | 47101 Lewis | not published; NASS 'other (combined) counties' value = 72.5 $/acre |
| cash_rent_usd_acre | 47151 Scott | not published; NASS 'other (combined) counties' value = 72.5 $/acre |
| cash_rent_usd_acre | 47161 Stewart | not published; NASS 'other (combined) counties' value = 72.5 $/acre |

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
| 47001 | Anderson | suburb | 32,457 | 45,920 | 354 | 896 | 28.07M | 22,796 | -13,530 | 0.635 | 20 |
| 47003 | Bedford | rural | 22,971 | 16,391 | 1,032 | 18,369 | 17.44M | 31,217 | 43,267 | 0.659 | 74 |
| 47005 | Benton | rural | 5,834 | 3,652 | 267 | 9,659 | 5.19M | 27,361 | -6,872 | 0.810 | 82 |
| 47007 | Bledsoe | rural | 5,497 | 2,646 | 620 | 4,883 | 4.13M | 15,055 | 14,936 | 0.753 | 52 |
| 47009 | Blount | suburb | 64,637 | 57,951 | 794 | 6,335 | 44.03M | 21,529 | -13,092 | 0.580 | 34 |
| 47011 | Bradley | suburb | 49,631 | 46,686 | 741 | 4,697 | 37.63M | 25,007 | 60,676 | 0.789 | 35 |
| 47013 | Campbell | suburb | 14,927 | 9,977 | 268 | 1,220 | 11.08M | 10,014 | -7,668 | 0.700 | 44 |
| 47015 | Cannon | suburb | 6,287 | 2,257 | 359 | 8,670 | 3.97M | 32,975 | -6,660 | 0.700 | 94 |
| 47017 | Carroll | rural | 11,616 | 7,730 | 573 | 39,768 | 8.97M | 34,019 | -18,140 | 0.638 | 105 |
| 47019 | Carter | suburb | 22,795 | 12,728 | 346 | 886 | 14.66M | 18,454 | -3,411 | 0.688 | 40 |
| 47021 | Cheatham | suburb | 20,410 | 10,802 | 276 | 4,833 | 8.30M | 38,280 | -17,049 | 0.720 | 60 |
| 47023 | Chester | suburb | 6,995 | 4,010 | 247 | 13,019 | 4.17M | 31,898 | -18,819 | 0.624 | 76 |
| 47025 | Claiborne | rural | 12,619 | 10,357 | 722 | 4,137 | 8.90M | 22,929 | -6,711 | 0.696 | 25 |
| 47027 | Clay | rural | 2,592 | 1,430 | 230 | 3,717 | 2.90M | 51,097 | 77,041 | 0.808 | 41 |
| 47029 | Cocke | rural | 14,604 | 8,467 | 482 | 4,394 | 11.15M | 37,878 | 17,037 | 0.746 | 44 |
| 47031 | Coffee | rural | 25,023 | 26,999 | 756 | 25,760 | 21.80M | 34,967 | 2,903 | 0.668 | 90 |
| 47033 | Crockett | suburb | 6,377 | 3,684 | 321 | 48,770 | 3.47M | 36,851 | -45,067 | 0.310 | 136 |
| 47035 | Cumberland | rural | 22,039 | 20,733 | 661 | 2,884 | 20.87M | 35,120 | 4,085 | 0.806 | 68 |
| 47037 | Davidson | core | 390,556 | 511,852 | 315 | 1,925 | 275.45M | 39,560 | 2,013 | 0.807 | 72* |
| 47039 | Decatur | rural | 4,370 | 3,616 | 266 | 8,931 | 3.60M | 31,563 | -8,080 | 0.735 | 59 |
| 47041 | DeKalb | rural | 8,153 | 6,539 | 557 | 7,617 | 5.32M | 86,742 | 13,001 | 0.725 | 78 |
| 47043 | Dickson | suburb | 25,497 | 19,970 | 825 | 6,163 | 14.57M | 17,501 | -14,126 | 0.832 | 51 |
| 47045 | Dyer | rural | 15,817 | 15,645 | 443 | 89,295 | 13.16M | 32,437 | 43,119 | 0.310 | 144 |
| 47047 | Fayette | suburb | 18,894 | 9,280 | 512 | 53,406 | 8.04M | 42,505 | -13,114 | 0.579 | 78 |
| 47049 | Fentress | rural | 7,127 | 5,238 | 373 | 2,991 | 5.42M | 27,601 | 9,718 | 0.735 | 39 |
| 47051 | Franklin | rural | 18,881 | 15,474 | 904 | 27,367 | 12.26M | 29,331 | 23,812 | 0.651 | 124 |
| 47053 | Gibson | suburb | 21,155 | 14,714 | 691 | 92,962 | 14.06M | 36,207 | 21,543 | 0.388 | 145 |
| 47055 | Giles | rural | 12,609 | 8,509 | 1,033 | 24,133 | 11.21M | 21,834 | -3,841 | 0.710 | 55 |
| 47057 | Grainger | suburb | 9,411 | 3,459 | 449 | 5,632 | 6.19M | 57,200 | -6,735 | 0.761 | 35 |
| 47059 | Greene | rural | 28,512 | 25,032 | 1,882 | 17,023 | 27.99M | 25,122 | -4,976 | 0.722 | 48 |
| 47061 | Grundy | rural | 5,266 | 2,566 | 195 | 3,479 | 3.20M | 26,997 | 43,088 | 0.790 | 57 |
| 47063 | Hamblen | suburb | 26,689 | 30,395 | 451 | 4,803 | 24.65M | 38,129 | 2,730 | 0.528 | 66 |
| 47065 | Hamilton | suburb | 179,167 | 222,862 | 457 | 2,163 | 156.28M | 18,089 | 8,390 | 0.791 | 32 |
| 47067 | Hancock | rural | 2,101 | 1,088 | 311 | 1,447 | 1.90M | 14,333 | -9,141 | 0.662 | 21 |
| 47069 | Hardeman | rural | 8,687 | 7,584 | 451 | 26,539 | 6.00M | 27,405 | -14,195 | 0.815 | 84 |
| 47071 | Hardin | rural | 10,426 | 9,419 | 498 | 18,719 | 8.73M | 18,345 | 724 | 0.819 | 57 |
| 47073 | Hawkins | suburb | 21,481 | 14,368 | 1,114 | 5,655 | 15.77M | 19,519 | -7,690 | 0.753 | 28 |
| 47075 | Haywood | rural | 7,153 | 4,935 | 396 | 81,222 | 5.77M | 39,909 | -39,559 | 0.372 | 147 |
| 47077 | Henderson | rural | 11,506 | 8,448 | 618 | 25,066 | 7.71M | 26,674 | -6,139 | 0.786 | 80 |
| 47079 | Henry | rural | 12,545 | 12,059 | 768 | 40,143 | 12.09M | 35,056 | 44,702 | 0.681 | 116 |
| 47081 | Hickman | suburb | 10,427 | 4,702 | 406 | 8,312 | 5.13M | 26,787 | -6,848 | 0.759 | 51 |
| 47083 | Houston | rural | 3,171 | 1,459 | 215 | 1,918 | 1.98M | 24,931 | -11,481 | 0.680 | 20 |
| 47085 | Humphreys | rural | 7,773 | 6,452 | 488 | 9,818 | 7.72M | 21,045 | -15,752 | 0.893 | 58 |
| 47087 | Jackson | rural | 4,704 | 1,881 | 321 | 2,623 | 2.75M | 18,222 | -10,129 | 0.816 | 56 |
| 47089 | Jefferson | suburb | 24,606 | 17,622 | 856 | 7,306 | 14.77M | 23,931 | -1,070 | 0.745 | 37 |
| 47091 | Johnson | rural | 6,298 | 4,387 | 333 | 2,176 | 4.29M | 20,697 | -7,572 | 0.792 | 38 |
| 47093 | Knox | suburb | 238,588 | 267,469 | 718 | 3,408 | 188.41M | 31,059 | -1,445 | 0.704 | 24 |
| 47095 | Lake | rural | 1,710 | 1,438 | 104 | 28,829 | 1.36M | 43,477 | 71,769 | 0.281 | 152 |
| 47097 | Lauderdale | rural | 9,045 | 6,783 | 474 | 59,868 | 4.90M | 38,280 | 5,801 | 0.370 | 121 |
| 47099 | Lawrence | rural | 18,192 | 13,423 | 1,218 | 30,023 | 14.80M | 20,378 | 5,858 | 0.673 | 76 |
| 47101 | Lewis | rural | 5,176 | 3,416 | 150 | 1,700 | 3.23M | 14,978 | -5,075 | 0.815 | 72* |
| 47103 | Lincoln | rural | 15,839 | 9,704 | 1,112 | 29,550 | 11.16M | 37,073 | 8,773 | 0.675 | 80 |
| 47105 | Loudon | suburb | 24,262 | 20,433 | 826 | 7,045 | 17.67M | 78,771 | 28,145 | 0.716 | 41 |
| 47107 | McMinn | rural | 22,261 | 19,854 | 908 | 11,605 | 19.26M | 17,353 | 8,065 | 0.783 | 34 |
| 47109 | McNairy | rural | 9,710 | 6,075 | 478 | 18,796 | 5.85M | 25,421 | -7,929 | 0.791 | 48 |
| 47111 | Macon | suburb | 11,481 | 6,018 | 689 | 10,557 | 6.33M | 20,636 | 22,873 | 0.755 | 141 |
| 47113 | Madison | suburb | 44,068 | 61,632 | 540 | 40,763 | 36.66M | 26,395 | -17,637 | 0.590 | 119 |
| 47115 | Marion | suburb | 11,826 | 8,848 | 250 | 4,368 | 8.62M | 20,079 | 18,784 | 0.663 | 59 |
| 47117 | Marshall | rural | 15,692 | 12,105 | 891 | 11,945 | 11.12M | 19,596 | 4,125 | 0.787 | 47 |
| 47119 | Maury | suburb | 49,963 | 44,431 | 1,194 | 20,575 | 31.41M | 26,283 | -8,139 | 0.680 | 79 |
| 47121 | Meigs | rural | 4,807 | 2,337 | 194 | 4,018 | 3.31M | 37,893 | -13,062 | 0.836 | 40 |
| 47123 | Monroe | rural | 17,921 | 15,694 | 649 | 10,107 | 12.70M | 25,942 | -10,392 | 0.713 | 54 |
| 47125 | Montgomery | suburb | 104,222 | 77,294 | 719 | 22,065 | 60.20M | 23,222 | 3,385 | 0.593 | 109 |
| 47127 | Moore | rural | 2,865 | 2,140 | 218 | 2,653 | 2.34M | 29,585 | -983 | 0.795 | 35 |
| 47129 | Morgan | suburb | 7,241 | 4,014 | 340 | 1,754 | 4.67M | 12,156 | 565 | 0.807 | 40 |
| 47131 | Obion | rural | 13,120 | 13,022 | 553 | 79,938 | 12.24M | 33,034 | 68,195 | 0.412 | 155 |
| 47133 | Overton | rural | 9,977 | 6,766 | 750 | 7,707 | 6.10M | 19,500 | -7,764 | 0.803 | 48 |
| 47135 | Perry | rural | 3,057 | 2,358 | 218 | 4,536 | 2.45M | 6,048 | -3,564 | 0.866 | 43 |
| 47137 | Pickett | rural | 1,692 | 1,117 | 203 | 2,255 | 2.05M | 23,790 | 21,883 | 0.729 | 42 |
| 47139 | Polk | suburb | 7,143 | 2,652 | 191 | 3,733 | 4.47M | 28,413 | 60,551 | 0.766 | 42 |
| 47141 | Putnam | rural | 37,665 | 43,766 | 763 | 4,820 | 25.66M | 14,766 | -12,774 | 0.773 | 49 |
| 47143 | Rhea | rural | 12,560 | 12,090 | 333 | 4,224 | 10.66M | 27,104 | 1,025 | 0.680 | 36 |
| 47145 | Roane | suburb | 23,119 | 15,526 | 312 | 2,373 | 16.81M | 35,211 | -21,259 | 0.777 | 28 |
| 47147 | Robertson | suburb | 35,452 | 25,826 | 1,081 | 45,379 | 20.43M | 47,754 | 9,085 | 0.463 | 187 |
| 47149 | Rutherford | suburb | 180,732 | 162,651 | 1,154 | 13,636 | 94.60M | 13,789 | -10,670 | 0.730 | 82 |
| 47151 | Scott | rural | 7,780 | 6,305 | 225 | 788 | 5.35M | 13,272 | -6,007 | 0.847 | 72* |
| 47153 | Sequatchie | suburb | 6,249 | 4,257 | 150 | 1,554 | 3.45M | 18,378 | -1,701 | 0.826 | 30 |
| 47155 | Sevier | rural | 45,941 | 49,514 | 439 | 2,891 | 29.26M | 17,439 | -2,748 | 0.707 | 30 |
| 47157 | Shelby | suburb | 422,464 | 496,037 | 396 | 29,216 | 401.07M | 23,552 | -4,224 | 0.513 | 94 |
| 47159 | Smith | suburb | 9,064 | 6,416 | 689 | 7,149 | 5.90M | 16,041 | -6,335 | 0.666 | 122 |
| 47161 | Stewart | suburb | 5,460 | 3,611 | 281 | 5,305 | 4.58M | 46,493 | 2,471 | 0.882 | 72* |
| 47163 | Sullivan | suburb | 67,689 | 73,774 | 912 | 2,589 | 60.34M | 17,180 | -2,106 | 0.680 | 33 |
| 47165 | Sumner | suburb | 98,077 | 73,738 | 1,065 | 17,381 | 50.87M | 31,856 | 1,210 | 0.666 | 148 |
| 47167 | Tipton | suburb | 27,667 | 13,375 | 425 | 61,396 | 10.19M | 33,621 | -9,357 | 0.359 | 135 |
| 47169 | Trousdale | suburb | 4,880 | 2,009 | 176 | 3,962 | 2.04M | 44,865 | -3,894 | 0.688 | 48 |
| 47171 | Unicoi | suburb | 7,508 | 5,565 | 81 | 126 | 5.54M | 26,693 | -5,760 | 0.659 | 56 |
| 47173 | Union | suburb | 8,124 | 3,710 | 288 | 1,094 | 4.41M | 18,972 | -12,752 | 0.889 | 29 |
| 47175 | Van Buren | rural | 2,421 | 983 | 147 | 1,641 | 1.67M | 19,249 | -9,599 | 0.870 | 35 |
| 47177 | Warren | rural | 17,419 | 14,076 | 1,389 | 17,632 | 12.22M | 25,525 | 16,938 | 0.696 | 88 |
| 47179 | Washington | suburb | 61,983 | 68,879 | 1,124 | 7,277 | 44.00M | 30,563 | 333 | 0.544 | 60 |
| 47181 | Wayne | rural | 6,155 | 3,967 | 450 | 7,376 | 4.49M | 23,363 | 14,147 | 0.756 | 44 |
| 47183 | Weakley | rural | 14,011 | 11,272 | 723 | 70,797 | 10.97M | 24,281 | 82,078 | 0.575 | 136 |
| 47185 | White | rural | 11,115 | 7,496 | 683 | 8,223 | 7.86M | 24,016 | -10,630 | 0.697 | 44 |
| 47187 | Williamson | suburb | 125,974 | 147,639 | 833 | 9,853 | 66.00M | 38,044 | -2,947 | 0.634 | 54 |
| 47189 | Wilson | suburb | 73,588 | 64,132 | 1,015 | 8,413 | 39.35M | 20,828 | -14,020 | 0.727 | 46 |
| EXT | External (out-of-state commuting) | external | 157,957 | 107,882 | 1,813 | 51,615 | 115.12M | 28,078 | n/a | 0.655 | n/a |

`*` filled, see above.
