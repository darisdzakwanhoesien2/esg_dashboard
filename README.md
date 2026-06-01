# esg_dashboard

Streamlit app for viewing a PDF alongside page-level extracted text (CSV) and a small analytics dashboard.

## What was wrong (bugs / broken logic)

- `components/pagination_controls.py` hard-coded `total_pages = 10`, so navigation could show pages that don't exist and hide pages that do.
- `components/text_viewer.py` re-read the uploaded CSV on every rerun; Streamlit reruns often, so this causes avoidable latency.
- `app.py` used `csv_file.seek(0)` repeatedly to work around re-reading behavior; this is fragile and unnecessary once reads are cached.
- `utils/data_loader.py` assumed data directories always exist and used brittle matching logic for PDFs ↔ CSVs.
- `components/keyword_visuals.py` and `components/wordcloud_visuals.py` had formatting issues and placeholder output.

## Fixes & cleanup (what changed and why)

- **Correct pagination**: `app.py` now derives `total_pages` from the CSV’s `page_number` max and passes it into `pagination_controls.render(total_pages=...)`.
- **Cached CSV parsing**: `components/text_viewer.py` adds `@st.cache_data` loader keyed by uploaded file bytes to avoid repeated parsing.
- **Safer navigation state**: `components/pagination_controls.py` clamps `current_page` when `total_pages` changes (e.g., after uploading a new document).
- **More robust data helpers**: `utils/data_loader.py` now returns an empty list if the expected directories are missing, matches PDFs to `*_text.csv` reliably, and validates that both PDF and CSV exist.
- **Packaging reliability**: added `components/__init__.py` and `utils/__init__.py` to make imports behave consistently across environments.
- **Small UX improvements**: `components/upload_panel.py` now rejects empty CSV uploads early; unimplemented visuals show an explicit info message.

## Requirements

- Python 3.12+
- Dependencies in `requirements.txt`

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Data format (CSV)

Required columns:

- `page_number` (int, starting at 1)
- `extracted_text` (string)

Other columns are allowed and ignored by the current UI.

---

## Project Overview

`esg_dashboard` is a Streamlit dashboard that lets you:

- Upload a PDF report
- Upload a corresponding page-level extracted-text CSV
- Page through extracted text while viewing the PDF
- View a simple “Analytics Dashboard” area (some tabs are currently placeholders)

Problem it solves: when you have OCR / extraction output in a CSV, it’s hard to QA it against the source PDF page-by-page. This app provides a lightweight review UI and a place to add analytics modules.

## Tech Stack

- **Language**: Python 3.12+
- **App framework**: Streamlit
- **Data handling**: pandas
- **Visualization libraries** (declared in `requirements.txt`):
  - Plotly
  - Altair
- **PDF tooling** (declared in `requirements.txt`):
  - PyMuPDF
- **NLP / ML tooling** (declared in `requirements.txt`; not fully implemented in the current UI):
  - spaCy
  - sentence-transformers
  - scikit-learn
- **Other utilities** (declared in `requirements.txt`; usage may be added by future components):
  - wordcloud
  - textdistance
  - weasyprint

## Architecture Overview

High-level flow:

1. `app.py` is the Streamlit entry point. It sets up the page, sidebar controls, and the two-column layout (PDF viewer + text viewer).
2. `components/upload_panel.py` handles PDF/CSV uploads and validates that the CSV contains required columns.
3. `components/text_viewer.py` loads and caches the CSV (keyed by upload bytes) and renders the extracted text for the current page.
4. `components/pagination_controls.py` manages navigation (`st.session_state["current_page"]`) and displays Previous/Next controls.
5. `components/pdf_viewer.py` renders the PDF (download button + inline viewer fallback).
6. `components/dashboard_summary.py` renders the tabbed “Analytics Dashboard” section; several modules are placeholders right now.

Directory layout:

- `components/`: UI modules (each exposes a `render(...)` function)
- `utils/`: shared helpers (e.g., data loading)
- `data/`: sample/demo assets (PDF + extracted-text CSV)

