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
    page_title="BAAC 2024 - Analyse Securite Routiere",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS: Dark/Light mode toggle, hover effects, modern UI ──
AUTHOR = "RIDARD Aurelien"

st.markdown(f"""
<style>
    /* Core theme variables */
    :root {{
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-card: #ffffff;
        --text-primary: #1a1a2e;
        --text-secondary: #495057;
        --border-color: #e9ecef;
        --accent: #4361ee;
        --accent-light: #eef0ff;
        --shadow: 0 2px 8px rgba(0,0,0,0.06);
        --shadow-hover: 0 8px 24px rgba(0,0,0,0.12);
    }}

    .main {{
        background-color: var(--bg-secondary);
    }}

    .block-container {{
        padding: 2rem 1.5rem !important;
        max-width: 1400px;
    }}

    /* Header */
    .app-header {{
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
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
    }}
    .app-header p {{
        font-size: 1rem;
        opacity: 0.85;
        margin: 0;
    }}
    .app-header .author {{
        font-size: 0.85rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }}

    /* Metric cards */
    .metric-card {{
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        cursor: default;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }}
    .metric-card .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent);
        margin: 0;
    }}
    .metric-card .metric-label {{
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.3rem;
    }}
    .metric-card .metric-detail {{
        font-size: 0.75rem;
        color: var(--text-secondary);
        opacity: 0.7;
        margin-top: 0.5rem;
        border-top: 1px solid var(--border-color);
        padding-top: 0.5rem;
    }}

    /* Section headers */
    .section-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--accent);
        margin-bottom: 1.5rem;
        margin-top: 1rem;
    }}

    /* Info cards */
    .info-card {{
        background: var(--accent-light);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid var(--accent);
        margin: 0.8rem 0;
        font-size: 0.9rem;
    }}

    /* Table styling */
    .dataframe {{
        font-size: 0.85rem !important;
    }}
    .dataframe thead tr th {{
        background-color: var(--accent) !important;
        color: white !important;
        padding: 0.5rem !important;
    }}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: var(--bg-card);
        padding: 0.3rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: var(--accent-light);
        transform: translateY(-1px);
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--accent) !important;
        color: white !important;
    }}

    /* Expander styling */
    .streamlit-expanderHeader {{
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }}
    .streamlit-expanderHeader:hover {{
        background: var(--accent-light) !important;
        transform: translateX(3px);
    }}

    /* Select box */
    .stSelectbox [data-baseweb="select"] {{
        border-radius: 8px !important;
    }}
    .stSelectbox [data-baseweb="select"]:hover {{
        border-color: var(--accent) !important;
    }}

    /* Buttons */
    .stButton button {{
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }}
    .stButton button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(67,97,238,0.3);
    }}

    /* Plotly chart container */
    .js-plotly-plot {{
        border-radius: 12px;
        background: var(--bg-card);
        padding: 0.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }}
    .js-plotly-plot:hover {{
        box-shadow: var(--shadow-hover);
    }}

    /* Status badges */
    .badge {{
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    .badge-critical {{ background: #fee2e2; color: #dc2626; }}
    .badge-high {{ background: #fef3c7; color: #d97706; }}
    .badge-medium {{ background: #dbeafe; color: #2563eb; }}
    .badge-low {{ background: #d1fae5; color: #059669; }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem 0 1rem 0;
        font-size: 0.8rem;
        color: var(--text-secondary);
        opacity: 0.6;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
    }}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:1rem 0">
        <div style="font-size:2rem;font-weight:700;color:var(--accent);">BAAC</div>
        <div style="font-size:0.85rem;color:var(--text-secondary);">2024</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("Actualiser les donnees", use_container_width=True):
        st.cache_data.clear()

    st.markdown("### A propos")
    st.markdown(f"""
    <div style="font-size:0.85rem;color:var(--text-secondary);">
    <strong>Analyse des accidents corporels</strong> de la circulation routiere en France (2024).<br><br>
    <strong>Auteur:</strong> {AUTHOR}<br>
    <strong>Source:</strong> data.gouv.fr<br>
    <strong>Dataset:</strong> BAAC 2005-2024
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Structure du pipeline")
    st.markdown("""
    <div style="font-size:0.8rem;">
    <span class="badge badge-medium">Bronze</span> CSV brut<br>
    <span class="badge badge-medium">Silver</span> Parquet nettoie<br>
    <span class="badge badge-medium">Gold</span> Modele analytique<br>
    <span class="badge badge-medium">BI</span> Dashboards
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ──
st.markdown(f"""
<div class="app-header">
    <h1>Analyse des Accidents de la Route - France 2024</h1>
    <p>Dataset BAAC : Profilage, Qualite des donnees, Architecture Medallion</p>
    <div class="author">Par {AUTHOR} | Data Integration TP | Juillet 2026</div>
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
    "Structure des donnees",
    "Valeurs manquantes",
    "Qualite des donnees",
    "Visualisations",
    "Architecture Medallion",
    "Rapport complet"
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1: DATA STRUCTURE
# ════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Inventaire des colonnes</div>', unsafe_allow_html=True)

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{carac.shape[0]:,}</div>
            <div class="metric-label">Accidents (caracteristiques)</div>
            <div class="metric-detail">{carac.shape[1]} colonnes</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{lieux.shape[0]:,}</div>
            <div class="metric-label">Troncons routiers (lieux)</div>
            <div class="metric-detail">{lieux.shape[1]} colonnes • {lieux['Num_Acc'].nunique():,} accidents lies</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{vehicules.shape[0]:,}</div>
            <div class="metric-label">Vehicules impliques</div>
            <div class="metric-detail">{vehicules.shape[1]} colonnes • {vehicules['Age_vehicule'].mean():.1f} ans moyen</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[3]:
        ratio = lieux.shape[0] / carac.shape[0]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{ratio:.2f}</div>
            <div class="metric-label">Troncons / Accident</div>
            <div class="metric-detail">Certains accidents couvrent plusieurs troncons</div>
        </div>
        """, unsafe_allow_html=True)

    for title, df, desc, rename_map in [
        ("Caracteristiques des accidents", carac,
         "Informations temporelles, meteorologiques et de localisation des accidents.",
         {'lat': 'Latitude', 'long': 'Longitude', 'lum': 'Eclairage', 'atm': 'Meteo',
          'col': 'Collision', 'agg': 'Agglomeration', 'int': 'Intersection',
          'hrmn': 'Heure', 'jour': 'Jour', 'mois': 'Mois', 'an': 'Annee',
          'dep': 'Departement', 'com': 'Commune', 'adr': 'Adresse'}),
        ("Details des lieux", lieux,
         "Caracteristiques detaillees de la voie et de l'environnement routier.",
         {'catr': 'CategorieRoute', 'voie': 'NomVoie', 'circ': 'Circulation',
          'nbv': 'NbVoies', 'vosp': 'VoieReservee', 'prof': 'Profil',
          'plan': 'Trace', 'surf': 'Surface', 'infra': 'Infrastructure',
          'situ': 'Situation', 'vma': 'VitesseMax', 'larrout': 'LargeurRoute',
          'pr': 'PR', 'pr1': 'PR1'}),
        ("Informations des vehicules", vehicules,
         "Details sur les vehicules impliques dans les accidents.",
         {'Lettre_Conventionnelle_Vehicule': 'LettreVehicule', 'Categorie_vehicule': 'Categorie',
          'Age_vehicule': 'Age', 'Territoire': 'Territoire', 'CNIT': 'NumChassis'})
    ]:
        with st.expander(f"{title} ({df.shape[1]} colonnes, {df.shape[0]:,} lignes)"):
            st.markdown(f'<div class="info-card">{desc}</div>', unsafe_allow_html=True)
            info = pd.DataFrame({
                'Colonne': df.columns,
                'Type': df.dtypes.astype(str).str.replace('int64','Entier').str.replace('float64','Decimal').str.replace('object','Texte'),
                'Valeurs non-nulles': df.shape[0] - df.isna().sum().values,
                '% Remplissage': (100 - df.isna().sum().values / df.shape[0] * 100).round(1),
                'Valeurs uniques': [df[c].nunique() for c in df.columns]
            })
            st.dataframe(info, use_container_width=True, hide_index=True,
                         column_config={
                             'Colonne': st.column_config.TextColumn(width='medium'),
                             'Type': st.column_config.TextColumn(width='small'),
                             '% Remplissage': st.column_config.ProgressColumn(format='%.1f%%', min_value=0, max_value=100)
                         })

# ════════════════════════════════════════════════════════════════════════
# TAB 2: MISSING VALUES
# ════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Analyse des valeurs manquantes</div>', unsafe_allow_html=True)

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
                    xaxis_title='% Valeurs manquantes',
                    height=250 + len(missing_pct) * 25,
                    margin=dict(l=10, r=30, t=40, b=10),
                    xaxis=dict(range=[0, min(105, missing_pct.max() * 1.2)]),
                    hovermode='y',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f'{name} : aucune valeur manquante')

    st.markdown('<div class="section-header">Matrice critique des valeurs manquantes</div>', unsafe_allow_html=True)
    st.markdown("""
    <table style="width:100%;border-collapse:collapse;font-size:0.9rem;">
        <thead>
            <tr style="background:#1a1a2e;color:white;">
                <th style="padding:0.6rem;text-align:left;">Colonne</th>
                <th style="padding:0.6rem;text-align:left;">Table</th>
                <th style="padding:0.6rem;text-align:right;">Manquants</th>
                <th style="padding:0.6rem;text-align:right;">%</th>
                <th style="padding:0.6rem;text-align:center;">Severite</th>
                <th style="padding:0.6rem;text-align:left;">Action recommandee</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">lartpc</td><td>lieux</td>
                <td style="text-align:right;">70,215</td><td style="text-align:right;color:#ef4444;font-weight:600;">99.95%</td>
                <td style="text-align:center;"><span class="badge badge-critical">CRITIQUE</span></td>
                <td>Supprimer la colonne (aucune valeur exploitable)</td>
            </tr>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">v2</td><td>lieux</td>
                <td style="text-align:right;">64,332</td><td style="text-align:right;color:#ef4444;font-weight:600;">91.58%</td>
                <td style="text-align:center;"><span class="badge badge-critical">CRITIQUE</span></td>
                <td>Supprimer ou archiver</td>
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
                <td>Enrichir par geocodage inverse</td>
            </tr>
            <tr style="border-bottom:1px solid #e9ecef;">
                <td style="padding:0.5rem;">Age vehicule</td><td>vehicules</td>
                <td style="text-align:right;">5,395</td><td style="text-align:right;color:#3b82f6;font-weight:600;">6.44%</td>
                <td style="text-align:center;"><span class="badge badge-medium">MOYEN</span></td>
                <td>Imputer par la mediane par categorie</td>
            </tr>
            <tr>
                <td style="padding:0.5rem;">adr</td><td>caracteristiques</td>
                <td style="text-align:right;">2,310</td><td style="text-align:right;color:#10b981;font-weight:600;">4.25%</td>
                <td style="text-align:center;"><span class="badge badge-low">FAIBLE</span></td>
                <td>Geocodage inverse depuis lat/long</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 3: DATA QUALITY
# ════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Controles de qualite</div>', unsafe_allow_html=True)

    q_cols = st.columns(3)
    with q_cols[0]:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label" style="font-size:0.9rem;font-weight:600;">Coordonnees geographiques</div>
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
            <div class="metric-label" style="font-size:0.9rem;font-weight:600;">Codes invalides</div>
        """, unsafe_allow_html=True)

        invalid_items = [
            ("col = -1", int((carac['col'] == -1).sum()), "#ef4444"),
            ("surf invalide (-1,8,9)", int(lieux['surf'].isin([-1, 8, 9]).sum()), "#ef4444"),
            ("vma = -1 (inconnu)", int((lieux['vma'] == -1).sum()), "#f59e0b"),
            ("vma > 150 (aberrant)", int((lieux['vma'] > 150).sum()), "#ef4444"),
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
            <div class="metric-label" style="font-size:0.9rem;font-weight:600;">Valeurs negatives</div>
        """, unsafe_allow_html=True)

        lieux['pr_num'] = pd.to_numeric(lieux['pr'], errors='coerce')
        lieux['pr1_num'] = pd.to_numeric(lieux['pr1'], errors='coerce')
        lieux['larrout_num'] = pd.to_numeric(lieux['larrout'], errors='coerce')

        neg_items = [
            ("pr (point de reference)", int((lieux['pr_num'] < 0).sum()), "#f59e0b"),
            ("pr1 (distance PR)", int((lieux['pr1_num'] < 0).sum()), "#f59e0b"),
            ("larrout (largeur route)", int((lieux['larrout_num'] < 0).sum()), "#ef4444"),
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
        <strong>Impact sur l'analyse :</strong> Les valeurs aberrantes (vma > 150, col = -1) doivent etre filtrees avant toute analyse.
        Les valeurs negatives de PR et PR1 codent une absence d'information et peuvent etre transformees en NaN.
        La largeur de route negative (69% des enregistrements) rend cette colonne inexploitable en l'etat.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Distributions categorielles</div>', unsafe_allow_html=True)
    col_cat = st.selectbox(
        "Selectionner une colonne categorielle",
        ['lum', 'atm', 'col', 'agg', 'int'],
        format_func=lambda x: {'lum': 'Eclairage', 'atm': 'Meteo', 'col': 'Collision',
                                'agg': 'Agglomeration', 'int': 'Intersection'}.get(x, x)
    )

    labels_map = {
        'lum': {1:'Plein jour', 2:'Crepuscule', 3:'Nuit sans eclairage',
                4:'Nuit eclairage allume', 5:'Nuit eclairage eteint'},
        'atm': {1:'Normale', 2:'Pluie legere', 3:'Pluie forte', 4:'Neige',
                5:'Brouillard', 6:'Vent fort', 7:'Eblouissement', 8:'Temps couvert', 9:'Autre'},
        'col': {-1:'Inconnu', 1:'Frontale', 2:'Meme sens', 3:'Perpendiculaire',
                4:'Oppose', 5:'En chaine', 6:'Multiples collisions', 7:'Autre', 8:'Sans collision'},
        'agg': {1:'Hors agglomeration', 2:'En agglomeration'},
        'int': {1:'Hors intersection', 2:'Croix', 3:'T', 4:'Y', 5:'Giratoire',
                6:'Place', 7:'Passage niveau', 8:'Autre', 9:'Non renseigne'}
    }

    if col_cat in carac.columns:
        vc = carac[col_cat].value_counts().sort_index()
        labels = labels_map.get(col_cat, {})
        vc.index = [labels.get(i, str(i)) for i in vc.index]
        total = vc.sum()
        vc_pct = (vc / total * 100).round(1)

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]],
                            subplot_titles=("Distribution (effectifs)", "Repartition (%)"))

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
        "Selectionner une visualisation",
        ["Accidents par heure", "Conditions meteorologiques",
         "Types de collision", "Categories de vehicules",
         "Limitations de vitesse", "Carte des accidents",
         "Repartition geographique", "Age des vehicules"],
        horizontal=True
    )

    if viz_type == "Accidents par heure":
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
            title='Accidents par heure de la journee',
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
                <div class="metric-label">Heure moyenne des accidents</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{peak_hour}h</div>
                <div class="metric-label">Heure de pic {hour_counts[peak_hour]:,} accidents</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{hour_counts.loc[7:9].sum():,}</div>
                <div class="metric-label">Accidents en heure de pointe matinale (7h-9h)</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{hour_counts.loc[16:19].sum():,}</div>
                <div class="metric-label">Accidents en heure de pointe soir (16h-19h)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "Conditions meteorologiques":
        labels = {1:'Normale', 2:'Pluie legere', 3:'Pluie forte', 4:'Neige',
                  5:'Brouillard', 6:'Vent fort', 7:'Eblouissement', 8:'Couvert', 9:'Autre'}
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
        fig.update_layout(height=450, title='Repartition par conditions meteorologiques', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        normal_pct = vc.iloc[0] / vc.sum() * 100
        st.markdown(f"""
        <div class="info-card">
            <strong>{normal_pct:.1f}%</strong> des accidents ont eu lieu par temps normal.
            Les conditions defavorables (pluie, brouillard, neige) representent <strong>{100 - normal_pct:.1f}%</strong> des accidents.
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "Types de collision":
        labels = {-1:'Inconnu', 1:'Frontale', 2:'Meme sens', 3:'Perpendiculaire',
                  4:'Oppose', 5:'En chaine', 6:'Multiples', 7:'Autre', 8:'Sans collision'}
        vc = carac['col'].value_counts().sort_index()
        vc.index = [labels.get(i, str(i)) for i in vc.index]

        fig = px.bar(
            x=vc.index, y=vc.values, color=vc.values,
            color_continuous_scale='turbo',
            labels={'x': 'Type de collision', 'y': "Nombre d'accidents"},
            title='Types de collision'
        )
        fig.update_traces(hovertemplate='%{x}<br>%{y} accidents<extra></extra>')
        fig.update_layout(height=450, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Categories de vehicules":
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

    elif viz_type == "Limitations de vitesse":
        valid_vma = lieux[lieux['vma'].between(0, 150)]
        invalid_vma = lieux[~lieux['vma'].between(0, 150)]

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "histogram"}, {"type": "box"}]],
            subplot_titles=("Distribution des vitesses maximales", "Box plot")
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
                <div class="metric-label">Vitesse limite la plus frequente</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{valid_vma['vma'].mean():.0f} km/h</div>
                <div class="metric-label">Vitesse limite moyenne</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-value">{invalid_vma.shape[0]:,}</div>
                <div class="metric-label">Troncons avec VMA invalide</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "Carte des accidents":
        st.markdown('<div class="info-card">Carte interactive des accidents en France metropolitaine (echantillon de 5 000 points pour la performance).</div>', unsafe_allow_html=True)

        map_filter = st.selectbox(
            "Filtrer par condition d'eclairage",
            ["Tous", "Plein jour", "Crepuscule", "Nuit sans eclairage",
             "Nuit eclairage allume", "Nuit eclairage eteint"]
        )
        lum_map = {"Tous": None, "Plein jour": 1, "Crepuscule": 2, "Nuit sans eclairage": 3,
                   "Nuit eclairage allume": 4, "Nuit eclairage eteint": 5}

        map_data = carac[carac['lat_num'].between(41, 52) & carac['long_num'].between(-5, 10)].copy()
        if lum_map[map_filter] is not None:
            map_data = map_data[map_data['lum'] == lum_map[map_filter]]

        map_data = map_data.dropna(subset=['lat_num', 'long_num'])
        sample_size = min(5000, len(map_data))
        if len(map_data) > sample_size:
            map_data = map_data.sample(sample_size)

        fig = px.scatter_map(
            map_data, lat='lat_num', lon='long_num',
            color='lum' if map_filter == "Tous" else None,
            opacity=0.6, zoom=5, height=600,
            title=f'Accidents 2024 - {map_filter} ({len(map_data):,} points)',
            labels={'lum': 'Eclairage'},
            color_continuous_scale=px.colors.sequential.Plasma if map_filter == "Tous" else None,
            hover_data={'Num_Acc': True, 'lat_num': False, 'long_num': False}
        )
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Repartition geographique":
        dept_counts = carac['dep'].value_counts().head(20)

        fig = px.bar(
            x=dept_counts.index, y=dept_counts.values,
            color=dept_counts.values,
            color_continuous_scale='magma',
            labels={'x': 'Departement', 'y': "Nombre d'accidents"},
            title='Top 20 des departements les plus accidentogenes'
        )
        fig.update_traces(hovertemplate='Dep %{x}<br>%{y} accidents<extra></extra>')
        fig.update_layout(height=450, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        urban_counts = carac['agg'].map({1: 'Hors agglomeration', 2: 'En agglomeration'}).value_counts()
        fig2 = px.pie(
            values=urban_counts.values, names=urban_counts.index,
            hole=0.4, title='Accidents en/hors agglomeration',
            color_discrete_sequence=['#4361ee', '#f59e0b']
        )
        fig2.update_traces(hovertemplate='%{label}: %{value} (%{percent})<extra></extra>')
        st.plotly_chart(fig2, use_container_width=True)

    elif viz_type == "Age des vehicules":
        age_col = 'Age_vehicule'
        valid_age = vehicules[vehicules[age_col].between(0, 50)].copy()

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "histogram"}, {"type": "box"}]],
                            subplot_titles=("Distribution de l'age des vehicules", "Box plot"))
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
            labels={'x': "Tranche d'age", 'y': 'Nombre de vehicules'},
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

    <div style="background:#fef3c7;border:2px solid #f59e0b;border-radius:12px;padding:1.5rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#92400e;margin-bottom:0.8rem;">COUCHE BRONZE - Donnees brutes</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;">
            <div style="background:white;border-radius:8px;padding:0.8rem;text-align:center;">
                <div style="font-weight:600;">caracteristiques.csv</div>
                <div style="font-size:0.8rem;color:#666;">54 402 lignes</div>
                <div style="font-size:0.8rem;color:#666;">15 colonnes</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;text-align:center;">
                <div style="font-weight:600;">lieux.csv</div>
                <div style="font-size:0.8rem;color:#666;">70 248 lignes</div>
                <div style="font-size:0.8rem;color:#666;">18 colonnes</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;text-align:center;">
                <div style="font-weight:600;">vehicules.csv</div>
                <div style="font-size:0.8rem;color:#666;">83 730 lignes</div>
                <div style="font-size:0.8rem;color:#666;">7 colonnes</div>
            </div>
        </div>
        <div style="text-align:center;margin-top:0.8rem;">
            <span class="badge badge-medium">Format: CSV</span>
            <span class="badge badge-medium">Stockage: /bronze/baac/2024/</span>
        </div>
    </div>

    <div style="display:flex;justify-content:center;">
        <div style="background:#1a1a2e;color:white;padding:0.6rem 1.5rem;border-radius:8px;font-size:0.85rem;">
            Controles de qualite : Schema validation | Detection valeurs manquantes | Suppression outliers | Conversion formats
        </div>
    </div>

    <div style="background:#dbeafe;border:2px solid #3b82f6;border-radius:12px;padding:1.5rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#1e40af;margin-bottom:0.8rem;">COUCHE SILVER - Donnees nettoyees et enrichies</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;">
            <div style="background:white;border-radius:8px;padding:0.8rem;">
                <div style="font-weight:600;">silver_caracteristiques</div>
                <div style="font-size:0.8rem;color:#666;">- Coordonnees standardisees</div>
                <div style="font-size:0.8rem;color:#666;">- Date complete construite</div>
                <div style="font-size:0.8rem;color:#666;">- Enrichi: heure, saison, jour_semaine</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;">
                <div style="font-weight:600;">silver_lieux</div>
                <div style="font-size:0.8rem;color:#666;">- Colonnes vides supprimees</div>
                <div style="font-size:0.8rem;color:#666;">- VMA corrigees (valeurs aberrantes)</div>
                <div style="font-size:0.8rem;color:#666;">- Codes surf normalises</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.8rem;">
                <div style="font-weight:600;">silver_vehicules</div>
                <div style="font-size:0.8rem;color:#666;">- Age impute par categorie</div>
                <div style="font-size:0.8rem;color:#666;">- Age plafonne a 50 ans</div>
                <div style="font-size:0.8rem;color:#666;">- CNIT flagge si manquant</div>
            </div>
        </div>
        <div style="text-align:center;margin-top:0.8rem;">
            <span class="badge badge-medium">Format: Parquet</span>
            <span class="badge badge-medium">Partitionne par: annee/mois</span>
        </div>
    </div>

    <div style="display:flex;justify-content:center;">
        <div style="background:#1a1a2e;color:white;padding:0.6rem 1.5rem;border-radius:8px;font-size:0.85rem;">
            Construction du modele en etoile : Tables de faits + Dimensions
        </div>
    </div>

    <div style="background:#d1fae5;border:2px solid #10b981;border-radius:12px;padding:1.5rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#065f46;margin-bottom:0.8rem;">COUCHE GOLD - Modele analytique (Star Schema)</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;">
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_date</strong><br>365 jours
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_time</strong><br>24 heures
            </div>
            <div style="background:white;border-radius:8px;padding:0.6rem;text-align:center;font-size:0.8rem;">
                <strong>dim_location</strong><br>Departements
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
            <strong>f_accidents</strong> (Table de faits) — 54 402 lignes<br>
            <span style="font-size:0.8rem;color:#666;">
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
            Consommation BI : Dashboards Power BI / Tableau / Streamlit
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
        st.warning("Rapport non trouve.")

# ── FOOTER ──
st.markdown(f"""
<div class="footer">
    BAAC 2024 - Analyse de donnees - {AUTHOR} |
    <a href="https://github.com/BabaDLero/tp1-data-integration" target="_blank">Voir sur GitHub</a> |
    Juillet 2026
</div>
""", unsafe_allow_html=True)
