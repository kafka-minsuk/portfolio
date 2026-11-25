# Utah 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state UT 2022`. 29 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 49 | `UT/CDL_2022_49.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=49 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_UT.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 3,380,800 | 3,380,800 | 0.000% |
| ACS workers by residence | 1,617,201 | 1,617,201 | 0.000% |
| ACS workers by workplace | 1,620,844 | 1,620,844 | 0.000% |
| ACS workers working out of state | 15,296 | 15,296 | 0.000% |
| BEA non-farm employment (L80) | 2,346,915 | 2,346,915 | 0.000% |
| BEA farm employment (L70) | 21,081 | 21,081 | 0.000% |
| BEA farm proprietors (L50) | 15,598 | 15,598 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 752,986,000 | 752,986,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 230,726,000 | 230,726,000 | 0.000% |
| CoA hired farm labour expense $ | 286,833,000 | 286,832,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 147,890,109,000 | 147,890,109,000 | 0.000% |
| ACS foreign born entered 2010+ | 80,714 | 80,714 | 0.000% |
| CoA owned acres | 8,857,808 | 8,857,808 | 0.000% |
| CoA rented-from-others acres | 1,637,115 | 1,637,115 | 0.000% |
| CoA land in farms, ha | 4,247,145 | 4,247,145 | 0.000% |
| CoA total cropland, ha | 584,405 | 584,405 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.479, median 0.668, max 0.824; BEA counts jobs, ACS counts people by main job). Sum N = 1,636,140 = sum HU + HA = 1,636,140. Farm jobs after scaling: 14,311 (BEA 21,081). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 18,939. Jobs = in-state residents working out of state = 15,296, split by the state farm share (HA = 135). Location: the 23 out-of-state counties within 1 km of the state (04001, 04005, 04015, 04017, 08033, 08045, 08077, 08081, 08083, 08085, 08103, 08113, 16007, 16031, 16041, 16071, 32007, 32017, 32033, 35045, 56023, 56037, 56041); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 643,614 ha vs Census of Agriculture cropland 584,405 ha and land in farms 4,247,145 ha; county ratio TF / CoA cropland 0.32 to 3.63. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 699,377 ha). County area covered by CDL pixels: 21,988,799 ha vs land area 21,392,128 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 3.07 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (63,015 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 45,712 $ per BEA farm job, 67,337 $ per farm worker; county range 26,323 to 102,572 $ per worker. State compensation per farm wage job by year: 2018 45,436 $, 2019 33,529 $, 2020 45,439 $, 2021 54,265 $, 2022 42,080 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 26,956,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (286,832,000 $ in 2022, column `hired_labor_coa_usd`) is 1.24x BEA farm compensation (230,726,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 35,719 $, county -6,092 to 238,613 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 92,055 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 770,015,000 $ vs CAINC45 752,986,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.844, county range 0.512 to 0.972.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 28 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,044 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 2 counties have no recent foreign born in the ACS sample (Daggett, Rich), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Salt Lake); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (8); rural = the rest (20). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 229.1 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 56.6 straight-line km/h between counties (median 16.0 to 78.7 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.33).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 49001 Beaver | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49007 Carbon | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49009 Daggett | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49011 Davis | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49017 Garfield | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49019 Grand | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49021 Iron | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49025 Kane | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49031 Piute | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49033 Rich | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49035 Salt Lake | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49037 San Juan | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49039 Sanpete | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49041 Sevier | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49043 Summit | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49047 Uintah | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49049 Utah | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49051 Wasatch | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49053 Washington | not published; NASS 'other (combined) counties' value = 27.5 $/acre |
| cash_rent_usd_acre | 49055 Wayne | not published; NASS 'other (combined) counties' value = 27.5 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26912) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 49001 | Beaver | rural | 3,023 | 2,568 | 460 | 14,498 | 3.78M | 100,889 | 121,928 | 0.850 | 28* |
| 49003 | Box Elder | rural | 26,707 | 22,142 | 1,029 | 116,861 | 19.92M | 68,813 | 27,581 | 0.802 | 30 |
| 49005 | Cache | suburb | 66,302 | 65,056 | 1,117 | 64,832 | 39.76M | 51,371 | 44,273 | 0.711 | 37 |
| 49007 | Carbon | rural | 8,067 | 8,201 | 228 | 4,814 | 7.63M | 60,582 | 5,288 | 0.568 | 28* |
| 49009 | Daggett | rural | 256 | 305 | 35 | 3,482 | 0.53M | 26,323 | 24,853 | 0.842 | 28* |
| 49011 | Davis | suburb | 178,241 | 147,380 | 467 | 4,593 | 111.24M | 75,677 | 27,484 | 0.880 | 28* |
| 49013 | Duchesne | rural | 7,930 | 7,673 | 715 | 39,185 | 6.81M | 66,013 | 19,761 | 0.952 | 32 |
| 49015 | Emery | rural | 3,955 | 2,988 | 377 | 22,618 | 4.50M | 55,456 | 21,225 | 0.725 | 18 |
| 49017 | Garfield | rural | 2,321 | 2,064 | 165 | 7,786 | 3.46M | 58,073 | 41,896 | 0.775 | 28* |
| 49019 | Grand | rural | 5,480 | 5,892 | 64 | 3,917 | 4.31M | 48,594 | 27,647 | 0.972 | 28* |
| 49021 | Iron | rural | 26,664 | 24,921 | 611 | 27,734 | 15.41M | 69,789 | 65,066 | 0.706 | 28* |
| 49023 | Juab | suburb | 5,412 | 4,129 | 279 | 18,256 | 5.66M | 53,096 | 54,489 | 0.776 | 12 |
| 49025 | Kane | rural | 3,422 | 3,960 | 113 | 1,734 | 3.82M | 60,134 | 18,308 | 0.692 | 28* |
| 49027 | Millard | rural | 5,230 | 4,440 | 738 | 60,607 | 7.04M | 80,999 | 72,562 | 0.797 | 12 |
| 49029 | Morgan | suburb | 5,292 | 2,842 | 146 | 5,800 | 2.74M | 100,359 | -6,092 | 0.579 | 20 |
| 49031 | Piute | rural | 570 | 296 | 84 | 5,494 | 0.96M | 55,808 | 238,613 | 0.856 | 28* |
| 49033 | Rich | rural | 976 | 806 | 96 | 9,178 | 1.12M | 102,572 | 76,930 | 0.868 | 28* |
| 49035 | Salt Lake | core | 619,466 | 701,404 | 523 | 6,841 | 384.85M | 45,205 | 3,486 | 0.512 | 28* |
| 49037 | San Juan | rural | 5,156 | 3,840 | 448 | 48,166 | 4.03M | 64,377 | 5,435 | 0.938 | 28* |
| 49039 | Sanpete | rural | 12,036 | 9,142 | 688 | 42,326 | 13.62M | 61,517 | 103,325 | 0.737 | 28* |
| 49041 | Sevier | rural | 9,170 | 8,707 | 501 | 18,336 | 10.17M | 62,768 | 46,620 | 0.804 | 28* |
| 49043 | Summit | rural | 22,696 | 28,624 | 375 | 3,857 | 10.76M | 53,284 | 18,014 | 0.827 | 28* |
| 49045 | Tooele | suburb | 36,512 | 22,993 | 461 | 8,565 | 17.80M | 70,597 | 26,216 | 0.685 | 20 |
| 49047 | Uintah | rural | 14,316 | 12,915 | 859 | 29,414 | 10.77M | 62,943 | 14,234 | 0.958 | 28* |
| 49049 | Utah | suburb | 320,495 | 299,364 | 2,083 | 46,782 | 171.79M | 74,505 | 16,647 | 0.792 | 28* |
| 49051 | Wasatch | rural | 16,948 | 13,195 | 279 | 3,208 | 8.73M | 70,114 | 3,220 | 0.627 | 28* |
| 49053 | Washington | suburb | 77,459 | 79,244 | 356 | 4,804 | 64.40M | 89,720 | 7,978 | 0.612 | 28* |
| 49055 | Wayne | rural | 1,271 | 1,168 | 126 | 6,484 | 1.56M | 84,805 | 46,626 | 0.668 | 28* |
| 49057 | Weber | suburb | 131,828 | 120,275 | 887 | 13,445 | 84.85M | 61,636 | 19,453 | 0.749 | 35 |
| EXT | External (out-of-state commuting) | external | 18,939 | 15,161 | 135 | 6,074 | 11.97M | 67,337 | n/a | 0.844 | n/a |

`*` filled, see above.
