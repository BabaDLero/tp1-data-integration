import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="BAAC 2024 - Road Safety Dashboard", layout="wide")
sns.set_style('whitegrid')

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@st.cache_data
def load_data():
    carac = pd.read_csv(os.path.join(DATA_DIR, 'vehicules_2024.csv'), sep=';', encoding='latin1')
    lieux = pd.read_csv(os.path.join(DATA_DIR, 'usagers_2024.csv'), sep=';', encoding='latin1')
    vehicules = pd.read_csv(os.path.join(DATA_DIR, 'caracteristiques_2024.csv'), sep=';', encoding='latin1')
    return carac, lieux, vehicules

carac, lieux, vehicules = load_data()

st.title("🚗 French Road Safety Data Analysis — BAAC 2024")
st.markdown("""
**Dataset:** Accidents corporels de la circulation routière  
**Source:** [data.gouv.fr](https://www.data.gouv.fr/) | **Year:** 2024  
""")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Data Overview", "🔍 Missing Values", "✅ Quality Checks",
    "📈 Visualizations", "🏛️ Medallion Arch", "📋 Full Report"
])

with tab1:
    st.header("Dataset Structure")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accidents (caractéristiques)", f"{carac.shape[0]:,}", help="54,402 accidents in 2024")
    with col2:
        st.metric("Location Records (lieux)", f"{lieux.shape[0]:,}", help="70,248 road segments")
    with col3:
        st.metric("Vehicles (vehicules)", f"{vehicules.shape[0]:,}", help="83,730 vehicles involved")

    for name, df, desc in [
        ("caracteristiques — Accident Characteristics", carac,
         "Time, location, weather, lighting, collision type, coordinates"),
        ("lieux — Location Details", lieux,
         "Road category, traffic direction, speed limit, surface, infrastructure"),
        ("vehicules — Vehicle Info", vehicules,
         "Vehicle category, age, VIN, territory")
    ]:
        with st.expander(f"**{name}** ({df.shape[1]} columns) — {desc}"):
            info = pd.DataFrame({
                'Column': df.columns,
                'Dtype': df.dtypes.values,
                'Nulls': df.isna().sum().values,
                'Null %': (df.isna().sum() / len(df) * 100).round(2).values,
                'Unique': [df[c].nunique() for c in df.columns]
            })
            st.dataframe(info, use_container_width=True, hide_index=True)

with tab2:
    st.header("Missing Values Analysis")
    fig_cols = st.columns(3)
    tables = [("caracteristiques", carac), ("lieux", lieux), ("vehicules", vehicules)]
    for i, (name, df) in enumerate(tables):
        with fig_cols[i]:
            missing_pct = (df.isna().sum() / len(df) * 100).round(2)
            missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=False)
            if len(missing_pct) > 0:
                fig, ax = plt.subplots(figsize=(6, 4))
                colors = ['#e74c3c' if v > 50 else '#f39c12' if v > 10 else '#3498db' for v in missing_pct.values]
                ax.barh(range(len(missing_pct)), missing_pct.values, color=colors)
                ax.set_yticks(range(len(missing_pct)))
                ax.set_yticklabels(missing_pct.index, fontsize=9)
                ax.set_xlabel('% Missing')
                ax.set_title(f'{name} — Missing Values')
                st.pyplot(fig)
            else:
                st.info(f"✅ {name}: No missing values")

    st.subheader("Critical Missingness")
    st.markdown("""
    | Column | Table | Missing | % | Severity |
    |--------|-------|---------|---|----------|
    | lartpc (reservation width) | lieux | 70,215 | **99.95%** | 🔴 Drop column |
    | v2 (road index 2) | lieux | 64,332 | **91.58%** | 🔴 Drop column |
    | CNIT (VIN) | vehicules | 20,028 | **23.92%** | 🟡 Impute as Unknown |
    | voie (road name) | lieux | 13,331 | **18.98%** | 🟡 Enrich from coords |
    | Age véhicule | vehicules | 5,395 | **6.44%** | 🟢 Impute by category |
    | adr (address) | caracteristiques | 2,310 | **4.25%** | 🟢 Reverse geocode |
    """)

