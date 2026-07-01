import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime

plt.rcParams['figure.figsize'] = (12, 6)
sns.set_style('whitegrid')

data_dir = 'C:/Users/aurel/OneDrive/Documents/Data integration/tp1/data/'
output_dir = 'C:/Users/aurel/OneDrive/Documents/Data integration/tp1/'

# ── Load the 3 tables for 2024 ──
carac = pd.read_csv(data_dir + 'vehicules_2024.csv', sep=';', encoding='utf-8')
lieux = pd.read_csv(data_dir + 'usagers_2024.csv', sep=';', encoding='utf-8')
vehicules = pd.read_csv(data_dir + 'caracteristiques_2024.csv', sep=';', encoding='utf-8')

# ──────────────────────────────────────────────
# PART 1: DATA PROFILING & DATA QUALITY ANALYSIS
# ──────────────────────────────────────────────
print("=" * 80)
print("PART 1: DATA PROFILING & DATA QUALITY ANALYSIS")
print("=" * 80)

# ── A.1 Column inventory ──
print("\n## A.1 COLUMN INVENTORY\n")

tables = {
    'caracteristiques (Accident characteristics)': carac,
    'lieux (Location details)': lieux,
    'vehicules (Vehicle info)': vehicules
}

for name, df in tables.items():
    print(f"\n### {name}  [{df.shape[0]} rows x {df.shape[1]} cols]")
    print("-" * 60)
    dtype_map = {'int64': 'Integer', 'float64': 'Float', 'object': 'String'}
    for col in df.columns:
        inferred = dtype_map.get(str(df[col].dtype), str(df[col].dtype))
        print(f"  {col:40s} | {inferred:10s} | {df[col].isna().sum():6d} nulls")

# ── A.2 Semantic meaning ──
print("\n## A.2 SEMANTIC MEANING OF COLUMNS\n")

carac_meaning = {
    'Num_Acc': "Unique accident identifier (format: YYYY + sequential number)",
    'jour': "Day of accident (1-31)",
    'mois': "Month of accident (1-12)",
    'an': "Year of accident",
    'hrmn': "Hour and minute of accident (HH:MM)",
    'lum': "Lighting condition (1=Daylight, 2=Twilight, 3=Night without public lighting, 4=Night with public lighting on, 5=Night with public lighting off)",
    'dep': "Department number (INSEE code)",
    'com': "Commune number (INSEE code)",
    'agg': "Urban area type (1=Outside built-up area, 2=In built-up area)",
    'int': "Intersection type (1=Not an intersection, 2=Cross-shaped, 3=T-shaped, 4=Y-shaped, 5=Roundabout, 6=Square, 7=Level crossing, 8=Other)",
    'atm': "Weather condition (1=Normal, 2=Light rain, 3=Heavy rain, 4=Snow, 5=Fog, 6=Strong wind, 7=Glare, 8=Cloudy, 9=Other)",
    'col': "Collision type (1=Two vehicles - frontal, 2=Two vehicles - same direction, 3=Two vehicles - perpendicular, 4=Two vehicles - opposite direction, 5=Three+ vehicles chain, 6=Three+ vehicles multiple collisions, 7=Other collision, 8=Without collision)",
    'adr': "Street address or road name",
    'lat': "Latitude (decimal, comma as separator)",
    'long': "Longitude (decimal, comma as separator)"
}
lieux_meaning = {
    'Num_Acc': "Unique accident identifier (FK to caracteristiques)",
    'catr': "Road category (1=Highway, 2=National road, 3=Departmental road, 4=Communal road, 5=Private road, 6=Pedestrian area, 7=Cycle path, 9=Other)",
    'voie': "Road name or number",
    'v1': "Road numbering: first index",
    'v2': "Road numbering: second index (letter)",
    'circ': "Traffic direction (1=One-way, 2=Two-way, 3=Separated carriageways)",
    'nbv': "Number of traffic lanes",
    'vosp': "Reserved lane (1=Bus/taxi/emergency, 2=Cycle lane, 3=Other)",
    'prof': "Road profile (1=Flat, 2=Slope, 3=Hilltop, 4=Bottom of slope, 5=Other)",
    'pr': "Reference point number (PR)",
    'pr1': "Reference point distance (meters)",
    'plan': "Road plan (1=Straight, 2=Curve left, 3=Curve right, 4=S-bend, 5=Other)",
    'lartpc': "Central reservation width (meters)",
    'larrout': "Road width (meters)",
    'surf': "Surface condition (1=Normal, 2=Wet, 3=Flooded, 4=Snow/ice, 5=Mud, 6=Oil/grease, 7=Other)",
    'infra': "Infrastructure (0=None, 1=Subway, 2=Bridge, 3=Tunnel, 4=Other)",
    'situ': "Situation (1=On road, 2=On pavement, 3=On cycle path, 4=On hard shoulder, 5=Other)",
    'vma': "Speed limit (km/h)"
}
vehicules_meaning = {
    'Id_accident': "Accident ID (joins to Num_Acc in caracteristiques/lieux)",
    'Lettre Conventionnelle Véhicule': "Vehicle letter within accident (A, B, C...)",
    'Année': "Year",
    'Lieu Admin Actuel - Territoire Nom': "Territory (Metropole, DOM, etc.)",
    'CNIT': "Vehicle identification number (VIN/chassis)",
    'Catégorie véhicule': "Vehicle category (VT=Car, VU=Utility, PL=Truck, TC=Public transport, Cyclo, Moto légère/lourde, etc.)",
    'Age véhicule': "Vehicle age in years at time of accident"
}