## Installation & Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

If you are missing system packages required by some optional dependencies (e.g., `weasyprint`), you can still run the app as long as the unused dependency isn’t imported at runtime. If installation fails, remove or pin problematic packages based on your OS, or install the system libraries they require.

## Usage Guide

### Using the app (manual upload mode)

1. Start the app: `streamlit run app.py`
2. In the sidebar:
   - Upload a PDF in **Upload PDF**
   - Upload a CSV in **Upload Extracted Text (CSV)**
3. Use **◀ Previous / Next ▶** to navigate pages.
4. The right pane shows extracted text for the current page number.
5. The bottom “Analytics Dashboard” section contains tabs (some may show “not implemented yet” depending on the module).

### CSV format example

Minimum required columns:

```csv
page_number,extracted_text
1,"Page 1 text ..."
2,"Page 2 text ..."
```

Notes:

- `page_number` should start at 1 and be an integer.
- The app currently uses `max(page_number)` to determine the page count, so missing page numbers will be navigable but show “No text available for this page.”

## API Reference (if applicable)

This project does not expose a backend HTTP API. It is a Streamlit UI application.

## Environment Variables

No `.env` variables are required by the current codebase.

If you add features that rely on external services (e.g., model downloads, hosted storage, analytics export), consider documenting variables here, for example:

- `MODEL_CACHE_DIR` – path for caching NLP models
- `EXPORT_DIR` – default directory for generated reports

## Contributing Guide

1. Fork the repository (or create a feature branch if you have direct access).
2. Create a virtual environment and install dependencies:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
3. Make changes in small, focused commits.
4. Prefer adding new UI features as new modules in `components/` with a `render(...)` function.
5. Validate code with:
   - `python3 -m compileall -q .`
6. Open a PR describing:
   - What changed
   - Why it changed
   - How to test it

## License

No license file is included in this repository yet. If you plan to distribute this project, add a `LICENSE` file (e.g., MIT, Apache-2.0) and reference it here.

---

## Scaling Guide

This project is currently a **single-process Streamlit app** that accepts **file uploads** (PDF + CSV) and renders views/analytics in the same process. Scaling it is mostly about (1) preventing per-user work from blocking others, and (2) moving storage + heavy compute out of the Streamlit runtime.

### 1) Current Bottlenecks (what breaks first under load)

- **Memory pressure from uploads**: Uploaded PDFs/CSVs live in memory per session; multiple concurrent users uploading multi‑MB files can exhaust RAM quickly.
- **CPU-bound analytics in the UI process**: Any expensive parsing/OCR/NLP/embedding work run inside Streamlit blocks the worker handling that user (and can degrade overall responsiveness).
- **Reruns amplify work**: Streamlit reruns the script frequently; if heavy steps aren’t cached or externalized, costs multiply under concurrency.
- **No shared persistence**: Results aren’t stored; repeated uploads re-trigger computation and increase compute cost.
- **Single instance limits**: One Streamlit instance has finite CPU/RAM; without horizontal scaling + shared state, you’ll hit a ceiling fast.

### 2) Database Scaling

This repo currently doesn’t use a database. If/when you add persistence (documents, extracted text, analytics results, users), typical choices:

- **Primary DB (Postgres recommended)**:
  - Tables you’ll likely need: `users`, `documents`, `document_pages`, `jobs`, `job_results`, `audit_events`.
  - **Indexing**: index by `user_id`, `document_id`, `page_number`, `created_at`; consider GIN indexes if you store searchable text.
  - **Read replicas**: add replicas once you have read-heavy dashboards or search.
  - **Caching**: cache “document summary” and “page text” reads in Redis to reduce DB load.
  - **Sharding**: usually unnecessary until very large scale; prefer partitioning by `created_at` or `tenant_id` first.

If you need vector search:

- Use a managed vector DB (Pinecone/Weaviate) or Postgres extensions (pgvector) depending on scale and ops preference.

