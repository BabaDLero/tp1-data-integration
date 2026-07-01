import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="BAAC 2024 - Road Safety Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

AUTHOR = "RIDARD Aurelien"

# ── CUSTOM CSS: Dark theme only ──
bg_primary = "#0f1117"
bg_secondary = "#1a1d27"
bg_card = "#1e2130"
text_primary = "#e8eaed"
text_secondary = "#9aa0a6"
border_color = "#2d3040"
accent = "#6c8cff"
accent_light = "#1e2a4a"
header_grad = "linear-gradient(135deg, #0f1117 0%, #1a1d27 50%, #2d3040 100%)"
shadow = "0 2px 8px rgba(0,0,0,0.3)"
shadow_hover = "0 8px 24px rgba(0,0,0,0.5)"
table_header_bg = "#2d3040"
badge_crit_bg = "#3b1a1a"
badge_crit_fg = "#f87171"
badge_high_bg = "#3b2e1a"
badge_high_fg = "#fbbf24"
badge_med_bg = "#1a2a3b"
badge_med_fg = "#60a5fa"
badge_low_bg = "#1a2e1a"
badge_low_fg = "#34d399"

st.markdown(f"""
<style>
    .main {{
        background-color: {bg_secondary};
    }}

    .block-container {{
        padding: 2rem 1.5rem !important;
        max-width: 1400px;
    }}

    p, li, span, div, label {{
        color: {text_primary};
    }}

    .app-header {{
        background: {header_grad};
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
    }}
    .app-header h1 {{
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.5px;
        color: white;
    }}
    .app-header p {{
        font-size: 1rem;
        opacity: 0.85;
        margin: 0;
        color: #ccc;
    }}
    .app-header .author {{
        font-size: 0.85rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        color: #999;
    }}

    .metric-card {{
        background: {bg_card};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: {shadow};
        border: 1px solid {border_color};
        transition: all 0.3s ease;
        cursor: default;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: {shadow_hover};
    }}
    .metric-card .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {accent};
        margin: 0;
    }}
    .metric-card .metric-label {{
        font-size: 0.85rem;
        color: {text_secondary};
        margin-top: 0.3rem;
    }}
    .metric-card .metric-detail {{
        font-size: 0.75rem;
        color: {text_secondary};
        opacity: 0.7;
        margin-top: 0.5rem;
        border-top: 1px solid {border_color};
        padding-top: 0.5rem;
    }}

    .section-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {text_primary};
        padding-bottom: 0.5rem;
        border-bottom: 3px solid {accent};
        margin-bottom: 1.5rem;
        margin-top: 1rem;
    }}

    .info-card {{
        background: {accent_light};
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid {accent};
        margin: 0.8rem 0;
        font-size: 0.9rem;
        color: {text_primary};
    }}
    .info-card strong {{
        color: {accent};
    }}

    .stDataFrame {{
        background: {bg_card};
    }}
    .dataframe {{
        font-size: 0.85rem !important;
    }}
    .dataframe thead tr th {{
        background-color: {table_header_bg} !important;
        color: white !important;
        padding: 0.5rem !important;
    }}
    .dataframe tbody tr:nth-child(even) {{
        background-color: {bg_secondary} !important;
    }}
    .dataframe tbody tr {{
        background-color: {bg_card} !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: {bg_card};
        padding: 0.3rem;
        border-radius: 12px;
        border: 1px solid {border_color};
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.2s ease;
        color: {text_secondary};
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: {accent_light};
        transform: translateY(-1px);
        color: {accent};
    }}
    .stTabs [aria-selected="true"] {{
        background: {accent} !important;
        color: white !important;
    }}

    .streamlit-expanderHeader {{
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        background: {bg_card} !important;
        border: 1px solid {border_color} !important;
    }}
    .streamlit-expanderHeader:hover {{
        background: {accent_light} !important;
        transform: translateX(3px);
    }}

    .stSelectbox [data-baseweb="select"] {{
        border-radius: 8px !important;
        background: {bg_card} !important;
        border-color: {border_color} !important;
    }}
    .stSelectbox [data-baseweb="select"]:hover {{
        border-color: {accent} !important;
    }}

    .stButton button {{
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        background: {accent} !important;
        color: white !important;
        border: none !important;
    }}
    .stButton button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(108,140,255,0.4);
    }}

    .js-plotly-plot {{
        border-radius: 12px;
        background: {bg_card};
        padding: 0.5rem;
        box-shadow: {shadow};
        transition: all 0.3s ease;
    }}
    .js-plotly-plot:hover {{
        box-shadow: {shadow_hover};
    }}

    .badge {{
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    .badge-critical {{ background: {badge_crit_bg}; color: {badge_crit_fg}; }}
    .badge-high {{ background: {badge_high_bg}; color: {badge_high_fg}; }}
    .badge-medium {{ background: {badge_med_bg}; color: {badge_med_fg}; }}
    .badge-low {{ background: {badge_low_bg}; color: {badge_low_fg}; }}

    .footer {{
        text-align: center;
        padding: 2rem 0 1rem 0;
        font-size: 0.8rem;
        color: {text_secondary};
        opacity: 0.6;
        border-top: 1px solid {border_color};
        margin-top: 3rem;
    }}

    .stRadio label {{
        color: {text_primary} !important;
    }}
    .stRadio div[data-testid="stMarkdownContainer"] p {{
        color: {text_secondary} !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {text_primary} !important;
    }}

    .stSidebar .sidebar-content {{
        background: {bg_card};
    }}
    .stSidebar p, .stSidebar label, .stSidebar span {{
        color: {text_secondary};
    }}
    .stSidebar h3 {{
        color: {text_primary};
    }}

    /* ── Force dark mode & remove theme toggle ── */
    [data-testid="stThemeToggle"] {{
        display: none !important;
    }}
    [data-testid="stSettings"] {{
        display: none !important;
    }}
    .stApp {{
        background-color: {bg_secondary} !important;
    }}
    .stApp header {{
        background-color: {bg_card} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {bg_card} !important;
    }}
    section[data-testid="stMain"] {{
        background-color: {bg_secondary} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME (dark) ──
import plotly.io as pio
pio.templates.default = "plotly_dark"
# Also update all existing figures by setting the template globally

# ── SIDEBAR ──
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:1rem 0">
        <div style="font-size:2rem;font-weight:700;color:{accent};">BAAC</div>
        <div style="font-size:0.85rem;color:{text_secondary};">2024</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("Refresh data", use_container_width=True):
        st.cache_data.clear()

    st.markdown("### About")
    st.markdown(f"""
    <div style="font-size:0.85rem;color:{text_secondary};">
    <strong style="color:{text_primary};">Road accident analysis</strong> for France metropolitan and overseas territories (2024).<br><br>
    <strong style="color:{text_primary};">Author:</strong> {AUTHOR}<br>
    <strong style="color:{text_primary};">Source:</strong> data.gouv.fr<br>
    <strong style="color:{text_primary};">Dataset:</strong> BAAC 2005-2024
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Pipeline layers")
    st.markdown(f"""
    <div style="font-size:0.8rem;">
    <span class="badge badge-medium">Bronze</span> Raw CSV<br>
    <span class="badge badge-medium">Silver</span> Cleaned Parquet<br>
    <span class="badge badge-medium">Gold</span> Analytical model<br>
    <span class="badge badge-medium">BI</span> Dashboards
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ──
st.markdown(f"""
<div class="app-header">
    <h1>French Road Safety Analysis - 2024</h1>
    <p>BAAC Dataset: Profiling, Data Quality, Medallion Architecture</p>
    <div class="author">By {AUTHOR} | Data Integration TP | July 2026</div>
</div>
""", unsafe_allow_html=True)

# ── DATA LOADING ──
@st.cache_data(ttl=3600)
def load_data():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    carac = pd.read_csv(os.path.join(data_dir, 'vehicules_2024.csv'), sep=';', encoding='utf-8')
    lieux = pd.read_csv(os.path.join(data_dir, 'usagers_2024.csv'), sep=';', encoding='utf-8')
    vehicules = pd.read_csv(os.path.join(data_dir, 'caracteristiques_2024.csv'), sep=';', encoding='utf-8')

    # Rename columns to avoid encoding issues (use unicode normalization)
    import unicodedata
    def normalize_key(name):
        return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii').strip()

    def build_rename_map(df):
        rename = {}
        for c in df.columns:
            key = normalize_key(c)
            if 'Lettre Conventionnelle' in key or 'Lettre_Conventionnelle' in key:
                rename[c] = 'Lettre_Conventionnelle_Vehicule'
            elif 'Annee' in key or 'Ann' in key:
                rename[c] = 'Annee'
            elif 'Categorie' in key and 'vehicule' in key:
                rename[c] = 'Categorie_vehicule'
            elif 'Age' in key and 'vehicule' in key:
                rename[c] = 'Age_vehicule'
            elif 'Lieu Admin' in key or 'Territoire' in key:
                rename[c] = 'Territoire'
        return rename

    carac = carac.rename(columns=build_rename_map(carac))
    vehicules = vehicules.rename(columns=build_rename_map(vehicules))

    return carac, lieux, vehicules

carac, lieux, vehicules = load_data()

# Pre-compute derived fields
carac['lat_num'] = pd.to_numeric(carac['lat'].str.replace(',', '.'), errors='coerce')
carac['long_num'] = pd.to_numeric(carac['long'].str.replace(',', '.'), errors='coerce')
carac['hour'] = carac['hrmn'].str.split(':').str[0].astype(int, errors='ignore')
carac['hour'] = pd.to_numeric(carac['hour'], errors='coerce')

# ── TABS ──
tabs = st.tabs([
    "Data Structure",
    "Missing Values",
    "Data Quality",
    "Visualizations",
    "Medallion Architecture",
    "Full Report"
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1: DATA STRUCTURE
# ════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Column Inventory</div>', unsafe_allow_html=True)

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{carac.shape[0]:,}</div>
            <div class="metric-label">Accidents (characteristics)</div>
            <div class="metric-detail">{carac.shape[1]} colonnes</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{lieux.shape[0]:,}</div>
            <div class="metric-label">Road segments (lieux)</div>
            <div class="metric-detail">{lieux.shape[1]} colonnes • {lieux['Num_Acc'].nunique():,} accidents lies</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{vehicules.shape[0]:,}</div>
            <div class="metric-label">Vehicles involved</div>
            <div class="metric-detail">{vehicules.shape[1]} colonnes • {vehicules['Age_vehicule'].mean():.1f} ans moyen</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[3]:
        ratio = lieux.shape[0] / carac.shape[0]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{ratio:.2f}</div>
            <div class="metric-label">Segments / Accident</div>
            <div class="metric-detail">Some accidents span multiple road segments</div>
        </div>
        """, unsafe_allow_html=True)

    for title, df, desc, rename_map in [
        ("Accident characteristics", carac,
         "Informations temporelles, meteorologiques et de localisation des accidents.",
         {'lat': 'Latitude', 'long': 'Longitude', 'lum': 'Lighting', 'atm': 'Weather',
          'col': 'Collision', 'agg': 'Urban area', 'int': 'Intersection',
          'hrmn': 'Heure', 'jour': 'Jour', 'mois': 'Mois', 'an': 'Annee',
          'dep': 'Department', 'com': 'Commune', 'adr': 'Adresse'}),
        ("Location details", lieux,
         "Caracteristiques detaillees de la voie et de l'environnement routier.",
         {'catr': 'CategorieRoute', 'voie': 'NomVoie', 'circ': 'Circulation',
          'nbv': 'NbVoies', 'vosp': 'VoieReservee', 'prof': 'Profil',
          'plan': 'Trace', 'surf': 'Surface', 'infra': 'Infrastructure',
          'situ': 'Situation', 'vma': 'VitesseMax', 'larrout': 'LargeurRoute',
          'pr': 'PR', 'pr1': 'PR1'}),
        ("Vehicle information", vehicules,
         "Details sur les vehicules impliques dans les accidents.",
         {'Lettre_Conventionnelle_Vehicule': 'LettreVehicule', 'Categorie_vehicule': 'Categorie',
          'Age_vehicule': 'Age', 'Territoire': 'Territoire', 'CNIT': 'NumChassis'})
    ]:
        with st.expander(f"{title} ({df.shape[1]} colonnes, {df.shape[0]:,} lignes)"):
            st.markdown(f'<div class="info-card">{desc}</div>', unsafe_allow_html=True)
            info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str).str.replace('int64','Entier').str.replace('float64','Decimal').str.replace('object','Texte'),
                'Non-null count': df.shape[0] - df.isna().sum().values,
                '% Fill': (100 - df.isna().sum().values / df.shape[0] * 100).round(1),
                'Unique values': [df[c].nunique() for c in df.columns]
            })
            st.dataframe(info, use_container_width=True, hide_index=True,
                         column_config={
                             'Column': st.column_config.TextColumn(width='medium'),
                             'Type': st.column_config.TextColumn(width='small'),
                             '% Fill': st.column_config.ProgressColumn(format='%.1f%%', min_value=0, max_value=100)
                         })

