# New Jersey 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state NJ 2022`. 21 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 34 | `NJ/CDL_2022_34.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=34 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NJ.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 9,261,699 | 9,261,699 | 0.000% |
| ACS workers by residence | 4,517,714 | 4,517,714 | 0.000% |
| ACS workers by workplace | 4,218,452 | 4,218,452 | 0.000% |
| ACS workers working out of state | 545,892 | 545,892 | 0.000% |
| BEA non-farm employment (L80) | 5,889,370 | 5,889,370 | 0.000% |
| BEA farm employment (L70) | 16,473 | 16,473 | 0.000% |
| BEA farm proprietors (L50) | 8,731 | 8,731 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 490,376,000 | 490,376,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 322,910,000 | 322,910,000 | 0.000% |
| CoA hired farm labour expense $ | 434,926,000 | 434,925,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 460,278,550,000 | 460,278,550,000 | 0.000% |
| ACS foreign born entered 2010+ | 585,731 | 585,731 | 0.000% |
| CoA owned acres | 486,216 | 486,301 | -0.017% |
| CoA rented-from-others acres | 225,185 | 225,201 | -0.007% |
| CoA land in farms, ha | 287,894 | 287,935 | -0.014% |
| CoA total cropland, ha | 181,980 | 181,994 | -0.008% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.646, median 0.729, max 0.785; BEA counts jobs, ACS counts people by main job). Sum N = 4,764,344 = sum HU + HA = 4,764,344. Farm jobs after scaling: 11,965 (BEA 16,473). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 246,630. Jobs = in-state residents working out of state = 545,892, split by the state farm share (HA = 1,548). Location: the 13 out-of-state counties within 1 km of the state (10003, 36005, 36061, 36071, 36085, 36087, 36119, 42017, 42045, 42089, 42095, 42101, 42103); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 167,082 ha vs Census of Agriculture cropland 181,994 ha and land in farms 287,935 ha; county ratio TF / CoA cropland 0.19 to 1.56. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 82,656 ha). County area covered by CDL pixels: 2,011,376 ha vs land area 1,904,913 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 7.68 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (78,154 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 31,526 $ per BEA farm job, 43,405 $ per farm worker; county range 28,681 to 81,409 $ per worker. State compensation per farm wage job by year: 2018 28,938 $, 2019 26,284 $, 2020 32,512 $, 2021 25,424 $, 2022 41,709 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 62,883,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (434,925,000 $ in 2022, column `hired_labor_coa_usd`) is 1.35x BEA farm compensation (322,910,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 29,768 $, county 4,984 to 47,005 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 109,421 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 717,282,000 $ vs CAINC45 490,376,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.683, county range 0.560 to 0.990.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 76 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 15,992 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Bergen); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (20); rural = the rest (0). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Hudson); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 87.7 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 55.0 straight-line km/h between counties (median 6.2 to 25.9 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.22).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 34017 Hudson | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 34013 Essex | state owner share |
| omega | 34017 Hudson | state owner share |
| cash_rent_usd_acre | 34001 Atlantic | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34003 Bergen | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34007 Camden | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34009 Cape May | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34013 Essex | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34017 Hudson | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34023 Middlesex | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34029 Ocean | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34031 Passaic | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| cash_rent_usd_acre | 34039 Union | not published; NASS 'other (combined) counties' value = 32.5 $/acre |
| owned_acres | 34013 Essex | (D) in Census of Ag; see fills above |
| owned_acres | 34017 Hudson | (D) in Census of Ag; see fills above |
| rented_acres | 34013 Essex | (D) in Census of Ag; see fills above |
| rented_acres | 34017 Hudson | (D) in Census of Ag; see fills above |

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
| 34001 | Atlantic | suburb | 126,468 | 121,593 | 957 | 8,190 | 73.63M | 39,877 | 37,646 | 0.822 | 32* |
| 34003 | Bergen | core | 482,857 | 459,425 | 386 | 36 | 309.95M | 53,867 | 42,703 | 0.983 | 32* |
| 34005 | Burlington | suburb | 234,607 | 214,749 | 944 | 23,624 | 137.28M | 45,110 | 25,804 | 0.736 | 72 |
| 34007 | Camden | suburb | 250,162 | 218,795 | 296 | 2,824 | 169.27M | 36,708 | 25,967 | 0.660 | 32* |
| 34009 | Cape May | suburb | 42,154 | 43,484 | 194 | 1,172 | 51.41M | 46,344 | 30,217 | 0.770 | 32* |
| 34011 | Cumberland | suburb | 61,388 | 59,154 | 1,415 | 21,928 | 44.66M | 40,391 | 47,005 | 0.668 | 82 |
| 34013 | Essex | suburb | 396,088 | 387,097 | 33 | 11 | 194.23M | 81,409 | 31,886 | 0.683 | 32* |
| 34015 | Gloucester | suburb | 152,194 | 127,138 | 1,027 | 14,891 | 100.47M | 45,096 | 36,743 | 0.582 | 84 |
| 34017 | Hudson | suburb | 375,393 | 313,942 | 0 | 12 | 122.61M | 0 | n/a | 0.683 | 32* |
| 34019 | Hunterdon | suburb | 66,185 | 55,311 | 1,326 | 17,200 | 27.10M | 43,685 | 11,857 | 0.647 | 52 |
| 34021 | Mercer | suburb | 181,170 | 230,620 | 289 | 6,139 | 105.90M | 29,676 | 19,200 | 0.560 | 67 |
| 34023 | Middlesex | suburb | 420,626 | 420,921 | 281 | 4,072 | 278.34M | 40,389 | 22,052 | 0.734 | 32* |
| 34025 | Monmouth | suburb | 325,055 | 296,489 | 934 | 8,528 | 189.67M | 53,510 | 29,353 | 0.736 | 82 |
| 34027 | Morris | suburb | 262,320 | 302,427 | 519 | 1,538 | 125.75M | 46,462 | 31,310 | 0.793 | 55 |
| 34029 | Ocean | suburb | 269,436 | 198,830 | 178 | 1,722 | 196.80M | 39,042 | 27,895 | 0.783 | 32* |
| 34031 | Passaic | suburb | 246,290 | 190,732 | 89 | 31 | 114.11M | 57,109 | 22,182 | 0.990 | 32* |
| 34033 | Salem | suburb | 28,330 | 23,176 | 1,089 | 31,253 | 21.99M | 46,654 | 33,002 | 0.604 | 98 |
| 34035 | Somerset | suburb | 180,486 | 197,836 | 351 | 5,998 | 91.38M | 43,981 | 14,034 | 0.682 | 38 |
| 34037 | Sussex | suburb | 75,861 | 46,841 | 752 | 4,053 | 23.66M | 28,681 | 4,984 | 0.740 | 52 |
| 34039 | Union | suburb | 285,292 | 260,704 | 55 | 18 | 157.57M | 47,300 | 39,315 | 0.928 | 32* |
| 34041 | Warren | suburb | 55,352 | 37,224 | 849 | 13,841 | 24.79M | 43,987 | 44,081 | 0.670 | 86 |
| EXT | External (out-of-state commuting) | external | 246,630 | 544,344 | 1,548 | 21,621 | 139.79M | 43,405 | n/a | 0.683 | n/a |

`*` filled, see above.
