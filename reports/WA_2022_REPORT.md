# Washington 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state WA 2022`. 39 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 53 | `WA/CDL_2022_53.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=53 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_WA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 7,785,786 | 7,785,786 | 0.000% |
| ACS workers by residence | 3,722,716 | 3,722,716 | 0.000% |
| ACS workers by workplace | 3,687,031 | 3,687,031 | 0.000% |
| ACS workers working out of state | 99,583 | 99,583 | 0.000% |
| BEA non-farm employment (L80) | 4,726,156 | 4,726,156 | 0.000% |
| BEA farm employment (L70) | 89,467 | 89,467 | 0.000% |
| BEA farm proprietors (L50) | 30,686 | 30,686 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 3,878,995,000 | 3,878,995,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 2,805,433,000 | 2,805,433,000 | 0.000% |
| CoA hired farm labour expense $ | 2,761,702,000 | 2,761,698,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 412,749,321,000 | 412,749,321,000 | 0.000% |
| ACS foreign born entered 2010+ | 361,568 | 361,568 | 0.000% |
| CoA owned acres | 7,627,321 | 8,140,932 | -6.309% |
| CoA rented-from-others acres | 5,688,819 | 5,714,482 | -0.449% |
| CoA land in farms, ha | 5,607,087 | 5,607,087 | 0.000% |
| CoA total cropland, ha | 2,981,910 | 2,981,910 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.596, median 0.775, max 0.907; BEA counts jobs, ACS counts people by main job). Sum N = 3,786,614 = sum HU + HA = 3,786,614. Farm jobs after scaling: 69,061 (BEA 89,467). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 63,898. Jobs = in-state residents working out of state = 99,583, split by the state farm share (HA = 1,865). Location: the 16 out-of-state counties within 1 km of the state (16009, 16017, 16021, 16055, 16057, 16069, 41007, 41009, 41021, 41027, 41049, 41051, 41055, 41059, 41063, 41065); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 2,645,514 ha vs Census of Agriculture cropland 2,981,910 ha and land in farms 5,607,087 ha; county ratio TF / CoA cropland 0.07 to 1.06. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 2,204,737 ha). County area covered by CDL pixels: 17,533,235 ha vs land area 17,211,886 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 7.67 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (87,333 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 41,691 $ per BEA farm job, 54,010 $ per farm worker; county range 32,595 to 83,963 $ per worker. State compensation per farm wage job by year: 2018 33,253 $, 2019 30,818 $, 2020 42,961 $, 2021 37,990 $, 2022 47,727 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 453,013,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (2,761,698,000 $ in 2022, column `hired_labor_coa_usd`) is 0.98x BEA farm compensation (2,805,433,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 43,357 $, county 3,057 to 107,221 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 114,083 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 4,054,040,000 $ vs CAINC45 3,878,995,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.573, county range 0.373 to 0.959.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 76 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,824 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 1 counties have no recent foreign born in the ACS sample (Garfield), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (King); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (18); rural = the rest (20). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 276.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 53.4 straight-line km/h between counties (median 12.4 to 68.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.39).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| omega | 53019 Ferry | state owner share |
| omega | 53029 Island | state owner share |
| cash_rent_usd_acre | 53005 Benton | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53007 Chelan | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53009 Clallam | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53015 Cowlitz | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53019 Ferry | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53021 Franklin | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53025 Grant | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53031 Jefferson | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53035 Kitsap | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53037 Kittitas | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53045 Mason | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53047 Okanogan | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53059 Skamania | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53069 Wahkiakum | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| cash_rent_usd_acre | 53077 Yakima | not published; NASS 'other (combined) counties' value = 48.5 $/acre |
| owned_acres | 53019 Ferry | (D) in Census of Ag; see fills above |
| owned_acres | 53029 Island | (D) in Census of Ag; see fills above |
| rented_acres | 53019 Ferry | (D) in Census of Ag; see fills above |
| rented_acres | 53029 Island | (D) in Census of Ag; see fills above |
| t | 53055 San Juan | no road route to 54 places (OSRM); straight-line distance at the median routed speed |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26910) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 53001 | Adams | rural | 8,050 | 6,518 | 1,267 | 283,055 | 7.63M | 66,991 | 76,317 | 0.486 | 38 |
| 53003 | Asotin | suburb | 9,300 | 7,353 | 166 | 22,575 | 12.47M | 41,487 | 44,853 | 0.654 | 44 |
| 53005 | Benton | suburb | 92,769 | 89,890 | 3,879 | 178,112 | 79.24M | 51,029 | 39,473 | 0.562 | 48* |
| 53007 | Chelan | suburb | 36,824 | 37,300 | 3,309 | 11,838 | 38.77M | 45,758 | 27,995 | 0.916 | 48* |
| 53009 | Clallam | rural | 29,996 | 28,446 | 528 | 440 | 25.69M | 64,161 | 13,168 | 0.782 | 48* |
| 53011 | Clark | suburb | 237,782 | 195,459 | 1,479 | 2,209 | 164.64M | 60,992 | 9,566 | 0.863 | 83 |
| 53013 | Columbia | rural | 1,743 | 1,397 | 261 | 72,655 | 2.14M | 64,708 | 71,149 | 0.538 | 80 |
| 53015 | Cowlitz | suburb | 45,906 | 41,877 | 612 | 914 | 44.59M | 83,963 | 40,264 | 0.827 | 48* |
| 53017 | Douglas | suburb | 20,326 | 13,052 | 1,709 | 152,956 | 20.07M | 43,939 | 41,907 | 0.456 | 46 |
| 53019 | Ferry | rural | 2,460 | 2,247 | 196 | 2,922 | 2.25M | 45,078 | 15,241 | 0.588 | 48* |
| 53021 | Franklin | suburb | 42,094 | 33,437 | 3,075 | 157,552 | 33.85M | 57,684 | 67,572 | 0.407 | 48* |
| 53023 | Garfield | rural | 862 | 638 | 147 | 61,652 | 1.32M | 47,678 | 100,507 | 0.549 | 68 |
| 53025 | Grant | rural | 42,635 | 38,492 | 6,524 | 306,481 | 37.91M | 47,434 | 47,283 | 0.455 | 48* |
| 53027 | Grays Harbor | rural | 28,624 | 26,143 | 683 | 1,631 | 29.90M | 55,288 | 41,072 | 0.959 | 51 |
| 53029 | Island | rural | 38,999 | 30,598 | 414 | 1,307 | 21.11M | 50,023 | 21,722 | 0.588 | 73 |
| 53031 | Jefferson | rural | 11,478 | 10,865 | 214 | 202 | 10.13M | 63,943 | 21,752 | 0.768 | 48* |
| 53033 | King | core | 1,212,908 | 1,401,215 | 2,152 | 1,922 | 690.32M | 70,461 | 31,780 | 0.721 | 103 |
| 53035 | Kitsap | suburb | 131,017 | 123,282 | 741 | 184 | 66.12M | 58,325 | 8,411 | 0.823 | 48* |
| 53037 | Kittitas | rural | 21,580 | 18,159 | 1,282 | 19,112 | 18.42M | 51,529 | 24,093 | 0.550 | 48* |
| 53039 | Klickitat | rural | 9,249 | 7,770 | 990 | 72,031 | 9.74M | 63,445 | 44,175 | 0.592 | 20 |
| 53041 | Lewis | rural | 33,406 | 28,570 | 1,415 | 4,359 | 30.84M | 66,253 | 54,547 | 0.793 | 53 |
| 53043 | Lincoln | rural | 4,418 | 3,064 | 578 | 294,854 | 6.29M | 54,569 | 64,413 | 0.378 | 60 |
| 53045 | Mason | rural | 25,535 | 17,208 | 456 | 545 | 15.75M | 69,331 | 28,342 | 0.844 | 48* |
| 53047 | Okanogan | rural | 17,501 | 15,270 | 2,576 | 34,487 | 14.15M | 41,536 | 25,464 | 0.806 | 48* |
| 53049 | Pacific | rural | 8,482 | 6,991 | 420 | 751 | 10.43M | 63,401 | 25,981 | 0.896 | 52 |
| 53051 | Pend Oreille | rural | 4,806 | 3,326 | 192 | 3,516 | 4.53M | 52,763 | 12,804 | 0.865 | 28 |
| 53053 | Pierce | suburb | 446,913 | 390,422 | 1,760 | 872 | 311.10M | 53,150 | 23,662 | 0.833 | 106 |
| 53055 | San Juan | rural | 8,106 | 7,718 | 210 | 212 | 5.57M | 54,992 | 9,527 | 0.609 | 40 |
| 53057 | Skagit | suburb | 57,119 | 54,760 | 2,299 | 23,746 | 47.62M | 59,626 | 52,783 | 0.542 | 262 |
| 53059 | Skamania | suburb | 5,511 | 3,210 | 133 | 418 | 2.67M | 32,595 | 3,057 | 0.743 | 48* |
| 53061 | Snohomish | suburb | 418,564 | 334,800 | 1,948 | 8,936 | 244.68M | 52,326 | 37,846 | 0.629 | 181 |
| 53063 | Spokane | suburb | 246,816 | 256,287 | 2,728 | 140,439 | 225.27M | 44,940 | 22,072 | 0.506 | 52 |
| 53065 | Stevens | suburb | 17,576 | 12,844 | 921 | 26,372 | 16.34M | 52,422 | 17,185 | 0.672 | 49 |
| 53067 | Thurston | suburb | 137,214 | 122,282 | 1,723 | 1,661 | 86.11M | 66,103 | 38,626 | 0.784 | 92 |
| 53069 | Wahkiakum | rural | 1,550 | 885 | 72 | 299 | 1.79M | 71,759 | 27,595 | 0.835 | 48* |
| 53071 | Walla Walla | suburb | 26,947 | 28,104 | 2,887 | 200,562 | 26.77M | 50,947 | 51,648 | 0.447 | 76 |
| 53073 | Whatcom | suburb | 109,391 | 102,742 | 3,443 | 26,988 | 73.02M | 52,214 | 47,902 | 0.675 | 200 |
| 53075 | Whitman | rural | 22,363 | 23,538 | 1,190 | 382,547 | 19.65M | 43,375 | 107,221 | 0.373 | 86 |
| 53077 | Yakima | suburb | 105,896 | 91,811 | 14,482 | 144,200 | 96.78M | 55,611 | 52,587 | 0.863 | 48* |
| EXT | External (out-of-state commuting) | external | 63,898 | 97,718 | 1,865 | 71,453 | 43.87M | 54,010 | n/a | 0.573 | n/a |

`*` filled, see above.