### 3) Backend Scaling

Streamlit is great for MVPs, but production scale usually benefits from separating responsibilities:

- **Keep Streamlit for UI only**: upload, preview, and read results.
- **Move heavy work to a backend service**:
  - Create a small API (FastAPI) for: starting jobs, fetching status, retrieving results.
  - Run long tasks in a worker system (Celery/RQ) so jobs don’t block UI threads.
- **Horizontal vs vertical**:
  - Vertical scaling (bigger instance) helps early but becomes expensive quickly.
  - Horizontal scaling (more instances) requires shared storage (object store) and shared state (DB/Redis).
- **Load balancing**:
  - Put Streamlit behind a load balancer.
  - Ensure “stateless” behavior: store session-affecting artifacts (uploads/results) outside the Streamlit process.

### 4) Frontend Scaling

The “frontend” here is Streamlit-rendered UI (server-driven), not a separate SPA. Still:

- **CDN for static assets**: if you introduce static files (reports, images, exports), serve from object storage + CDN.
- **Lazy/partial loading**:
  - Load only the current page’s extracted text; avoid preloading full-document data into memory.
  - For analytics, fetch only the data required for the active tab.
- **SSR/SSG options**:
  - If you later build a marketing/docs site, use Next.js (SSG/SSR) separately.
  - Streamlit itself isn’t SSR/SSG; treat it as an internal app UI.

### 5) Infrastructure (recommended cloud setup)

Below is a practical, production-friendly baseline. Equivalent services exist across AWS/GCP/Azure.

**AWS (reference architecture)**

- **UI**: Streamlit app on ECS Fargate (or EKS) behind an ALB.
- **API** (optional but recommended as you scale): FastAPI on ECS Fargate behind the same ALB (path-based routing).
- **Workers**: Celery/RQ workers on ECS Fargate.
- **Object storage**: S3 for uploaded PDFs/CSVs + generated outputs (HTML/PDF exports).
- **Database**: RDS Postgres for metadata + results.
- **Cache/queue**: ElastiCache Redis for caching + job queues (or SQS for queue + Redis for cache).
- **Observability**: CloudWatch logs/metrics + X-Ray (or OpenTelemetry + a vendor).
- **Secrets**: Secrets Manager / SSM Parameter Store for credentials.
- **CDN**: CloudFront in front of S3 for downloads/exports.

**GCP equivalents**

- Cloud Run (UI/API/workers), Cloud Storage, Cloud SQL (Postgres), Memorystore (Redis), Cloud Logging/Monitoring, Secret Manager, Cloud CDN.

**Azure equivalents**

- Container Apps (UI/API/workers), Blob Storage, Azure Database for PostgreSQL, Azure Cache for Redis, App Insights/Monitor, Key Vault, Azure CDN.

### 6) Cost Estimate (rough; depends heavily on usage)

These are order-of-magnitude monthly ranges for a typical “upload + light analytics + occasional exports” workload. Assumptions:

- Average active session is short-lived (a few minutes).
- Upload sizes are modest (single-digit MBs).
- Heavy NLP/ML jobs are either rare (at 1k users) or offloaded to workers (at higher scale).
- Costs include compute + managed DB + cache + object storage + basic monitoring; they exclude engineering time and vendor lock-in costs.

- **~1k users/month** (low concurrency): **$50–$300/mo**
  - 1 small container (UI), minimal DB, small Redis or none, low S3 usage.
- **~10k users/month** (moderate concurrency): **$300–$2,000/mo**
  - Multiple UI instances + autoscaling, RDS Postgres, Redis cache/queue, more egress from exports/downloads.
- **~100k users/month** (high concurrency / heavier jobs): **$2,000–$20,000+/mo**
  - Many containers + workers, stronger DB tier + read replicas, significant object storage + CDN egress, possible GPU spend if you add embedding/LLM workloads.

If your workload includes **OCR**, **large PDFs**, or **embedding generation**, costs can increase significantly due to CPU/GPU time.

