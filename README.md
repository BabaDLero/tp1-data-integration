# TP Data Integration - French Road Safety Analysis (BAAC 2024)

**Dataset:** Accidents corporels de la circulation routière - France 2024  
**Source:** [data.gouv.fr](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)

## Project Structure

```
tp1/
├── streamlit_app.py              # Interactive dashboard
├── analysis.py                   # Data profiling script
├── Rapport_Data_Integration_TP1.md  # Full report
├── requirements.txt              # Python dependencies
├── .gitignore
├── data/
│   ├── caracteristiques_2024.csv  # Vehicle info (misnamed)
│   ├── vehicules_2024.csv         # Accident characteristics (misnamed)
│   ├── usagers_2024.csv           # Location details (misnamed)
│   ├── documentation_variables.pdf
│   └── fiche_baac.pdf
└── README.md
```

## Contents

1. **Data Profiling & Data Quality Analysis** - Column inventory, missing values, anomalies, duplicates
2. **Transformations Plan** - Silver layer standardization, cleaning, enrichment, deduplication
3. **Analytical Model** - Gold layer star schema (fact + 8 dimensions)
4. **Medallion Architecture** - Bronze → Silver → Gold → BI pipeline
5. **Interactive Dashboard** - Streamlit-based exploration

## How to Run

### Dashboard
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Analysis Script
```bash
python analysis.py
```
