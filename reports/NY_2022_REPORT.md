# New York 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state NY 2022`. 62 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 36 | `NY/CDL_2022_36.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=36 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| ghsl_R4_C13 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C13.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| ghsl_R5_C13 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C13.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C13.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NY.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 19,677,151 | 19,677,151 | 0.000% |
| ACS workers by residence | 9,394,994 | 9,394,994 | 0.000% |
| ACS workers by workplace | 9,776,743 | 9,776,743 | 0.000% |
| ACS workers working out of state | 190,755 | 190,755 | 0.000% |
| BEA non-farm employment (L80) | 12,839,113 | 12,839,113 | 0.000% |
| BEA farm employment (L70) | 52,933 | 52,933 | 0.000% |
| BEA farm proprietors (L50) | 30,191 | 30,191 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,442,888,000 | 2,442,888,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 856,967,000 | 856,967,000 | 0.000% |
| CoA hired farm labour expense $ | 1,227,224,000 | 1,227,448,000 | -0.018% |
| BEA non-farm earnings $ (CAINC5N L82) | 1,167,590,861,000 | 1,167,590,861,000 | 0.000% |
| ACS foreign born entered 2010+ | 1,113,351 | 1,113,351 | 0.000% |
| CoA owned acres | 4,731,835 | 4,733,327 | -0.032% |
| CoA rented-from-others acres | 1,768,722 | 1,768,959 | -0.013% |
| CoA land in farms, ha | 2,631,372 | 2,631,382 | -0.000% |
| CoA total cropland, ha | 1,649,580 | 1,649,590 | -0.001% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.626, median 0.821, max 0.966; BEA counts jobs, ACS counts people by main job). Sum N = 9,967,498 = sum HU + HA = 9,967,498. Farm jobs after scaling: 43,530 (BEA 52,933). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 572,504. Jobs = in-state residents working out of state = 190,755, split by the state farm share (HA = 849). Location: the 23 out-of-state counties within 1 km of the state (09160, 09190, 25003, 34003, 34017, 34023, 34031, 34037, 34039, 42015, 42049, 42083, 42103, 42105, 42115, 42117, 42123, 42127, 50001, 50003, 50007, 50013, 50021); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,541,777 ha vs Census of Agriculture cropland 1,649,590 ha and land in farms 2,631,382 ha; county ratio TF / CoA cropland 0.28 to 20.24. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,178,396 ha). County area covered by CDL pixels: 12,694,359 ha vs land area 12,204,908 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 11.78 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (90,940 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 31,148 $ per BEA farm job, 37,876 $ per farm worker; county range 20,507 to 53,586 $ per worker. State compensation per farm wage job by year: 2018 31,884 $, 2019 26,075 $, 2020 28,801 $, 2021 27,335 $, 2022 37,682 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 126,922,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,227,448,000 $ in 2022, column `hired_labor_coa_usd`) is 1.43x BEA farm compensation (856,967,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 46,151 $, county 81 to 118,206 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 119,959 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,751,937,000 $ vs CAINC45 2,442,888,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.728, county range 0.000 to 1.000.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 76 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 4,102 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (New York); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (36); rural = the rest (25). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 6 counties have no BEA farm jobs (Bronx, Hamilton, Kings, New York, Queens, Richmond); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 226.3 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 56.7 straight-line km/h between counties (median 4.2 to 46.0 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.28).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 36005 Bronx | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 36041 Hamilton | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 36047 Kings | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 36061 New York | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 36081 Queens | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 36085 Richmond | 0 farm jobs: no farm sector in the model (spec §3.11) |
| owned_acres | 36061 New York | land in farms minus the other tenure (Census of Ag identity) |
| rented_acres | 36085 Richmond | land in farms minus the other tenure (Census of Ag identity) |
| omega | 36005 Bronx | state owner share |
| omega | 36041 Hamilton | state owner share |
| omega | 36047 Kings | state owner share |
| cash_rent_usd_acre | 36005 Bronx | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36027 Dutchess | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36033 Franklin | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36035 Fulton | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36037 Genesee | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36039 Greene | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36041 Hamilton | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36047 Kings | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36059 Nassau | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36061 New York | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36073 Orleans | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36079 Putnam | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36081 Queens | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36085 Richmond | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36087 Rockland | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36093 Schenectady | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36105 Sullivan | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36113 Warren | not published; NASS 'other (combined) counties' value = 90 $/acre |
| cash_rent_usd_acre | 36119 Westchester | not published; NASS 'other (combined) counties' value = 90 $/acre |
| land_value_usd_acre | 36005 Bronx | (D) in Census of Ag; see fills above |
| land_value_usd_acre | 36061 New York | (D) in Census of Ag; see fills above |
| owned_acres | 36041 Hamilton | (D) in Census of Ag; see fills above |
| owned_acres | 36047 Kings | (D) in Census of Ag; see fills above |
| rented_acres | 36005 Bronx | (D) in Census of Ag; see fills above |
| rented_acres | 36041 Hamilton | (D) in Census of Ag; see fills above |
| rented_acres | 36047 Kings | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 36041 Hamilton | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 36081 Queens | (D) in Census of Ag; left null (comparison column only) |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26918) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 36001 | Albany | suburb | 157,506 | 214,559 | 542 | 11,439 | 86.96M | 41,123 | 20,387 | 0.601 | 50 |
| 36003 | Allegany | rural | 18,985 | 14,376 | 731 | 33,206 | 10.43M | 32,416 | 29,321 | 0.813 | 32 |
| 36005 | Bronx | suburb | 564,284 | 410,347 | 0 | 14 | 142.47M | 0 | n/a | 0.728 | 90* |
| 36007 | Broome | suburb | 84,789 | 89,789 | 520 | 9,035 | 53.39M | 23,483 | 25,787 | 0.834 | 46 |
| 36009 | Cattaraugus | rural | 32,488 | 28,822 | 966 | 38,115 | 18.39M | 33,940 | 34,759 | 0.817 | 61 |
| 36011 | Cayuga | rural | 34,081 | 25,483 | 1,136 | 73,600 | 23.07M | 50,802 | 90,305 | 0.662 | 148 |
| 36013 | Chautauqua | rural | 53,861 | 51,645 | 1,811 | 49,007 | 42.36M | 29,664 | 38,369 | 0.759 | 74 |
| 36015 | Chemung | suburb | 35,625 | 36,253 | 352 | 6,905 | 29.33M | 28,239 | 16,990 | 0.806 | 38 |
| 36017 | Chenango | rural | 20,856 | 18,442 | 750 | 20,380 | 12.09M | 30,278 | 47,147 | 0.764 | 43 |
| 36019 | Clinton | rural | 35,098 | 33,990 | 880 | 26,778 | 23.78M | 45,471 | 54,448 | 0.829 | 50 |
| 36021 | Columbia | rural | 29,002 | 24,005 | 605 | 16,342 | 13.98M | 46,515 | 39,471 | 0.549 | 48 |
| 36023 | Cortland | rural | 22,643 | 19,456 | 567 | 22,055 | 11.17M | 32,538 | 59,087 | 0.755 | 60 |
| 36025 | Delaware | rural | 18,859 | 19,075 | 687 | 15,386 | 12.71M | 27,969 | 23,978 | 0.686 | 34 |
| 36027 | Dutchess | suburb | 145,279 | 119,129 | 863 | 10,693 | 52.88M | 44,534 | 24,745 | 0.717 | 90* |
| 36029 | Erie | suburb | 455,254 | 480,876 | 1,324 | 39,849 | 296.85M | 35,016 | 25,391 | 0.678 | 63 |
| 36031 | Essex | rural | 16,875 | 15,707 | 261 | 4,768 | 10.64M | 32,651 | 8,060 | 0.745 | 22 |
| 36033 | Franklin | rural | 18,873 | 18,704 | 710 | 29,487 | 11.48M | 33,856 | 45,407 | 0.856 | 90* |
| 36035 | Fulton | rural | 23,844 | 19,578 | 219 | 7,282 | 16.37M | 22,452 | 26,440 | 0.859 | 90* |
| 36037 | Genesee | rural | 28,247 | 24,889 | 1,009 | 57,616 | 16.70M | 45,866 | 69,550 | 0.659 | 90* |
| 36039 | Greene | rural | 21,390 | 17,073 | 259 | 3,907 | 11.51M | 43,722 | 14,109 | 0.823 | 90* |
| 36041 | Hamilton | rural | 2,223 | 2,138 | 0 | 192 | 2.39M | 0 | n/a | 0.728 | 90* |
| 36043 | Herkimer | suburb | 27,448 | 18,350 | 655 | 32,068 | 18.44M | 35,968 | 40,656 | 0.787 | 53 |
| 36045 | Jefferson | suburb | 54,156 | 54,980 | 1,025 | 66,186 | 30.50M | 40,283 | 86,958 | 0.683 | 78 |
| 36047 | Kings | suburb | 1,222,797 | 964,940 | 0 | 18 | 261.81M | 0 | n/a | 0.728 | 90* |
| 36049 | Lewis | rural | 11,676 | 8,295 | 770 | 35,105 | 8.63M | 34,793 | 118,206 | 0.724 | 78 |
| 36051 | Livingston | suburb | 28,236 | 22,108 | 886 | 68,167 | 13.95M | 49,950 | 77,868 | 0.626 | 128 |
| 36053 | Madison | suburb | 30,850 | 22,458 | 927 | 36,358 | 15.29M | 33,038 | 55,203 | 0.711 | 55 |
| 36055 | Monroe | suburb | 365,663 | 389,803 | 681 | 36,765 | 200.59M | 37,504 | 25,104 | 0.625 | 73 |
| 36057 | Montgomery | rural | 21,665 | 18,987 | 675 | 34,874 | 15.03M | 34,490 | 45,505 | 0.743 | 61 |
| 36059 | Nassau | suburb | 689,613 | 607,734 | 64 | 42 | 381.81M | 53,585 | 31,637 | 0.872 | 90* |
| 36061 | New York | core | 870,794 | 2,341,314 | 0 | 4 | 131.93M | 0 | n/a | 0.000 | 90* |
| 36063 | Niagara | suburb | 98,566 | 76,652 | 1,017 | 49,535 | 70.73M | 43,238 | 32,611 | 0.607 | 58 |
| 36065 | Oneida | suburb | 100,408 | 106,687 | 1,057 | 43,987 | 66.67M | 30,229 | 42,342 | 0.719 | 51 |
| 36067 | Onondaga | suburb | 222,274 | 249,719 | 923 | 41,035 | 130.33M | 38,280 | 90,440 | 0.724 | 84 |
| 36069 | Ontario | suburb | 54,283 | 54,010 | 1,037 | 58,875 | 27.21M | 53,586 | 65,085 | 0.676 | 92 |
| 36071 | Orange | suburb | 183,472 | 162,746 | 1,037 | 18,064 | 71.60M | 34,620 | 28,812 | 0.662 | 71 |
| 36073 | Orleans | suburb | 17,535 | 12,401 | 840 | 49,462 | 9.67M | 51,497 | 41,515 | 0.694 | 90* |
| 36075 | Oswego | suburb | 53,261 | 39,044 | 795 | 17,824 | 29.59M | 27,142 | 20,771 | 0.834 | 62 |
| 36077 | Otsego | rural | 26,908 | 26,515 | 960 | 32,307 | 13.98M | 26,607 | 26,029 | 0.766 | 38 |
| 36079 | Putnam | suburb | 49,087 | 31,523 | 89 | 181 | 11.64M | 43,052 | 19,750 | 0.727 | 90* |
| 36081 | Queens | suburb | 1,112,766 | 796,674 | 0 | 16 | 277.54M | 0 | n/a | 0.913 | 90* |
| 36083 | Rensselaer | suburb | 78,978 | 67,032 | 583 | 16,374 | 31.34M | 35,452 | 27,429 | 0.760 | 50 |
| 36085 | Richmond | suburb | 221,119 | 145,073 | 0 | 41 | 89.70M | 0 | n/a | 1.000 | 90* |
| 36087 | Rockland | suburb | 144,661 | 124,004 | 52 | 72 | 72.32M | 36,737 | 22,025 | 0.394 | 90* |
| 36089 | St. Lawrence | rural | 43,767 | 40,653 | 1,554 | 40,427 | 27.40M | 32,838 | 67,945 | 0.805 | 68 |
| 36091 | Saratoga | suburb | 123,295 | 102,131 | 730 | 13,427 | 52.37M | 42,644 | 45,727 | 0.699 | 54 |
| 36093 | Schenectady | suburb | 75,018 | 68,430 | 152 | 3,968 | 41.12M | 20,507 | 81 | 0.746 | 90* |
| 36095 | Schoharie | suburb | 13,550 | 9,779 | 534 | 20,930 | 8.82M | 33,894 | 41,243 | 0.682 | 30 |
| 36097 | Schuyler | rural | 7,982 | 5,839 | 423 | 13,669 | 5.24M | 37,461 | 51,172 | 0.748 | 50 |
| 36099 | Seneca | rural | 14,480 | 13,846 | 740 | 40,039 | 9.15M | 33,479 | 59,584 | 0.708 | 74 |
| 36101 | Steuben | rural | 41,256 | 40,285 | 1,723 | 69,332 | 26.16M | 36,309 | 43,921 | 0.766 | 46 |
| 36103 | Suffolk | suburb | 765,877 | 678,895 | 2,301 | 2,813 | 512.39M | 42,199 | 36,018 | 0.660 | 122 |
| 36105 | Sullivan | rural | 33,267 | 28,523 | 309 | 5,203 | 15.47M | 29,738 | 2,021 | 0.634 | 90* |
| 36107 | Tioga | suburb | 22,405 | 14,692 | 451 | 14,112 | 11.48M | 32,627 | 27,467 | 0.798 | 18 |
| 36109 | Tompkins | suburb | 48,267 | 58,408 | 737 | 21,929 | 20.39M | 30,253 | 36,758 | 0.697 | 48 |
| 36111 | Ulster | suburb | 83,839 | 71,908 | 721 | 8,511 | 34.95M | 34,011 | 21,841 | 0.836 | 118 |
| 36113 | Warren | suburb | 31,577 | 36,910 | 126 | 551 | 21.90M | 38,368 | 12,049 | 0.853 | 90* |
| 36115 | Washington | suburb | 27,765 | 17,877 | 1,053 | 32,095 | 16.75M | 37,100 | 40,318 | 0.719 | 60 |
| 36117 | Wayne | suburb | 42,736 | 31,125 | 1,360 | 47,743 | 19.09M | 44,552 | 30,173 | 0.718 | 68 |
| 36119 | Westchester | suburb | 485,163 | 465,577 | 296 | 250 | 209.88M | 43,020 | 28,129 | 0.889 | 90* |
| 36121 | Wyoming | rural | 17,810 | 14,319 | 1,203 | 61,885 | 9.11M | 53,017 | 114,077 | 0.668 | 115 |
| 36123 | Yates | rural | 10,662 | 8,629 | 854 | 31,475 | 7.25M | 40,282 | 42,819 | 0.760 | 98 |
| EXT | External (out-of-state commuting) | external | 572,504 | 189,906 | 849 | 30,082 | 239.37M | 37,876 | n/a | 0.728 | n/a |

`*` filled, see above.