### 7) Roadmap (MVP → production-grade)

1. **MVP hardening (single instance)**
   - Enforce upload limits (file size, page count) and validate CSV schema.
   - Cache aggressively (already started via `st.cache_data`) and avoid holding full PDFs in memory longer than needed.
   - Add basic logging and error reporting.
2. **Persist artifacts**
   - Store uploads and generated outputs in object storage (S3/GCS/Azure Blob).
   - Add a DB for document metadata and results so users don’t re-upload/recompute.
3. **Async processing**
   - Introduce a job queue (Redis/SQS) and background workers.
   - UI triggers jobs and polls job status; analytics views read stored results.
4. **Split UI and API**
   - Add a small API service for job control and retrieval.
   - Keep Streamlit focused on presentation and lightweight interaction.
5. **Horizontal scaling**
   - Run multiple UI instances behind a load balancer.
   - Ensure everything needed is stored in DB/object storage/cache (no instance-local state).
6. **Observability + reliability**
   - Centralized logs, metrics, tracing; dashboards + alerts.
   - Add rate limiting and abuse protections (especially for uploads/exports).
7. **Performance + data scaling**
   - Add indexing, caching, read replicas, and partitioning as data grows.
   - Introduce vector search only when you have a clear retrieval use case.
8. **Security + compliance**
   - Authentication/authorization, tenant isolation, encryption at rest/in transit.
   - Audit logs for document access; consider retention policies for uploaded files.

---

## Similar Apps / Companies (Competitive Landscape)

Below are 10 well-known solutions that address adjacent problems (document OCR / extraction / QA / IDP workflows). “Tech stack” is listed only when it’s publicly documented.

### 1) Amazon Textract (AWS)

- **What they do**: Managed OCR + document understanding (text, forms, tables, IDs, expenses) as APIs.
- **Tech stack (known)**: AWS-managed service (implementation not public); integrates naturally with S3/Lambda/Step Functions.
- **Business model**: Usage-based cloud API billing (per-page/feature).
- **Scale**: Hyperscale (AWS service).
- **Why successful**: Tight integration with AWS ecosystem, operational reliability, and a clear per-page consumption model.

### 2) Google Cloud Document AI

- **What they do**: Managed document OCR/extraction processors (generic OCR and specialized processors) with Google Cloud integration.
- **Tech stack (known)**: Google Cloud managed service.
- **Business model**: Usage-based pricing (processor/page-based depending on processor type).
- **Scale**: Hyperscale (Google Cloud service).
- **Why successful**: Strong ML capabilities, enterprise cloud primitives, and “processor” abstraction for different doc types.

### 3) Azure AI Document Intelligence (Form Recognizer)

- **What they do**: Managed OCR + layout + prebuilt/custom extraction models for documents.
- **Tech stack (known)**: Azure managed service (web/container options).
- **Business model**: Usage-based (per-page, model-dependent).
- **Scale**: Hyperscale (Microsoft Azure service).
- **Why successful**: Enterprise integration story (Azure), prebuilt models, and clear “model types” for different needs.

### 4) UiPath Document Understanding

- **What they do**: Intelligent Document Processing (IDP) inside automation workflows; extraction + validation + RPA integration.
- **Tech stack (known)**: Proprietary platform; integrates with UiPath automations.
- **Business model**: Enterprise licensing / consumption (page-based entitlements and platform units).
- **Scale**: Enterprise customers running automated back-office workflows.
- **Why successful**: End-to-end automation value (documents → actions), plus strong ecosystem in RPA environments.

### 5) ABBYY FlexiCapture

- **What they do**: Enterprise-grade document capture/extraction platform (cloud/on-prem/SDK) with validation workflows.
- **Tech stack (known)**: Proprietary; cloud offering hosted on Microsoft Azure is publicly stated.
- **Business model**: Enterprise software (SaaS/on-prem/SDK licensing).
- **Scale**: Enterprise adoption; ABBYY states “trusted by 10,000+” companies.
- **Why successful**: Mature OCR + enterprise deployment options + strong validation/controls for regulated workflows.