# ════════════════════════════════════════════════════════════════════════
# TAB 2: MISSING VALUES
# ════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Missing Values Analysis</div>', unsafe_allow_html=True)

    col_missing = st.columns(2)
    tables_missing = [
        ("Caracteristiques", carac),
        ("Lieux", lieux),
        ("Vehicules", vehicules),
    ]
    for i, (name, df) in enumerate(tables_missing):
        with col_missing[i % 2]:
            missing_pct = (df.isna().sum() / len(df) * 100).round(2)
            missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=True)
            if len(missing_pct) > 0:
                colors = ['#ef4444' if v > 50 else '#f59e0b' if v > 10 else '#3b82f6' for v in missing_pct.values]
                fig = go.Figure(go.Bar(
                    x=missing_pct.values,
                    y=missing_pct.index,
                    orientation='h',
                    marker_color=colors,
                    text=[f'{v:.1f}%' for v in missing_pct.values],
                    textposition='outside',
                    hovertemplate='%{y}: %{x:.1f}% manquant<extra></extra>'
                ))
                fig.update_layout(
                    title=f'{name}',
                    xaxis_title='% Missing',
                    height=250 + len(missing_pct) * 25,
                    margin=dict(l=10, r=30, t=40, b=10),
                    xaxis=dict(range=[0, min(105, missing_pct.max() * 1.2)]),
                    hovermode='y',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f'{name} : no missing values')

    st.markdown('<div class="section-header">Critical Missingness Matrix</div>', unsafe_allow_html=True)
    st.markdown("""
    <table style="width:100%;border-collapse:collapse;font-size:0.9rem;">
        <thead>
            <tr style="background:#1a1a2e;color:white;">
                <th style="padding:0.6rem;text-align:left;">Column</th>
                <th style="padding:0.6rem;text-align:left;">Table</th>
                <th style="padding:0.6rem;text-align:right;">Manquants</th>
                <th style="padding:0.6rem;text-align:right;">%</th>
                <th style="padding:0.6rem;text-align:center;">Severity</th>
                <th style="padding:0.6rem;text-align:left;">Recommended action</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">lartpc</td><td>lieux</td>
                <td style="text-align:right;">70,215</td><td style="text-align:right;color:#ef4444;font-weight:600;">99.95%</td>
                <td style="text-align:center;"><span class="badge badge-critical">CRITIQUE</span></td>
                <td>Drop column (no usable data)</td>
            </tr>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">v2</td><td>lieux</td>
                <td style="text-align:right;">64,332</td><td style="text-align:right;color:#ef4444;font-weight:600;">91.58%</td>
                <td style="text-align:center;"><span class="badge badge-critical">CRITIQUE</span></td>
                <td>Drop or archive</td>
            </tr>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">CNIT (VIN)</td><td>vehicules</td>
                <td style="text-align:right;">20,028</td><td style="text-align:right;color:#f59e0b;font-weight:600;">23.92%</td>
                <td style="text-align:center;"><span class="badge badge-high">ELEVE</span></td>
                <td>Imputer par 'Inconnu'</td>
            </tr>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">voie</td><td>lieux</td>
                <td style="text-align:right;">13,331</td><td style="text-align:right;color:#f59e0b;font-weight:600;">18.98%</td>
                <td style="text-align:center;"><span class="badge badge-high">ELEVE</span></td>
                <td>Enrich via reverse geocoding</td>
            </tr>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">Age vehicule</td><td>vehicules</td>
                <td style="text-align:right;">5,395</td><td style="text-align:right;color:#3b82f6;font-weight:600;">6.44%</td>
                <td style="text-align:center;"><span class="badge badge-medium">MOYEN</span></td>
                <td>Impute by category median</td>
            </tr>
            <tr>
                <td style="padding:0.5rem;">adr</td><td>caracteristiques</td>
                <td style="text-align:right;">2,310</td><td style="text-align:right;color:#10b981;font-weight:600;">4.25%</td>
                <td style="text-align:center;"><span class="badge badge-low">FAIBLE</span></td>
                <td>Reverse geocode from lat/lng</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 3: DATA QUALITY
# ════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Quality Checks</div>', unsafe_allow_html=True)

    q_cols = st.columns(3)
    with q_cols[0]:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label" style="font-size:0.9rem;font-weight:600;">Geographic coordinates</div>
            <div style="margin-top:0.8rem;">
        """, unsafe_allow_html=True)

        fr_lat = carac[carac['lat_num'].between(41, 52)].shape[0]
        dom_lat = carac[~carac['lat_num'].between(41, 52)].shape[0]
        total_coords = carac['lat_num'].notna().sum()

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=fr_lat / total_coords * 100 if total_coords else 0,
            title={'text': "Coords en France metropolitaine"},
            delta={'reference': 90},
            gauge={
                'axis': {'range': [None, 100], 'tickvals': [0, 25, 50, 75, 100]},
                'bar': {'color': "#4361ee"},
                'steps': [
                    {'range': [0, 50], 'color': "#fee2e2"},
                    {'range': [50, 85], 'color': "#fef3c7"},
                    {'range': [85, 100], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 93
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
            <div style="font-size:0.8rem;margin-top:0.3rem;">
                France metropolitaine: <strong>{fr_lat:,}</strong> |
                DOM-TOM: <strong>{dom_lat:,}</strong> |
                Total: <strong>{total_coords:,}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with q_cols[1]:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label" style="font-size:0.9rem;font-weight:600;">Invalid codes</div>
        """, unsafe_allow_html=True)

        invalid_items = [
            ("col = -1", int((carac['col'] == -1).sum()), "#ef4444"),
            ("surf invalid (-1,8,9)", int(lieux['surf'].isin([-1, 8, 9]).sum()), "#ef4444"),
            ("vma = -1 (unknown)", int((lieux['vma'] == -1).sum()), "#f59e0b"),
            ("vma > 150 (outlier)", int((lieux['vma'] > 150).sum()), "#ef4444"),
        ]
        for label, val, color in invalid_items:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">
                <span style="font-size:0.85rem;">{label}</span>
                <span style="font-weight:600;color:{color};">{val:,}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with q_cols[2]:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label" style="font-size:0.9rem;font-weight:600;">Negative values</div>
        """, unsafe_allow_html=True)

        lieux['pr_num'] = pd.to_numeric(lieux['pr'], errors='coerce')
        lieux['pr1_num'] = pd.to_numeric(lieux['pr1'], errors='coerce')
        lieux['larrout_num'] = pd.to_numeric(lieux['larrout'], errors='coerce')

        neg_items = [
            ("pr (reference point)", int((lieux['pr_num'] < 0).sum()), "#f59e0b"),
            ("pr1 (PR distance)", int((lieux['pr1_num'] < 0).sum()), "#f59e0b"),
            ("larrout (road width)", int((lieux['larrout_num'] < 0).sum()), "#ef4444"),
            ("Age vehicule < 0", 0, "#10b981"),
        ]
        for label, val, color in neg_items:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #f0f0f0;">
                <span style="font-size:0.85rem;">{label}</span>
                <span style="font-weight:600;color:{color};">{val:,}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <strong>Impact on analysis:</strong> Les valeurs aberrantes (vma > 150, col = -1) doivent etre filtrees avant toute analyse.
        Les valeurs negatives de PR et PR1 codent une absence d'information et peuvent etre transformees en NaN.
        La largeur de route negative (69% des enregistrements) rend cette colonne inexploitable en l'etat.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Categorical Distributions</div>', unsafe_allow_html=True)
    col_cat = st.selectbox(
        "Select a categorical column",
        ['lum', 'atm', 'col', 'agg', 'int'],
        format_func=lambda x: {'lum': 'Lighting', 'atm': 'Weather', 'col': 'Collision',
                                'agg': 'Urban area', 'int': 'Intersection'}.get(x, x)
    )

    labels_map = {
        'lum': {1:'Daylight', 2:'Twilight', 3:'Night no lighting',
                4:'Night lighting on', 5:'Night lighting off'},
        'atm': {1:'Normale', 2:'Light rain', 3:'Heavy rain', 4:'Snow',
                5:'Fog', 6:'Strong wind', 7:'Glare', 8:'Cloudy', 9:'Autre'},
        'col': {-1:'Inconnu', 1:'Frontal', 2:'Same direction', 3:'Perpendicular',
                4:'Opposite', 5:'Chain', 6:'Multiple collisions', 7:'Autre', 8:'No collision'},
        'agg': {1:'Outside urban area', 2:'Inside urban area'},
        'int': {1:'Not intersection', 2:'Cross', 3:'T', 4:'Y', 5:'Roundabout',
                6:'Square', 7:'Level crossing', 8:'Autre', 9:'Not specified'}
    }

    if col_cat in carac.columns:
        vc = carac[col_cat].value_counts().sort_index()
        labels = labels_map.get(col_cat, {})
        vc.index = [labels.get(i, str(i)) for i in vc.index]
        total = vc.sum()
        vc_pct = (vc / total * 100).round(1)

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]],
                            subplot_titles=("Distribution (counts)", "Share (%)"))

        fig.add_trace(go.Bar(
            x=vc.index, y=vc.values,
            marker_color=px.colors.sequential.Viridis[:len(vc)],
            text=vc.values, textposition='outside',
            hovertemplate='%{x}<br>Effectif: %{y}<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Pie(
            labels=vc.index, values=vc.values,
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='%{label}<br>%{value} accidents (%{percent})<extra></extra>'
        ), row=1, col=2)

        fig.update_layout(
            height=400,
            margin=dict(t=40, b=10, l=10, r=10),
            showlegend=False,
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 4: VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Exploration visuelle</div>', unsafe_allow_html=True)

    viz_type = st.radio(
        "Select a visualization",
        ["Accidents by Hour", "Weather Conditions",
         "Collision Types", "Vehicle Categories",
         "Speed Limits", "Accident Map",
         "Geographic Distribution", "Vehicle Age"],
        horizontal=True
    )

    if viz_type == "Accidents by Hour":
        carac['hour'] = pd.to_numeric(carac['hour'], errors='coerce')
        hour_counts = carac['hour'].value_counts().sort_index().reindex(range(24), fill_value=0)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hour_counts.index,
            y=hour_counts.values,
            marker_color=['#ef4444' if 7 <= h <= 9 or 16 <= h <= 19 else '#3b82f6' for h in hour_counts.index],
            hovertemplate='Heure: %{x}h<br>Accidents: %{y}<extra></extra>'
        ))
        fig.add_vline(x=8, line_dash="dash", line_color="#10b981",
                      annotation_text="Pic matinal (8h)", annotation_position="top left")
        fig.add_vline(x=17, line_dash="dash", line_color="#f59e0b",
                      annotation_text="Pic soir (17h)", annotation_position="top right")
        fig.update_layout(
            title='Accidents by Hour de la journee',
            xaxis=dict(tickmode='linear', tick0=0, dtick=2, title='Heure'),
            yaxis=dict(title="Nombre d'accidents"),
            height=450,
            hovermode='x',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

        avg_hour = carac['hour'].mean()
        peak_hour = hour_counts.idxmax()
        st.markdown(f"""
        <div style="display:flex;gap:1rem;flex-wrap:wrap;">
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{avg_hour:.1f}h</div>
                <div class="metric-label">Average accident hour</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{peak_hour}h</div>
                <div class="metric-label">Peak hour {hour_counts[peak_hour]:,} accidents</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{hour_counts.loc[7:9].sum():,}</div>
                <div class="metric-label">Morning peak accidents (7-9 AM)</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{hour_counts.loc[16:19].sum():,}</div>
                <div class="metric-label">Evening peak accidents (4-7 PM)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "Weather Conditions":
        labels = {1:'Normale', 2:'Light rain', 3:'Heavy rain', 4:'Snow',
                  5:'Fog', 6:'Strong wind', 7:'Glare', 8:'Couvert', 9:'Autre'}
        vc = carac['atm'].value_counts().sort_index()
        vc.index = [labels.get(i, str(i)) for i in vc.index]

        colors = ['#10b981', '#60a5fa', '#3b82f6', '#e2e8f0', '#94a3b8',
                  '#f59e0b', '#fbbf24', '#64748b', '#cbd5e1']

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
        fig.add_trace(go.Pie(
            labels=vc.index, values=vc.values, hole=0.4,
            marker=dict(colors=colors[:len(vc)]),
            textinfo='percent',
            hovertemplate='%{label}: %{value} accidents (%{percent})<extra></extra>'
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=vc.values, y=vc.index, orientation='h',
            marker_color=colors[:len(vc)],
            text=vc.values, textposition='outside',
            hovertemplate='%{y}: %{x} accidents<extra></extra>'
        ), row=1, col=2)
        fig.update_layout(height=450, title='Distribution by Weather Conditions', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        normal_pct = vc.iloc[0] / vc.sum() * 100
        st.markdown(f"""
        <div class="info-card">
            <strong>{normal_pct:.1f}%</strong> des accidents ont eu lieu par temps normal.
            Les conditions defavorables (pluie, brouillard, neige) representent <strong>{100 - normal_pct:.1f}%</strong> des accidents.
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "Collision Types":
        labels = {-1:'Inconnu', 1:'Frontal', 2:'Same direction', 3:'Perpendicular',
                  4:'Opposite', 5:'Chain', 6:'Multiples', 7:'Autre', 8:'No collision'}
        vc = carac['col'].value_counts().sort_index()
        vc.index = [labels.get(i, str(i)) for i in vc.index]

        fig = px.bar(
            x=vc.index, y=vc.values, color=vc.values,
            color_continuous_scale='turbo',
            labels={'x': 'Type de collision', 'y': "Nombre d'accidents"},
            title='Collision Types'
        )
        fig.update_traces(hovertemplate='%{x}<br>%{y} accidents<extra></extra>')
        fig.update_layout(height=450, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Vehicle Categories":
        cat_col = 'Categorie_vehicule'
        vc = vehicules[cat_col].value_counts()
        colors = px.colors.qualitative.Plotly[:len(vc)]

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]],
                            subplot_titles=("Effectifs", "Repartition"))
        fig.add_trace(go.Bar(
            x=vc.index, y=vc.values, marker_color=colors,
            text=vc.values, textposition='outside',
            hovertemplate='%{x}<br>%{y} vehicules<extra></extra>'
        ), row=1, col=1)
        fig.add_trace(go.Pie(
            labels=vc.index, values=vc.values, hole=0.4,
            marker=dict(colors=colors),
            textinfo='percent',
            hovertemplate='%{label}: %{value}<extra></extra>'
        ), row=1, col=2)
        fig.update_layout(height=450, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Speed Limits":
        valid_vma = lieux[lieux['vma'].between(0, 150)]
        invalid_vma = lieux[~lieux['vma'].between(0, 150)]

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "histogram"}, {"type": "box"}]],
            subplot_titles=("Speed Limit Distribution", "Box plot")
        )
        fig.add_trace(go.Histogram(
            x=valid_vma['vma'], nbinsx=30,
            marker_color='#4361ee',
            hovertemplate='%{x} km/h: %{y} troncons<extra></extra>'
        ), row=1, col=1)
        fig.add_trace(go.Box(
            y=valid_vma['vma'], name='VMA',
            marker_color='#4361ee',
            boxmean='sd',
            hovertemplate='%{y} km/h<extra></extra>'
        ), row=1, col=2)
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div style="display:flex;gap:1rem;flex-wrap:wrap;">
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{valid_vma['vma'].mode().values[0]} km/h</div>
                <div class="metric-label">Most common speed limit</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{valid_vma['vma'].mean():.0f} km/h</div>
                <div class="metric-label">Average speed limit</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{invalid_vma.shape[0]:,}</div>
                <div class="metric-label">Segments with invalid VMA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "Accident Map":
        st.markdown('<div class="info-card">Carte interactive des accidents en France metropolitaine (echantillon de 5 000 points pour la performance).</div>', unsafe_allow_html=True)

        map_filter = st.selectbox(
            "Filter by lighting condition",
            ["All", "Daylight", "Twilight", "Night no lighting",
             "Night lighting on", "Night lighting off"]
        )
        lum_map = {"All": None, "Daylight": 1, "Twilight": 2, "Night no lighting": 3,
                   "Night lighting on": 4, "Night lighting off": 5}

        map_data = carac[carac['lat_num'].between(41, 52) & carac['long_num'].between(-5, 10)].copy()
        if lum_map[map_filter] is not None:
            map_data = map_data[map_data['lum'] == lum_map[map_filter]]

        map_data = map_data.dropna(subset=['lat_num', 'long_num'])
        sample_size = min(5000, len(map_data))
        if len(map_data) > sample_size:
            map_data = map_data.sample(sample_size)

        fig = px.scatter_map(
            map_data, lat='lat_num', lon='long_num',
            color='lum' if map_filter == "All" else None,
            opacity=0.6, zoom=5, height=600,
            title=f'Accidents 2024 - {map_filter} ({len(map_data):,} points)',
            labels={'lum': 'Lighting'},
            color_continuous_scale=px.colors.sequential.Plasma if map_filter == "All" else None,
            hover_data={'Num_Acc': True, 'lat_num': False, 'long_num': False}
        )
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Geographic Distribution":
        dept_counts = carac['dep'].value_counts().head(20)

        fig = px.bar(
            x=dept_counts.index, y=dept_counts.values,
            color=dept_counts.values,
            color_continuous_scale='magma',
            labels={'x': 'Department', 'y': "Nombre d'accidents"},
            title='Top 20 most accident-prone departments'
        )
        fig.update_traces(hovertemplate='Dep %{x}<br>%{y} accidents<extra></extra>')
        fig.update_layout(height=450, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        urban_counts = carac['agg'].map({1: 'Outside urban area', 2: 'Inside urban area'}).value_counts()
        fig2 = px.pie(
            values=urban_counts.values, names=urban_counts.index,
            hole=0.4, title='Inside/Outside Urban Area',
            color_discrete_sequence=['#4361ee', '#f59e0b']
        )
        fig2.update_traces(hovertemplate='%{label}: %{value} (%{percent})<extra></extra>')
        st.plotly_chart(fig2, use_container_width=True)

    elif viz_type == "Vehicle Age":
        age_col = 'Age_vehicule'
        valid_age = vehicules[vehicules[age_col].between(0, 50)].copy()

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "histogram"}, {"type": "box"}]],
                            subplot_titles=("Vehicle Age Distribution", "Box plot"))
        fig.add_trace(go.Histogram(
            x=valid_age[age_col], nbinsx=40,
            marker_color='#4361ee',
            hovertemplate='%{x} ans: %{y} vehicules<extra></extra>'
        ), row=1, col=1)
        fig.add_trace(go.Box(
            y=valid_age[age_col], name='Age vehicule',
            marker_color='#f59e0b', boxmean='sd',
            hovertemplate='%{y} ans<extra></extra>'
        ), row=1, col=2)
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        age_groups = pd.cut(valid_age[age_col], bins=[0, 2, 5, 10, 20, 50],
                            labels=['0-2 ans', '3-5 ans', '6-10 ans', '11-20 ans', '20+ ans'])
        age_dist = age_groups.value_counts().sort_index()
        fig2 = px.bar(
            x=age_dist.index, y=age_dist.values,
            color=age_dist.values, color_continuous_scale='viridis',
            labels={'x': "Age range", 'y': 'Number of vehicles'},
            title='Repartition par tranche d\'age des vehicules'
        )
        fig2.update_layout(height=400, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 5: MEDALLION ARCHITECTURE
# ════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Architecture Medallion (Bronze - Silver - Gold)</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:1rem;font-family:monospace;">

    <div style="background:#fde4cc;border:2px solid #b45309;border-radius:12px;padding:1.5rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#0d2137;margin-bottom:0.8rem;">BRONZE LAYER - Raw data</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;">
            <div style="background:white;border-radius:8px;padding:0.8rem;text-align:center;">
                <div style="font-weight:600;">caracteristiques.csv</div>
                <div style="font-size:0.8rem;color:#0d2137;">54 402 lignes</div>
                <div style="font-size:0.8rem;color:#0d2137;">15 colonnes</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;text-align:center;">
                <div style="font-weight:600;">lieux.csv</div>
                <div style="font-size:0.8rem;color:#0d2137;">70 248 lignes</div>
                <div style="font-size:0.8rem;color:#0d2137;">18 colonnes</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;text-align:center;">
                <div style="font-weight:600;">vehicules.csv</div>
                <div style="font-size:0.8rem;color:#0d2137;">83 730 lignes</div>
                <div style="font-size:0.8rem;color:#0d2137;">7 colonnes</div>
            </div>
        </div>
        <div style="text-align:center;margin-top:0.8rem;">
            <span class="badge badge-medium">Format: CSV</span>
            <span class="badge badge-medium">Storage: /bronze/baac/2024/</span>
        </div>
    </div>

    <div style="display:flex;justify-content:center;">
        <div style="background:#1a1a2e;color:white;padding:0.6rem 1.5rem;border-radius:8px;font-size:0.85rem;">
            Quality Checks : Schema validation | Detection valeurs manquantes | Suppression outliers | Conversion formats
        </div>
    </div>

    <div style="background:#f1f5f9;border:2px solid #64748b;border-radius:12px;padding:1.5rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#0d2137;margin-bottom:0.8rem;">SILVER LAYER - Cleaned and enriched</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;">
            <div style="background:white;border-radius:8px;padding:0.8rem;">
                <div style="font-weight:600;">silver_caracteristiques</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Coordinates standardized</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Date complete construite</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Enriched: hour, season, weekday</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;">
                <div style="font-weight:600;">silver_lieux</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Columns vides supprimees</div>
                <div style="font-size:0.8rem;color:#0d2137;">- VMA corrected (outliers)</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Codes surf normalises</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;">
                <div style="font-weight:600;">silver_vehicules</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Age imputed by category</div>
                <div style="font-size:0.8rem;color:#0d2137;">- Age capped at 50</div>
                <div style="font-size:0.8rem;color:#0d2137;">- CNIT flagge si manquant</div>
            </div>
        </div>
        <div style="text-align:center;margin-top:0.8rem;">
            <span class="badge badge-medium">Format: Parquet</span>
            <span class="badge badge-medium">Partitionne par: annee/mois</span>
        </div>
    </div>

    <div style="display:flex;justify-content:center;">
        <div style="background:#1a1a2e;color:white;padding:0.6rem 1.5rem;border-radius:8px;font-size:0.85rem;">
            Star schema: Fact tables + Dimensions
        </div>
    </div>

    <div style="background:#fef9c3;border:2px solid #eab308;border-radius:12px;padding:1.5rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#0d2137;margin-bottom:0.8rem;">GOLD LAYER - Analytical model (Star Schema)</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;">
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_date</strong><br>365 jours
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_time</strong><br>24 heures
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_location</strong><br>Departments
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_weather</strong><br>9 conditions
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_lighting</strong><br>5 eclairages
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_collision</strong><br>8 types
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_road</strong><br>Profils route
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_vehicle</strong><br>Categories
            </div>
        </div>
        <div style="background:white;border-radius:8px;padding:1rem;margin-top:0.8rem;text-align:center;">
            <strong>f_accidents</strong> (Fact table) — 54 402 lignes<br>
            <span style="font-size:0.8rem;color:#0d2137;">
            Keys: date_key + time_key + location_key + weather_key + lighting_key + collision_key + road_key<br>
            Measures: vehicle_count, severity_index
            </span>
        </div>
        <div style="text-align:center;margin-top:0.8rem;">
            <span class="badge badge-medium">Format: Parquet</span>
            <span class="badge badge-medium">Partitionne par: annee</span>
        </div>
    </div>

    <div style="display:flex;justify-content:center;">
        <div style="background:#1a1a2e;color:white;padding:0.6rem 1.5rem;border-radius:8px;font-size:0.85rem;">
            BI: Power BI / Tableau / Streamlit dashboards
        </div>
    </div>

    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 6: FULL REPORT
# ════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Rapport complet d\'analyse</div>', unsafe_allow_html=True)
    report_path = os.path.join(os.path.dirname(__file__), 'Rapport_Data_Integration_TP1.md')
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            report = f.read()
        st.markdown(report)
    else:
        st.warning("Report not found.")

# ── FOOTER ──
st.markdown(f"""
<div class="footer">
    BAAC 2024 - Data Analysis - {AUTHOR} |
    <a href="https://github.com/BabaDLero/tp1-data-integration" target="_blank">Voir sur GitHub</a> |
    Juillet 2026
</div>
""", unsafe_allow_html=True)