print("### caracteristiques (Accident characteristics)")
for k, v in carac_meaning.items():
    print(f"  {k:20s} : {v}")
print("\n### lieux (Location details)")
for k, v in lieux_meaning.items():
    print(f"  {k:20s} : {v}")
print("\n### vehicules (Vehicle info)")
for k, v in vehicules_meaning.items():
    print(f"  {k:20s} : {v}")

# ── B. MISSING VALUES AND COMPLETENESS ──
print("\n" + "=" * 80)
print("B. MISSING VALUES AND COMPLETENESS")
print("=" * 80)

missing_report = {}
for name, df in tables.items():
    missing = df.isna().sum()
    missing_pct = (missing / len(df)) * 100
    report = pd.DataFrame({'Missing': missing, 'Percent': missing_pct})
    report = report[report['Missing'] > 0].sort_values('Percent', ascending=False)
    missing_report[name] = report
    print(f"\n### {name}")
    if len(report) > 0:
        print(report.to_string())
    else:
        print("  No missing values")

# ── C. CONSISTENCY AND VALIDITY CHECKS ──
print("\n" + "=" * 80)
print("C. CONSISTENCY AND VALIDITY CHECKS")
print("=" * 80)

# C.1 Value ranges and anomalies
print("\n## C.1 Out-of-range values & anomalies\n")

# Caracteristiques
print("### caracteristiques")
print(f"  lat range: {carac['lat'].dropna().unique()[:5]}...")
carac['lat_num'] = pd.to_numeric(carac['lat'].str.replace(',', '.'), errors='coerce')
carac['long_num'] = pd.to_numeric(carac['long'].str.replace(',', '.'), errors='coerce')
print(f"  lat numeric: min={carac['lat_num'].min():.4f}, max={carac['lat_num'].max():.4f}")
print(f"  long numeric: min={carac['long_num'].min():.4f}, max={carac['long_num'].max():.4f}")
# France bounds approx
bad_lat = carac[(carac['lat_num'] < 41) | (carac['lat_num'] > 52)].shape[0]
bad_long = carac[(carac['long_num'] < -5) | (carac['long_num'] > 10)].shape[0]
# For DOM-TOM include wider range
bad_lat_wide = carac[(carac['lat_num'] < -22) | (carac['lat_num'] > 52)].shape[0]
bad_long_wide = carac[(carac['long_num'] < -180) | (carac['long_num'] > 180)].shape[0]
print(f"  Coordinates outside France mainland (lat<41|>52): {bad_lat}")
print(f"  Coordinates outside France mainland (long<-5|>10): {bad_long}")

