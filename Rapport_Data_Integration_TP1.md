# TP Data Integration And Applications
## Data Profiling, Data Quality Analysis, Transformations, Modeling & Medallion Architecture

**Date:** July 1, 2026  
**Dataset:** French Road Safety Open Data (BAAC) - 2024  
**Source:** https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024

---

# Part 1: Data Profiling and Data Quality Analysis

## A. Dataset Structure

### A.1 Column Inventory

The dataset for 2024 consists of 3 tables:

#### Table 1: caracteristiques (Accident Characteristics)
**54,402 rows × 15 columns**

| Column | Data Type | Nulls | Description |
|--------|-----------|-------|-------------|
| Num_Acc | Integer | 0 | Unique accident identifier (YYYY + sequential) |
| jour | Integer | 0 | Day of accident (1-31) |
| mois | Integer | 0 | Month of accident (1-12) |
| an | Integer | 0 | Year of accident |
| hrmn | String | 0 | Hour and minute (HH:MM) |
| lum | Integer | 0 | Lighting condition (1-5) |
| dep | String | 0 | Department INSEE code |
| com | String | 0 | Commune INSEE code |
| agg | Integer | 0 | Urban area type (1-2) |
| int | Integer | 0 | Intersection type (1-8) |
| atm | Integer | 0 | Weather condition (1-9) |
| col | Integer | 0 | Collision type (1-8) |
| adr | String | 2,310 | Street address |
| lat | String | 0 | Latitude (comma decimal) |
| long | String | 0 | Longitude (comma decimal) |

#### Table 2: lieux (Location Details)
**70,248 rows × 18 columns**

| Column | Data Type | Nulls | Description |
|--------|-----------|-------|-------------|
| Num_Acc | Integer | 0 | FK to caracteristiques |
| catr | Integer | 0 | Road category (1-9) |
| voie | String | 13,331 | Road name/number |
| v1 | Integer | 0 | Road numbering index 1 |
| v2 | String | 64,332 | Road numbering index 2 |
| circ | Integer | 0 | Traffic direction (1-3) |
| nbv | String | 0 | Number of lanes |
| vosp | Integer | 0 | Reserved lane (1-3) |
| prof | Integer | 0 | Road profile (1-5) |
| pr | String | 0 | Reference point number |
| pr1 | String | 0 | Reference point distance (m) |
| plan | Integer | 0 | Road plan (1-5) |
| lartpc | String | 70,215 | Central reservation width (m) |
| larrout | String | 0 | Road width (m) |
| surf | Integer | 0 | Surface condition (1-7) |
| infra | Integer | 0 | Infrastructure (0-4) |
| situ | Integer | 0 | Situation (1-5) |
| vma | Integer | 0 | Speed limit (km/h) |

#### Table 3: vehicules (Vehicle Info)
**83,730 rows × 7 columns**

| Column | Data Type | Nulls | Description |
|--------|-----------|-------|-------------|
| Id_accident | String | 0 | Accident ID (joins to Num_Acc) |
| Lettre Conventionnelle Véhicule | String | 1 | Vehicle letter (A, B, C...) |
| Année | Integer | 0 | Year |
| Lieu Admin Actuel - Territoire Nom | String | 0 | Territory (Métropole, DOM) |
| CNIT | String | 20,028 | Vehicle VIN/chassis number |
| Catégorie véhicule | String | 0 | Vehicle category (VT, VU, PL...) |
| Age véhicule | Float | 5,395 | Vehicle age in years |

### A.2 Semantic Meaning

- **Num_Acc**: Primary key for accidents, format YYYY + 9-digit sequential number (e.g., 202400000001)
- **lum**: Lighting at time of accident (1=Daylight, 2=Twilight, 3=Night no lighting, 4=Night lighting on, 5=Night lighting off)
- **atm**: Weather (1=Normal, 2=Light rain, 3=Heavy rain, 4=Snow, 5=Fog, 6=Strong wind, 7=Glare, 8=Cloudy, 9=Other)
- **col**: Collision type (1=Frontal, 2=Same direction, 3=Perpendicular, 4=Opposite, 5=Chain, 6=Multiple, 7=Other, 8=None)
- **catr**: Road type (1=Highway, 2=National, 3=Departmental, 4=Communal, 5=Private, 6=Pedestrian, 7=Cycle path, 9=Other)
- **Catégorie véhicule**: VT=Passenger car, VU=Utility, PL=Truck, TC=Public transport, Cyclo, Moto légère, Moto lourde, Autres, Indéterminable

---

