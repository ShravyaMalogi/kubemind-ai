# KubeMind AI — Kubernetes Troubleshooting Assistant

**An AI-powered DevOps assistant that helps diagnose Kubernetes issues, identify potential root causes, and recommend troubleshooting steps.**

KubeMind AI combines Kubernetes diagnostics with Google's Gemini API to make Kubernetes troubleshooting easier to understand and more accessible.

Instead of manually interpreting pod failures and container statuses, KubeMind analyzes diagnostic information and provides clear explanations, severity levels, recommended commands, and possible resolutions.

## Features

- **AI-Powered Troubleshooting:** Uses Google Gemini to analyze Kubernetes pod information and explain potential issues.
- **Automated Diagnostics:** Detects common Kubernetes problems such as `CrashLoopBackOff`, `ImagePullBackOff`, and `Pending` pods.
- **Severity Classification:** Categorizes detected issues by severity.
- **Troubleshooting Recommendations:** Suggests useful `kubectl` commands and possible solutions.
- **Streamlit Dashboard:** Displays pod health, restart counts, and diagnostic results through an interactive dashboard.
- **Rule-Based Fallback:** Provides basic diagnostics even when the AI service is unavailable.
- **Modular Architecture:** Separates Kubernetes diagnostics, AI analysis, and dashboard functionality.

## Dashboard

The Streamlit dashboard provides an overview of Kubernetes pod health, including:

- Total pods
- Healthy pods
- Pods with issues
- Container restart counts
- AI-generated troubleshooting reports

*The current dashboard uses sample pod data. Live cluster integration is a planned enhancement.*

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Streamlit | Interactive dashboard |
| Google Gemini API | AI-powered troubleshooting |
| Kubernetes Python Client | Kubernetes cluster interaction |
| python-dotenv | Environment variable management |
| Pytest | Automated testing |

## Project Structure

```text
kubemind-ai/
│
├── app/
│   ├── main.py
│   └── dashboard.py
│
├── kubemind/
│   ├── cluster.py
│   ├── diagnostics.py
│   └── logs.py
│
├── ai_engine/
│   └── analyzer.py
│
├── tests/
│   ├── test_cluster.py
│   └── test_diagnostics.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/kubemind-ai.git
cd kubemind-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Never commit your `.env` file or expose your API key publicly.

### 4. Run the application

```bash
python -m streamlit run app/dashboard.py --server.address 0.0.0.0
```

Open the Streamlit URL provided in your terminal to access the dashboard.

## How It Works

1. Kubernetes pod information is collected or supplied to the diagnostic engine.
2. The diagnostic module identifies common pod issues.
3. The AI engine sends relevant diagnostic information to Google Gemini.
4. Gemini analyzes the information and generates a troubleshooting explanation.
5. The dashboard displays the diagnosis, severity, recommended commands, and suggested resolution.
6. If AI analysis fails, KubeMind falls back to its rule-based diagnostic engine.

## Running Tests

Run the automated tests using:

```bash
pytest -v
```
---

KubeMind AI was built to explore the intersection of **Artificial Intelligence, Kubernetes, and DevOps**.

The goal is to simplify Kubernetes troubleshooting by combining traditional diagnostic techniques with AI-generated explanations, helping developers understand infrastructure problems and investigate them more efficiently.