# Check lum (lighting)
invalid_lum = carac[~carac['lum'].isin([1,2,3,4,5])]['lum'].value_counts()
print(f"  Invalid lum values: {dict(invalid_lum) if len(invalid_lum)>0 else 'None'}")

# Check atm (weather)
invalid_atm = carac[~carac['atm'].isin(range(0,10))]['atm'].value_counts()
print(f"  Invalid atm values: {dict(invalid_atm) if len(invalid_atm)>0 else 'None'}")

# Check col (collision)
invalid_col = carac[~carac['col'].isin(range(0,9))]['col'].value_counts()
print(f"  Invalid col values: {dict(invalid_col) if len(invalid_col)>0 else 'None'}")

# Check hrmn format
invalid_time = carac[~carac['hrmn'].str.match(r'^\d{2}:\d{2}$', na=True)]['hrmn'].value_counts()
print(f"  Invalid hrmn format: {len(invalid_time)}")

print("\n### lieux")
# Check catr (road category)
valid_catr = [1,2,3,4,5,6,7,9]
invalid_catr = lieux[~lieux['catr'].isin(valid_catr)]['catr'].value_counts()
print(f"  Invalid catr: {dict(invalid_catr) if len(invalid_catr)>0 else 'None'}")

# Check surf (surface)
invalid_surf = lieux[~lieux['surf'].isin(range(0,8))]['surf'].value_counts()
print(f"  Invalid surf: {dict(invalid_surf) if len(invalid_surf)>0 else 'None'}")

# Check vma (speed limit)
invalid_vma = lieux[(lieux['vma'] < 0) | (lieux['vma'] > 150)]['vma'].value_counts().head(10)
print(f"  Invalid vma (<0 or >150): {dict(invalid_vma) if len(invalid_vma)>0 else 'None'}")

# Check negative pr/pr1 (convert to numeric first)
lieux['pr_num'] = pd.to_numeric(lieux['pr'], errors='coerce')
lieux['pr1_num'] = pd.to_numeric(lieux['pr1'], errors='coerce')
lieux['larrout_num'] = pd.to_numeric(lieux['larrout'], errors='coerce')
neg_pr = (lieux['pr_num'] < 0).sum()
neg_pr1 = (lieux['pr1_num'] < 0).sum()
print(f"  Negative pr: {neg_pr} values")
print(f"  Negative pr1: {neg_pr1} values")
neg_larrout = (lieux['larrout_num'] < 0).sum()
print(f"  Negative larrout: {neg_larrout} values")

print("\n### vehicules")
# Use column indices to avoid encoding issues
age_col = vehicules.columns[6]  # Age véhicule
cat_col = vehicules.columns[5]  # Catégorie véhicule
terr_col = vehicules.columns[3]  # Lieu Admin Actuel - Territoire Nom

neg_age = vehicules[vehicules[age_col] < 0].shape[0]
unreal_age = vehicules[vehicules[age_col] > 50].shape[0]
print(f"  Negative age: {neg_age}")
print(f"  Unrealistic age (>50 years): {unreal_age}")

# Check vehicle category
veh_cats = vehicules[cat_col].value_counts()
print(f"  Vehicle categories: {dict(veh_cats)}")

# Territory distribution
print(f"\n  Territory distribution:")
print(f"  {vehicules[terr_col].value_counts().to_string()}")

# C.2 Categorical anomalies
print("\n## C.2 Categorical anomalies\n")