### 6) Hyperscience

- **What they do**: Enterprise IDP platform (“Hypercell”) for automating complex document workflows at scale (especially public sector / regulated orgs).
- **Tech stack (known)**: Proprietary platform; marketed as multi-cloud capable.
- **Business model**: Enterprise SaaS / platform licensing.
- **Scale**: Enterprise deployments; positioned in analyst reports for IDP.
- **Why successful**: Focus on enterprise constraints (security, accuracy, configurability, scale) and workflow-centric outcomes.

### 7) Rossum (Coupa)

- **What they do**: Cloud-native IDP for transactional documents (notably invoices/AP workflows), with validation and automation.
- **Tech stack (known)**: SaaS platform; marketed as cloud-native and low-code.
- **Business model**: SaaS (typically enterprise-oriented).
- **Scale**: Enterprise transactional automation; now part of Coupa’s ecosystem.
- **Why successful**: Clear ROI story in AP/invoice automation + strong product focus on validation and straight-through processing.

### 8) Nanonets

- **What they do**: Document OCR/extraction workflows and APIs with configurable blocks and integrations.
- **Tech stack (known)**: SaaS + API platform (implementation not public).
- **Business model**: Usage-based / volume-priced SaaS (credits/runs; plans from free → enterprise).
- **Scale**: SMB-to-enterprise (volume pricing tiers).
- **Why successful**: Developer-friendly API, quick time-to-value, and packaging “OCR + workflow blocks” into a usable product.

### 9) Mindee

- **What they do**: Developer-focused OCR/extraction APIs (e.g., invoice parsing) with predictable, page-based credits.
- **Tech stack (known)**: API + SDKs (multiple languages supported).
- **Business model**: Subscription + usage-based credits (page-count based), plus enterprise plans.
- **Scale**: Developer/SMB through enterprise (tiered plans).
- **Why successful**: Strong developer experience (docs/SDKs), clear pricing model, and focused extraction outputs (JSON-ready fields).

### 10) Label Studio (HumanSignal)

- **What they do**: Open-source data labeling/annotation platform (useful for building/QA’ing extraction/NER datasets and human-in-the-loop review).
- **Tech stack (known)**: Backend is Python + Django; frontend uses React (as documented in their architecture overview).
- **Business model**: Open-source + commercial/enterprise cloud edition.
- **Scale**: Widely used in ML teams; community + enterprise deployments.
- **Why successful**: Flexible annotation UI, extensibility, and it becomes “infrastructure” for improving model quality over time.

## How your project can differentiate (niche ideas)

This repo is currently best positioned as a **lightweight review UI** for PDF + extracted text. That’s valuable because many “IDP platforms” optimize for extraction automation, not for human QA and auditability.

Concrete niche directions:

1. **QA-first “extraction validation” product**  
   - Make correctness measurable: page coverage, missing-page detection, confidence calibration, and discrepancy checks (PDF text vs OCR text).
2. **Privacy-first / on-prem reviewer**  
   - Many companies can’t upload sensitive docs to cloud OCR vendors. A local-only Streamlit reviewer + optional self-hosted processing can be compelling.
3. **ESG / sustainability reporting specialization**  
   - Add domain-specific checks: emissions tables, policy statements, KPI extraction templates, and citation-to-page traceability for audits.
4. **Human-in-the-loop workflow**  
   - Add “flag / correct / approve” per page, export a corrections file, and feed it back into training or rules.
5. **Pluggable analytics modules**  
   - Treat `components/` as a plugin surface: keyword search, topic summaries, similarity, NER, and “what changed” diff between two extractions.

If you tell me your intended audience (internal QA tool vs SaaS product) and your target document types (ESG reports, invoices, contracts, etc.), I can rewrite this section to be more opinionated and suggest a sharper positioning statement.
