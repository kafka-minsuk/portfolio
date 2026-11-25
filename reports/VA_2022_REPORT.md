# Virginia 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state VA 2022`. 105 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 51 | `VA/CDL_2022_51.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=51 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_VA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

BEA combination areas are single zones here (every source is summed to them): 51901 Albemarle + Charlottesville = 51003, 51540; 51903 Alleghany + Covington = 51005, 51580; 51907 Augusta, Staunton + Waynesboro = 51015, 51790, 51820; 51911 Campbell + Lynchburg = 51031, 51680; 51913 Carroll + Galax = 51035, 51640; 51918 Dinwiddie, Colonial Heights + Petersburg = 51053, 51570, 51730; 51919 Fairfax, Fairfax City + Falls Church = 51059, 51600, 51610; 51921 Frederick + Winchester = 51069, 51840; 51923 Greensville + Emporia = 51081, 51595; 51929 Henry + Martinsville = 51089, 51690; 51931 James City + Williamsburg = 51095, 51830; 51933 Montgomery + Radford = 51121, 51750; 51939 Pittsylvania + Danville = 51143, 51590; 51941 Prince George + Hopewell = 51149, 51670; 51942 Prince William, Manassas + Manassas Park = 51153, 51683, 51685; 51944 Roanoke + Salem = 51161, 51775; 51945 Rockbridge, Buena Vista + Lexington = 51163, 51530, 51678; 51947 Rockingham + Harrisonburg = 51165, 51660; 51949 Southampton + Franklin = 51175, 51620; 51951 Spotsylvania + Fredericksburg = 51177, 51630; 51953 Washington + Bristol = 51191, 51520; 51955 Wise + Norton = 51195, 51720; 51958 York + Poquoson = 51199, 51735.

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 8,683,619 | 8,683,619 | 0.000% |
| ACS workers by residence | 4,290,610 | 4,290,610 | 0.000% |
| ACS workers by workplace | 4,259,920 | 4,259,920 | 0.000% |
| ACS workers working out of state | 287,746 | 287,746 | 0.000% |
| BEA non-farm employment (L80) | 5,553,685 | 5,553,685 | 0.000% |
| BEA farm employment (L70) | 45,900 | 45,900 | 0.000% |
| BEA farm proprietors (L50) | 36,287 | 36,287 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 1,087,289,000 | 1,087,289,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 376,524,000 | 376,524,000 | 0.000% |
| CoA hired farm labour expense $ | 503,418,000 | 503,419,000 | -0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 407,167,787,000 | 407,167,787,000 | 0.000% |
| ACS foreign born entered 2010+ | 322,479 | 322,479 | 0.000% |
| CoA owned acres | 4,833,623 | 4,833,623 | 0.000% |
| CoA rented-from-others acres | 2,476,064 | 2,476,064 | 0.000% |
| CoA land in farms, ha | 2,958,125 | 2,958,125 | 0.000% |
| CoA total cropland, ha | 1,167,232 | 1,167,232 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.457, median 0.745, max 0.942; BEA counts jobs, ACS counts people by main job). Sum N = 4,547,666 = sum HU + HA = 4,547,666. Farm jobs after scaling: 33,616 (BEA 45,900). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 257,056. Jobs = in-state residents working out of state = 287,746, split by the state farm share (HA = 2,271). Location: the 45 out-of-state counties within 1 km of the state (11001, 21013, 21095, 21133, 21195, 24017, 24021, 24031, 24033, 24039, 24043, 24047, 37005, 37009, 37029, 37033, 37053, 37073, 37077, 37091, 37131, 37145, 37157, 37169, 37171, 37181, 37185, 47025, 47067, 47073, 47091, 47163, 54003, 54025, 54027, 54031, 54037, 54047, 54055, 54059, 54063, 54065, 54071, 54075, 54089); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,313,675 ha vs Census of Agriculture cropland 1,167,232 ha and land in farms 2,958,125 ha; county ratio TF / CoA cropland 0.58 to 11.58. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,008,261 ha). County area covered by CDL pixels: 10,480,295 ha vs land area 10,225,818 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 7.22 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (73,315 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 32,420 $ per BEA farm job, 44,267 $ per farm worker; county range 12,527 to 103,622 $ per worker. State compensation per farm wage job by year: 2018 28,726 $, 2019 28,211 $, 2020 33,478 $, 2021 30,650 $, 2022 39,168 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 86,484,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (503,419,000 $ in 2022, column `hired_labor_coa_usd`) is 1.34x BEA farm compensation (376,524,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 23,688 $, county -49,717 to 222,264 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 96,341 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,494,552,000 $ vs CAINC45 1,087,289,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.661, county range 0.291 to 1.000.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 63 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 5,303 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 5 counties have no recent foreign born in the ACS sample (Bland, Craig, Highland, Mathews, Surry), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Fairfax, Fairfax City + Falls Church); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (60); rural = the rest (44). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 8 counties have no BEA farm jobs (Arlington, Alexandria, Hampton, Newport News, Norfolk, Portsmouth, Richmond, Roanoke); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 195.6 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.0 straight-line km/h between counties (median 3.4 to 27.6 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.27).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 51013 Arlington | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51510 Alexandria | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51650 Hampton | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51700 Newport News | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51710 Norfolk | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51740 Portsmouth | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51760 Richmond | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 51770 Roanoke | 0 farm jobs: no farm sector in the model (spec §3.11) |
| rented_acres | 51013 Arlington | land in farms minus the other tenure (Census of Ag identity) |
| omega | 51510 Alexandria | state owner share |
| omega | 51650 Hampton | state owner share |
| omega | 51700 Newport News | state owner share |
| omega | 51710 Norfolk | state owner share |
| omega | 51740 Portsmouth | state owner share |
| omega | 51760 Richmond | state owner share |
| omega | 51770 Roanoke | state owner share |
| cash_rent_usd_acre | 51013 Arlington | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51027 Buchanan | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51036 Charles City | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51051 Dickenson | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51073 Gloucester | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51079 Greene | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51087 Henrico | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51099 King George | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51103 Lancaster | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51115 Mathews | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51119 Middlesex | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51187 Warren | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51510 Alexandria | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51650 Hampton | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51700 Newport News | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51710 Norfolk | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51740 Portsmouth | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51760 Richmond | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51770 Roanoke | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51919 Fairfax, Fairfax City + Falls Church | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51931 James City + Williamsburg | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51944 Roanoke + Salem | not published; NASS 'other (combined) counties' value = 56 $/acre |
| cash_rent_usd_acre | 51958 York + Poquoson | not published; NASS 'other (combined) counties' value = 56 $/acre |
| hired_labor_coa_usd | 51013 Arlington | (D) in Census of Ag; left null (comparison column only) |

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
| 51001 | Accomack | rural | 14,099 | 13,677 | 279 | 30,078 | 12.42M | 44,580 | 222,264 | 0.395 | 90 |
| 51007 | Amelia | suburb | 6,079 | 2,306 | 228 | 16,024 | 3.70M | 82,680 | 97,694 | 0.713 | 42 |
| 51009 | Amherst | suburb | 14,609 | 8,105 | 248 | 9,363 | 6.26M | 46,345 | -6,039 | 0.715 | 21 |
| 51011 | Appomattox | suburb | 7,614 | 3,983 | 313 | 14,439 | 4.00M | 14,743 | -9,692 | 0.687 | 27 |
| 51013 | Arlington | suburb | 148,246 | 191,549 | 0 | 9 | 57.04M | 0 | n/a | 1.000 | 56* |
| 51017 | Bath | rural | 1,722 | 1,969 | 83 | 3,486 | 1.42M | 31,952 | 12,610 | 0.836 | 32 |
| 51019 | Bedford | suburb | 36,473 | 21,228 | 803 | 31,044 | 19.30M | 36,279 | -6,456 | 0.698 | 30 |
| 51021 | Bland | rural | 2,277 | 1,808 | 255 | 6,939 | 1.80M | 12,527 | 880 | 0.810 | 34 |
| 51023 | Botetourt | suburb | 15,827 | 11,884 | 362 | 13,084 | 10.67M | 55,436 | -5,683 | 0.738 | 34 |
| 51025 | Brunswick | rural | 6,248 | 3,315 | 197 | 12,914 | 4.39M | 75,015 | -8,931 | 0.744 | 38 |
| 51027 | Buchanan | rural | 5,805 | 5,948 | 76 | 397 | 4.04M | 27,215 | -3,766 | 0.777 | 56* |
| 51029 | Buckingham | rural | 6,479 | 2,995 | 226 | 13,043 | 3.98M | 42,364 | 38,124 | 0.799 | 32 |
| 51033 | Caroline | rural | 15,767 | 7,522 | 187 | 19,988 | 5.81M | 49,251 | 19,163 | 0.431 | 71 |
| 51036 | Charles City | suburb | 3,222 | 1,485 | 68 | 8,052 | 1.85M | 53,333 | 35,508 | 0.562 | 56* |
| 51037 | Charlotte | rural | 4,537 | 2,640 | 294 | 18,444 | 3.52M | 52,514 | -1,670 | 0.807 | 35 |
| 51041 | Chesterfield | suburb | 184,760 | 146,379 | 136 | 3,975 | 79.69M | 40,287 | 13,581 | 0.794 | 24 |
| 51043 | Clarke | suburb | 7,421 | 4,310 | 304 | 9,667 | 3.55M | 67,448 | 5,597 | 0.676 | 38 |
| 51045 | Craig | suburb | 1,964 | 627 | 89 | 5,248 | 1.33M | 63,434 | -9,392 | 0.748 | 36 |
| 51047 | Culpeper | suburb | 25,422 | 17,855 | 527 | 24,546 | 10.96M | 56,571 | 2,287 | 0.531 | 46 |
| 51049 | Cumberland | rural | 4,917 | 2,145 | 227 | 8,821 | 2.88M | 33,669 | 75,596 | 0.701 | 28 |
| 51051 | Dickenson | rural | 4,444 | 3,922 | 119 | 816 | 3.01M | 12,881 | -3,266 | 0.594 | 56* |
| 51057 | Essex | rural | 4,073 | 3,693 | 68 | 17,139 | 3.19M | 66,117 | -26,884 | 0.464 | 86 |
| 51061 | Fauquier | suburb | 38,097 | 27,003 | 937 | 28,128 | 13.63M | 60,738 | 7,730 | 0.714 | 58 |
| 51063 | Floyd | suburb | 7,584 | 4,130 | 537 | 12,186 | 4.08M | 54,649 | -4,622 | 0.673 | 34 |
| 51065 | Fluvanna | suburb | 13,164 | 5,542 | 158 | 6,808 | 4.45M | 77,151 | -11,996 | 0.791 | 20 |
| 51067 | Franklin | suburb | 23,512 | 16,659 | 711 | 28,278 | 17.34M | 46,157 | 1,426 | 0.650 | 47 |
| 51071 | Giles | suburb | 7,406 | 5,172 | 241 | 4,330 | 4.92M | 31,801 | -3,514 | 0.673 | 28 |
| 51073 | Gloucester | suburb | 19,083 | 9,985 | 120 | 6,872 | 7.69M | 17,683 | 4,621 | 0.443 | 56* |
| 51075 | Goochland | suburb | 11,326 | 14,969 | 158 | 9,852 | 5.58M | 72,930 | -13,323 | 0.701 | 46 |
| 51077 | Grayson | rural | 5,827 | 3,062 | 427 | 11,250 | 4.50M | 49,857 | -14,955 | 0.576 | 53 |
| 51079 | Greene | suburb | 10,557 | 5,003 | 142 | 4,236 | 3.31M | 55,519 | 8,050 | 0.735 | 56* |
| 51083 | Halifax | rural | 13,505 | 11,802 | 657 | 26,090 | 12.70M | 42,091 | -4,015 | 0.785 | 31 |
| 51085 | Hanover | suburb | 56,934 | 48,388 | 422 | 22,016 | 35.33M | 63,759 | 18,368 | 0.483 | 56 |
| 51087 | Henrico | suburb | 173,906 | 192,259 | 85 | 5,239 | 115.07M | 70,270 | 9,050 | 0.468 | 56* |
| 51091 | Highland | rural | 805 | 606 | 140 | 3,895 | 1.24M | 48,851 | 49,650 | 0.663 | 28 |
| 51093 | Isle of Wight | suburb | 18,470 | 11,240 | 151 | 24,118 | 9.47M | 46,091 | 35,880 | 0.458 | 90 |
| 51097 | King and Queen | suburb | 3,248 | 1,186 | 81 | 14,880 | 1.92M | 61,354 | 17,024 | 0.479 | 74 |
| 51099 | King George | rural | 13,820 | 14,146 | 113 | 6,711 | 5.44M | 43,160 | -1,638 | 0.621 | 56* |
| 51101 | King William | suburb | 9,155 | 5,466 | 120 | 15,534 | 4.64M | 25,924 | 333 | 0.650 | 74 |
| 51103 | Lancaster | rural | 3,953 | 4,705 | 45 | 6,904 | 3.53M | 60,023 | 7,176 | 0.524 | 56* |
| 51105 | Lee | rural | 6,901 | 3,880 | 576 | 14,572 | 5.71M | 26,385 | -8,405 | 0.749 | 30 |
| 51107 | Loudoun | suburb | 226,387 | 214,780 | 1,165 | 13,451 | 86.30M | 46,153 | 5,810 | 0.601 | 44 |
| 51109 | Louisa | rural | 17,615 | 11,502 | 316 | 16,062 | 7.48M | 41,179 | -182 | 0.666 | 44 |
| 51111 | Lunenburg | rural | 4,556 | 2,728 | 248 | 13,780 | 3.08M | 103,622 | -13,748 | 0.784 | 30 |
| 51113 | Madison | rural | 6,470 | 4,501 | 393 | 15,892 | 3.37M | 42,435 | -6,118 | 0.712 | 44 |
| 51115 | Mathews | suburb | 3,172 | 1,912 | 28 | 2,119 | 2.48M | 22,229 | 19,091 | 0.463 | 56* |
| 51117 | Mecklenburg | rural | 12,273 | 12,692 | 473 | 24,343 | 10.62M | 46,519 | -26,912 | 0.675 | 38 |
| 51119 | Middlesex | rural | 4,437 | 3,660 | 48 | 7,480 | 3.48M | 100,541 | 24,264 | 0.472 | 56* |
| 51125 | Nelson | suburb | 6,495 | 5,096 | 339 | 7,739 | 3.65M | 49,801 | 6,574 | 0.754 | 32 |
| 51127 | New Kent | suburb | 12,083 | 6,759 | 78 | 5,829 | 4.27M | 39,056 | -28,145 | 0.634 | 75 |
| 51131 | Northampton | rural | 4,850 | 4,917 | 283 | 18,346 | 3.70M | 67,129 | 124,254 | 0.291 | 86 |
| 51133 | Northumberland | rural | 4,336 | 2,455 | 50 | 14,035 | 4.15M | 94,887 | 43,753 | 0.437 | 84 |
| 51135 | Nottoway | rural | 5,833 | 6,771 | 365 | 11,812 | 4.46M | 28,727 | 76,848 | 0.732 | 38 |
| 51137 | Orange | rural | 17,338 | 10,315 | 480 | 17,294 | 7.10M | 61,593 | 32,332 | 0.615 | 70 |
| 51139 | Page | rural | 10,681 | 6,186 | 412 | 10,903 | 9.09M | 39,722 | 161,210 | 0.583 | 45 |
| 51141 | Patrick | rural | 7,210 | 4,878 | 399 | 10,575 | 5.04M | 40,978 | 3,062 | 0.832 | 44 |
| 51145 | Powhatan | suburb | 15,147 | 9,955 | 159 | 7,188 | 5.45M | 44,239 | 16,714 | 0.834 | 28 |
| 51147 | Prince Edward | rural | 8,237 | 9,357 | 293 | 12,605 | 5.24M | 36,929 | 28,734 | 0.872 | 26 |
| 51155 | Pulaski | suburb | 14,880 | 14,278 | 313 | 11,224 | 12.04M | 36,067 | 79 | 0.622 | 42 |
| 51157 | Rappahannock | suburb | 3,468 | 2,003 | 208 | 6,178 | 1.72M | 58,666 | -10,904 | 0.759 | 20 |
| 51159 | Richmond | rural | 3,208 | 3,137 | 101 | 12,889 | 2.32M | 57,162 | 32,212 | 0.341 | 77 |
| 51167 | Russell | rural | 8,527 | 5,651 | 541 | 11,610 | 6.47M | 46,739 | -2,390 | 0.718 | 44 |
| 51169 | Scott | suburb | 7,808 | 4,424 | 700 | 11,182 | 6.43M | 34,781 | -3,083 | 0.781 | 40 |
| 51171 | Shenandoah | rural | 20,387 | 14,195 | 701 | 20,219 | 14.36M | 28,782 | 71,039 | 0.613 | 56 |
| 51173 | Smyth | rural | 11,673 | 10,554 | 476 | 11,311 | 9.57M | 50,164 | -590 | 0.621 | 43 |
| 51179 | Stafford | suburb | 78,696 | 55,275 | 130 | 4,161 | 23.67M | 48,847 | -20,727 | 0.551 | 48 |
| 51181 | Surry | suburb | 3,069 | 1,861 | 84 | 14,963 | 2.52M | 40,985 | 16,443 | 0.529 | 79 |
| 51183 | Sussex | suburb | 4,307 | 3,542 | 133 | 20,429 | 3.46M | 32,356 | 24,503 | 0.477 | 70 |
| 51185 | Tazewell | rural | 14,127 | 13,573 | 378 | 9,596 | 10.56M | 32,827 | 8,112 | 0.673 | 49 |
| 51187 | Warren | suburb | 19,244 | 15,733 | 252 | 3,520 | 9.93M | 36,105 | -5,541 | 0.683 | 56* |
| 51193 | Westmoreland | rural | 7,028 | 4,008 | 203 | 16,189 | 5.29M | 54,252 | 62,869 | 0.608 | 89 |
| 51197 | Wythe | rural | 12,341 | 11,595 | 674 | 21,083 | 10.45M | 41,602 | 4,884 | 0.713 | 40 |
| 51510 | Alexandria | suburb | 97,901 | 101,877 | 0 | 7 | 34.71M | 0 | n/a | 0.661 | 56* |
| 51550 | Chesapeake | suburb | 123,540 | 102,981 | 203 | 17,617 | 89.11M | 76,048 | 24,051 | 0.480 | 80 |
| 51650 | Hampton | suburb | 67,348 | 65,575 | 0 | 145 | 49.89M | 0 | n/a | 0.661 | 56* |
| 51700 | Newport News | suburb | 92,115 | 119,265 | 0 | 198 | 69.50M | 0 | n/a | 0.661 | 56* |
| 51710 | Norfolk | suburb | 125,430 | 182,206 | 0 | 22 | 81.74M | 0 | n/a | 0.661 | 56* |
| 51740 | Portsmouth | suburb | 45,028 | 54,146 | 0 | 37 | 34.49M | 0 | n/a | 0.661 | 56* |
| 51760 | Richmond | suburb | 119,758 | 176,599 | 0 | 94 | 81.36M | 0 | n/a | 0.661 | 56* |
| 51770 | Roanoke | suburb | 46,368 | 69,722 | 0 | 176 | 52.89M | 0 | n/a | 0.661 | 56* |
| 51800 | Suffolk | suburb | 45,875 | 39,085 | 358 | 24,041 | 26.33M | 78,427 | 54,224 | 0.377 | 85 |
| 51810 | Virginia Beach | suburb | 242,547 | 222,761 | 169 | 9,554 | 141.68M | 32,535 | -7,484 | 0.397 | 63 |
| 51901 | Albemarle + Charlottesville | suburb | 77,508 | 102,439 | 904 | 16,773 | 36.56M | 37,220 | -1,513 | 0.720 | 25 |
| 51903 | Alleghany + Covington | rural | 8,339 | 7,682 | 144 | 2,950 | 8.33M | 35,801 | -4,514 | 0.745 | 33 |
| 51907 | Augusta, Staunton + Waynesboro | suburb | 60,047 | 52,007 | 1,306 | 41,838 | 42.63M | 38,488 | 77,529 | 0.595 | 65 |
| 51911 | Campbell + Lynchburg | suburb | 61,695 | 78,855 | 668 | 24,142 | 37.38M | 26,503 | -1,820 | 0.812 | 30 |
| 51913 | Carroll + Galax | rural | 14,825 | 11,934 | 658 | 16,853 | 10.99M | 50,403 | 5,946 | 0.643 | 50 |
| 51918 | Dinwiddie, Colonial Heights + Petersburg | suburb | 36,215 | 35,227 | 298 | 17,664 | 27.69M | 36,860 | -11,031 | 0.745 | 54 |
| 51919 | Fairfax, Fairfax City + Falls Church | core | 632,609 | 707,054 | 144 | 522 | 287.77M | 37,689 | 47,178 | 0.990 | 56* |
| 51921 | Frederick + Winchester | suburb | 58,809 | 64,092 | 531 | 12,634 | 37.14M | 45,012 | -6,863 | 0.663 | 38 |
| 51923 | Greensville + Emporia | rural | 6,053 | 7,181 | 112 | 13,060 | 5.32M | 56,425 | -3,310 | 0.673 | 76 |
| 51929 | Henry + Martinsville | rural | 24,772 | 24,718 | 178 | 4,874 | 23.45M | 71,544 | 34,017 | 0.755 | 19 |
| 51931 | James City + Williamsburg | suburb | 41,774 | 43,986 | 69 | 2,550 | 25.02M | 44,560 | -49,717 | 0.783 | 56* |
| 51933 | Montgomery + Radford | suburb | 52,959 | 59,306 | 537 | 10,575 | 31.25M | 31,613 | 7,666 | 0.720 | 38 |
| 51939 | Pittsylvania + Danville | rural | 41,333 | 39,096 | 1,071 | 39,754 | 39.20M | 45,197 | 2,800 | 0.722 | 34 |
| 51941 | Prince George + Hopewell | suburb | 29,258 | 30,687 | 140 | 9,936 | 21.20M | 23,943 | -10,018 | 0.662 | 52 |
| 51942 | Prince William, Manassas + Manassas Park | suburb | 282,202 | 201,326 | 260 | 5,514 | 104.05M | 43,764 | -2,648 | 0.631 | 46 |
| 51944 | Roanoke + Salem | suburb | 58,835 | 59,462 | 194 | 3,038 | 48.08M | 26,665 | -914 | 0.749 | 56* |
| 51945 | Rockbridge, Buena Vista + Lexington | rural | 15,746 | 14,612 | 559 | 15,500 | 12.75M | 41,549 | 2,897 | 0.655 | 28 |
| 51947 | Rockingham + Harrisonburg | suburb | 64,921 | 70,881 | 1,854 | 47,211 | 52.35M | 40,018 | 188,121 | 0.644 | 100 |
| 51949 | Southampton + Franklin | rural | 11,206 | 7,951 | 262 | 43,047 | 8.62M | 56,430 | 41,211 | 0.567 | 94 |
| 51951 | Spotsylvania + Fredericksburg | suburb | 84,062 | 70,859 | 274 | 9,939 | 30.90M | 31,500 | 7,319 | 0.778 | 40 |
| 51953 | Washington + Bristol | suburb | 30,841 | 33,387 | 1,225 | 17,501 | 24.65M | 31,686 | 4,266 | 0.657 | 48 |
| 51955 | Wise + Norton | rural | 13,677 | 15,143 | 118 | 1,642 | 10.16M | 15,007 | -5,490 | 0.429 | 22 |
| 51958 | York + Poquoson | suburb | 41,873 | 31,363 | 45 | 843 | 25.39M | 46,107 | 27,852 | 0.665 | 56* |
| EXT | External (out-of-state commuting) | external | 257,056 | 285,475 | 2,271 | 88,735 | 144.13M | 44,267 | n/a | 0.661 | n/a |

`*` filled, see above.
