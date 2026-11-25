# Kentucky 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state KY 2022`. 120 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 21 | `KY/CDL_2022_21.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=21 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_KY.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (16 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 4,512,310 | 4,512,310 | 0.000% |
| ACS workers by residence | 1,993,847 | 1,993,847 | 0.000% |
| ACS workers by workplace | 2,010,409 | 2,010,409 | 0.000% |
| ACS workers working out of state | 123,943 | 123,943 | 0.000% |
| BEA non-farm employment (L80) | 2,576,594 | 2,576,594 | 0.000% |
| BEA farm employment (L70) | 82,385 | 82,385 | 0.000% |
| BEA farm proprietors (L50) | 65,949 | 65,949 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,005,095,000 | 2,005,095,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 419,231,000 | 419,231,000 | 0.000% |
| CoA hired farm labour expense $ | 600,372,000 | 610,356,000 | -1.636% |
| BEA non-farm earnings $ (CAINC5N L82) | 156,767,203,000 | 156,767,203,000 | 0.000% |
| ACS foreign born entered 2010+ | 80,430 | 80,430 | 0.000% |
| CoA owned acres | 8,509,139 | 8,524,047 | -0.175% |
| CoA rented-from-others acres | 3,906,906 | 3,907,143 | -0.006% |
| CoA land in farms, ha | 5,030,724 | 5,030,724 | 0.000% |
| CoA total cropland, ha | 2,599,139 | 2,599,139 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.355, median 0.736, max 1.172; BEA counts jobs, ACS counts people by main job). Sum N = 2,134,352 = sum HU + HA = 2,134,352. Farm jobs after scaling: 58,679 (BEA 82,385). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 140,505. Jobs = in-state residents working out of state = 123,943, split by the state farm share (HA = 3,618). Location: the 47 out-of-state counties within 1 km of the state (17003, 17059, 17069, 17127, 17151, 17153, 18019, 18025, 18029, 18043, 18061, 18077, 18115, 18123, 18129, 18147, 18155, 18163, 18173, 29133, 29143, 39001, 39015, 39025, 39061, 39087, 39145, 47013, 47025, 47027, 47079, 47095, 47111, 47125, 47131, 47137, 47147, 47151, 47161, 47165, 47183, 51027, 51051, 51105, 51195, 54059, 54099); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 2,004,613 ha vs Census of Agriculture cropland 2,599,139 ha and land in farms 5,030,724 ha; county ratio TF / CoA cropland 0.00 to 1.26. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,673,225 ha). County area covered by CDL pixels: 10,465,233 ha vs land area 10,226,658 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 5.14 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (60,843 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 20,210 $ per BEA farm job, 28,375 $ per farm worker; county range 1,254 to 86,529 $ per worker. State compensation per farm wage job by year: 2018 22,265 $, 2019 18,935 $, 2020 20,107 $, 2021 18,703 $, 2022 25,507 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 90,499,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (610,356,000 $ in 2022, column `hired_labor_coa_usd`) is 1.46x BEA farm compensation (419,231,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 24,338 $, county -23,118 to 221,356 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 80,322 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,514,789,000 $ vs CAINC45 2,005,095,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.685, county range 0.100 to 0.982.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 156 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 4,929 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 10 counties have no recent foreign born in the ACS sample (Edmonson, Elliott, Fulton, Hancock, Lee, Livingston, Nicholas, Owsley, Powell, Rockcastle), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Jefferson); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (38); rural = the rest (81). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 174.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 63.3 straight-line km/h between counties (median 7.9 to 22.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.25).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| omega | 21095 Harlan | state owner share |
| omega | 21133 Letcher | state owner share |
| cash_rent_usd_acre | 21013 Bell | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21019 Boyd | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21021 Boyle | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21025 Breathitt | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21037 Campbell | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21063 Elliott | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21077 Gallatin | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21095 Harlan | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21103 Henry | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21109 Jackson | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21117 Kenton | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21119 Knott | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21121 Knox | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21127 Lawrence | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21129 Lee | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21131 Leslie | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21133 Letcher | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21153 Magoffin | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21159 Martin | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21165 Menifee | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21181 Nicholas | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21193 Perry | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21195 Pike | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21197 Powell | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21205 Rowan | not published; NASS 'other (combined) counties' value = 91 $/acre |
| cash_rent_usd_acre | 21223 Trimble | not published; NASS 'other (combined) counties' value = 91 $/acre |
| owned_acres | 21095 Harlan | (D) in Census of Ag; see fills above |
| owned_acres | 21133 Letcher | (D) in Census of Ag; see fills above |
| rented_acres | 21095 Harlan | (D) in Census of Ag; see fills above |
| rented_acres | 21133 Letcher | (D) in Census of Ag; see fills above |
| farm_comp_per_ws_job | 21013 Bell | 2018: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21159 Martin | 2018: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21013 Bell | 2019: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21159 Martin | 2019: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21013 Bell | 2020: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21159 Martin | 2020: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21013 Bell | 2021: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21159 Martin | 2021: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21013 Bell | 2022: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 21159 Martin | 2022: compensation (D) or no farm wage jobs; state value |
| hired_labor_coa_usd | 21131 Leslie | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 21205 Rowan | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 21213 Simpson | (D) in Census of Ag; left null (comparison column only) |

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
| 21001 | Adair | rural | 7,592 | 4,491 | 732 | 20,835 | 7.30M | 37,508 | 18,402 | 0.768 | 101 |
| 21003 | Allen | suburb | 8,711 | 5,368 | 775 | 17,051 | 5.71M | 20,266 | 23,600 | 0.754 | 107 |
| 21005 | Anderson | rural | 10,865 | 5,021 | 420 | 4,001 | 7.50M | 19,956 | -9,412 | 0.783 | 70 |
| 21007 | Ballard | suburb | 3,224 | 1,755 | 262 | 34,108 | 4.23M | 49,984 | 83,635 | 0.569 | 142 |
| 21009 | Barren | rural | 18,337 | 15,828 | 1,415 | 45,429 | 18.59M | 25,040 | 13,467 | 0.737 | 153 |
| 21011 | Bath | rural | 4,661 | 1,584 | 364 | 8,233 | 3.28M | 21,280 | -555 | 0.871 | 81 |
| 21013 | Bell | rural | 6,848 | 8,009 | 55 | 239 | 7.00M | 29,034 | -18,129 | 0.928 | 91* |
| 21015 | Boone | suburb | 69,275 | 94,003 | 472 | 5,038 | 60.06M | 30,320 | 7,762 | 0.826 | 70 |
| 21017 | Bourbon | suburb | 8,999 | 5,991 | 1,010 | 14,686 | 7.50M | 54,954 | 108,147 | 0.685 | 108 |
| 21019 | Boyd | suburb | 18,840 | 23,941 | 151 | 1,073 | 21.41M | 20,456 | -11,568 | 0.936 | 91* |
| 21021 | Boyle | rural | 12,192 | 15,346 | 509 | 13,439 | 12.67M | 21,800 | 3,866 | 0.586 | 91* |
| 21023 | Bracken | suburb | 3,557 | 1,387 | 319 | 3,996 | 2.85M | 25,976 | -2,787 | 0.882 | 60 |
| 21025 | Breathitt | rural | 4,508 | 3,049 | 113 | 485 | 3.06M | 15,384 | -1,899 | 0.911 | 91* |
| 21027 | Breckinridge | rural | 7,611 | 3,190 | 682 | 31,982 | 8.30M | 37,194 | 18,005 | 0.798 | 132 |
| 21029 | Bullitt | suburb | 40,309 | 29,439 | 363 | 4,958 | 28.16M | 18,035 | -7,119 | 0.810 | 74 |
| 21031 | Butler | suburb | 4,548 | 2,469 | 392 | 24,498 | 4.34M | 26,345 | 31,694 | 0.741 | 138 |
| 21033 | Caldwell | rural | 5,305 | 3,995 | 353 | 34,422 | 4.66M | 58,857 | 4,871 | 0.538 | 142 |
| 21035 | Calloway | rural | 17,096 | 17,202 | 749 | 38,268 | 16.37M | 26,245 | 35,854 | 0.560 | 140 |
| 21037 | Campbell | suburb | 47,046 | 34,309 | 401 | 1,804 | 30.19M | 18,116 | 2,838 | 0.876 | 91* |
| 21039 | Carlisle | suburb | 1,792 | 616 | 120 | 26,382 | 2.07M | 86,529 | 95,246 | 0.372 | 171 |
| 21041 | Carroll | rural | 4,464 | 6,649 | 193 | 3,884 | 9.75M | 29,557 | -2,887 | 0.810 | 58 |
| 21043 | Carter | suburb | 8,799 | 5,908 | 554 | 4,503 | 8.02M | 29,019 | -2,679 | 0.888 | 50 |
| 21045 | Casey | rural | 5,331 | 3,376 | 604 | 21,049 | 6.47M | 36,095 | -31 | 0.794 | 101 |
| 21047 | Christian | suburb | 30,102 | 48,588 | 960 | 78,232 | 27.27M | 47,877 | 44,032 | 0.541 | 180 |
| 21049 | Clark | suburb | 16,615 | 14,184 | 706 | 9,126 | 14.20M | 28,154 | -9,861 | 0.703 | 73 |
| 21051 | Clay | rural | 6,120 | 4,647 | 223 | 1,247 | 4.04M | 30,785 | 2,862 | 0.747 | 44 |
| 21053 | Clinton | rural | 3,710 | 3,922 | 436 | 8,591 | 3.84M | 17,347 | 39,360 | 0.718 | 88 |
| 21055 | Crittenden | rural | 3,374 | 1,823 | 400 | 26,129 | 3.44M | 21,315 | 18,887 | 0.575 | 160 |
| 21057 | Cumberland | rural | 2,193 | 1,609 | 182 | 7,001 | 2.37M | 23,772 | 6,408 | 0.798 | 108 |
| 21059 | Daviess | suburb | 46,641 | 47,448 | 808 | 65,419 | 46.09M | 32,761 | 64,067 | 0.435 | 194 |
| 21061 | Edmonson | suburb | 4,518 | 1,777 | 349 | 10,947 | 3.93M | 22,283 | 17,315 | 0.734 | 101 |
| 21063 | Elliott | rural | 1,818 | 913 | 214 | 2,344 | 1.79M | 15,153 | -906 | 0.811 | 91* |
| 21065 | Estill | rural | 4,572 | 2,432 | 233 | 3,134 | 3.58M | 31,415 | -5,501 | 0.847 | 32 |
| 21067 | Fayette | suburb | 165,422 | 196,542 | 1,600 | 8,147 | 140.58M | 43,894 | 85,547 | 0.791 | 85 |
| 21069 | Fleming | rural | 5,874 | 3,254 | 629 | 23,620 | 5.77M | 37,894 | 11,754 | 0.847 | 124 |
| 21071 | Floyd | rural | 10,890 | 9,370 | 66 | 14 | 6.81M | 11,368 | 8,433 | 0.942 | 52 |
| 21073 | Franklin | rural | 24,289 | 33,542 | 483 | 4,503 | 20.31M | 25,398 | 4,431 | 0.659 | 70 |
| 21075 | Fulton | rural | 2,160 | 2,207 | 172 | 35,075 | 2.90M | 38,766 | 97,785 | 0.369 | 178 |
| 21077 | Gallatin | suburb | 3,908 | 2,446 | 146 | 2,231 | 4.17M | 17,368 | 5,413 | 0.638 | 91* |
| 21079 | Garrard | rural | 7,139 | 2,569 | 470 | 11,102 | 5.52M | 22,823 | -5,440 | 0.715 | 50 |
| 21081 | Grant | suburb | 10,990 | 5,640 | 540 | 5,334 | 5.84M | 17,580 | -10,995 | 0.750 | 45 |
| 21083 | Graves | rural | 15,060 | 11,571 | 1,133 | 73,139 | 14.77M | 35,435 | 106,433 | 0.544 | 167 |
| 21085 | Grayson | rural | 10,404 | 7,547 | 896 | 26,230 | 11.01M | 20,925 | 11,378 | 0.784 | 106 |
| 21087 | Green | rural | 3,961 | 1,661 | 490 | 20,700 | 4.76M | 37,575 | 5,120 | 0.722 | 153 |
| 21089 | Greenup | suburb | 13,549 | 7,829 | 412 | 3,495 | 13.02M | 11,149 | -4,459 | 0.817 | 65 |
| 21091 | Hancock | rural | 3,917 | 4,878 | 335 | 11,412 | 6.20M | 16,488 | 10,926 | 0.546 | 146 |
| 21093 | Hardin | suburb | 49,975 | 53,233 | 1,069 | 42,372 | 35.57M | 21,407 | -1,666 | 0.704 | 124 |
| 21095 | Harlan | rural | 7,271 | 6,719 | 24 | 47 | 4.79M | 7,454 | -9,143 | 0.686 | 91* |
| 21097 | Harrison | rural | 8,227 | 5,525 | 879 | 14,606 | 6.09M | 21,701 | -5,567 | 0.717 | 92 |
| 21099 | Hart | rural | 7,675 | 5,308 | 1,045 | 24,005 | 7.40M | 12,791 | 5,885 | 0.810 | 146 |
| 21101 | Henderson | rural | 19,291 | 18,338 | 398 | 73,348 | 18.77M | 42,648 | 70,481 | 0.414 | 219 |
| 21103 | Henry | suburb | 6,857 | 3,242 | 608 | 16,276 | 5.25M | 28,273 | 403 | 0.743 | 91* |
| 21105 | Hickman | rural | 1,810 | 1,026 | 289 | 40,974 | 2.61M | 36,612 | 221,356 | 0.630 | 156 |
| 21107 | Hopkins | rural | 17,727 | 17,035 | 598 | 39,074 | 17.86M | 29,431 | 92,602 | 0.512 | 138 |
| 21109 | Jackson | rural | 4,274 | 1,655 | 304 | 3,432 | 3.27M | 20,733 | -4,870 | 0.735 | 91* |
| 21111 | Jefferson | core | 384,235 | 468,950 | 340 | 2,372 | 385.18M | 29,781 | 6,625 | 0.837 | 62 |
| 21113 | Jessamine | suburb | 24,518 | 20,789 | 597 | 5,713 | 18.49M | 25,158 | 144,078 | 0.675 | 58 |
| 21115 | Johnson | rural | 7,168 | 5,278 | 150 | 185 | 4.86M | 9,923 | -8,159 | 0.864 | 30 |
| 21117 | Kenton | suburb | 87,466 | 69,045 | 319 | 2,174 | 51.14M | 31,609 | -1,114 | 0.883 | 91* |
| 21119 | Knott | rural | 4,104 | 2,557 | 25 | 54 | 2.44M | 16,880 | -16,971 | 0.512 | 91* |
| 21121 | Knox | rural | 8,941 | 7,327 | 157 | 1,862 | 7.96M | 11,275 | -7,156 | 0.803 | 91* |
| 21123 | Larue | suburb | 6,371 | 2,405 | 407 | 28,789 | 5.41M | 30,235 | 2,329 | 0.626 | 165 |
| 21125 | Laurel | rural | 25,559 | 27,959 | 748 | 8,252 | 18.50M | 18,253 | -2,598 | 0.814 | 48 |
| 21127 | Lawrence | suburb | 4,394 | 2,849 | 146 | 708 | 3.64M | 10,622 | -2,687 | 0.864 | 91* |
| 21129 | Lee | rural | 2,232 | 1,756 | 109 | 547 | 1.82M | 15,538 | -9,543 | 0.802 | 91* |
| 21131 | Leslie | rural | 3,236 | 1,911 | 12 | 53 | 1.86M | 1,254 | -9,286 | 0.641 | 91* |
| 21133 | Letcher | rural | 6,866 | 5,067 | 46 | 4 | 3.89M | 6,117 | -3,635 | 0.686 | 91* |
| 21135 | Lewis | rural | 3,977 | 1,667 | 309 | 9,643 | 4.37M | 23,350 | 787 | 0.904 | 94 |
| 21137 | Lincoln | rural | 9,532 | 4,121 | 728 | 24,424 | 8.02M | 32,012 | 9,151 | 0.729 | 95 |
| 21139 | Livingston | suburb | 3,797 | 2,031 | 199 | 23,630 | 3.69M | 57,739 | 12,267 | 0.536 | 154 |
| 21141 | Logan | rural | 11,345 | 9,610 | 899 | 67,442 | 11.40M | 38,884 | 33,183 | 0.578 | 225 |
| 21143 | Lyon | rural | 3,086 | 2,602 | 151 | 10,344 | 2.84M | 26,668 | 1,768 | 0.697 | 132 |
| 21145 | McCracken | suburb | 29,475 | 40,567 | 372 | 20,127 | 32.45M | 17,758 | 8,799 | 0.399 | 137 |
| 21147 | McCreary | rural | 4,724 | 2,797 | 97 | 746 | 3.31M | 6,252 | -18,946 | 0.873 | 44 |
| 21149 | McLean | suburb | 3,687 | 1,879 | 365 | 42,367 | 5.27M | 45,008 | 181,090 | 0.594 | 172 |
| 21151 | Madison | rural | 43,928 | 39,920 | 1,068 | 13,281 | 28.10M | 18,790 | 5,327 | 0.692 | 28 |
| 21153 | Magoffin | rural | 2,859 | 1,617 | 264 | 910 | 2.81M | 8,859 | -4,362 | 0.835 | 91* |
| 21155 | Marion | rural | 7,362 | 7,796 | 720 | 26,970 | 8.51M | 22,813 | 7,448 | 0.702 | 163 |
| 21157 | Marshall | rural | 13,664 | 11,863 | 550 | 18,248 | 17.36M | 19,612 | 30,795 | 0.683 | 118 |
| 21159 | Martin | rural | 2,992 | 2,958 | 20 | 6 | 1.93M | 19,448 | -23,118 | 0.100 | 91* |
| 21161 | Mason | rural | 7,236 | 8,065 | 538 | 17,692 | 8.31M | 22,056 | 4,905 | 0.746 | 98 |
| 21163 | Meade | suburb | 13,684 | 6,881 | 691 | 20,117 | 8.20M | 15,181 | 1,613 | 0.643 | 149 |
| 21165 | Menifee | rural | 1,989 | 850 | 169 | 953 | 1.67M | 8,712 | -3,522 | 0.886 | 91* |
| 21167 | Mercer | rural | 9,949 | 6,856 | 735 | 16,972 | 9.21M | 37,084 | 5,934 | 0.600 | 77 |
| 21169 | Metcalfe | rural | 4,206 | 2,063 | 582 | 14,592 | 3.84M | 21,768 | -222 | 0.770 | 164 |
| 21171 | Monroe | rural | 4,782 | 3,357 | 596 | 15,258 | 5.12M | 23,703 | 44,645 | 0.808 | 135 |
| 21173 | Montgomery | rural | 11,427 | 11,304 | 438 | 5,894 | 8.90M | 30,211 | -1,710 | 0.717 | 66 |
| 21175 | Morgan | rural | 4,323 | 3,361 | 562 | 3,593 | 3.47M | 13,273 | -1,736 | 0.895 | 30 |
| 21177 | Muhlenberg | rural | 12,094 | 9,591 | 570 | 22,290 | 10.49M | 20,529 | 65,385 | 0.703 | 130 |
| 21179 | Nelson | suburb | 22,182 | 16,628 | 945 | 28,584 | 17.50M | 26,274 | 1,611 | 0.699 | 143 |
| 21181 | Nicholas | rural | 2,897 | 878 | 288 | 5,956 | 2.14M | 43,422 | 3,946 | 0.795 | 91* |
| 21183 | Ohio | rural | 9,620 | 7,343 | 703 | 36,905 | 8.81M | 32,558 | 62,331 | 0.735 | 158 |
| 21185 | Oldham | suburb | 32,388 | 20,211 | 341 | 5,128 | 15.25M | 37,787 | 23,375 | 0.828 | 112 |
| 21187 | Owen | rural | 4,839 | 2,058 | 510 | 9,390 | 3.65M | 15,868 | -8,658 | 0.786 | 64 |
| 21189 | Owsley | rural | 1,091 | 774 | 114 | 495 | 1.11M | 13,798 | -1,776 | 0.917 | 34 |
| 21191 | Pendleton | suburb | 6,637 | 2,449 | 467 | 8,236 | 3.91M | 46,853 | -5,970 | 0.864 | 45 |
| 21193 | Perry | rural | 9,916 | 11,799 | 38 | 175 | 6.73M | 22,800 | -4,341 | 0.982 | 91* |
| 21195 | Pike | rural | 18,901 | 22,012 | 55 | 10 | 10.93M | 12,291 | -969 | 0.632 | 91* |
| 21197 | Powell | rural | 4,637 | 2,635 | 135 | 2,145 | 3.20M | 27,334 | -1,121 | 0.757 | 91* |
| 21199 | Pulaski | rural | 26,510 | 26,457 | 1,250 | 28,130 | 27.13M | 29,453 | 2,305 | 0.719 | 110 |
| 21201 | Robertson | rural | 816 | 320 | 140 | 2,011 | 0.91M | 20,389 | 610 | 0.871 | 41 |
| 21203 | Rockcastle | rural | 5,875 | 4,304 | 706 | 6,745 | 4.85M | 7,397 | -2,224 | 0.800 | 82 |
| 21205 | Rowan | rural | 10,525 | 12,281 | 335 | 3,570 | 5.92M | 28,012 | -5,254 | 0.853 | 91* |
| 21207 | Russell | rural | 7,306 | 6,322 | 561 | 12,610 | 8.08M | 28,067 | 15,812 | 0.681 | 82 |
| 21209 | Scott | suburb | 28,795 | 30,875 | 981 | 9,133 | 19.61M | 28,509 | 15,864 | 0.686 | 89 |
| 21211 | Shelby | suburb | 23,908 | 18,457 | 1,338 | 29,940 | 16.77M | 30,851 | 4,395 | 0.612 | 140 |
| 21213 | Simpson | rural | 8,711 | 9,288 | 402 | 38,395 | 7.22M | 49,657 | 58,117 | 0.494 | 210 |
| 21215 | Spencer | suburb | 9,528 | 2,756 | 311 | 9,936 | 4.68M | 24,046 | 1,739 | 0.826 | 129 |
| 21217 | Taylor | rural | 11,795 | 12,193 | 664 | 20,135 | 10.88M | 25,794 | 1,999 | 0.753 | 148 |
| 21219 | Todd | rural | 4,967 | 2,610 | 548 | 49,446 | 5.88M | 37,441 | 67,380 | 0.565 | 207 |
| 21221 | Trigg | suburb | 5,676 | 3,776 | 368 | 25,902 | 4.64M | 42,511 | 29,361 | 0.605 | 176 |
| 21223 | Trimble | rural | 3,515 | 1,174 | 249 | 4,899 | 3.13M | 34,334 | -2,698 | 0.832 | 91* |
| 21225 | Union | rural | 5,643 | 5,312 | 364 | 59,348 | 5.91M | 38,203 | 55,991 | 0.355 | 231 |
| 21227 | Warren | suburb | 65,956 | 71,982 | 1,330 | 41,648 | 44.34M | 24,051 | 17,170 | 0.685 | 164 |
| 21229 | Washington | rural | 5,686 | 3,921 | 819 | 21,223 | 5.38M | 21,994 | 2,466 | 0.773 | 73 |
| 21231 | Wayne | rural | 6,769 | 5,436 | 750 | 13,208 | 7.65M | 36,987 | 26,100 | 0.777 | 117 |
| 21233 | Webster | rural | 5,288 | 3,364 | 479 | 42,014 | 5.38M | 30,178 | 139,074 | 0.493 | 195 |
| 21235 | Whitley | rural | 12,974 | 13,410 | 340 | 2,183 | 9.66M | 17,946 | -1,501 | 0.760 | 21 |
| 21237 | Wolfe | rural | 1,505 | 1,147 | 157 | 1,713 | 2.17M | 10,453 | -4,330 | 0.895 | 42 |
| 21239 | Woodford | suburb | 13,540 | 10,508 | 1,202 | 7,526 | 11.29M | 38,230 | 87,714 | 0.761 | 88 |
| EXT | External (out-of-state commuting) | external | 140,505 | 120,325 | 3,618 | 123,586 | 120.68M | 28,375 | n/a | 0.685 | n/a |

`*` filled, see above.
