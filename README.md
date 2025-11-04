pdf_text_analytics_app/
│
├── app.py                             # Main Streamlit entry point
│
├── components/                        # Streamlit UI components (modular views)
│   ├── pdf_viewer.py                  # Renders the PDF file in the app
│   ├── text_viewer.py                 # Shows extracted text (paged)
│   ├── pagination_controls.py         # Navigation buttons, page slider, etc.
│   ├── upload_panel.py                # File upload logic (PDF + CSV)
│   ├── sidebar_settings.py            # Font size, theme, layout toggles
│   ├── extraction_quality.py          # Heatmap + completeness visualization
│   ├── keyword_visuals.py             # Keyword search + frequency heatmap
│   ├── wordcloud_visuals.py           # Page-level and full-doc word clouds
│   ├── ner_visuals.py                 # Named Entity Recognition highlight view
│   ├── sentiment_visuals.py           # Sentiment trendlines
│   ├── topic_visuals.py               # Topic modeling (LDA/BERTopic)
│   ├── similarity_visuals.py          # Embedding clustering + similarity maps
│   ├── comparison_view.py             # OCR–NLP text comparison diff
│   ├── dashboard_summary.py           # Combined analytics dashboard
│   ├── report_generator.py            # Exports analytics as HTML/PDF
│   └── annotation_panel.py            # (Later) interactive text corrections
│
├── utils/                             # Helper functions, utilities
│   ├── data_loader.py                 # Load CSV, parse PDF, validate files
│   ├── state_manager.py               # Manage session state (current page, prefs)
│   ├── visuals.py                     # Shared visualization helpers (Altair, Plotly)
│   ├── text_processing.py             # Tokenization, keyword counting, etc.
│   ├── ner_utils.py                   # Entity extraction helpers (spaCy)
│   ├── sentiment_utils.py             # Sentiment analysis functions
│   ├── topic_utils.py                 # Topic modeling pipeline
│   ├── similarity_utils.py            # Embedding + clustering helpers
│   ├── export_utils.py                # Save/export CSV/JSON/HTML reports
│   └── layout_utils.py                # Layout, spacing, and theme utilities
│

│
├── models/                            # (Optional) ML/NLP models
│   ├── spacy_model/                   # Cached spaCy model for NER
│   ├── sentiment_model/               # Finetuned transformer (if used)
│   └── topic_model/                   # BERTopic/LDA model artifacts
│
├── assets/                            # Static assets for UI (icons, CSS, etc.)
│   ├── styles.css
│   └── icons/
│
└── requirements.txt                   # Python dependencies

│
├── data/                              # Local demo data
│   ├── sample.pdf
│   ├── sample_text.csv
│   └── demo_results/                  # Cached analytics and results

│   ├── documents/                          # All PDF files live here
│   │   ├── report_a.pdf
│   │   ├── report_b.pdf
│   │   ├── esg_policy.pdf
│   │   └── research_study.pdf
│   │
│   ├── extracted_text/                     # Corresponding CSVs for each PDF
│   │   ├── report_a_text.csv
│   │   ├── report_b_text.csv
│   │   ├── esg_policy_text.csv
│   │   └── research_study_text.csv
│   │
│   ├── analytics_cache/                    # Optional: precomputed visualizations, embeddings, etc.
│   │   ├── report_a_summary.json
│   │   ├── esg_policy_topics.json
│   │   └── embeddings.pkl
│   │
│   └── metadata/                           # Optional: global or per-document metadata
│       ├── documents_overview.csv
│       └── extraction_config.json

| Folder                  | Purpose                           | Example Files                              |
| ----------------------- | --------------------------------- | ------------------------------------------ |
| `data/documents/`       | Original PDFs                     | `report_a.pdf`, `esg_policy.pdf`           |
| `data/extracted_text/`  | Page-level extracted text (CSV)   | `report_a_text.csv`, `esg_policy_text.csv` |
| `data/analytics_cache/` | Cached embeddings, JSON summaries | `report_a_summary.json`                    |
| `data/metadata/`        | Document metadata and configs     | `documents_overview.csv`, `config.json`    |


Schema for sample_text.csv

page_number,extracted_text,char_count,word_count,confidence,sentiment,dominant_topic,entities,keywords
1,"Climate change poses significant risks to financial stability. The European Union’s Green Deal emphasizes carbon neutrality by 2050.",156,22,0.97,0.45,"Climate Policy","ORG:European Union;POLICY:Green Deal","climate,green deal,carbon neutrality"
2,"Companies must disclose ESG-related risks and impacts in their annual sustainability reports.",109,15,0.91,0.10,"Corporate Reporting","ORG:Companies;CONCEPT:ESG","esg,risk,disclosure"
3,"The transition to renewable energy requires policy alignment across regions and industries.",118,17,0.95,0.52,"Energy Transition","SECTOR:Energy;CONCEPT:Renewable","renewable,policy,alignment"

| Column Name      | Type   | Description                                           |
| ---------------- | ------ | ----------------------------------------------------- |
| `page_number`    | int    | Page index starting from 1                            |
| `extracted_text` | string | Full extracted text for that page                     |
| `char_count`     | int    | Length of extracted text (helps detect missing pages) |
| `word_count`     | int    | Count of words in extracted text                      |
| `confidence`     | float  | Extraction confidence (0–1 or 0–100)                  |
| `sentiment`      | float  | Sentiment score (−1 = negative, +1 = positive)        |
| `dominant_topic` | string | Main topic assigned via topic modeling                |
| `entities`       | string | JSON or semicolon-separated list of NER entities      |
| `keywords`       | string | Comma-separated top keywords (optional)               |

Schema for data/metadata/documents_overview.csv
🧠 3. Optional: Metadata File for Tracking (Optional But Very Useful)

| document_name      | pages | processed_date | model_version | avg_confidence | source         |
| ------------------ | ----- | -------------- | ------------- | -------------- | -------------- |
| report_a.pdf       | 12    | 2025-10-28     | v1.0          | 0.94           | local          |
| esg_policy.pdf     | 8     | 2025-11-01     | v1.2          | 0.91           | EU Database    |
| research_study.pdf | 15    | 2025-11-03     | v1.1          | 0.88           | Kaggle Dataset |
# esg_dashboard
