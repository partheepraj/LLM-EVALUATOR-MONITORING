# 🤖 LLM Evaluation & Monitoring Platform

## 📌 Project Overview

LLM Evaluation & Monitoring Platform is a complete AI-powered evaluation system that helps analyze, compare, and monitor Large Language Model (LLM) responses.

The platform evaluates prompts using locally hosted LLMs through Ollama and provides detailed analytics including quality scoring, hallucination analysis, latency tracking, prompt benchmarking, and model comparison.

This project was built using Python, Streamlit, Ollama, Plotly, and Sentence Transformers.

---

## 🚀 Features

### Prompt Evaluation

* Evaluate prompts directly from the dashboard
* Generate responses using local LLMs
* Measure response latency
* Calculate response quality score
* Detect hallucination risk
* Generate response ratings

### Monitoring Dashboard

* Evaluation history tracking
* KPI metrics
* Prompt leaderboard
* Detailed response analysis
* Quality score monitoring

### Analytics

* Latency Analysis
* Response Length Trend
* Quality Score Trend
* Hallucination Analysis
* Latency vs Response Length
* Response Rating Distribution

### A/B Prompt Testing

* Compare two prompts
* Evaluate quality differences
* Select the best-performing prompt

### Multi-Model Benchmarking

Compare multiple LLMs:

* Llama 3.2
* Mistral
* Gemma 3

Metrics:

* Latency
* Word Count
* Character Count

### Reporting

* Download evaluation reports
* Historical evaluation tracking
* Benchmark analysis

---

## 🏗️ System Architecture

User Prompt
↓
Streamlit Dashboard
↓
Evaluator Engine
↓
Ollama LLM
↓
Response Generation
↓
Quality Evaluation
↓
Hallucination Analysis
↓
CSV Storage
↓
Analytics Dashboard

---

## 🛠️ Technologies Used

### Frontend

* Streamlit

### Backend

* Python

### AI Models

* Ollama
* Llama 3.2
* Mistral
* Gemma 3

### Data Processing

* Pandas

### Visualization

* Plotly

### NLP Evaluation

* Sentence Transformers
* Cosine Similarity

---

## 📂 Project Structure

```text
llm_EV/
│
├── app.py
├── evaluator.py
├── quality_score.py
├── hallucination.py
├── benchmark.py
├── benchmark_dashboard.py
├── test.py
├── ab_test.py
│
├── results.csv
├── model_benchmark.csv
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone <your-github-repository>
cd llm_EV
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download and install Ollama.

Pull required models:

```bash
ollama pull llama3.2
ollama pull mistral
ollama pull gemma3
```

Verify installation:

```bash
ollama list
```

---

## ▶️ Run Application

Start Ollama:

```bash
ollama serve
```

Run Streamlit Dashboard:

```bash
streamlit run app.py
```

Open browser:

```text
http://localhost:8501
```

---

## 📊 Dashboard Components

### Evaluation Dashboard

* Evaluation Data
* KPI Metrics
* Most Detailed Response
* Highest Quality Prompt
* Latency Analysis
* Response Length Trend
* Quality Score Trend
* Hallucination Analysis
* Prompt Leaderboard
* Recent Evaluations

### A/B Testing

* Prompt Comparison
* Quality Comparison
* Winner Selection

### Multi-Model Benchmark

* Latency Comparison
* Word Count Comparison
* Character Count Comparison
* Fastest Model Detection

---

## 📈 Evaluation Metrics

### Quality Score

Measures semantic similarity between prompt and response.

### Hallucination Score

Measures potential hallucination risk using embedding similarity.

### Response Rating

| Score    | Rating          |
| -------- | --------------- |
| 85+      | Excellent ⭐⭐⭐⭐⭐ |
| 70–84    | Good ⭐⭐⭐⭐       |
| 50–69    | Average ⭐⭐⭐     |
| Below 50 | Poor ⭐⭐         |

---

## 🎯 Future Improvements

* RAG Evaluation
* LLM-as-a-Judge
* PDF Report Generation
* SQLite Database Integration
* User Authentication
* Cloud Deployment
* Real-Time Monitoring

---

## 👨‍💻 Author

Partheep

Aspiring Data Scientist & AI Engineer

---

## ⭐ Project Status

Completed

LLM Evaluation + Monitoring + Benchmarking Platform