## B. Missing Values and Completeness

| Table | Column | Missing | % Missing | Severity |
|-------|--------|---------|-----------|----------|
| lieux | lartpc | 70,215 | 99.95% | CRITICAL - essentially empty column |
| lieux | v2 | 64,332 | 91.58% | CRITICAL - mostly empty |
| lieux | voie | 13,331 | 18.98% | HIGH - road name missing |
| vehicules | CNIT | 20,028 | 23.92% | HIGH - VIN not recorded |
| vehicules | Age véhicule | 5,395 | 6.44% | MEDIUM - vehicle age unknown |
| caracteristiques | adr | 2,310 | 4.25% | LOW - address missing but coords available |
| vehicules | Lettre Conv. | 1 | <0.01% | NEGLIGIBLE |

**Critical Missingness Analysis:**
- **lartpc (99.95%)**: Central reservation width is almost never recorded. This column should be excluded from analysis as it provides no analytical value.
- **v2 (91.58%)**: Road numbering second index is rarely populated. Useful only for specific road segments.
- **CNIT (23.92%)**: VIN/chassis numbers missing for nearly 1/4 of vehicles. This limits vehicle identification and cross-referencing.
- **Age véhicule (6.44%)**: Missing vehicle ages affect age-based accident risk analysis.

**Remediation Strategies:**
1. Drop `lartpc` column entirely (99.95% empty)
2. Drop `v2` or flag as sparsely populated
3. For `Age véhicule`: impute with median age by vehicle category
4. For `CNIT`: mark as "Unknown" or derive from other fields if possible
5. `adr`: can be reconstructed from lat/long via reverse geocoding if needed

---

## C. Consistency and Validity Checks

### C.1 Out-of-Range Values & Anomalies

**Coordinates (caracteristiques):**
- Latitude range: -22.4332 to 51.0787
- Longitude range: -178.0944 to 167.8632
- 3,339 records outside mainland France bounds (DOM-TOM territories: Guadeloupe, Martinique, Guyane, Réunion, Mayotte, Polynésie, Nouvelle-Calédonie, etc.)
- This is VALID for the dataset (includes overseas territories)
- No truly invalid coordinates detected

**Invalid or Anomalous Values:**

| Table | Column | Anomaly | Count | Issue |
|-------|--------|---------|-------|-------|
| caracteristiques | col | -1 | 6 | Invalid collision type code |
| lieux | surf | -1 | 38 | Invalid surface condition code |
| lieux | surf | 8 | 85 | Code 8 not in standard spec |
| lieux | surf | 9 | 296 | Code 9 not in standard spec |
| lieux | vma | -1 | 3,630 | Negative speed limit (probably "unknown") |
| lieux | vma | 500 | 21 | Unrealistic speed limit |
| lieux | vma | 300+ | 27 | Unrealistic speed limit (>150 km/h) |
| lieux | pr | Negative | 27,364 | Negative reference point numbers |
| lieux | pr1 | Negative | 27,448 | Negative reference distances |
| lieux | larrout | Negative | 48,646 | Negative road width (69.2% of records!) |
| vehicules | Age | Negative | ? | Negative vehicle age |

### C.2 Categorical Anomalies

All categorical columns have valid code ranges with minor exceptions:
- `col=-1` (6 records): likely encoding error or "unknown"
- `surf` has codes 8 and 9 not in standard documentation
- `vma=-1` for 3,630 records: semantic meaning = "speed limit unknown/not applicable"

### C.3 Duplicates

| Table | Exact Duplicates | Duplicate IDs |
|-------|-----------------|---------------|
| caracteristiques | 0 | 0 (Num_Acc is unique) |
| lieux | 0 | 0 (multiple rows per accident OK - road segments) |
| vehicules | 0 | 83,730 unique (Id_accident) - 0 duplicate accident IDs |

No duplicate records found in any table. Note: lieux has 70,248 records for 54,402 accidents (1.29 locations per accident on average), which is expected as some accidents span multiple road segments.

---

## D. Data Quality Summary

### Main Issues Discovered

1. **lartpc (99.95% empty)**: Column provides zero analytical value
2. **v2 (91.58% empty)**: Sparsely populated road numbering field
3. **Negative values pervasive**: vma (-1), pr, pr1, larrout all have negative values indicating "unknown/missing" codes
4. **CNIT missing (23.9%)**: VIN data gaps limit vehicle tracing
5. **Invalid category codes**: surf (8,9) and col (-1) outside specification
6. **Extreme speed limits**: 500, 300, 900 km/h clearly erroneous
7. **Address missing (4.25%)**: Low impact since coordinates are available
8. **Comma decimal format**: Coordinates use French locale (comma separator) requiring conversion

