# Michigan 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state MI 2022`. 83 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 26 | `MI/CDL_2022_26.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=26 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MI.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 10,034,113 | 10,034,113 | 0.000% |
| ACS workers by residence | 4,613,166 | 4,613,166 | 0.000% |
| ACS workers by workplace | 4,579,902 | 4,579,902 | 0.000% |
| ACS workers working out of state | 79,655 | 79,655 | 0.000% |
| BEA non-farm employment (L80) | 5,802,112 | 5,802,112 | 0.000% |
| BEA farm employment (L70) | 61,897 | 61,897 | 0.000% |
| BEA farm proprietors (L50) | 38,801 | 38,801 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,382,608,000 | 2,382,608,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 933,349,000 | 933,349,000 | 0.000% |
| CoA hired farm labour expense $ | 1,266,086,000 | 1,270,534,000 | -0.350% |
| BEA non-farm earnings $ (CAINC5N L82) | 386,961,613,000 | 386,961,613,000 | 0.000% |
| ACS foreign born entered 2010+ | 234,680 | 234,680 | 0.000% |
| CoA owned acres | 5,550,510 | 5,550,510 | 0.000% |
| CoA rented-from-others acres | 3,921,559 | 3,921,559 | 0.000% |
| CoA land in farms, ha | 3,833,210 | 3,833,210 | 0.000% |
| CoA total cropland, ha | 3,041,512 | 3,041,512 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.626, median 0.815, max 1.076; BEA counts jobs, ACS counts people by main job). Sum N = 4,659,557 = sum HU + HA = 4,659,557. Farm jobs after scaling: 50,182 (BEA 61,897). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 46,391. Jobs = in-state residents working out of state = 79,655, split by the state farm share (HA = 873). Location: the 13 out-of-state counties within 1 km of the state (18039, 18087, 18091, 18141, 18151, 39051, 39095, 39171, 55037, 55041, 55051, 55075, 55125); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 3,259,804 ha vs Census of Agriculture cropland 3,041,512 ha and land in farms 3,833,210 ha; county ratio TF / CoA cropland 0.28 to 3.17. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 703,984 ha). County area covered by CDL pixels: 15,090,924 ha vs land area 14,661,915 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 10.43 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (66,693 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 42,610 $ per BEA farm job, 52,557 $ per farm worker; county range 6,089 to 99,681 $ per worker. State compensation per farm wage job by year: 2018 42,327 $, 2019 41,457 $, 2020 40,414 $, 2021 40,838 $, 2022 40,412 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 223,943,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,270,534,000 $ in 2022, column `hired_labor_coa_usd`) is 1.36x BEA farm compensation (933,349,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 38,493 $, county -8,736 to 102,658 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 85,427 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,599,408,000 $ vs CAINC45 2,382,608,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.586, county range 0.410 to 1.000.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 137 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 5,879 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 1 counties have no recent foreign born in the ACS sample (Baraga), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Oakland); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (29); rural = the rest (53). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 2 counties have no BEA farm jobs (Crawford, Keweenaw); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 212.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 59.5 straight-line km/h between counties (median 15.1 to 36.0 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.31).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 26039 Crawford | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 26083 Keweenaw | 0 farm jobs: no farm sector in the model (spec §3.11) |
| rented_acres | 26083 Keweenaw | land in farms minus the other tenure (Census of Ag identity) |
| cash_rent_usd_acre | 26009 Antrim | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26013 Baraga | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26019 Benzie | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26039 Crawford | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26047 Emmet | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26053 Gogebic | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26061 Houghton | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26079 Kalkaska | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26083 Keweenaw | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26085 Lake | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26095 Luce | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26097 Mackinac | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26103 Marquette | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26131 Ontonagon | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26135 Oscoda | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26143 Roscommon | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26151 Sanilac | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26153 Schoolcraft | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26157 Tuscola | not published; NASS 'other (combined) counties' value = 153 $/acre |
| cash_rent_usd_acre | 26165 Wexford | not published; NASS 'other (combined) counties' value = 153 $/acre |
| hired_labor_coa_usd | 26013 Baraga | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 26053 Gogebic | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 26095 Luce | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 26153 Schoolcraft | (D) in Census of Ag; left null (comparison column only) |

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
| 26001 | Alcona | rural | 3,446 | 2,172 | 141 | 12,870 | 4.30M | 50,330 | 15,056 | 0.750 | 30 |
| 26003 | Alger | rural | 2,856 | 2,705 | 63 | 2,352 | 2.55M | 50,693 | 679 | 0.793 | 20 |
| 26005 | Allegan | rural | 56,188 | 44,229 | 1,875 | 84,489 | 34.70M | 69,371 | 64,071 | 0.526 | 146 |
| 26007 | Alpena | rural | 11,893 | 12,587 | 338 | 25,208 | 12.74M | 31,069 | 28,269 | 0.654 | 33 |
| 26009 | Antrim | rural | 10,480 | 7,811 | 422 | 13,289 | 7.76M | 43,181 | 27,409 | 0.885 | 153* |
| 26011 | Arenac | rural | 6,023 | 4,695 | 339 | 27,491 | 5.58M | 51,673 | 32,056 | 0.658 | 96 |
| 26013 | Baraga | rural | 2,935 | 2,962 | 44 | 2,329 | 2.80M | 28,163 | 8,679 | 0.716 | 153* |
| 26015 | Barry | suburb | 28,461 | 15,316 | 830 | 47,247 | 16.19M | 57,161 | 51,594 | 0.603 | 115 |
| 26017 | Bay | suburb | 47,237 | 38,905 | 674 | 66,581 | 39.19M | 42,451 | 32,800 | 0.522 | 151 |
| 26019 | Benzie | suburb | 7,895 | 5,115 | 117 | 5,252 | 4.45M | 68,543 | 21,473 | 0.805 | 153* |
| 26021 | Berrien | suburb | 69,571 | 65,174 | 1,344 | 67,080 | 48.73M | 60,371 | 51,124 | 0.604 | 131 |
| 26023 | Branch | rural | 18,889 | 15,653 | 822 | 80,261 | 17.87M | 59,732 | 34,676 | 0.473 | 125 |
| 26025 | Calhoun | suburb | 58,169 | 61,491 | 954 | 79,896 | 46.09M | 50,710 | 19,886 | 0.604 | 127 |
| 26027 | Cass | suburb | 23,505 | 13,174 | 738 | 63,401 | 14.09M | 60,933 | 31,372 | 0.663 | 129 |
| 26029 | Charlevoix | rural | 12,426 | 11,409 | 199 | 6,575 | 10.42M | 29,427 | 13,185 | 0.774 | 32 |
| 26031 | Cheboygan | rural | 10,225 | 7,604 | 218 | 6,403 | 8.81M | 40,335 | 1,720 | 0.772 | 29 |
| 26033 | Chippewa | rural | 15,504 | 15,013 | 331 | 23,573 | 8.58M | 30,750 | 11,512 | 0.770 | 15 |
| 26035 | Clare | rural | 10,714 | 8,051 | 318 | 18,292 | 8.92M | 44,008 | 17,624 | 0.784 | 58 |
| 26037 | Clinton | suburb | 38,854 | 24,175 | 1,217 | 86,019 | 20.76M | 54,102 | 45,154 | 0.565 | 161 |
| 26039 | Crawford | rural | 5,115 | 5,149 | 0 | 474 | 5.00M | 0 | n/a | 0.989 | 153* |
| 26041 | Delta | rural | 14,790 | 13,723 | 198 | 16,034 | 16.34M | 44,942 | 13,448 | 0.812 | 20 |
| 26043 | Dickinson | rural | 11,750 | 13,633 | 110 | 4,036 | 15.60M | 34,869 | 3,139 | 0.811 | 24 |
| 26045 | Eaton | suburb | 52,669 | 50,680 | 884 | 73,905 | 36.28M | 38,685 | 19,037 | 0.556 | 136 |
| 26047 | Emmet | rural | 16,802 | 19,871 | 230 | 4,057 | 11.21M | 35,804 | -313 | 0.862 | 153* |
| 26049 | Genesee | suburb | 170,085 | 149,021 | 804 | 40,130 | 123.68M | 48,229 | 18,435 | 0.492 | 92 |
| 26051 | Gladwin | rural | 9,131 | 6,112 | 370 | 20,327 | 8.40M | 31,777 | 5,928 | 0.658 | 62 |
| 26053 | Gogebic | rural | 6,038 | 5,772 | 52 | 180 | 4.32M | 6,089 | 468 | 0.901 | 153* |
| 26055 | Grand Traverse | suburb | 47,745 | 55,648 | 400 | 19,776 | 26.66M | 40,388 | 29,809 | 0.745 | 54 |
| 26057 | Gratiot | rural | 16,782 | 14,090 | 941 | 103,191 | 14.77M | 55,200 | 67,886 | 0.459 | 178 |
| 26059 | Hillsdale | rural | 19,694 | 14,138 | 1,238 | 81,293 | 14.90M | 55,050 | 28,564 | 0.528 | 138 |
| 26061 | Houghton | rural | 16,375 | 15,886 | 160 | 3,486 | 9.82M | 18,058 | 9,616 | 0.798 | 153* |
| 26063 | Huron | rural | 13,374 | 12,382 | 1,458 | 162,749 | 15.44M | 55,721 | 102,658 | 0.496 | 231 |
| 26065 | Ingham | suburb | 137,987 | 162,463 | 960 | 61,258 | 94.76M | 46,062 | 34,166 | 0.513 | 138 |
| 26067 | Ionia | suburb | 29,980 | 19,457 | 1,423 | 83,094 | 17.32M | 53,460 | 43,849 | 0.584 | 172 |
| 26069 | Iosco | rural | 9,130 | 9,546 | 220 | 14,059 | 9.09M | 30,479 | 15,071 | 0.752 | 48 |
| 26071 | Iron | rural | 4,427 | 4,018 | 96 | 2,286 | 4.28M | 40,064 | 6,763 | 0.792 | 17 |
| 26073 | Isabella | rural | 30,645 | 33,099 | 814 | 71,875 | 21.82M | 44,989 | 29,261 | 0.580 | 101 |
| 26075 | Jackson | suburb | 68,511 | 62,650 | 831 | 57,441 | 41.88M | 41,460 | 6,074 | 0.606 | 111 |
| 26077 | Kalamazoo | suburb | 129,059 | 135,701 | 1,216 | 47,151 | 88.43M | 62,046 | 58,177 | 0.418 | 128 |
| 26079 | Kalkaska | suburb | 7,438 | 5,101 | 146 | 5,763 | 5.72M | 99,681 | 10,456 | 0.884 | 153* |
| 26081 | Kent | suburb | 336,075 | 393,342 | 1,352 | 54,738 | 227.09M | 68,301 | 47,947 | 0.610 | 126 |
| 26083 | Keweenaw | rural | 774 | 819 | 0 | 27 | 0.64M | 0 | n/a | 1.000 | 153* |
| 26085 | Lake | rural | 3,935 | 2,211 | 121 | 5,156 | 2.78M | 36,899 | 3,269 | 0.848 | 153* |
| 26087 | Lapeer | suburb | 40,090 | 25,737 | 900 | 58,061 | 23.26M | 53,680 | 21,884 | 0.624 | 98 |
| 26089 | Leelanau | suburb | 9,470 | 8,019 | 372 | 16,441 | 6.40M | 78,808 | 22,960 | 0.817 | 70 |
| 26091 | Lenawee | rural | 42,860 | 30,782 | 1,304 | 122,224 | 28.13M | 55,231 | 34,450 | 0.494 | 159 |
| 26093 | Livingston | suburb | 97,209 | 69,310 | 540 | 27,991 | 39.64M | 39,667 | 18,476 | 0.688 | 86 |
| 26095 | Luce | rural | 1,417 | 1,618 | 31 | 1,449 | 2.25M | 94,281 | 15,864 | 0.806 | 153* |
| 26097 | Mackinac | rural | 4,287 | 4,344 | 74 | 4,891 | 4.91M | 38,333 | 35,358 | 0.684 | 153* |
| 26099 | Macomb | suburb | 422,678 | 358,572 | 648 | 26,000 | 300.75M | 42,504 | 32,141 | 0.531 | 92 |
| 26101 | Manistee | rural | 9,535 | 8,749 | 233 | 10,750 | 8.25M | 47,092 | 5,893 | 0.738 | 30 |
| 26103 | Marquette | rural | 30,498 | 30,992 | 129 | 2,558 | 22.22M | 16,913 | -8,736 | 0.955 | 153* |
| 26105 | Mason | rural | 12,200 | 11,613 | 384 | 27,015 | 10.80M | 55,492 | 42,000 | 0.680 | 62 |
| 26107 | Mecosta | rural | 16,342 | 15,541 | 715 | 38,205 | 10.90M | 43,891 | 11,302 | 0.611 | 56 |
| 26109 | Menominee | rural | 10,557 | 8,499 | 367 | 26,395 | 10.27M | 35,497 | 49,939 | 0.620 | 32 |
| 26111 | Midland | suburb | 37,379 | 37,861 | 393 | 30,233 | 33.74M | 68,200 | 15,359 | 0.559 | 142 |
| 26113 | Missaukee | rural | 6,424 | 3,487 | 627 | 32,769 | 5.06M | 53,824 | 55,447 | 0.631 | 88 |
| 26115 | Monroe | suburb | 69,702 | 44,893 | 1,217 | 78,397 | 47.03M | 48,803 | 28,370 | 0.410 | 149 |
| 26117 | Montcalm | suburb | 28,450 | 19,967 | 1,177 | 79,644 | 17.68M | 50,503 | 38,023 | 0.616 | 94 |
| 26119 | Montmorency | rural | 3,115 | 2,697 | 103 | 6,431 | 3.07M | 35,522 | 28,008 | 0.771 | 40 |
| 26121 | Muskegon | suburb | 75,385 | 66,361 | 499 | 23,747 | 53.79M | 79,464 | 46,786 | 0.669 | 90 |
| 26123 | Newaygo | rural | 21,259 | 14,250 | 856 | 39,693 | 12.53M | 56,711 | 49,014 | 0.698 | 82 |
| 26125 | Oakland | core | 646,051 | 733,359 | 504 | 6,251 | 436.50M | 42,660 | 14,646 | 0.669 | 55 |
| 26127 | Oceana | rural | 11,214 | 8,198 | 1,053 | 37,603 | 8.10M | 38,841 | 27,496 | 0.649 | 84 |
| 26129 | Ogemaw | rural | 7,482 | 6,785 | 282 | 22,733 | 7.09M | 49,810 | 62,763 | 0.708 | 40 |
| 26131 | Ontonagon | rural | 1,992 | 1,543 | 69 | 4,207 | 2.17M | 28,719 | 5,452 | 0.776 | 153* |
| 26133 | Osceola | rural | 8,921 | 7,510 | 505 | 32,470 | 7.21M | 49,320 | 21,408 | 0.722 | 74 |
| 26135 | Oscoda | rural | 2,719 | 2,615 | 216 | 3,365 | 2.73M | 9,710 | 8,986 | 0.840 | 153* |
| 26137 | Otsego | rural | 11,517 | 12,510 | 148 | 5,994 | 8.61M | 39,030 | 5,169 | 0.809 | 33 |
| 26139 | Ottawa | suburb | 150,765 | 138,368 | 2,067 | 55,204 | 83.72M | 72,234 | 71,070 | 0.608 | 119 |
| 26141 | Presque Isle | rural | 4,614 | 3,557 | 240 | 20,714 | 4.68M | 75,843 | 23,322 | 0.675 | 54 |
| 26143 | Roscommon | rural | 7,879 | 7,285 | 39 | 1,035 | 6.56M | 10,512 | -1,978 | 0.836 | 153* |
| 26145 | Saginaw | suburb | 79,772 | 90,174 | 1,112 | 111,646 | 73.65M | 48,087 | 30,405 | 0.552 | 148 |
| 26147 | St. Clair | suburb | 71,975 | 52,472 | 807 | 67,216 | 53.28M | 40,724 | 21,650 | 0.598 | 73 |
| 26149 | St. Joseph | rural | 27,239 | 25,331 | 958 | 75,855 | 20.37M | 62,846 | 60,526 | 0.460 | 127 |
| 26151 | Sanilac | rural | 17,035 | 12,771 | 1,457 | 171,956 | 17.61M | 53,121 | 71,382 | 0.609 | 153* |
| 26153 | Schoolcraft | rural | 3,155 | 2,921 | 63 | 2,471 | 3.24M | 31,421 | 13,247 | 0.829 | 153* |
| 26155 | Shiawassee | rural | 31,454 | 20,524 | 852 | 81,645 | 20.31M | 46,127 | 24,092 | 0.560 | 117 |
| 26157 | Tuscola | rural | 22,372 | 13,962 | 1,067 | 116,517 | 17.13M | 52,607 | 46,256 | 0.508 | 153* |
| 26159 | Van Buren | rural | 33,874 | 26,246 | 1,365 | 65,803 | 20.58M | 67,155 | 51,411 | 0.614 | 149 |
| 26161 | Washtenaw | suburb | 184,417 | 228,742 | 1,074 | 54,906 | 89.03M | 39,525 | 10,591 | 0.544 | 109 |
| 26163 | Wayne | suburb | 742,431 | 792,777 | 448 | 5,530 | 812.71M | 43,141 | 23,975 | 0.623 | 73 |
| 26165 | Wexford | rural | 13,849 | 16,024 | 280 | 12,697 | 10.80M | 48,941 | 7,137 | 0.664 | 153* |
| EXT | External (out-of-state commuting) | external | 46,391 | 78,782 | 873 | 56,695 | 34.97M | 52,557 | n/a | 0.586 | n/a |

`*` filled, see above.