print("### caracteristiques - Unique values per categorical column")
for col in ['lum', 'atm', 'col', 'agg', 'int']:
    vals = carac[col].value_counts().sort_index()
    print(f"  {col}: {dict(vals)}")

print("\n### lieux - Unique values per categorical column")
for col in ['catr', 'circ', 'vosp', 'prof', 'plan', 'surf', 'infra', 'situ']:
    vals = lieux[col].value_counts().sort_index()
    print(f"  {col}: {dict(vals)}")

# C.3 Duplicates
print("\n## C.3 Duplicates\n")

for name, df in tables.items():
    dups = df.duplicated().sum()
    dup_id_col = 'Num_Acc' if 'Num_Acc' in df.columns else df.columns[0]
    try:
        dups_subset = df.duplicated(subset=[dup_id_col]).sum()
    except:
        dups_subset = 'N/A'
    print(f"  {name}: {dups} exact duplicates, {dups_subset} duplicate IDs")

# ── D. DATA QUALITY SUMMARY ──
print("\n" + "=" * 80)
print("D. DATA QUALITY SUMMARY")
print("=" * 80)

print("""
### Main Issues Discovered:

1. MISSING COORDINATES: Some accidents have missing lat/long values,
   preventing geospatial analysis.

2. INVALID COORDINATES: Some coordinates fall outside expected French
   territory bounds.

3. NEGATIVE AGES: Vehicle ages with negative values are clearly erroneous.

4. EXTREME VEHICLE AGES: Vehicles older than 50 years are suspicious and
   may indicate data entry errors.

5. STANDARDIZATION ISSUES: Coordinates use comma as decimal separator
   (French format) which requires conversion for analysis tools.

6. DOM-TOM vs METROPOLE: The dataset covers both mainland France and
   overseas territories with different coordinate ranges.

7. CATEGORICAL CONSISTENCY: Some categorical columns have unexpected
   values (e.g., 0 values where min should be 1).

### Impact on Downstream Analytics:

- Missing/invalid coordinates limit geospatial analysis and mapping.
- Vehicle age errors affect fleet analysis and accident-risk correlation.
- Format inconsistencies cause parsing failures in BI tools.
- Category anomalies may lead to incorrect aggregations.
- Duplicate accident IDs could inflate accident counts.
"""
)

print("=" * 80)
print("END OF PART 1 - DATA PROFILING REPORT")
print("=" * 80)

# ──────────────────────────────────────────────────
# PART 2: TRANSFORMATIONS, MODELING & MEDALLION ARCH
# ──────────────────────────────────────────────────
print("\n\n")
print("=" * 80)
print("PART 2: TRANSFORMATIONS, MODELING & MEDALLION ARCHITECTURE")
print("=" * 80)