### Impact on Downstream Analytics

- **Geospatial analysis**: Coordinate format requires parsing but is workable. DOM-TOM data extends range beyond mainland France.
- **Vehicle fleet analysis**: 6.4% missing ages + 23.9% missing VINs introduce bias
- **Road safety modeling**: Negative `vma` values (-1) will skew speed-limit analysis unless filtered
- **Road width analysis**: 69% of `larrout` values are negative/meaningless
- **Surface analysis**: Invalid codes (8,9) represent ~0.5% of data - minor impact
- **Time-series analysis**: Clean with no missing date/time values

---

# Part 2: Transformations, Modeling & Medallion Architecture

## A. Required Transformations (Silver Layer)

### A.1 Standardization

| Transformation | Table | Column(s) | Rule |
|---------------|-------|-----------|------|
| Coordinate format | caracteristiques | lat, long | Replace `,` with `.`; cast to float |
| Date construction | caracteristiques | jour, mois, an | Build date YYYY-MM-DD |
| Time format | caracteristiques | hrmn | Ensure HH:MM with leading zeros |
| Categorical mapping | All | All coded columns | Replace codes with labels |
| Territory normalization | vehicules | Territoire Nom | Standardize casing |

### A.2 Cleaning

| Cleaning Operation | Table | Condition | Action |
|-------------------|-------|-----------|--------|
| Drop useless column | lieux | lartpc 99.95% empty | Drop column |
| Drop sparse column | lieux | v2 91.58% empty | Drop or archive |
| Filter invalid col | caracteristiques | col = -1 | Set to NaN or map to "Unknown" |
| Filter invalid surf | lieux | surf in (-1, 8, 9) | Set to NaN |
| Cap vma outliers | lieux | vma > 150 or vma < 0 | Set to NaN |
| Handle negative pr/pr1 | lieux | pr < 0 or pr1 < 0 | Interpret as "unknown", set to NaN |
| Handle negative larrout | lieux | larrout < 0 | Set to NaN |
| Impute age | vehicules | Age véhicule NaN | Fill with median per vehicle category |
| Cap extreme ages | vehicules | Age véhicule > 50 | Cap at 50 |
| Handle missing CNIT | vehicules | CNIT NaN | Flag as "UNKNOWN" |

### A.3 Enrichment

| Derived Field | Table | Logic | Purpose |
|--------------|-------|-------|---------|
| accident_date | caracteristiques | DATE(an, mois, jour) | Date dimension key |
| hour | caracteristiques | HOUR(hrmn) | Time analysis |
| minute | caracteristiques | MINUTE(hrmn) | Time granularity |
| time_of_day | caracteristiques | Night(0-6), Morning(6-12), Afternoon(12-18), Evening(18-24) | Time-of-day patterns |
| season | caracteristiques | Winter(DJF), Spring(MAM), Summer(JJA), Fall(SON) | Seasonal patterns |
| day_of_week | caracteristiques | DOW(accident_date) | Weekend/weekday analysis |
| weekend_flag | caracteristiques | True if Sat/Sun | Weekend risk analysis |
| vehicle_count | caracteristiques | COUNT(vehicules per Num_Acc) | Accident complexity |
| accident_severity | caracteristiques | Computed from collision type + vehicle count | Severity index |
| age_group | vehicules | 0-2, 3-5, 6-10, 11-20, 20+ | Vehicle age cohorts |
| territory_group | vehicules | Métropole, DOM, Autre | Geographic grouping |

### A.4 Deduplication

- No exact duplicates found in any table
- Referential integrity: ensure every `lieux.Num_Acc` and `vehicules.Id_accident` exists in `caracteristiques`
- Remove orphan records (if any)

### A.5 Transformation Documentation

All transformation steps logged with:
- Row counts before/after each operation
- Number of records modified per rule
- Parameters used for imputation
- Timestamp of execution
- Script versioning via Git

---

## B. Modeling (Gold Layer)

