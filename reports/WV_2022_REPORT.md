# West Virginia 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state WV 2022`. 55 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 54 | `WV/CDL_2022_54.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=54 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_WV.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 1,775,156 | 1,775,156 | 0.000% |
| ACS workers by residence | 723,217 | 723,217 | 0.000% |
| ACS workers by workplace | 704,554 | 704,554 | 0.000% |
| ACS workers working out of state | 91,016 | 91,016 | 0.000% |
| BEA non-farm employment (L80) | 868,272 | 868,272 | 0.000% |
| BEA farm employment (L70) | 22,338 | 22,338 | 0.000% |
| BEA farm proprietors (L50) | 20,655 | 20,655 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 48,900,000 | 48,900,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 42,447,000 | 42,447,000 | 0.000% |
| CoA hired farm labour expense $ | 58,091,000 | 58,253,000 | -0.278% |
| BEA non-farm earnings $ (CAINC5N L82) | 51,589,647,000 | 51,589,647,000 | 0.000% |
| ACS foreign born entered 2010+ | 9,477 | 9,477 | 0.000% |
| CoA owned acres | 2,765,381 | 2,768,524 | -0.114% |
| CoA rented-from-others acres | 780,153 | 780,580 | -0.055% |
| CoA land in farms, ha | 1,436,271 | 1,436,271 | 0.000% |
| CoA total cropland, ha | 354,907 | 355,193 | -0.081% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.436, median 0.771, max 0.997; BEA counts jobs, ACS counts people by main job). Sum N = 795,570 = sum HU + HA = 795,570. Farm jobs after scaling: 16,519 (BEA 22,338). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 72,353. Jobs = in-state residents working out of state = 91,016, split by the state farm share (HA = 2,134). Location: the 34 out-of-state counties within 1 km of the state (21019, 21127, 21159, 21195, 24001, 24023, 24043, 39009, 39013, 39029, 39053, 39081, 39087, 39105, 39111, 39167, 42007, 42051, 42059, 42125, 51005, 51015, 51017, 51021, 51027, 51043, 51045, 51069, 51071, 51091, 51107, 51165, 51171, 51185); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 278,371 ha vs Census of Agriculture cropland 355,193 ha and land in farms 1,436,271 ha; county ratio TF / CoA cropland 0.18 to 2.26. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 340,723 ha). County area covered by CDL pixels: 6,275,555 ha vs land area 6,226,646 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 1.53 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (59,416 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 21,949 $ per BEA farm job, 29,680 $ per farm worker; county range 3,943 to 66,445 $ per worker. State compensation per farm wage job by year: 2018 22,529 $, 2019 19,023 $, 2020 20,017 $, 2021 18,658 $, 2022 25,221 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 14,376,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (58,253,000 $ in 2022, column `hired_labor_coa_usd`) is 1.37x BEA farm compensation (42,447,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 2,189 $, county -18,076 to 59,483 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 74,981 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 190,322,000 $ vs CAINC45 48,900,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.780, county range 0.475 to 0.949.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 42 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,303 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 10 counties have no recent foreign born in the ACS sample (Clay, Doddridge, Lewis, Mineral, Pleasants, Summers, Tyler, Webster, Wirt, Wyoming), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Kanawha); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (19); rural = the rest (35). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 2 counties have no BEA farm jobs (McDowell, Mingo); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 182.0 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 50.0 straight-line km/h between counties (median 9.2 to 32.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.46).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 54047 McDowell | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 54059 Mingo | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 54005 Boone | state owner share |
| omega | 54047 McDowell | state owner share |
| cash_rent_usd_acre | 54005 Boone | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54009 Brooke | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54011 Cabell | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54015 Clay | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54017 Doddridge | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54019 Fayette | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54021 Gilmer | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54023 Grant | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54029 Hancock | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54035 Jackson | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54039 Kanawha | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54041 Lewis | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54043 Lincoln | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54045 Logan | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54047 McDowell | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54049 Marion | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54051 Marshall | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54059 Mingo | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54067 Nicholas | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54069 Ohio | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54073 Pleasants | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54079 Putnam | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54089 Summers | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54091 Taylor | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54095 Tyler | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54097 Upshur | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54099 Wayne | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54101 Webster | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54103 Wetzel | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| cash_rent_usd_acre | 54109 Wyoming | not published; NASS 'other (combined) counties' value = 26.5 $/acre |
| owned_acres | 54005 Boone | (D) in Census of Ag; see fills above |
| owned_acres | 54047 McDowell | (D) in Census of Ag; see fills above |
| rented_acres | 54005 Boone | (D) in Census of Ag; see fills above |
| rented_acres | 54047 McDowell | (D) in Census of Ag; see fills above |
| farm_comp_per_ws_job | 54005 Boone | 2018: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54045 Logan | 2018: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54109 Wyoming | 2018: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54005 Boone | 2019: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54045 Logan | 2019: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54109 Wyoming | 2019: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54005 Boone | 2020: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54045 Logan | 2020: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54109 Wyoming | 2020: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54005 Boone | 2021: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54045 Logan | 2021: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54109 Wyoming | 2021: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54005 Boone | 2022: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54045 Logan | 2022: compensation (D) or no farm wage jobs; state value |
| farm_comp_per_ws_job | 54109 Wyoming | 2022: compensation (D) or no farm wage jobs; state value |
| hired_labor_coa_usd | 54005 Boone | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 54047 McDowell | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 54059 Mingo | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 54101 Webster | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 54109 Wyoming | (D) in Census of Ag; left null (comparison column only) |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26917) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 54001 | Barbour | rural | 5,578 | 3,264 | 321 | 2,266 | 3.55M | 18,593 | -5,374 | 0.586 | 19 |
| 54003 | Berkeley | suburb | 61,078 | 42,153 | 628 | 14,894 | 28.18M | 32,700 | 1,524 | 0.699 | 35 |
| 54005 | Boone | suburb | 7,010 | 5,715 | 19 | 365 | 3.77M | 22,404 | -8,842 | 0.780 | 26* |
| 54007 | Braxton | rural | 3,730 | 3,258 | 265 | 4,254 | 3.33M | 43,842 | 6,730 | 0.732 | 18 |
| 54009 | Brooke | suburb | 9,282 | 9,097 | 87 | 1,648 | 7.03M | 8,695 | -8,700 | 0.804 | 26* |
| 54011 | Cabell | suburb | 39,546 | 52,862 | 310 | 2,250 | 35.85M | 35,871 | -874 | 0.922 | 26* |
| 54013 | Calhoun | rural | 1,794 | 1,037 | 99 | 2,535 | 1.43M | 35,636 | -6,588 | 0.830 | 36 |
| 54015 | Clay | suburb | 2,519 | 1,435 | 82 | 1,395 | 1.45M | 8,471 | -588 | 0.923 | 26* |
| 54017 | Doddridge | rural | 2,927 | 1,640 | 268 | 1,150 | 1.70M | 13,783 | -9,752 | 0.847 | 26* |
| 54019 | Fayette | suburb | 13,818 | 10,011 | 171 | 4,519 | 9.07M | 37,551 | 1,648 | 0.836 | 26* |
| 54021 | Gilmer | rural | 2,245 | 2,096 | 179 | 1,949 | 1.79M | 31,626 | -8,648 | 0.784 | 26* |
| 54023 | Grant | rural | 4,973 | 3,732 | 403 | 7,448 | 4.64M | 20,001 | 10,589 | 0.766 | 26* |
| 54025 | Greenbrier | rural | 13,148 | 13,292 | 739 | 23,004 | 10.47M | 20,172 | 4,034 | 0.635 | 40 |
| 54027 | Hampshire | suburb | 8,516 | 4,164 | 493 | 8,614 | 5.96M | 31,121 | 10,587 | 0.744 | 21 |
| 54029 | Hancock | suburb | 12,409 | 10,156 | 86 | 910 | 11.32M | 19,839 | -5,748 | 0.758 | 26* |
| 54031 | Hardy | rural | 6,157 | 6,260 | 547 | 10,758 | 6.16M | 26,567 | 59,483 | 0.693 | 44 |
| 54033 | Harrison | rural | 28,346 | 37,636 | 628 | 4,106 | 20.81M | 27,134 | -4,828 | 0.800 | 13 |
| 54035 | Jackson | rural | 10,149 | 7,692 | 510 | 9,669 | 10.37M | 31,005 | -9,568 | 0.789 | 26* |
| 54037 | Jefferson | suburb | 27,856 | 19,006 | 461 | 18,324 | 10.21M | 41,617 | 6,124 | 0.602 | 68 |
| 54039 | Kanawha | core | 76,292 | 95,437 | 172 | 2,307 | 51.68M | 43,044 | -6,413 | 0.942 | 26* |
| 54041 | Lewis | rural | 6,537 | 5,613 | 346 | 1,791 | 4.49M | 30,295 | -30 | 0.718 | 26* |
| 54043 | Lincoln | rural | 6,418 | 2,729 | 129 | 1,486 | 3.32M | 34,125 | -12,043 | 0.949 | 26* |
| 54045 | Logan | rural | 9,181 | 10,158 | 9 | 270 | 5.11M | 26,940 | 9,273 | 0.860 | 26* |
| 54047 | McDowell | rural | 3,175 | 3,333 | 0 | 150 | 3.23M | 0 | n/a | 0.780 | 26* |
| 54049 | Marion | rural | 24,828 | 19,254 | 431 | 4,541 | 15.95M | 14,660 | -7,972 | 0.879 | 26* |
| 54051 | Marshall | suburb | 12,888 | 10,329 | 543 | 6,490 | 11.47M | 18,914 | -14,674 | 0.927 | 26* |
| 54053 | Mason | rural | 9,091 | 5,612 | 833 | 16,636 | 8.49M | 31,655 | 11,855 | 0.758 | 88 |
| 54055 | Mercer | rural | 22,693 | 20,895 | 358 | 5,270 | 17.51M | 19,278 | 17,413 | 0.825 | 30 |
| 54057 | Mineral | rural | 11,553 | 7,931 | 309 | 4,359 | 7.60M | 26,470 | 2,630 | 0.787 | 18 |
| 54059 | Mingo | rural | 6,017 | 4,539 | 0 | 181 | 4.40M | 0 | n/a | 0.475 | 26* |
| 54061 | Monongalia | suburb | 53,500 | 64,497 | 402 | 5,897 | 30.95M | 33,634 | -5,025 | 0.908 | 12 |
| 54063 | Monroe | rural | 4,208 | 1,841 | 452 | 16,092 | 4.00M | 36,780 | 1,988 | 0.766 | 40 |
| 54065 | Morgan | suburb | 7,721 | 3,436 | 135 | 3,242 | 3.74M | 24,178 | 541 | 0.801 | 24 |
| 54067 | Nicholas | rural | 9,044 | 7,691 | 333 | 6,876 | 6.31M | 12,130 | -3,015 | 0.808 | 26* |
| 54069 | Ohio | suburb | 18,314 | 29,244 | 168 | 3,010 | 11.27M | 36,420 | -18,076 | 0.838 | 26* |
| 54071 | Pendleton | rural | 2,432 | 1,249 | 309 | 11,334 | 4.38M | 33,109 | 44,955 | 0.736 | 40 |
| 54073 | Pleasants | rural | 2,989 | 2,597 | 118 | 492 | 3.50M | 18,572 | -13,448 | 0.823 | 26* |
| 54075 | Pocahontas | rural | 2,486 | 2,307 | 208 | 9,134 | 3.05M | 38,140 | 1,830 | 0.790 | 33 |
| 54077 | Preston | suburb | 13,272 | 7,281 | 740 | 10,852 | 8.61M | 30,196 | -2,720 | 0.846 | 28 |
| 54079 | Putnam | suburb | 25,790 | 22,231 | 465 | 6,517 | 19.07M | 46,792 | 6,998 | 0.881 | 26* |
| 54081 | Raleigh | suburb | 26,338 | 30,203 | 261 | 4,028 | 21.84M | 15,943 | -3,898 | 0.857 | 32 |
| 54083 | Randolph | rural | 10,436 | 11,112 | 329 | 3,652 | 9.01M | 26,924 | 6,237 | 0.813 | 33 |
| 54085 | Ritchie | rural | 2,859 | 3,375 | 314 | 2,423 | 2.61M | 24,460 | 1,964 | 0.817 | 12 |
| 54087 | Roane | rural | 4,125 | 3,120 | 378 | 8,528 | 3.16M | 66,445 | -4,920 | 0.769 | 18 |
| 54089 | Summers | rural | 3,356 | 2,131 | 220 | 6,657 | 2.76M | 35,184 | -4,803 | 0.758 | 26* |
| 54091 | Taylor | rural | 6,456 | 3,942 | 336 | 3,253 | 3.50M | 35,254 | -3,891 | 0.804 | 26* |
| 54093 | Tucker | rural | 2,972 | 2,463 | 107 | 1,079 | 2.33M | 36,077 | 16,689 | 0.760 | 25 |
| 54095 | Tyler | rural | 2,925 | 2,244 | 240 | 2,215 | 2.55M | 37,298 | -3,443 | 0.793 | 26* |
| 54097 | Upshur | rural | 9,267 | 7,669 | 318 | 1,400 | 6.91M | 41,826 | -8,861 | 0.687 | 26* |
| 54099 | Wayne | suburb | 13,872 | 9,003 | 157 | 1,546 | 8.68M | 19,384 | 1,364 | 0.896 | 26* |
| 54101 | Webster | rural | 2,578 | 1,911 | 59 | 1,040 | 2.00M | 3,943 | 3,969 | 0.855 | 26* |
| 54103 | Wetzel | rural | 5,082 | 5,024 | 223 | 1,710 | 4.06M | 24,933 | -4,713 | 0.948 | 26* |
| 54105 | Wirt | suburb | 1,949 | 752 | 134 | 1,666 | 1.29M | 37,126 | -12,037 | 0.866 | 18 |
| 54107 | Wood | suburb | 35,520 | 37,781 | 665 | 1,838 | 30.30M | 28,214 | -8,605 | 0.900 | 31 |
| 54109 | Wyoming | rural | 5,972 | 4,597 | 20 | 350 | 3.82M | 28,903 | -9,000 | 0.885 | 26* |
| EXT | External (out-of-state commuting) | external | 72,353 | 88,882 | 2,134 | 35,961 | 51.03M | 29,680 | n/a | 0.780 | n/a |

`*` filled, see above.
