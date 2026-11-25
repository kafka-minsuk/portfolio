# Missouri 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state MO 2022`. 115 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 29 | `MO/CDL_2022_29.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=29 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MO.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (16 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 6,177,957 | 6,177,957 | 0.000% |
| ACS workers by residence | 2,920,193 | 2,920,193 | 0.000% |
| ACS workers by workplace | 2,958,219 | 2,958,219 | 0.000% |
| ACS workers working out of state | 159,487 | 159,487 | 0.000% |
| BEA non-farm employment (L80) | 3,841,188 | 3,841,188 | 0.000% |
| BEA farm employment (L70) | 93,207 | 93,207 | 0.000% |
| BEA farm proprietors (L50) | 86,398 | 86,398 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,635,756,000 | 2,635,756,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 271,769,000 | 271,769,000 | 0.000% |
| CoA hired farm labour expense $ | 585,137,000 | 585,141,000 | -0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 245,345,782,000 | 245,345,782,000 | 0.000% |
| ACS foreign born entered 2010+ | 90,162 | 90,162 | 0.000% |
| CoA owned acres | 17,412,359 | 17,412,359 | 0.000% |
| CoA rented-from-others acres | 9,613,884 | 9,613,884 | 0.000% |
| CoA land in farms, ha | 10,937,133 | 10,937,133 | -0.000% |
| CoA total cropland, ha | 5,975,082 | 5,975,082 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.449, median 0.703, max 1.222; BEA counts jobs, ACS counts people by main job). Sum N = 3,117,706 = sum HU + HA = 3,117,706. Farm jobs after scaling: 65,525 (BEA 93,207). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 197,513. Jobs = in-state residents working out of state = 159,487, split by the state farm share (HA = 3,533). Location: the 55 out-of-state counties within 1 km of the state (05005, 05007, 05009, 05015, 05021, 05031, 05049, 05055, 05089, 05093, 05121, 05135, 17001, 17003, 17013, 17067, 17077, 17083, 17119, 17133, 17149, 17157, 17163, 17181, 19007, 19051, 19053, 19071, 19111, 19145, 19159, 19173, 19177, 19185, 20005, 20011, 20021, 20037, 20043, 20091, 20103, 20107, 20121, 20209, 21007, 21039, 21075, 21105, 31127, 31131, 31147, 40041, 40115, 47045, 47095); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 4,796,740 ha vs Census of Agriculture cropland 5,975,082 ha and land in farms 10,937,133 ha; county ratio TF / CoA cropland 0.04 to 1.23. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 4,517,132 ha). County area covered by CDL pixels: 18,054,526 ha vs land area 17,805,225 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 7.25 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (63,872 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 40,183 $ per BEA farm job, 57,160 $ per farm worker; county range 14,915 to 262,938 $ per worker. State compensation per farm wage job by year: 2018 42,249 $, 2019 39,077 $, 2020 35,906 $, 2021 41,339 $, 2022 39,913 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 79,976,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (585,141,000 $ in 2022, column `hired_labor_coa_usd`) is 2.15x BEA farm compensation (271,769,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 28,279 $, county -16,359 to 239,496 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 84,816 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 3,444,241,000 $ vs CAINC45 2,635,756,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.644, county range 0.188 to 0.914.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 139 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 4,612 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 7 counties have no recent foreign born in the ACS sample (Carter, Hickory, Knox, Mississippi, Montgomery, Stoddard, Worth), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (St. Louis); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (34); rural = the rest (80). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (St. Louis); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 235.3 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.5 straight-line km/h between counties (median 6.8 to 29.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.29).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 29510 St. Louis | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 29510 St. Louis | state owner share |
| cash_rent_usd_acre | 29029 Camden | not published; NASS 'other (combined) counties' value = 50.5 $/acre |
| cash_rent_usd_acre | 29039 Cedar | not published; NASS 'other (combined) counties' value = 50.5 $/acre |
| cash_rent_usd_acre | 29057 Dade | not published; NASS 'other (combined) counties' value = 50.5 $/acre |
| cash_rent_usd_acre | 29091 Howell | not published; NASS 'other (combined) counties' value = 50.5 $/acre |
| cash_rent_usd_acre | 29510 St. Louis | not published; NASS 'other (combined) counties' value = 50.5 $/acre |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26915) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 29001 | Adair | rural | 10,035 | 10,542 | 584 | 43,210 | 9.02M | 35,748 | 11,391 | 0.698 | 106 |
| 29003 | Andrew | suburb | 8,499 | 2,480 | 355 | 58,918 | 6.37M | 40,631 | 28,024 | 0.603 | 159 |
| 29005 | Atchison | rural | 2,521 | 1,818 | 293 | 110,879 | 3.17M | 71,922 | 124,715 | 0.477 | 203 |
| 29007 | Audrain | rural | 10,706 | 8,391 | 718 | 118,345 | 12.66M | 59,641 | 68,629 | 0.491 | 161 |
| 29009 | Barry | rural | 14,783 | 13,991 | 1,013 | 10,687 | 15.87M | 59,455 | 115,077 | 0.777 | 53 |
| 29011 | Barton | rural | 4,603 | 3,215 | 558 | 74,300 | 6.46M | 73,063 | 68,025 | 0.610 | 78 |
| 29013 | Bates | suburb | 6,860 | 3,590 | 682 | 93,458 | 7.38M | 51,065 | 31,273 | 0.567 | 129 |
| 29015 | Benton | rural | 6,959 | 4,187 | 462 | 22,354 | 8.31M | 64,483 | 35,733 | 0.711 | 55 |
| 29017 | Bollinger | suburb | 4,464 | 1,628 | 331 | 28,899 | 4.00M | 55,329 | 6,256 | 0.709 | 64 |
| 29019 | Boone | suburb | 95,304 | 100,856 | 773 | 37,739 | 54.60M | 56,614 | 7,269 | 0.589 | 143 |
| 29021 | Buchanan | suburb | 38,201 | 46,517 | 557 | 49,221 | 43.54M | 28,469 | 38,380 | 0.583 | 125 |
| 29023 | Butler | rural | 17,147 | 18,313 | 377 | 86,112 | 15.77M | 71,604 | 60,208 | 0.387 | 88 |
| 29025 | Caldwell | suburb | 3,747 | 1,817 | 503 | 44,437 | 4.06M | 48,282 | 20,922 | 0.692 | 179 |
| 29027 | Callaway | suburb | 20,411 | 14,785 | 914 | 49,980 | 14.46M | 85,859 | -8,543 | 0.694 | 148 |
| 29029 | Camden | rural | 17,783 | 17,367 | 336 | 1,431 | 24.53M | 67,075 | -3,169 | 0.836 | 50* |
| 29031 | Cape Girardeau | suburb | 40,636 | 43,908 | 847 | 54,544 | 38.11M | 55,870 | 13,553 | 0.571 | 116 |
| 29033 | Carroll | rural | 3,823 | 2,313 | 651 | 98,376 | 6.11M | 56,627 | 63,559 | 0.565 | 148 |
| 29035 | Carter | rural | 2,311 | 1,782 | 139 | 485 | 1.75M | 24,566 | -3,873 | 0.914 | 14 |
| 29037 | Cass | suburb | 53,652 | 30,838 | 976 | 53,527 | 30.94M | 62,339 | 20,962 | 0.576 | 101 |
| 29039 | Cedar | rural | 5,168 | 3,500 | 469 | 10,822 | 5.67M | 43,102 | 6,199 | 0.784 | 50* |
| 29041 | Chariton | rural | 3,172 | 1,568 | 475 | 103,089 | 5.33M | 91,353 | 36,247 | 0.662 | 148 |
| 29043 | Christian | suburb | 43,032 | 21,117 | 638 | 3,976 | 23.47M | 51,996 | -1,000 | 0.694 | 36 |
| 29045 | Clark | rural | 2,832 | 1,265 | 378 | 62,805 | 3.37M | 27,536 | 39,707 | 0.606 | 159 |
| 29047 | Clay | suburb | 131,772 | 114,223 | 393 | 20,287 | 84.53M | 81,219 | 11,179 | 0.651 | 155 |
| 29049 | Clinton | suburb | 9,070 | 4,916 | 497 | 49,053 | 7.31M | 47,137 | 10,046 | 0.597 | 197 |
| 29051 | Cole | suburb | 37,693 | 51,481 | 748 | 14,149 | 29.00M | 46,918 | 1,218 | 0.742 | 69 |
| 29053 | Cooper | suburb | 7,186 | 4,123 | 483 | 63,493 | 6.90M | 65,168 | 55,650 | 0.630 | 95 |
| 29055 | Crawford | rural | 9,009 | 6,620 | 433 | 3,546 | 7.41M | 19,824 | -4,813 | 0.783 | 57 |
| 29057 | Dade | rural | 3,055 | 1,820 | 463 | 24,750 | 3.28M | 66,310 | 38,819 | 0.673 | 50* |
| 29059 | Dallas | suburb | 6,291 | 2,953 | 664 | 4,664 | 5.86M | 55,955 | 6,895 | 0.766 | 38 |
| 29061 | Daviess | rural | 3,625 | 1,719 | 636 | 62,857 | 4.52M | 39,928 | 93 | 0.676 | 162 |
| 29063 | DeKalb | suburb | 4,208 | 3,010 | 563 | 50,055 | 3.92M | 46,195 | 11,117 | 0.663 | 135 |
| 29065 | Dent | rural | 5,917 | 4,721 | 504 | 1,857 | 5.82M | 40,258 | 6,308 | 0.753 | 36 |
| 29067 | Douglas | rural | 4,272 | 2,703 | 561 | 889 | 5.40M | 50,906 | -6,656 | 0.766 | 40 |
| 29069 | Dunklin | rural | 10,860 | 8,792 | 303 | 116,712 | 10.27M | 95,359 | 126,814 | 0.220 | 126 |
| 29071 | Franklin | suburb | 49,186 | 40,225 | 1,219 | 29,808 | 32.20M | 37,498 | -6,713 | 0.652 | 72 |
| 29073 | Gasconade | rural | 6,988 | 5,317 | 529 | 16,103 | 6.55M | 58,838 | 5,673 | 0.775 | 60 |
| 29075 | Gentry | rural | 2,781 | 1,968 | 430 | 53,360 | 3.81M | 95,868 | 9,801 | 0.679 | 149 |
| 29077 | Greene | suburb | 142,571 | 179,800 | 1,228 | 9,047 | 118.58M | 44,972 | -7,021 | 0.612 | 42 |
| 29079 | Grundy | rural | 3,979 | 3,155 | 463 | 52,508 | 6.01M | 50,565 | 29,884 | 0.565 | 152 |
| 29081 | Harrison | rural | 3,335 | 2,561 | 655 | 68,763 | 4.53M | 44,354 | 15,771 | 0.715 | 146 |
| 29083 | Henry | rural | 9,114 | 8,236 | 637 | 52,218 | 10.19M | 54,006 | 30,132 | 0.642 | 104 |
| 29085 | Hickory | rural | 2,478 | 1,494 | 268 | 7,643 | 3.49M | 56,708 | 13,444 | 0.715 | 58 |
| 29087 | Holt | rural | 1,918 | 1,431 | 243 | 84,349 | 2.72M | 83,270 | 107,640 | 0.539 | 205 |
| 29089 | Howard | suburb | 4,286 | 2,403 | 409 | 43,429 | 4.30M | 84,249 | 25,305 | 0.714 | 140 |
| 29091 | Howell | rural | 15,459 | 15,518 | 1,049 | 1,682 | 14.38M | 41,542 | 9,594 | 0.787 | 50* |
| 29093 | Iron | rural | 3,879 | 2,918 | 164 | 852 | 2.88M | 23,427 | -12,551 | 0.903 | 30 |
| 29095 | Jackson | suburb | 355,790 | 403,971 | 560 | 24,815 | 278.68M | 21,883 | 11,126 | 0.665 | 142 |
| 29097 | Jasper | suburb | 56,502 | 58,948 | 993 | 47,921 | 51.53M | 51,659 | 34,885 | 0.660 | 90 |
| 29099 | Jefferson | suburb | 113,879 | 58,509 | 503 | 6,426 | 62.78M | 46,497 | -6,165 | 0.700 | 58 |
| 29101 | Johnson | rural | 26,671 | 22,277 | 1,258 | 67,142 | 17.48M | 70,686 | 25,504 | 0.679 | 100 |
| 29103 | Knox | rural | 1,630 | 1,044 | 393 | 67,005 | 2.86M | 50,442 | 18,077 | 0.681 | 161 |
| 29105 | Laclede | rural | 15,409 | 14,981 | 1,021 | 5,251 | 12.83M | 34,828 | 634 | 0.821 | 43 |
| 29107 | Lafayette | suburb | 15,360 | 10,001 | 835 | 95,604 | 14.64M | 89,478 | 41,608 | 0.571 | 174 |
| 29109 | Lawrence | rural | 16,375 | 10,356 | 1,442 | 25,468 | 14.72M | 48,744 | 48,348 | 0.731 | 60 |
| 29111 | Lewis | rural | 4,296 | 2,586 | 495 | 68,435 | 4.47M | 37,153 | 12,055 | 0.545 | 169 |
| 29113 | Lincoln | suburb | 28,259 | 12,515 | 667 | 56,666 | 14.89M | 82,440 | 13,030 | 0.639 | 147 |
| 29115 | Linn | rural | 5,457 | 4,097 | 628 | 61,886 | 6.40M | 67,162 | 20,058 | 0.663 | 132 |
| 29117 | Livingston | rural | 6,131 | 6,808 | 572 | 70,040 | 8.90M | 57,996 | 42,694 | 0.727 | 186 |
| 29119 | McDonald | rural | 9,528 | 6,496 | 609 | 4,125 | 6.66M | 56,865 | 101,803 | 0.751 | 44 |
| 29121 | Macon | rural | 6,511 | 4,708 | 741 | 74,120 | 7.53M | 66,974 | 23,143 | 0.714 | 119 |
| 29123 | Madison | rural | 5,399 | 4,384 | 282 | 2,326 | 4.06M | 97,616 | -3,959 | 0.859 | 22 |
| 29125 | Maries | rural | 3,441 | 1,247 | 379 | 8,442 | 3.53M | 77,098 | -2,932 | 0.750 | 22 |
| 29127 | Marion | rural | 13,135 | 14,442 | 559 | 56,550 | 14.62M | 33,321 | 30,112 | 0.576 | 192 |
| 29129 | Mercer | rural | 1,484 | 874 | 392 | 36,544 | 2.62M | 262,938 | 18,851 | 0.655 | 119 |
| 29131 | Miller | rural | 11,107 | 7,762 | 613 | 8,631 | 9.92M | 53,483 | 19,532 | 0.721 | 77 |
| 29133 | Mississippi | rural | 4,271 | 3,098 | 204 | 91,127 | 4.83M | 79,231 | 205,204 | 0.259 | 189 |
| 29135 | Moniteau | suburb | 6,708 | 3,705 | 617 | 24,897 | 6.98M | 61,157 | 45,404 | 0.712 | 76 |
| 29137 | Monroe | rural | 3,592 | 1,844 | 590 | 76,768 | 5.41M | 74,612 | 25,348 | 0.604 | 156 |
| 29139 | Montgomery | rural | 5,004 | 3,358 | 476 | 58,158 | 6.09M | 81,398 | 20,573 | 0.614 | 129 |
| 29141 | Morgan | rural | 7,673 | 5,842 | 654 | 14,511 | 11.29M | 59,317 | 91,551 | 0.682 | 95 |
| 29143 | New Madrid | rural | 6,385 | 6,506 | 287 | 154,193 | 9.26M | 79,692 | 239,496 | 0.257 | 139 |
| 29145 | Newton | suburb | 26,066 | 25,282 | 1,358 | 17,409 | 20.17M | 40,744 | 79,187 | 0.761 | 61 |
| 29147 | Nodaway | rural | 9,880 | 8,951 | 808 | 129,228 | 10.34M | 55,686 | 24,455 | 0.632 | 175 |
| 29149 | Oregon | rural | 3,205 | 2,567 | 495 | 972 | 3.52M | 56,560 | 7,368 | 0.786 | 36 |
| 29151 | Osage | suburb | 6,686 | 4,383 | 702 | 18,642 | 6.94M | 61,777 | 22,355 | 0.740 | 64 |
| 29153 | Ozark | rural | 2,892 | 1,498 | 319 | 645 | 3.90M | 45,641 | -2,380 | 0.800 | 32 |
| 29155 | Pemiscot | rural | 5,504 | 4,988 | 234 | 110,431 | 5.06M | 76,848 | 219,908 | 0.188 | 135 |
| 29157 | Perry | rural | 8,936 | 9,647 | 681 | 40,055 | 9.75M | 61,130 | 20,196 | 0.658 | 128 |
| 29159 | Pettis | rural | 19,837 | 20,887 | 1,031 | 77,829 | 21.27M | 56,522 | 63,613 | 0.696 | 116 |
| 29161 | Phelps | rural | 18,728 | 20,551 | 567 | 3,354 | 15.30M | 14,915 | -9,808 | 0.780 | 22 |
| 29163 | Pike | rural | 6,653 | 5,802 | 679 | 72,679 | 7.31M | 58,768 | 22,268 | 0.650 | 137 |
| 29165 | Platte | suburb | 56,479 | 51,492 | 417 | 39,447 | 33.10M | 46,925 | 39,230 | 0.493 | 189 |
| 29167 | Polk | suburb | 13,854 | 9,822 | 970 | 13,106 | 10.14M | 49,471 | 24,639 | 0.734 | 30 |
| 29169 | Pulaski | rural | 26,813 | 27,535 | 471 | 2,031 | 11.98M | 16,767 | -7,810 | 0.745 | 17 |
| 29171 | Putnam | rural | 2,064 | 1,093 | 423 | 34,848 | 2.98M | 97,692 | 13,435 | 0.634 | 122 |
| 29173 | Ralls | rural | 4,518 | 2,942 | 384 | 59,095 | 6.11M | 77,790 | 26,166 | 0.465 | 171 |
| 29175 | Randolph | rural | 10,602 | 10,558 | 603 | 41,814 | 11.38M | 37,279 | 26,508 | 0.671 | 157 |
| 29177 | Ray | suburb | 10,894 | 5,338 | 810 | 60,514 | 8.71M | 47,503 | 29,704 | 0.635 | 160 |
| 29179 | Reynolds | rural | 2,365 | 1,974 | 262 | 935 | 2.02M | 18,909 | -16,359 | 0.817 | 20 |
| 29181 | Ripley | rural | 4,194 | 2,572 | 249 | 10,195 | 3.76M | 40,253 | 22,261 | 0.638 | 22 |
| 29183 | St. Charles | suburb | 215,074 | 173,208 | 401 | 45,641 | 127.46M | 66,750 | 23,970 | 0.493 | 149 |
| 29185 | St. Clair | rural | 3,728 | 2,051 | 469 | 31,039 | 3.86M | 55,809 | 17,497 | 0.584 | 109 |
| 29186 | Ste. Genevieve | rural | 8,261 | 5,716 | 375 | 18,627 | 7.01M | 92,465 | 5,094 | 0.679 | 87 |
| 29187 | St. Francois | rural | 26,358 | 24,767 | 507 | 5,039 | 20.74M | 20,679 | -8,940 | 0.762 | 52 |
| 29189 | St. Louis | core | 491,731 | 593,216 | 179 | 6,053 | 471.04M | 73,817 | 22,500 | 0.578 | 161 |
| 29195 | Saline | rural | 10,279 | 9,148 | 732 | 126,255 | 12.36M | 75,405 | 101,726 | 0.535 | 169 |
| 29197 | Schuyler | rural | 1,591 | 593 | 253 | 26,773 | 1.83M | 34,290 | 14,191 | 0.650 | 133 |
| 29199 | Scotland | rural | 1,923 | 1,372 | 398 | 55,526 | 3.44M | 47,323 | 27,672 | 0.656 | 133 |
| 29201 | Scott | rural | 17,157 | 17,194 | 398 | 81,058 | 17.35M | 91,041 | 117,730 | 0.320 | 202 |
| 29203 | Shannon | rural | 2,672 | 1,935 | 272 | 830 | 2.40M | 42,062 | 118 | 0.864 | 26 |
| 29205 | Shelby | rural | 2,665 | 1,608 | 385 | 73,476 | 3.68M | 52,132 | 22,499 | 0.562 | 155 |
| 29207 | Stoddard | rural | 11,774 | 10,806 | 655 | 153,835 | 12.35M | 77,593 | 92,821 | 0.321 | 115 |
| 29209 | Stone | rural | 11,736 | 8,217 | 353 | 1,226 | 11.99M | 46,503 | 22,212 | 0.818 | 49 |
| 29211 | Sullivan | rural | 2,621 | 2,400 | 572 | 40,507 | 3.60M | 249,021 | 15,505 | 0.716 | 118 |
| 29213 | Taney | rural | 24,653 | 28,226 | 293 | 541 | 19.63M | 33,629 | 11,302 | 0.748 | 15 |
| 29215 | Texas | rural | 8,980 | 10,939 | 1,430 | 4,225 | 8.51M | 29,912 | 10,253 | 0.808 | 31 |
| 29217 | Vernon | rural | 8,229 | 7,095 | 1,002 | 78,322 | 9.43M | 33,005 | 38,776 | 0.588 | 91 |
| 29219 | Warren | suburb | 16,913 | 9,185 | 390 | 24,608 | 9.46M | 66,916 | 14,638 | 0.711 | 136 |
| 29221 | Washington | rural | 9,003 | 5,164 | 367 | 1,272 | 5.79M | 26,605 | -7,651 | 0.872 | 26 |
| 29223 | Wayne | rural | 3,658 | 2,238 | 234 | 3,317 | 3.44M | 27,492 | 4,617 | 0.877 | 26 |
| 29225 | Webster | suburb | 15,919 | 8,878 | 1,011 | 5,040 | 11.76M | 51,317 | -3,655 | 0.782 | 36 |
| 29227 | Worth | rural | 888 | 465 | 225 | 21,628 | 1.00M | 24,514 | 7,333 | 0.770 | 157 |
| 29229 | Wright | rural | 6,803 | 5,045 | 819 | 1,934 | 7.55M | 47,640 | -1,100 | 0.836 | 37 |
| 29510 | St. Louis | suburb | 151,829 | 247,093 | 0 | 17 | 135.67M | 0 | n/a | 0.644 | 50* |
| EXT | External (out-of-state commuting) | external | 197,513 | 155,954 | 3,533 | 258,608 | 163.47M | 57,160 | n/a | 0.644 | n/a |

`*` filled, see above.
