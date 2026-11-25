# Alabama 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state AL 2022`. 67 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 01 | `AL/CDL_2022_01.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=01 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R6_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip |
| ghsl_R6_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_AL.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 5,074,296 | 5,074,296 | 0.000% |
| ACS workers by residence | 2,183,677 | 2,183,677 | 0.000% |
| ACS workers by workplace | 2,144,623 | 2,144,623 | 0.000% |
| ACS workers working out of state | 90,942 | 90,942 | 0.000% |
| BEA non-farm employment (L80) | 2,828,727 | 2,828,727 | 0.000% |
| BEA farm employment (L70) | 41,204 | 41,204 | 0.000% |
| BEA farm proprietors (L50) | 33,784 | 33,784 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 1,688,831,000 | 1,688,831,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 155,935,000 | 155,935,000 | 0.000% |
| CoA hired farm labour expense $ | 313,996,000 | 314,000,000 | -0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 166,305,598,000 | 166,305,598,000 | 0.000% |
| ACS foreign born entered 2010+ | 58,370 | 58,370 | 0.000% |
| CoA owned acres | 6,208,442 | 6,208,442 | 0.000% |
| CoA rented-from-others acres | 2,420,659 | 2,420,659 | 0.000% |
| CoA land in farms, ha | 3,492,073 | 3,492,073 | 0.000% |
| CoA total cropland, ha | 1,188,380 | 1,188,380 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.519, median 0.728, max 0.874; BEA counts jobs, ACS counts people by main job). Sum N = 2,235,565 = sum HU + HA = 2,235,565. Farm jobs after scaling: 29,972 (BEA 41,204). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 51,888. Jobs = in-state residents working out of state = 90,942, split by the state farm share (HA = 1,271). Location: the 42 out-of-state counties within 1 km of the state (12033, 12059, 12063, 12091, 12113, 12131, 13045, 13053, 13055, 13061, 13083, 13099, 13115, 13143, 13145, 13149, 13215, 13233, 13239, 13253, 13259, 13285, 13295, 28023, 28039, 28041, 28057, 28059, 28069, 28075, 28087, 28095, 28103, 28141, 28153, 47051, 47055, 47071, 47099, 47103, 47115, 47181); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,052,750 ha vs Census of Agriculture cropland 1,188,380 ha and land in farms 3,492,073 ha; county ratio TF / CoA cropland 0.35 to 1.48. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,590,458 ha). County area covered by CDL pixels: 13,389,278 ha vs land area 13,118,504 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 5.69 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (58,792 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 23,045 $ per BEA farm job, 31,681 $ per farm worker; county range 10,930 to 63,202 $ per worker. State compensation per farm wage job by year: 2018 22,803 $, 2019 21,269 $, 2020 19,941 $, 2021 24,822 $, 2022 21,015 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 55,531,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (314,000,000 $ in 2022, column `hired_labor_coa_usd`) is 2.01x BEA farm compensation (155,935,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 40,987 $, county -30,358 to 148,805 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 78,644 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,274,726,000 $ vs CAINC45 1,688,831,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.719, county range 0.389 to 0.899.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 66 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,659 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (Clay, Conecuh, Henry), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Jefferson); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (30); rural = the rest (36). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 194.2 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 59.0 straight-line km/h between counties (median 19.7 to 34.0 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.23).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 01013 Butler | not published; NASS 'other (combined) counties' value = 43.5 $/acre |
| cash_rent_usd_acre | 01037 Coosa | not published; NASS 'other (combined) counties' value = 43.5 $/acre |
| cash_rent_usd_acre | 01073 Jefferson | not published; NASS 'other (combined) counties' value = 43.5 $/acre |
| cash_rent_usd_acre | 01123 Tallapoosa | not published; NASS 'other (combined) counties' value = 43.5 $/acre |
| cash_rent_usd_acre | 01129 Washington | not published; NASS 'other (combined) counties' value = 43.5 $/acre |

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
| 01001 | Autauga | suburb | 27,031 | 14,312 | 283 | 16,840 | 17.29M | 26,566 | 31,804 | 0.665 | 51 |
| 01003 | Baldwin | suburb | 105,865 | 91,127 | 757 | 43,339 | 66.91M | 43,048 | -3,065 | 0.672 | 72 |
| 01005 | Barbour | rural | 8,341 | 7,625 | 350 | 23,659 | 9.47M | 46,910 | 76,473 | 0.817 | 50 |
| 01007 | Bibb | suburb | 8,064 | 4,714 | 93 | 3,019 | 5.38M | 43,620 | -9,119 | 0.865 | 15 |
| 01009 | Blount | suburb | 24,402 | 9,283 | 689 | 11,114 | 15.38M | 34,339 | 83,387 | 0.801 | 28 |
| 01011 | Bullock | rural | 3,679 | 3,049 | 408 | 9,300 | 3.06M | 21,084 | 22,817 | 0.726 | 26 |
| 01013 | Butler | rural | 7,394 | 6,335 | 268 | 8,321 | 7.17M | 37,873 | 126,740 | 0.846 | 44* |
| 01015 | Calhoun | suburb | 48,898 | 48,696 | 487 | 8,896 | 57.18M | 36,230 | 29,758 | 0.734 | 70 |
| 01017 | Chambers | rural | 14,660 | 8,821 | 209 | 4,286 | 10.85M | 32,731 | 30,606 | 0.789 | 40 |
| 01019 | Cherokee | rural | 10,079 | 5,901 | 404 | 19,726 | 9.41M | 47,584 | 82,210 | 0.602 | 105 |
| 01021 | Chilton | suburb | 18,524 | 10,460 | 353 | 6,447 | 11.21M | 36,829 | -8,024 | 0.795 | 20 |
| 01023 | Choctaw | rural | 4,402 | 3,968 | 138 | 1,248 | 5.17M | 12,236 | 50,514 | 0.894 | 30 |
| 01025 | Clarke | rural | 7,694 | 7,830 | 152 | 2,291 | 7.67M | 17,079 | 14,155 | 0.814 | 20 |
| 01027 | Clay | rural | 5,176 | 4,465 | 268 | 4,015 | 5.26M | 19,120 | 85,743 | 0.768 | 20 |
| 01029 | Cleburne | rural | 5,593 | 2,408 | 209 | 2,614 | 4.72M | 40,094 | 124,883 | 0.745 | 32 |
| 01031 | Coffee | rural | 22,669 | 18,352 | 657 | 34,129 | 19.16M | 36,304 | 74,349 | 0.708 | 54 |
| 01033 | Colbert | suburb | 25,195 | 25,789 | 497 | 24,220 | 32.50M | 32,558 | -5,477 | 0.603 | 100 |
| 01035 | Conecuh | rural | 3,664 | 2,841 | 177 | 11,174 | 4.09M | 31,077 | 50,667 | 0.738 | 36 |
| 01037 | Coosa | rural | 3,851 | 1,737 | 96 | 1,497 | 2.61M | 24,027 | -441 | 0.899 | 44* |
| 01039 | Covington | rural | 14,928 | 13,080 | 773 | 27,135 | 16.82M | 27,178 | 49,998 | 0.843 | 56 |
| 01041 | Crenshaw | rural | 5,128 | 3,533 | 381 | 11,846 | 5.59M | 20,833 | 148,805 | 0.824 | 26 |
| 01043 | Cullman | rural | 38,671 | 33,557 | 1,537 | 11,688 | 34.14M | 21,965 | 78,504 | 0.747 | 54 |
| 01045 | Dale | rural | 19,769 | 21,185 | 367 | 24,076 | 14.29M | 25,074 | 135,658 | 0.705 | 51 |
| 01047 | Dallas | rural | 14,138 | 12,078 | 417 | 29,676 | 16.04M | 43,607 | 18,707 | 0.730 | 39 |
| 01049 | DeKalb | rural | 30,290 | 24,214 | 1,422 | 25,222 | 28.11M | 39,939 | 95,335 | 0.722 | 48 |
| 01051 | Elmore | suburb | 38,872 | 21,113 | 350 | 12,773 | 19.52M | 33,253 | -1,489 | 0.663 | 39 |
| 01053 | Escambia | rural | 12,733 | 12,953 | 307 | 27,109 | 14.31M | 31,625 | -30,358 | 0.658 | 80 |
| 01055 | Etowah | suburb | 43,715 | 37,173 | 583 | 9,208 | 43.57M | 21,991 | 33,801 | 0.688 | 48 |
| 01057 | Fayette | rural | 6,236 | 4,477 | 289 | 6,792 | 5.20M | 32,865 | 9,975 | 0.838 | 36 |
| 01059 | Franklin | rural | 13,403 | 12,508 | 651 | 8,716 | 12.27M | 24,638 | 51,890 | 0.762 | 78 |
| 01061 | Geneva | suburb | 10,627 | 5,213 | 581 | 46,179 | 10.53M | 35,577 | 39,089 | 0.718 | 56 |
| 01063 | Greene | suburb | 2,170 | 1,575 | 150 | 5,015 | 3.00M | 49,394 | -2,738 | 0.843 | 20 |
| 01065 | Hale | suburb | 5,358 | 2,519 | 243 | 6,807 | 4.48M | 63,202 | 9,004 | 0.739 | 34 |
| 01067 | Henry | suburb | 7,154 | 4,259 | 332 | 36,283 | 5.84M | 33,726 | 106,574 | 0.697 | 50 |
| 01069 | Houston | suburb | 45,364 | 51,565 | 560 | 57,722 | 48.99M | 35,516 | -3,853 | 0.575 | 58 |
| 01071 | Jackson | rural | 20,023 | 15,764 | 881 | 37,138 | 21.44M | 28,412 | 45,486 | 0.635 | 60 |
| 01073 | Jefferson | core | 306,222 | 373,054 | 244 | 1,608 | 304.45M | 30,436 | -18,114 | 0.812 | 44* |
| 01075 | Lamar | rural | 5,222 | 3,688 | 227 | 5,724 | 5.17M | 23,259 | 2,638 | 0.895 | 28 |
| 01077 | Lauderdale | suburb | 42,958 | 37,226 | 1,063 | 32,233 | 39.51M | 22,610 | -3,106 | 0.524 | 86 |
| 01079 | Lawrence | suburb | 13,720 | 5,286 | 807 | 39,510 | 12.75M | 47,031 | 17,717 | 0.495 | 105 |
| 01081 | Lee | suburb | 80,729 | 71,073 | 223 | 4,549 | 47.82M | 34,770 | 7,850 | 0.815 | 24 |
| 01083 | Limestone | suburb | 47,315 | 34,275 | 979 | 50,216 | 32.09M | 22,455 | 19,397 | 0.389 | 124 |
| 01085 | Lowndes | suburb | 3,642 | 2,054 | 259 | 14,843 | 4.38M | 47,181 | 60,122 | 0.714 | 38 |
| 01087 | Macon | suburb | 6,787 | 5,873 | 298 | 8,832 | 5.72M | 44,002 | -13,670 | 0.876 | 46 |
| 01089 | Madison | suburb | 191,093 | 227,811 | 778 | 46,150 | 162.12M | 26,518 | -14,897 | 0.442 | 88 |
| 01091 | Marengo | rural | 7,399 | 6,041 | 260 | 14,392 | 8.00M | 40,513 | 10,975 | 0.782 | 48 |
| 01093 | Marion | rural | 11,051 | 9,746 | 414 | 9,298 | 10.63M | 22,351 | 70,480 | 0.764 | 31 |
| 01095 | Marshall | rural | 40,866 | 41,124 | 1,081 | 15,531 | 35.78M | 30,638 | 59,614 | 0.727 | 44 |
| 01097 | Mobile | suburb | 173,909 | 182,938 | 659 | 18,588 | 145.46M | 41,673 | 17,717 | 0.751 | 57 |
| 01099 | Monroe | rural | 6,220 | 5,784 | 264 | 18,814 | 7.95M | 41,000 | 7,960 | 0.763 | 58 |
| 01101 | Montgomery | suburb | 98,021 | 135,151 | 516 | 17,100 | 114.67M | 26,544 | 25,559 | 0.664 | 24 |
| 01103 | Morgan | suburb | 54,268 | 55,340 | 903 | 14,261 | 65.22M | 25,299 | 11,997 | 0.729 | 54 |
| 01105 | Perry | rural | 2,156 | 1,783 | 236 | 19,771 | 2.80M | 32,124 | 23,024 | 0.776 | 46 |
| 01107 | Pickens | suburb | 6,691 | 3,745 | 269 | 7,683 | 7.02M | 31,197 | 80,279 | 0.710 | 28 |
| 01109 | Pike | rural | 13,338 | 16,098 | 448 | 20,424 | 13.09M | 35,701 | 72,305 | 0.846 | 30 |
| 01111 | Randolph | rural | 8,456 | 5,420 | 388 | 4,574 | 8.11M | 27,764 | 133,933 | 0.878 | 28 |
| 01113 | Russell | suburb | 23,566 | 15,228 | 215 | 8,508 | 18.93M | 38,346 | 14,342 | 0.850 | 28 |
| 01115 | St. Clair | suburb | 41,302 | 25,164 | 380 | 4,014 | 20.06M | 43,179 | 28,155 | 0.693 | 19 |
| 01117 | Shelby | suburb | 112,772 | 94,946 | 271 | 6,450 | 65.19M | 29,314 | 3,685 | 0.703 | 26 |
| 01119 | Sumter | rural | 4,136 | 3,652 | 325 | 5,570 | 4.02M | 24,826 | 44,911 | 0.787 | 22 |
| 01121 | Talladega | rural | 31,194 | 32,892 | 409 | 16,456 | 25.76M | 28,151 | 15,183 | 0.735 | 50 |
| 01123 | Tallapoosa | rural | 15,388 | 12,738 | 194 | 2,947 | 12.01M | 19,451 | 29,316 | 0.721 | 44* |
| 01125 | Tuscaloosa | suburb | 107,697 | 116,528 | 392 | 6,659 | 77.09M | 25,451 | 12,426 | 0.723 | 48 |
| 01127 | Walker | suburb | 25,402 | 19,556 | 313 | 2,914 | 19.46M | 32,135 | 49,522 | 0.699 | 29 |
| 01129 | Washington | rural | 5,516 | 4,424 | 274 | 3,286 | 8.16M | 10,930 | 51,162 | 0.867 | 44* |
| 01131 | Wilcox | rural | 3,174 | 2,935 | 222 | 9,801 | 4.07M | 18,432 | 54,493 | 0.844 | 17 |
| 01133 | Winston | rural | 9,707 | 8,603 | 338 | 2,523 | 9.08M | 41,316 | 10,593 | 0.833 | 22 |
| EXT | External (out-of-state commuting) | external | 51,888 | 89,671 | 1,271 | 44,641 | 45.03M | 31,681 | n/a | 0.719 | n/a |

`*` filled, see above.