print("""
## A. REQUIRED TRANSFORMATIONS (Silver Layer)

### A.1 Standardization
  - Convert coordinate decimal format: replace ',' with '.' in lat/long
  - Standardize date formats: ensure consistent YYYY-MM-DD
  - Normalize hour format: pad single-digit hours (e.g., 7:40 -> 07:40)
  - Map categorical codes to human-readable labels

### A.2 Cleaning
  - Remove records with invalid coordinates (outside France bounds)
  - Cap or remove negative vehicle ages (set to NaN or impute with median)
  - Cap unrealistic vehicle ages (>50 years) at 50
  - Handle invalid categorical values (outside defined code ranges)

### A.3 Enrichment
  - Add accident severity index (based on number of vehicles involved)
  - Add time-of-day category (Night, Morning, Afternoon, Evening)
  - Add season (Winter, Spring, Summer, Fall)
  - Add day-of-week and weekend flag
  - Merge department names from external reference

### A.4 Deduplication
  - Remove exact duplicate rows
  - Keep first occurrence for duplicate (Num_Acc, vehicle letter) pairs

### A.5 Documentation
  - All transformations are logged with row counts before/after
  - Transformation rules are stored in a JSON metadata file
  - Referential integrity: Num_Acc must match across all tables

## B. MODELING (Gold Layer)

### Star Schema Design:

FACT TABLE: f_accidents
  - Num_Acc (PK)
  - date_key (FK -> dim_date)
  - location_key (FK -> dim_location)
  - time_key (FK -> dim_time)
  - weather_key (FK -> dim_weather)
  - lighting_key (FK -> dim_lighting)
  - collision_type_key (FK -> dim_collision_type)
  - accident_count (measure)
  - vehicle_count (measure)
  - severity_score (measure)

DIMENSION TABLES:
  - dim_date: date, year, month, day, day_of_week, weekend_flag, season
  - dim_time: hour, minute, time_of_day_category
  - dim_location: department, commune, road_category, speed_limit,
                  urban_area, coordinates
  - dim_weather: weather_condition, surface_condition
  - dim_lighting: lighting_condition
  - dim_collision_type: collision_type, intersection_type
  - dim_vehicle: vehicle_category, vehicle_age_group
  - dim_road: road_profile, road_plan, infrastructure, situation

## C. MEDALLION ARCHITECTURE DIAGRAM

### BRONZE LAYER (Raw data)
  ┌─────────────────────────────────────────────────────┐
  │                   BRONZE LAYER                       │
  │                                                      │
  │  caracteristiques_2024.csv  (accident char.)         │
  │  lieux_2024.csv             (location details)       │
  │  vehicules_2024.csv         (vehicle info)           │
  │  usagers_2024.csv           (person info - if avail) │
  │                                                      │
  │  Format: CSV, raw as extracted                       │
  │  Storage: /bronze/accidents/                         │
  └──────────────────────┬──────────────────────────────┘
                         │
                         │ Data Quality Checks
                         │ Standardization
                         │ Cleaning
                         │ Enrichment
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │                   SILVER LAYER                       │
  │                                                      │
  │  silver_caracteristiques  (cleaned, standardized)    │
  │  silver_lieux             (cleaned, enriched)        │
  │  silver_vehicules         (cleaned, deduplicated)    │
  │                                                      │
  │  Format: Parquet (columnar, compressed)              │
  │  Storage: /silver/accidents/                         │
  └──────────────────────┬──────────────────────────────┘
                         │
                         │ Aggregation
                         │ Model transformation
                         │ Star schema building
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │                   GOLD LAYER                         │
  │                                                      │
  │  Fact: f_accidents                                   │
  │  Dim: dim_date, dim_time, dim_location,              │
  │       dim_weather, dim_lighting, dim_collision_type, │
  │       dim_vehicle, dim_road                          │
  │                                                      │
  │  Format: Parquet, partitioned by year/month          │
  │  Storage: /gold/accidents/                           │
  └──────────────────────┬──────────────────────────────┘
                         │
                         │ BI / Dashboards
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │              CONSUMPTION LAYER                       │
  │                                                      │
  │  - Power BI / Tableau dashboards                     │
  │  - SQL analytics queries                             │
  │  - Geospatial maps (Leaflet, Kepler.gl)              │
  │  - Annual road safety reports                        │
  └─────────────────────────────────────────────────────┘

## DESIGN CHOICES JUSTIFICATION

1. Star Schema over Snowflake: Optimized for analytical queries
   with fewer joins; denormalized dimensions for BI tool performance.

2. Parquet format: Columnar storage enables efficient compression
   and predicate pushdown; ideal for analytical workloads.

3. Partitioning by year/month: Most queries filter by time period;
   partition pruning significantly reduces scan volume.

4. Separate time/date dimensions: Enables flexible time-based
   analysis (hourly patterns, seasonal trends, year-over-year).

5. Geospatial enrichment: Adding coordinates in the Silver layer
   enables map-based analytics in the Gold layer.

6. Data quality gates: Each layer transition includes validation
   checks to prevent corrupted data from propagating.
"""
)

print("=" * 80)
print("END OF REPORT")
print("=" * 80)
