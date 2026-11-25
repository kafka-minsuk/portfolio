# Pennsylvania 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state PA 2022`. 67 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 42 | `PA/CDL_2022_42.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=42 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_PA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 12,972,008 | 12,972,008 | 0.000% |
| ACS workers by residence | 6,200,303 | 6,200,303 | 0.000% |
| ACS workers by workplace | 6,149,039 | 6,149,039 | 0.000% |
| ACS workers working out of state | 285,884 | 285,884 | 0.000% |
| BEA non-farm employment (L80) | 7,910,832 | 7,910,832 | 0.000% |
| BEA farm employment (L70) | 67,488 | 67,488 | 0.000% |
| BEA farm proprietors (L50) | 48,074 | 48,074 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,339,191,000 | 2,339,191,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 758,568,000 | 758,568,000 | 0.000% |
| CoA hired farm labour expense $ | 1,022,301,000 | 1,023,296,000 | -0.097% |
| BEA non-farm earnings $ (CAINC5N L82) | 565,707,023,000 | 565,707,023,000 | 0.000% |
| ACS foreign born entered 2010+ | 312,172 | 312,172 | 0.000% |
| CoA owned acres | 4,849,030 | 4,849,030 | 0.000% |
| CoA rented-from-others acres | 2,209,295 | 2,209,295 | 0.000% |
| CoA land in farms, ha | 2,856,403 | 2,856,403 | 0.000% |
| CoA total cropland, ha | 1,793,288 | 1,793,288 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.684, median 0.800, max 0.885; BEA counts jobs, ACS counts people by main job). Sum N = 6,434,923 = sum HU + HA = 6,434,923. Farm jobs after scaling: 52,779 (BEA 67,488). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 234,620. Jobs = in-state residents working out of state = 285,884, split by the state farm share (HA = 2,454). Location: the 38 out-of-state counties within 1 km of the state (10003, 24001, 24005, 24013, 24015, 24021, 24023, 24025, 24043, 34005, 34007, 34015, 34019, 34021, 34033, 34037, 34041, 36003, 36007, 36009, 36013, 36015, 36025, 36071, 36101, 36105, 36107, 39007, 39029, 39099, 39155, 54009, 54029, 54051, 54061, 54069, 54077, 54103); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,527,120 ha vs Census of Agriculture cropland 1,793,288 ha and land in farms 2,856,403 ha; county ratio TF / CoA cropland 0.13 to 3.09. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,142,818 ha). County area covered by CDL pixels: 11,734,027 ha vs land area 11,588,212 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 10.72 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (71,510 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 29,338 $ per BEA farm job, 37,514 $ per farm worker; county range 21,051 to 66,458 $ per worker. State compensation per farm wage job by year: 2018 28,078 $, 2019 25,120 $, 2020 31,232 $, 2021 24,285 $, 2022 39,073 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 123,189,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,023,296,000 $ in 2022, column `hired_labor_coa_usd`) is 1.35x BEA farm compensation (758,568,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 34,661 $, county -8,550 to 105,590 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 92,796 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 3,031,940,000 $ vs CAINC45 2,339,191,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.687, county range 0.388 to 0.938.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 100 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 8,019 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Philadelphia); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (32); rural = the rest (34). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 202.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 54.6 straight-line km/h between counties (median 10.5 to 32.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.31).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 42023 Cameron | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42045 Delaware | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42047 Elk | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42053 Forest | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42101 Philadelphia | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42103 Pike | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42113 Sullivan | not published; NASS 'other (combined) counties' value = 137 $/acre |
| cash_rent_usd_acre | 42133 York | not published; NASS 'other (combined) counties' value = 137 $/acre |
| hired_labor_coa_usd | 42047 Elk | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 42053 Forest | (D) in Census of Ag; left null (comparison column only) |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

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
| 42001 | Adams | suburb | 50,568 | 34,673 | 1,255 | 44,848 | 29.63M | 53,866 | 30,507 | 0.563 | 90 |
| 42003 | Allegheny | suburb | 627,652 | 706,169 | 372 | 3,208 | 442.06M | 21,051 | 7,934 | 0.822 | 24 |
| 42005 | Armstrong | suburb | 29,788 | 18,782 | 585 | 25,942 | 16.57M | 29,024 | 12,296 | 0.644 | 28 |
| 42007 | Beaver | suburb | 78,748 | 61,932 | 541 | 7,198 | 47.84M | 25,591 | 4,911 | 0.815 | 65 |
| 42009 | Bedford | rural | 21,872 | 17,058 | 944 | 33,172 | 15.76M | 37,799 | 23,007 | 0.743 | 88 |
| 42011 | Berks | suburb | 206,685 | 180,527 | 2,206 | 57,670 | 104.08M | 60,845 | 57,999 | 0.658 | 92 |
| 42013 | Blair | suburb | 56,376 | 60,754 | 529 | 19,065 | 45.07M | 39,103 | 68,850 | 0.652 | 179 |
| 42015 | Bradford | rural | 25,435 | 22,898 | 1,266 | 63,193 | 19.55M | 31,790 | 20,275 | 0.728 | 28 |
| 42017 | Bucks | suburb | 334,130 | 290,231 | 727 | 13,835 | 167.96M | 47,401 | 22,711 | 0.476 | 50 |
| 42019 | Butler | suburb | 94,590 | 95,981 | 845 | 32,606 | 46.89M | 34,864 | 7,205 | 0.633 | 48 |
| 42021 | Cambria | suburb | 56,653 | 52,501 | 428 | 16,992 | 36.92M | 38,275 | 7,383 | 0.595 | 36 |
| 42023 | Cameron | rural | 1,777 | 1,795 | 28 | 513 | 1.29M | 23,744 | 15,364 | 0.938 | 137* |
| 42025 | Carbon | suburb | 29,552 | 16,329 | 147 | 4,974 | 12.63M | 45,208 | -8,550 | 0.713 | 36 |
| 42027 | Centre | suburb | 73,011 | 81,506 | 875 | 30,781 | 33.89M | 41,641 | 28,050 | 0.763 | 95 |
| 42029 | Chester | suburb | 278,038 | 268,854 | 3,909 | 28,415 | 113.01M | 48,030 | 37,852 | 0.586 | 165 |
| 42031 | Clarion | rural | 17,008 | 14,738 | 498 | 22,445 | 11.80M | 38,391 | 10,908 | 0.754 | 26 |
| 42033 | Clearfield | rural | 34,235 | 31,707 | 418 | 10,227 | 20.77M | 26,587 | 9,565 | 0.801 | 18 |
| 42035 | Clinton | rural | 17,268 | 14,848 | 422 | 10,280 | 10.95M | 40,818 | 32,350 | 0.724 | 76 |
| 42037 | Columbia | rural | 29,912 | 26,923 | 750 | 26,766 | 19.44M | 40,180 | 14,599 | 0.639 | 66 |
| 42039 | Crawford | rural | 35,404 | 31,615 | 1,107 | 54,323 | 22.21M | 45,641 | 15,741 | 0.669 | 35 |
| 42041 | Cumberland | suburb | 128,792 | 138,236 | 1,121 | 41,902 | 100.03M | 32,791 | 53,187 | 0.547 | 132 |
| 42043 | Dauphin | suburb | 142,055 | 181,223 | 606 | 24,380 | 97.51M | 44,032 | 49,285 | 0.557 | 70 |
| 42045 | Delaware | suburb | 279,844 | 231,373 | 115 | 586 | 157.71M | 42,262 | 20,708 | 0.819 | 137* |
| 42047 | Elk | rural | 14,790 | 14,454 | 182 | 2,683 | 10.61M | 31,571 | 1,299 | 0.844 | 137* |
| 42049 | Erie | suburb | 122,518 | 125,941 | 1,205 | 41,095 | 99.54M | 43,551 | 10,883 | 0.776 | 46 |
| 42051 | Fayette | suburb | 53,239 | 39,485 | 640 | 19,792 | 35.27M | 41,375 | 3,846 | 0.740 | 31 |
| 42053 | Forest | rural | 1,589 | 2,249 | 43 | 1,364 | 1.65M | 43,883 | 14,592 | 0.815 | 137* |
| 42055 | Franklin | suburb | 74,492 | 65,694 | 1,782 | 65,421 | 53.08M | 34,682 | 72,776 | 0.637 | 121 |
| 42057 | Fulton | rural | 6,793 | 4,976 | 508 | 15,410 | 5.66M | 30,852 | 29,440 | 0.705 | 72 |
| 42059 | Greene | rural | 13,771 | 13,751 | 646 | 6,308 | 10.29M | 34,854 | 3,256 | 0.789 | 31 |
| 42061 | Huntingdon | rural | 18,037 | 14,241 | 759 | 25,381 | 11.08M | 34,290 | 36,812 | 0.750 | 70 |
| 42063 | Indiana | rural | 35,567 | 32,640 | 983 | 31,851 | 22.27M | 28,023 | 8,524 | 0.704 | 50 |
| 42065 | Jefferson | rural | 19,578 | 17,485 | 451 | 16,006 | 12.72M | 25,567 | 13,481 | 0.653 | 27 |
| 42067 | Juniata | rural | 10,838 | 7,678 | 590 | 19,816 | 7.23M | 30,021 | 67,348 | 0.640 | 95 |
| 42069 | Lackawanna | suburb | 100,713 | 98,062 | 220 | 3,029 | 69.49M | 60,376 | -1,034 | 0.648 | 30 |
| 42071 | Lancaster | suburb | 274,411 | 263,801 | 5,107 | 96,656 | 154.13M | 39,597 | 84,828 | 0.675 | 260 |
| 42073 | Lawrence | suburb | 38,089 | 30,628 | 483 | 21,833 | 26.66M | 50,410 | 6,838 | 0.665 | 51 |
| 42075 | Lebanon | suburb | 68,005 | 60,488 | 1,198 | 30,294 | 39.95M | 29,535 | 105,590 | 0.619 | 221 |
| 42077 | Lehigh | suburb | 180,104 | 194,298 | 443 | 20,998 | 101.78M | 66,458 | 33,270 | 0.492 | 101 |
| 42079 | Luzerne | suburb | 150,800 | 152,526 | 442 | 12,273 | 101.31M | 26,807 | 1,176 | 0.660 | 49 |
| 42081 | Lycoming | suburb | 51,688 | 51,748 | 911 | 27,238 | 40.02M | 32,893 | 19,508 | 0.863 | 52 |
| 42083 | McKean | rural | 17,283 | 15,361 | 208 | 5,515 | 8.91M | 29,361 | 11,815 | 0.841 | 15 |
| 42085 | Mercer | rural | 47,137 | 47,929 | 957 | 43,557 | 39.68M | 31,534 | 1,592 | 0.666 | 51 |
| 42087 | Mifflin | rural | 21,056 | 17,088 | 668 | 19,237 | 12.88M | 27,168 | 46,823 | 0.726 | 94 |
| 42089 | Monroe | rural | 77,614 | 66,393 | 254 | 4,313 | 29.68M | 34,013 | 3,231 | 0.848 | 65 |
| 42091 | Montgomery | suburb | 443,958 | 518,148 | 489 | 6,325 | 222.29M | 44,996 | 12,204 | 0.575 | 59 |
| 42093 | Montour | rural | 8,683 | 15,351 | 392 | 11,792 | 7.33M | 38,209 | 25,098 | 0.720 | 103 |
| 42095 | Northampton | suburb | 153,491 | 142,614 | 469 | 23,492 | 86.17M | 31,143 | -575 | 0.388 | 71 |
| 42097 | Northumberland | rural | 40,657 | 30,618 | 782 | 33,277 | 27.08M | 39,370 | 39,955 | 0.621 | 113 |
| 42099 | Perry | suburb | 22,091 | 9,999 | 680 | 25,078 | 10.31M | 33,664 | 62,909 | 0.654 | 71 |
| 42101 | Philadelphia | core | 717,569 | 790,134 | 35 | 66 | 281.33M | 27,436 | 50,512 | 0.791 | 137* |
| 42103 | Pike | rural | 25,645 | 14,755 | 34 | 464 | 8.37M | 63,277 | 12,417 | 0.806 | 137* |
| 42105 | Potter | rural | 6,670 | 6,178 | 360 | 12,207 | 4.40M | 47,821 | 34,668 | 0.805 | 28 |
| 42107 | Schuylkill | rural | 63,364 | 54,314 | 878 | 24,164 | 36.70M | 36,377 | 30,605 | 0.618 | 40 |
| 42109 | Snyder | rural | 19,142 | 17,668 | 819 | 21,856 | 12.96M | 24,595 | 75,518 | 0.679 | 82 |
| 42111 | Somerset | rural | 31,886 | 25,833 | 944 | 39,201 | 20.14M | 27,508 | 23,739 | 0.712 | 38 |
| 42113 | Sullivan | rural | 2,507 | 1,992 | 142 | 5,667 | 2.19M | 26,459 | 14,506 | 0.795 | 137* |
| 42115 | Susquehanna | rural | 16,495 | 11,271 | 687 | 13,039 | 10.92M | 30,311 | 19,271 | 0.765 | 16 |
| 42117 | Tioga | rural | 18,275 | 15,871 | 933 | 33,464 | 10.77M | 21,949 | 12,818 | 0.728 | 30 |
| 42119 | Union | rural | 16,432 | 20,247 | 523 | 18,915 | 12.20M | 32,129 | 93,284 | 0.697 | 104 |
| 42121 | Venango | rural | 21,359 | 18,952 | 338 | 12,525 | 13.14M | 23,773 | 105 | 0.731 | 24 |
| 42123 | Warren | rural | 16,977 | 15,638 | 477 | 11,079 | 12.37M | 29,725 | 13,721 | 0.831 | 24 |
| 42125 | Washington | suburb | 100,001 | 93,875 | 1,370 | 16,789 | 60.22M | 29,601 | -2,168 | 0.830 | 18 |
| 42127 | Wayne | rural | 20,812 | 18,352 | 509 | 2,035 | 11.72M | 59,317 | 12,262 | 0.741 | 26 |
| 42129 | Westmoreland | suburb | 169,014 | 149,940 | 1,063 | 29,958 | 111.33M | 29,603 | 12,362 | 0.672 | 40 |
| 42131 | Wyoming | suburb | 11,892 | 11,395 | 427 | 8,760 | 8.48M | 24,305 | -6,840 | 0.739 | 16 |
| 42133 | York | suburb | 225,878 | 195,549 | 2,051 | 73,574 | 134.32M | 26,927 | 12,475 | 0.574 | 137* |
| EXT | External (out-of-state commuting) | external | 234,620 | 283,430 | 2,454 | 71,000 | 135.17M | 37,514 | n/a | 0.687 | n/a |

`*` filled, see above.