with tab3:
    st.header("Data Quality Checks")
    q1, q2, q3 = st.columns(3)
    with q1:
        st.subheader("Coordinates")
        carac['lat_num'] = pd.to_numeric(carac['lat'].str.replace(',', '.'), errors='coerce')
        carac['long_num'] = pd.to_numeric(carac['long'].str.replace(',', '.'), errors='coerce')
        st.metric("Outside mainland France", f"{(carac['lat_num'] < 41).sum() + (carac['lat_num'] > 52).sum():,}")
        st.metric("Invalid lat (-22 to 52)", f"0 ✅" if carac['lat_num'].between(-22, 52).all() else "Some issues")

    with q2:
        st.subheader("Invalid Codes")
        invalid_col = (carac['col'] == -1).sum()
        invalid_surf = lieux['surf'].isin([-1, 8, 9]).sum()
        invalid_vma = lieux['vma'].isin([-1, 500, 300, 900]).sum()
        st.metric("Invalid collision (col=-1)", f"{invalid_col}")
        st.metric("Invalid surface (surf)", f"{invalid_surf:,}")
        st.metric("Invalid speed limit (vma)", f"{invalid_vma:,}")

    with q3:
        st.subheader("Negative Values")
        lieux['pr_num'] = pd.to_numeric(lieux['pr'], errors='coerce')
        lieux['pr1_num'] = pd.to_numeric(lieux['pr1'], errors='coerce')
        lieux['larrout_num'] = pd.to_numeric(lieux['larrout'], errors='coerce')
        st.metric("Negative pr", f"{(lieux['pr_num'] < 0).sum():,}")
        st.metric("Negative pr1", f"{(lieux['pr1_num'] < 0).sum():,}")
        st.metric("Negative larrout", f"{(lieux['larrout_num'] < 0).sum():,}")

    st.subheader("Categorical Distributions")
    col_cat = st.selectbox("Select column", ['lum', 'atm', 'col', 'agg', 'int'])
    if col_cat in carac.columns:
        vc = carac[col_cat].value_counts().sort_index()
        labels = {
            'lum': {1:'Daylight',2:'Twilight',3:'Night no light',4:'Night light on',5:'Night light off'},
            'atm': {1:'Normal',2:'Light rain',3:'Heavy rain',4:'Snow',5:'Fog',6:'Strong wind',7:'Glare',8:'Cloudy',9:'Other'},
            'col': {-1:'Unknown',1:'Frontal',2:'Same dir',3:'Perpend.',4:'Opposite',5:'Chain',6:'Multiple',7:'Other',8:'None'},
            'agg': {1:'Outside urban',2:'In urban'},
            'int': {1:'None',2:'Cross',3:'T-shape',4:'Y-shape',5:'Roundabout',6:'Square',7:'Level xing',8:'Other',9:'Not specified'}
        }
        fig = px.bar(x=vc.index, y=vc.values,
                     labels={'x': col_cat, 'y': 'Count'},
                     title=f'{col_cat} Distribution')
        fig.update_layout(xaxis=dict(tickmode='array',
                                     tickvals=list(labels.get(col_cat, {}).keys()),
                                     ticktext=list(labels.get(col_cat, {}).values())))
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Visualizations")
    viz_type = st.radio("Select chart", ["Accidents by Hour", "Weather Conditions",
                                          "Collision Types", "Vehicle Categories",
                                          "Speed Limit Distribution", "Accident Map"],
                        horizontal=True)

    if viz_type == "Accidents by Hour":
        carac['hour'] = carac['hrmn'].str.split(':').str[0].astype(int)
        hour_counts = carac['hour'].value_counts().sort_index()
        fig = px.bar(x=hour_counts.index, y=hour_counts.values,
                     labels={'x': 'Hour', 'y': 'Number of Accidents'},
                     title='Accidents by Hour of Day')
        fig.add_vline(x=8, line_dash="dash", line_color="green", annotation_text="Morning peak")
        fig.add_vline(x=17, line_dash="dash", line_color="red", annotation_text="Evening peak")
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Weather Conditions":
        labels = {1:'Normal',2:'Light rain',3:'Heavy rain',4:'Snow',5:'Fog',
                  6:'Strong wind',7:'Glare',8:'Cloudy',9:'Other'}
        vc = carac['atm'].value_counts().sort_index()
        vc.index = [labels.get(i, str(i)) for i in vc.index]
        fig = px.pie(values=vc.values, names=vc.index, title='Weather Conditions at Accident Time')
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Collision Types":
        labels = {-1:'Unknown',1:'Frontal',2:'Same direction',3:'Perpendicular',
                  4:'Opposite',5:'Chain',6:'Multiple',7:'Other',8:'None'}
        vc = carac['col'].value_counts().sort_index()
        vc.index = [labels.get(i, str(i)) for i in vc.index]
        fig = px.bar(x=vc.index, y=vc.values, title='Collision Types', color=vc.values,
                     color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Vehicle Categories":
        cat_col = vehicules.columns[5]
        vc = vehicules[cat_col].value_counts()
        fig = px.bar(x=vc.index, y=vc.values, title='Vehicle Categories',
                     color=vc.values, color_continuous_scale='plasma')
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Speed Limit Distribution":
        valid_vma = lieux[lieux['vma'].between(0, 150)]
        fig = px.histogram(valid_vma, x='vma', nbins=30,
                           title='Speed Limit Distribution (valid values)',
                           labels={'vma': 'Speed Limit (km/h)'})
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Accident Map":
        carac['lat_num'] = pd.to_numeric(carac['lat'].str.replace(',', '.'), errors='coerce')
        carac['long_num'] = pd.to_numeric(carac['long'].str.replace(',', '.'), errors='coerce')
        main_france = carac[(carac['lat_num'].between(41, 52)) &
                            (carac['long_num'].between(-5, 10))].sample(min(5000, len(carac)))
        fig = px.scatter_map(main_france, lat='lat_num', lon='long_num',
                             color='lum', opacity=0.5, zoom=5,
                             title='Accident Locations (mainland France, sampled)',
                             labels={'lum': 'Lighting'})
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Medallion Architecture")
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────────┐
    │                         BRONZE LAYER (Raw CSV)                      │
    ├─────────────────────────────────────────────────────────────────────┤
    │  caracteristiques_2024.csv   │   lieux_2024.csv   │  vehicules.csv │
    │  (Accident characteristics)  │  (Location details) │  (Vehicle info)│
    │  54,402 rows × 15 cols       │  70,248 rows × 18   │  83,730 × 7   │
    └───────────────────────────────┬─────────────────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        │   Data Quality Gates  │
                        │  ✓ Schema validation  │
                        │  ✓ Missing detection  │
                        │  ✓ Outlier removal    │
                        │  ✓ Format conversion  │
                        └───────────┬───────────┘
                                    │
    ┌───────────────────────────────┴─────────────────────────────────────┐
    │                    SILVER LAYER (Cleaned + Enriched)                 │
    ├─────────────────────────────────────────────────────────────────────┤
    │  silver_caracteristiques    │  silver_lieux      │ silver_vehicules │
    │  ├─ Coords standardized     │  ├─ lartpc dropped │ ├─ Age imputed  │
    │  ├─ Date/time built        │  ├─ v2 dropped     │ ├─ CNIT flagged │
    │  ├─ Time-of-day, season    │  ├─ vma capped     │ └─ Age capped   │
    │  └─ Day-of-week, weekend   │  └─ surf fixed     │                  │
    └───────────────────────────────┬─────────────────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        │  Star Schema Build    │
                        │  Fact + 8 Dimensions │
                        └───────────┬───────────┘
                                    │
    ┌───────────────────────────────┴─────────────────────────────────────┐
    │                     GOLD LAYER (Analytical Model)                   │
    ├─────────────────────────────────────────────────────────────────────┤
    │  Fact: f_accidents — 54,402 rows                                   │
    │  Dims: dim_date, dim_time, dim_location, dim_weather,              │
    │        dim_lighting, dim_collision_type, dim_road, dim_vehicle     │
    └───────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │               CONSUMPTION LAYER (BI Dashboards)                    │
    │  Power BI / Tableau / Streamlit — Hotspot maps, trends, KPIs      │
    └─────────────────────────────────────────────────────────────────────┘
    ```""")
    st.info("**Format:** Bronze=CSV → Silver=Parquet (partitioned by month) → Gold=Parquet (partitioned by year)")

with tab6:
    st.header("Full Report")
    with open(os.path.join(os.path.dirname(__file__), 'Rapport_Data_Integration_TP1.md'), 'r', encoding='utf-8') as f:
        report = f.read()
    st.markdown(report)