### Star Schema Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     FACT TABLE: f_accidents                     │
├─────────────────────────────────────────────────────────────────┤
│  Num_Acc (PK)          │  INTEGER                               │
│  date_key (FK)         │  INTEGER  → dim_date                  │
│  time_key (FK)         │  INTEGER  → dim_time                  │
│  location_key (FK)     │  INTEGER  → dim_location              │
│  weather_key (FK)      │  INTEGER  → dim_weather               │
│  lighting_key (FK)     │  INTEGER  → dim_lighting              │
│  collision_key (FK)    │  INTEGER  → dim_collision_type        │
│  road_key (FK)         │  INTEGER  → dim_road                  │
│  vehicle_count         │  INTEGER  │  (# vehicles involved)    │
│  severity_index        │  FLOAT    │  (composite score)        │
│  has_fatalities        │  BOOLEAN  │                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
     ┌──────────────────────┼──────────────────────┐
     │                      │                      │
     ▼                      ▼                      ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  dim_date    │  │  dim_time        │  │  dim_location    │
├──────────────┤  ├──────────────────┤  ├──────────────────┤
│ date_key(PK) │  │ time_key(PK)     │  │ location_key(PK) │
│ full_date    │  │ hour             │  │ department       │
│ year         │  │ minute           │  │ commune          │
│ month        │  │ time_of_day      │  │ road_category    │
│ day          │  │ (Night/Morning/  │  │ urban_area       │
│ day_of_week  │  │  Afternoon/Eve)  │  │ speed_limit      │
│ weekend_flag │  │                  │  │ latitude         │
│ season       │  │                  │  │ longitude        │
└──────────────┘  └──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────────┐  ┌──────────────────┐
│  dim_weather     │  │  dim_lighting        │  │ dim_collision    │
├──────────────────┤  ├──────────────────────┤  ├──────────────────┤
│ weather_key(PK)  │  │ lighting_key(PK)     │  │ collision_key(PK)│
│ weather_cond     │  │ lighting_cond        │  │ collision_type   │
│ surface_cond     │  │ (Daylight/Twilight/  │  │ intersection_type│
│ (Normal/Rain/    │  │  Night no light/     │  │                  │
│  Snow/Fog/...)   │  │  Night light on/off) │  │                  │
└──────────────────┘  └──────────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────────┐
│  dim_road        │  │  dim_vehicle (bridge)│
├──────────────────┤  ├──────────────────────┤
│ road_key(PK)     │  │ vehicle_key(PK)      │
│ road_profile     │  │ vehicle_category     │
│ road_plan        │  │ vehicle_age_group    │
│ infrastructure   │  │ territory            │
│ situation        │  │                      │
│ traffic_dir      │  │ Note: bridge table   │
│ num_lanes        │  │ links accidents to   │
│ road_width       │  │ multiple vehicles    │
└──────────────────┘  └──────────────────────┘
```

### Fact Table: `f_accidents`
- Grain: One row per accident
- Measures: vehicle_count, severity_index
- Foreign keys to 7 dimensions

### Dimension Tables
- **dim_date**: Date hierarchy for time-series analysis
- **dim_time**: Hour/minute granularity with time-of-day categories
- **dim_location**: Geographic hierarchy (department → commune)
- **dim_weather**: Weather + surface conditions
- **dim_lighting**: Lighting conditions
- **dim_collision_type**: Collision + intersection types
- **dim_road**: Road geometry and characteristics
- **dim_vehicle**: Vehicle attributes (bridge table for many-to-many)

---

## C. Medallion Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MEDALLION ARCHITECTURE                              │
│                     French Road Safety Open Data (BAAC)                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  BRONZE LAYER (Raw Data Ingestion)                                          │
│                                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │ caracteristiques.csv│  │   lieux.csv         │  │  vehicules.csv      │  │
│  │ (Accident char.)    │  │ (Location details)  │  │ (Vehicle info)       │  │
│  │ 54,402 rows         │  │ 70,248 rows         │  │ 83,730 rows         │  │
│  │ 15 columns          │  │ 18 columns          │  │ 7 columns           │  │
│  └──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘  │
│             │                        │                        │             │
│  Format: CSV (raw source)                                      │             │
│  Encoding: latin1                                              │             │
│  Storage: /bronze/baac/2024/                                   │             │
└─────────────┬──────────────────────────────────────────────────┘             │
              │                                                                 │
              │  Data Quality Checks & Validation                              │
              │  ├─ Schema validation                                           │
              │  ├─ Missing value quantification                               │
              │  ├─ Outlier detection                                          │
              │  ├─ Format standardization                                     │
              │  └─ Referential integrity checks                               │
              │                                                                 │
              ▼                                                                 │
┌─────────────────────────────────────────────────────────────────────────────┐
│  SILVER LAYER (Cleaned & Standardized)                                      │
│                                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │ silver_caracteristiques│  │  silver_lieux     │  │ silver_vehicules    │  │
│  │                       │  │                    │  │                     │  │
│  │ ├─ Coordinates fixed  │  │ ├─ lartpc dropped │  │ ├─ Age imputed      │  │
│  │ ├─ Date built        │  │ ├─ v2 dropped      │  │ ├─ CNIT flagged     │  │
│  │ ├─ Time-of-day added │  │ ├─ vma capped      │  │ ├─ Age capped >50   │  │
│  │ ├─ Season added      │  │ ├─ surf codes fixed│  │ ├─ Territory labeled │  │
│  │ └─ Day-of-week added │  │ └─ larrout cleaned │  │ └─ Deduplicated     │  │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │
│                                                                             │
│  Format: Parquet (columnar, compressed)                                     │
│  Partitioning: by year, month                                               │
│  Storage: /silver/baac/2024/                                                │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               │  Aggregation & Modeling
                               │  ├─ Star schema construction
                               │  ├─ Dimension table creation
                               │  ├─ Fact table building
                               │  └─ Business logic application
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  GOLD LAYER (Analytical Model)                                              │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  dim_date    │  │  dim_time    │  │ dim_location  │  │ dim_weather  │   │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤   │
│  │ 365 rows     │  │ 24 hours     │  │ ~100 depts   │  │ 7 conditions │   │
│  │ + hierarchy  │  │ + 4 periods  │  │ + communes   │  │ + surface    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                             │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐                  │
│  │ dim_lighting │  │ dim_collision    │  │  dim_road    │                  │
│  ├──────────────┤  ├──────────────────┤  ├──────────────┤                  │
│  │ 5 conditions │  │ 8 types + inter  │  │ 5 profiles   │                  │
│  └──────────────┘  └──────────────────┘  └──────────────┘                  │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    f_accidents (Fact Table)                        │    │
│  │                    ~54,402 rows                                    │    │
│  │                    Keys to all dims + measures                     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  Format: Parquet, partitioned by year                                      │
│  Storage: /gold/baac/                                                      │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               │  BI / Dashboards
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONSUMPTION LAYER (BI & Dashboards)                                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Dashboards & Reports                                                │   │
│  │                                                                      │   │
│  │  ├─ Accident Hotspot Map (geospatial with lat/long)                  │   │
│  │  ├─ Monthly Accident Trends (time series)                            │   │
│  │  ├─ Severity by Road Type (bar charts)                               │   │
│  │  ├─ Weather Impact Analysis (heatmap)                                │   │
│  │  ├─ Vehicle Fleet Profile (age distribution)                         │   │
│  │  ├─ Speed Limit Compliance Analysis                                  │   │
│  │  └─ Department-level Comparative Dashboard                           │   │
│  │                                                                      │   │
│  │  Tools: Power BI / Tableau / Superset / Metabase                    │   │
│  │  Refresh: Daily incremental / Monthly full refresh                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Design Choices Justification

| Choice | Justification |
|--------|---------------|
| **Star Schema** | Optimized for analytical queries with fewer joins; denormalized dimensions improve BI tool performance vs. snowflake |
| **Parquet format** | Columnar storage enables efficient compression (5-10x vs CSV); predicate pushdown for fast filtering |
| **Partitioning by year/month** | Most queries filter by time period; partition pruning significantly reduces scan volume |
| **Separate time/date dimensions** | Enables flexible time-based analysis (hourly patterns, seasonal trends, YoY comparisons) |
| **8 dimensions** | Each dimension is independent and slowly changing; enables drill-down analysis across multiple axes |
| **Silver enrichment at table level** | Keeps transformations focused; easier to maintain and debug |
| **Severity index** | Composite measure combining collision type + vehicle count enables ranking accidents by seriousness |
| **Vehicle bridge table** | Handles many-to-many relationship (one accident → many vehicles) correctly |
| **Reverse geocoding optional** | Address can be derived from coordinates if needed, avoiding 4.25% missing address gap |
| **DOM-TOM inclusion** | Overseas territories are kept as valid data points with appropriate coordinate range handling |

---

## Files Available

| Logical Table | Physical File | Rows | Columns |
|--------------|---------------|------|---------|
| caracteristiques | vehicules_2024.csv | 54,402 | 15 |
| lieux | usagers_2024.csv | 70,248 | 18 |
| vehicules | caracteristiques_2024.csv | 83,730 | 7 |
| Documentation | documentation_variables.pdf | — | Variable descriptions |
| Documentation | fiche_baac.pdf | — | BAAC form structure |

**Note:** The CSV files as downloaded from data.gouv.fr have names that do not match their content. The mapping above reflects the actual data contained in each file.
