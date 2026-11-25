# New Mexico 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state NM 2022`. 33 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 35 | `NM/CDL_2022_35.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=35 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R6_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C9.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NM.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 2,113,344 | 2,113,344 | 0.000% |
| ACS workers by residence | 901,687 | 901,687 | 0.000% |
| ACS workers by workplace | 893,895 | 893,895 | 0.000% |
| ACS workers working out of state | 33,812 | 33,812 | 0.000% |
| BEA non-farm employment (L80) | 1,113,072 | 1,113,072 | 0.000% |
| BEA farm employment (L70) | 26,416 | 26,416 | 0.000% |
| BEA farm proprietors (L50) | 20,491 | 20,491 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 884,704,000 | 884,704,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 309,405,000 | 309,405,000 | 0.000% |
| CoA hired farm labour expense $ | 305,603,000 | 335,513,000 | -8.915% |
| BEA non-farm earnings $ (CAINC5N L82) | 68,102,045,000 | 68,102,045,000 | 0.000% |
| ACS foreign born entered 2010+ | 41,036 | 41,036 | 0.000% |
| CoA owned acres | 27,615,100 | 28,219,002 | -2.140% |
| CoA rented-from-others acres | 10,805,607 | 10,909,561 | -0.953% |
| CoA land in farms, ha | 15,730,589 | 15,834,768 | -0.658% |
| CoA total cropland, ha | 847,506 | 847,506 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.375, median 0.776, max 0.944; BEA counts jobs, ACS counts people by main job). Sum N = 927,707 = sum HU + HA = 927,707. Farm jobs after scaling: 20,446 (BEA 26,416). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 26,020. Jobs = in-state residents working out of state = 33,812, split by the state farm share (HA = 773). Location: the 28 out-of-state counties within 1 km of the state (04001, 04003, 04011, 08007, 08009, 08021, 08023, 08067, 08071, 08083, 40025, 48003, 48017, 48079, 48109, 48111, 48117, 48141, 48165, 48205, 48229, 48301, 48359, 48369, 48389, 48495, 48501, 49037); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 697,853 ha vs Census of Agriculture cropland 847,506 ha and land in farms 15,834,768 ha; county ratio TF / CoA cropland 0.00 to 2.28. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 4,392,671 ha). County area covered by CDL pixels: 31,491,842 ha vs land area 31,419,857 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 2.55 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (61,184 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 43,700 $ per BEA farm job, 56,459 $ per farm worker; county range 17,627 to 97,140 $ per worker. State compensation per farm wage job by year: 2018 41,827 $, 2019 33,090 $, 2020 45,621 $, 2021 53,776 $, 2022 52,220 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 56,819,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (335,513,000 $ in 2022, column `hired_labor_coa_usd`) is 1.08x BEA farm compensation (309,405,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 33,491 $, county -4,956 to 153,084 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 77,969 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,443,317,000 $ vs CAINC45 884,704,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.719, county range 0.300 to 0.952.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 16 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 838 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (De Baca, Mora, Sierra), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Bernalillo); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (6); rural = the rest (26). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Los Alamos); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 281.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.5 straight-line km/h between counties (median 9.0 to 71.6 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.31).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 35028 Los Alamos | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 35001 Bernalillo | state owner share |
| omega | 35028 Los Alamos | state owner share |
| omega | 35061 Valencia | state owner share |
| cash_rent_usd_acre | 35001 Bernalillo | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35003 Catron | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35005 Chaves | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35006 Cibola | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35007 Colfax | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35009 Curry | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35011 De Baca | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35013 Doña Ana | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35015 Eddy | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35017 Grant | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35019 Guadalupe | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35021 Harding | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35023 Hidalgo | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35025 Lea | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35027 Lincoln | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35028 Los Alamos | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35029 Luna | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35031 McKinley | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35035 Otero | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35039 Rio Arriba | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35043 Sandoval | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35045 San Juan | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35047 San Miguel | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35049 Santa Fe | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35051 Sierra | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35053 Socorro | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35057 Torrance | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35059 Union | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| cash_rent_usd_acre | 35061 Valencia | not published; NASS 'other (combined) counties' value = 16.5 $/acre |
| owned_acres | 35001 Bernalillo | (D) in Census of Ag; see fills above |
| owned_acres | 35028 Los Alamos | (D) in Census of Ag; see fills above |
| owned_acres | 35061 Valencia | (D) in Census of Ag; see fills above |
| rented_acres | 35001 Bernalillo | (D) in Census of Ag; see fills above |
| rented_acres | 35028 Los Alamos | (D) in Census of Ag; see fills above |
| rented_acres | 35061 Valencia | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 35006 Cibola | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 35045 San Juan | (D) in Census of Ag; left null (comparison column only) |

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
| 35001 | Bernalillo | core | 320,828 | 348,313 | 729 | 432 | 302.07M | 48,295 | 2,463 | 0.721 | 16* |
| 35003 | Catron | rural | 961 | 928 | 232 | 253 | 2.04M | 51,400 | 25,953 | 0.591 | 16* |
| 35005 | Chaves | rural | 25,977 | 22,452 | 891 | 38,388 | 25.91M | 65,166 | 101,256 | 0.630 | 16* |
| 35006 | Cibola | rural | 8,842 | 8,179 | 409 | 57 | 7.05M | 32,057 | 19,672 | 0.821 | 16* |
| 35007 | Colfax | rural | 4,949 | 4,624 | 253 | 10,573 | 7.25M | 37,274 | 64,095 | 0.596 | 16* |
| 35009 | Curry | rural | 21,564 | 21,851 | 886 | 153,161 | 22.01M | 64,729 | 153,084 | 0.718 | 16* |
| 35011 | De Baca | rural | 722 | 623 | 187 | 4,826 | 1.16M | 48,747 | 61,869 | 0.587 | 16* |
| 35013 | Doña Ana | suburb | 91,502 | 80,695 | 2,296 | 39,386 | 86.00M | 74,242 | 30,376 | 0.741 | 16* |
| 35015 | Eddy | rural | 27,002 | 31,397 | 613 | 27,518 | 23.33M | 63,922 | 52,612 | 0.565 | 16* |
| 35017 | Grant | rural | 9,731 | 9,719 | 285 | 1,499 | 12.06M | 74,550 | 30,984 | 0.765 | 16* |
| 35019 | Guadalupe | rural | 1,526 | 1,539 | 351 | 1,477 | 1.92M | 39,898 | 21,105 | 0.753 | 16* |
| 35021 | Harding | rural | 271 | 143 | 99 | 1,500 | 0.53M | 97,140 | 22,006 | 0.744 | 16* |
| 35023 | Hidalgo | rural | 1,629 | 1,463 | 142 | 18,946 | 2.50M | 49,708 | 62,694 | 0.726 | 16* |
| 35025 | Lea | rural | 30,122 | 30,457 | 470 | 34,059 | 33.07M | 75,129 | 114,992 | 0.469 | 16* |
| 35027 | Lincoln | rural | 8,220 | 8,035 | 271 | 760 | 13.11M | 58,392 | 20,880 | 0.791 | 16* |
| 35028 | Los Alamos | rural | 10,197 | 19,363 | 0 | 80 | 8.38M | 0 | n/a | 0.721 | 16* |
| 35029 | Luna | rural | 8,172 | 7,624 | 227 | 35,151 | 10.24M | 68,914 | 83,175 | 0.300 | 16* |
| 35031 | McKinley | rural | 23,701 | 20,497 | 1,692 | 78 | 13.09M | 17,627 | 2,249 | 0.947 | 16* |
| 35033 | Mora | rural | 1,312 | 443 | 212 | 6,654 | 2.11M | 88,130 | 25,635 | 0.875 | 15 |
| 35035 | Otero | rural | 26,803 | 25,061 | 421 | 3,361 | 22.75M | 54,274 | 18,893 | 0.618 | 16* |
| 35037 | Quay | rural | 3,422 | 2,582 | 399 | 63,297 | 5.74M | 39,227 | 54,212 | 0.761 | 14 |
| 35039 | Rio Arriba | rural | 15,331 | 10,463 | 1,394 | 11,957 | 16.16M | 30,645 | 6,315 | 0.855 | 16* |
| 35041 | Roosevelt | rural | 8,672 | 6,401 | 860 | 128,056 | 9.24M | 53,489 | 107,775 | 0.763 | 16 |
| 35043 | Sandoval | suburb | 66,313 | 44,878 | 792 | 2,302 | 52.79M | 33,681 | 3,026 | 0.749 | 16* |
| 35045 | San Juan | suburb | 44,516 | 41,437 | 1,847 | 39,569 | 43.89M | 81,244 | 6,344 | 0.952 | 16* |
| 35047 | San Miguel | rural | 10,620 | 9,057 | 764 | 3,618 | 11.78M | 41,717 | 9,649 | 0.752 | 16* |
| 35049 | Santa Fe | suburb | 70,746 | 72,152 | 523 | 9,144 | 52.62M | 49,739 | -4,956 | 0.893 | 16* |
| 35051 | Sierra | rural | 3,546 | 3,628 | 231 | 3,335 | 8.45M | 84,141 | 41,754 | 0.680 | 16* |
| 35053 | Socorro | rural | 5,045 | 4,371 | 481 | 5,688 | 6.60M | 79,556 | 31,765 | 0.628 | 16* |
| 35055 | Taos | rural | 13,876 | 12,169 | 635 | 5,267 | 12.29M | 51,349 | 850 | 0.742 | 24 |
| 35057 | Torrance | suburb | 5,431 | 3,076 | 391 | 16,505 | 4.96M | 89,214 | 50,519 | 0.669 | 16* |
| 35059 | Union | rural | 1,315 | 1,186 | 257 | 26,522 | 2.34M | 65,936 | 41,810 | 0.628 | 16* |
| 35061 | Valencia | suburb | 28,823 | 18,643 | 1,206 | 4,435 | 27.37M | 65,762 | 3,372 | 0.721 | 16* |
| EXT | External (out-of-state commuting) | external | 26,020 | 33,039 | 773 | 26,397 | 24.55M | 56,459 | n/a | 0.719 | n/a |

`*` filled, see above.
