# Wisconsin 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state WI 2022`. 72 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 55 | `WI/CDL_2022_55.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=55 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_WI.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 5,892,539 | 5,892,539 | 0.000% |
| ACS workers by residence | 2,974,249 | 2,974,249 | 0.000% |
| ACS workers by workplace | 2,949,797 | 2,949,797 | 0.000% |
| ACS workers working out of state | 98,853 | 98,853 | 0.000% |
| BEA non-farm employment (L80) | 3,733,696 | 3,733,696 | 0.000% |
| BEA farm employment (L70) | 85,484 | 85,484 | 0.000% |
| BEA farm proprietors (L50) | 58,236 | 58,236 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 3,367,930,000 | 3,367,930,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 1,191,677,000 | 1,191,677,000 | 0.000% |
| CoA hired farm labour expense $ | 1,451,710,000 | 1,451,709,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 245,167,058,000 | 245,167,058,000 | 0.000% |
| ACS foreign born entered 2010+ | 88,141 | 88,141 | 0.000% |
| CoA owned acres | 9,049,340 | 9,056,395 | -0.078% |
| CoA rented-from-others acres | 4,725,664 | 4,728,283 | -0.055% |
| CoA land in farms, ha | 5,576,913 | 5,578,461 | -0.028% |
| CoA total cropland, ha | 3,872,479 | 3,873,691 | -0.031% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.635, median 0.766, max 0.876; BEA counts jobs, ACS counts people by main job). Sum N = 3,048,650 = sum HU + HA = 3,048,650. Farm jobs after scaling: 65,083 (BEA 85,484). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 74,401. Jobs = in-state residents working out of state = 98,853, split by the state farm share (HA = 2,181). Location: the 23 out-of-state counties within 1 km of the state (17007, 17085, 17097, 17111, 17177, 17201, 19005, 19043, 19061, 26043, 26053, 26071, 26109, 27017, 27025, 27037, 27049, 27055, 27115, 27137, 27157, 27163, 27169); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 3,794,985 ha vs Census of Agriculture cropland 3,873,691 ha and land in farms 5,578,461 ha; county ratio TF / CoA cropland 0.18 to 1.48. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,241,208 ha). County area covered by CDL pixels: 14,533,735 ha vs land area 14,029,252 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 6.76 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (65,663 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 44,815 $ per BEA farm job, 58,864 $ per farm worker; county range 31,560 to 88,127 $ per worker. State compensation per farm wage job by year: 2018 43,237 $, 2019 43,726 $, 2020 40,892 $, 2021 41,010 $, 2022 43,734 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 88,588,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,451,709,000 $ in 2022, column `hired_labor_coa_usd`) is 1.22x BEA farm compensation (1,191,677,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 39,398 $, county -7,638 to 88,229 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 84,988 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 3,559,758,000 $ vs CAINC45 3,367,930,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.657, county range 0.437 to 0.908.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 145 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 6,117 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 1 counties have no recent foreign born in the ACS sample (Florence), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Milwaukee); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (26); rural = the rest (45). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Menominee); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 211.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 57.2 straight-line km/h between counties (median 13.4 to 34.6 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.27).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 55078 Menominee | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 55078 Menominee | state owner share |
| omega | 55079 Milwaukee | state owner share |
| omega | 55125 Vilas | state owner share |
| cash_rent_usd_acre | 55019 Clark | not published; NASS 'other (combined) counties' value = 149 $/acre |
| cash_rent_usd_acre | 55027 Dodge | not published; NASS 'other (combined) counties' value = 149 $/acre |
| cash_rent_usd_acre | 55051 Iron | not published; NASS 'other (combined) counties' value = 149 $/acre |
| cash_rent_usd_acre | 55078 Menominee | not published; NASS 'other (combined) counties' value = 149 $/acre |
| cash_rent_usd_acre | 55079 Milwaukee | not published; NASS 'other (combined) counties' value = 149 $/acre |
| cash_rent_usd_acre | 55125 Vilas | not published; NASS 'other (combined) counties' value = 149 $/acre |
| land_value_usd_acre | 55078 Menominee | (D) in Census of Ag; see fills above |
| land_value_usd_acre | 55125 Vilas | (D) in Census of Ag; see fills above |
| owned_acres | 55078 Menominee | (D) in Census of Ag; see fills above |
| owned_acres | 55079 Milwaukee | (D) in Census of Ag; see fills above |
| owned_acres | 55125 Vilas | (D) in Census of Ag; see fills above |
| rented_acres | 55079 Milwaukee | (D) in Census of Ag; see fills above |
| rented_acres | 55125 Vilas | (D) in Census of Ag; see fills above |

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
| 55001 | Adams | rural | 7,987 | 4,701 | 406 | 40,144 | 8.48M | 81,757 | 35,578 | 0.624 | 91 |
| 55003 | Ashland | rural | 7,581 | 8,650 | 177 | 5,732 | 5.48M | 45,414 | 15,606 | 0.823 | 34 |
| 55005 | Barron | rural | 22,230 | 21,305 | 1,281 | 82,213 | 17.25M | 74,442 | 37,145 | 0.677 | 96 |
| 55007 | Bayfield | rural | 7,301 | 4,767 | 228 | 8,473 | 5.70M | 84,033 | 2,738 | 0.735 | 28 |
| 55009 | Brown | suburb | 139,271 | 155,753 | 1,306 | 64,641 | 113.06M | 55,213 | 52,316 | 0.553 | 210 |
| 55011 | Buffalo | rural | 6,802 | 3,747 | 808 | 56,724 | 6.54M | 61,811 | 39,940 | 0.736 | 134 |
| 55013 | Burnett | rural | 6,800 | 5,003 | 301 | 14,958 | 6.27M | 63,413 | 31,645 | 0.689 | 57 |
| 55015 | Calumet | suburb | 28,601 | 18,387 | 876 | 51,228 | 20.75M | 59,487 | 61,297 | 0.628 | 171 |
| 55017 | Chippewa | suburb | 32,569 | 27,887 | 1,589 | 97,485 | 23.08M | 48,194 | 34,155 | 0.698 | 102 |
| 55019 | Clark | rural | 15,788 | 11,228 | 1,903 | 126,402 | 15.51M | 62,257 | 51,175 | 0.745 | 149* |
| 55021 | Columbia | suburb | 30,294 | 23,640 | 1,307 | 94,199 | 21.62M | 46,873 | 38,764 | 0.603 | 184 |
| 55023 | Crawford | rural | 7,013 | 6,959 | 808 | 26,577 | 9.04M | 52,705 | 20,735 | 0.733 | 123 |
| 55025 | Dane | suburb | 314,337 | 350,045 | 2,529 | 144,638 | 169.10M | 62,255 | 47,113 | 0.626 | 206 |
| 55027 | Dodge | rural | 46,378 | 35,483 | 1,901 | 129,516 | 34.24M | 50,219 | 40,056 | 0.624 | 149* |
| 55029 | Door | rural | 14,156 | 13,866 | 633 | 36,736 | 14.64M | 68,548 | 22,885 | 0.584 | 100 |
| 55031 | Douglas | suburb | 21,745 | 19,753 | 272 | 2,064 | 18.50M | 44,704 | 3,920 | 0.751 | 24 |
| 55033 | Dunn | rural | 23,558 | 18,784 | 1,229 | 92,093 | 15.15M | 58,864 | 37,652 | 0.626 | 122 |
| 55035 | Eau Claire | suburb | 56,723 | 61,652 | 1,131 | 49,059 | 34.36M | 54,416 | 20,945 | 0.676 | 107 |
| 55037 | Florence | rural | 1,902 | 1,015 | 51 | 1,873 | 2.03M | 31,560 | -7,638 | 0.703 | 24 |
| 55039 | Fond du Lac | suburb | 52,489 | 47,246 | 1,665 | 105,160 | 41.62M | 63,391 | 61,000 | 0.639 | 163 |
| 55041 | Forest | rural | 3,744 | 3,168 | 81 | 3,170 | 3.15M | 65,713 | -2,612 | 0.838 | 20 |
| 55043 | Grant | rural | 25,660 | 19,488 | 2,100 | 108,182 | 23.12M | 46,387 | 61,075 | 0.621 | 217 |
| 55045 | Green | suburb | 19,534 | 15,350 | 1,250 | 86,753 | 15.17M | 56,195 | 39,280 | 0.620 | 180 |
| 55047 | Green Lake | rural | 8,845 | 6,996 | 532 | 41,865 | 8.22M | 49,724 | 36,808 | 0.703 | 169 |
| 55049 | Iowa | suburb | 12,784 | 10,722 | 1,227 | 63,499 | 9.77M | 54,252 | 26,606 | 0.697 | 185 |
| 55051 | Iron | rural | 2,649 | 2,211 | 51 | 1,273 | 2.27M | 83,680 | 17,082 | 0.878 | 149* |
| 55053 | Jackson | rural | 9,119 | 7,106 | 846 | 48,913 | 8.58M | 78,602 | 47,220 | 0.731 | 137 |
| 55055 | Jefferson | rural | 46,221 | 36,859 | 1,326 | 72,421 | 36.95M | 62,263 | 30,302 | 0.629 | 167 |
| 55057 | Juneau | rural | 12,034 | 9,853 | 779 | 40,474 | 10.76M | 86,071 | 45,209 | 0.687 | 102 |
| 55059 | Kenosha | suburb | 85,204 | 75,207 | 436 | 29,071 | 57.64M | 56,128 | 31,051 | 0.437 | 159 |
| 55061 | Kewaunee | suburb | 10,700 | 6,703 | 1,075 | 51,485 | 9.77M | 67,346 | 88,229 | 0.601 | 194 |
| 55063 | La Crosse | suburb | 62,724 | 72,041 | 670 | 25,501 | 48.17M | 38,370 | 31,129 | 0.747 | 134 |
| 55065 | Lafayette | rural | 8,303 | 4,972 | 1,106 | 94,839 | 8.35M | 65,601 | 58,315 | 0.589 | 235 |
| 55067 | Langlade | rural | 8,688 | 7,663 | 525 | 32,713 | 8.73M | 58,265 | 35,985 | 0.681 | 114 |
| 55069 | Lincoln | rural | 13,099 | 11,419 | 396 | 19,852 | 9.97M | 54,067 | 25,522 | 0.676 | 59 |
| 55071 | Manitowoc | rural | 40,326 | 34,667 | 1,569 | 78,528 | 36.65M | 57,617 | 45,638 | 0.613 | 193 |
| 55073 | Marathon | suburb | 70,785 | 70,926 | 2,291 | 150,842 | 68.38M | 53,903 | 46,621 | 0.657 | 86 |
| 55075 | Marinette | rural | 18,739 | 18,546 | 556 | 37,538 | 19.69M | 65,433 | 57,501 | 0.655 | 120 |
| 55077 | Marquette | rural | 6,911 | 3,870 | 376 | 31,977 | 5.30M | 74,638 | 22,480 | 0.675 | 76 |
| 55078 | Menominee | rural | 1,364 | 1,862 | 0 | 214 | 0.73M | 0 | n/a | 0.657 | 149* |
| 55079 | Milwaukee | core | 445,979 | 462,041 | 86 | 2,607 | 319.22M | 64,163 | 18,226 | 0.657 | 149* |
| 55081 | Monroe | rural | 21,749 | 21,838 | 1,724 | 51,744 | 19.68M | 63,051 | 30,813 | 0.767 | 130 |
| 55083 | Oconto | suburb | 18,925 | 10,104 | 900 | 63,390 | 15.61M | 59,113 | 44,931 | 0.536 | 119 |
| 55085 | Oneida | rural | 16,525 | 16,642 | 224 | 4,499 | 13.64M | 53,093 | 21,910 | 0.908 | 52 |
| 55087 | Outagamie | suburb | 101,029 | 105,460 | 1,312 | 81,862 | 95.68M | 57,931 | 49,884 | 0.553 | 158 |
| 55089 | Ozaukee | suburb | 48,123 | 45,899 | 400 | 22,125 | 29.95M | 69,679 | 55,682 | 0.559 | 111 |
| 55091 | Pepin | rural | 3,533 | 2,567 | 363 | 25,220 | 3.23M | 61,638 | 29,567 | 0.674 | 143 |
| 55093 | Pierce | suburb | 22,212 | 11,848 | 958 | 67,576 | 12.20M | 53,743 | 30,390 | 0.691 | 157 |
| 55095 | Polk | rural | 21,893 | 16,906 | 1,108 | 58,973 | 14.48M | 63,123 | 24,706 | 0.682 | 86 |
| 55097 | Portage | rural | 36,822 | 37,453 | 1,229 | 78,447 | 29.25M | 64,975 | 37,192 | 0.638 | 56 |
| 55099 | Price | rural | 6,013 | 5,784 | 381 | 12,846 | 6.52M | 59,294 | 17,346 | 0.784 | 35 |
| 55101 | Racine | suburb | 94,221 | 81,223 | 598 | 38,904 | 69.14M | 63,400 | 35,700 | 0.471 | 146 |
| 55103 | Richland | rural | 7,914 | 5,780 | 940 | 32,425 | 6.78M | 60,197 | 31,570 | 0.749 | 124 |
| 55105 | Rock | suburb | 80,958 | 70,781 | 1,421 | 117,911 | 72.33M | 59,855 | 41,540 | 0.577 | 178 |
| 55107 | Rusk | rural | 6,111 | 5,054 | 457 | 33,405 | 6.12M | 44,775 | 33,169 | 0.775 | 74 |
| 55109 | St. Croix | suburb | 50,444 | 40,990 | 1,323 | 80,923 | 26.84M | 52,241 | 34,397 | 0.661 | 136 |
| 55111 | Sauk | rural | 33,750 | 33,831 | 1,417 | 70,567 | 29.45M | 58,277 | 31,723 | 0.668 | 139 |
| 55113 | Sawyer | rural | 7,703 | 7,959 | 177 | 7,780 | 5.63M | 48,493 | 29,000 | 0.697 | 56 |
| 55115 | Shawano | rural | 19,602 | 13,497 | 1,349 | 79,878 | 16.88M | 46,789 | 48,245 | 0.650 | 109 |
| 55117 | Sheboygan | suburb | 60,282 | 60,691 | 1,171 | 61,498 | 45.32M | 68,892 | 31,243 | 0.555 | 123 |
| 55119 | Taylor | rural | 9,763 | 8,189 | 898 | 54,161 | 9.09M | 49,413 | 34,052 | 0.691 | 90 |
| 55121 | Trempealeau | rural | 15,240 | 12,993 | 1,220 | 71,879 | 12.69M | 54,554 | 35,310 | 0.661 | 124 |
| 55123 | Vernon | suburb | 13,711 | 9,238 | 1,524 | 48,392 | 12.30M | 61,976 | 27,675 | 0.716 | 137 |
| 55125 | Vilas | rural | 10,001 | 9,661 | 52 | 997 | 7.79M | 78,372 | 50,676 | 0.657 | 149* |
| 55127 | Walworth | rural | 54,345 | 49,407 | 910 | 77,983 | 38.42M | 57,013 | 36,664 | 0.521 | 198 |
| 55129 | Washburn | rural | 7,064 | 6,418 | 307 | 13,871 | 5.69M | 63,724 | 32,501 | 0.773 | 59 |
| 55131 | Washington | suburb | 73,600 | 60,421 | 737 | 37,497 | 42.95M | 64,878 | 35,825 | 0.552 | 135 |
| 55133 | Waukesha | suburb | 215,530 | 250,834 | 504 | 23,586 | 168.89M | 57,931 | 19,661 | 0.602 | 137 |
| 55135 | Waupaca | rural | 25,573 | 20,678 | 1,130 | 63,120 | 22.05M | 48,883 | 36,574 | 0.672 | 104 |
| 55137 | Waushara | rural | 10,588 | 6,469 | 592 | 54,411 | 8.86M | 65,387 | 27,119 | 0.588 | 71 |
| 55139 | Winnebago | suburb | 88,979 | 97,905 | 1,059 | 52,019 | 78.65M | 44,005 | 29,770 | 0.621 | 100 |
| 55141 | Wood | rural | 35,109 | 36,653 | 1,019 | 55,463 | 35.78M | 88,127 | 32,783 | 0.762 | 86 |
| EXT | External (out-of-state commuting) | external | 74,401 | 96,672 | 2,181 | 127,177 | 56.41M | 58,864 | n/a | 0.657 | n/a |

`*` filled, see above.
