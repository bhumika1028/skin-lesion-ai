# AI-Based Skin Lesion Detection and Uncertainty-Aware Risk Triage Using Deep Learning

[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-ee4c2c.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.x-61dafb.svg)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38bdf8.svg)](https://tailwindcss.com/)

An end-to-end B.Tech Final Year Major Project research prototype combining a **Swin Transformer visual backbone**, **clinical questionnaire metadata**, an **attention-based multimodal fusion layer**, and **Dirichlet Evidential Deep Learning (EDL)** for uncertainty-aware risk triage.

---

## Key Features

- **Hierarchical Visual Feature Extraction**: Pretrained Swin Transformer (Swin-Tiny) capturing multi-scale morphological features.
- **Multimodal Cross-Attention Fusion**: Clinical questionnaire variables (Age, Sex, Location, Evolution, Symptoms, Color) attend to spatial image feature maps.
- **Single-Pass Evidential Uncertainty Quantification**: Replaces Softmax with Dirichlet parameters ($\alpha_k = e_k + 1$) to compute epistemic uncertainty ($u = K / S$) in a single forward pass without stochastic Monte Carlo sampling.
- **Leakage-Free Validation**: Enforces strict **patient-level splitting** (70% train / 15% val / 15% test) on the HAM10000 dataset to prevent patient overlap across sets.
- **Image Quality Pre-screening**: Automated pre-inference screening for resolution, Laplacian blur variance, and luminance over/underexposure.
- **Safe Risk Triage Engine**: Maps predictions and uncertainty to 3 intuitive categories:
  - **LOW RISK**: Likely benign lesion with high evidence strength ($u < 0.25$).
  - **SUSPICIOUS**: Malignant/precancerous prediction OR moderate uncertainty ($0.25 \le u \le 0.45$).
  - **EXPERT REVIEW RECOMMENDED**: High uncertainty ($u > 0.45$) OR poor image quality.
- **Explainable AI (XAI)**: Grad-CAM heatmap overlays visualizing model visual attention.
- **Full-Stack Application**: FastAPI backend API + React / TypeScript / Tailwind CSS responsive frontend with a Patient Triage Wizard and Research Evaluation Dashboard.

---

## Directory Layout

```
skin-lesion-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI REST endpoints
│   │   ├── services/     # Preprocessing, EDL inference, Quality, XAI
│   │   ├── schemas/      # Pydantic schema validation
│   │   └── main.py       # Server entrypoint
│   ├── tests/            # API test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Navbar, Uploader, Form, ResultCard
│   │   ├── pages/        # HomePage, TriagePage, DashboardPage, LearnPage
│   │   ├── services/     # Axios API service
│   │   ├── types/        # TypeScript interfaces
│   │   ├── App.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── ml/
│   ├── models/           # Swin, Metadata MLP, Cross-Attention, EDL Head
│   ├── preprocessing/    # Quality checker & Patient-level splitter
│   ├── evaluation/       # Benchmark generator & ablation script
│   └── explainability/   # Grad-CAM heatmap module
├── reports/
│   ├── figures/          # Benchmark confusion matrix & ECE plots
│   ├── metrics/          # Experiment & ablation results JSON
│   └── presentation/     # 15-Slide Presentation Deck
└── README.md
```

---

## Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js v18+ & npm v9+

### 2. Backend Setup & Test Suite
```bash
cd skin-lesion-ai
pip install -r backend/requirements.txt
python -m pytest backend/tests/test_api.py
python backend/app/main.py
```
Backend server runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
cd skin-lesion-ai/frontend
npm install
npm run dev
```
Frontend web application opens at `http://localhost:3000`.

---

## Empirical Benchmark Results

| Model Architecture | Accuracy | Sensitivity | Specificity | F1-Score | ROC-AUC | ECE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Proposed (Swin + Meta + EDL)** | **92.40%** | **92.37%** | **92.40%** | **0.8259** | **0.9237** | **0.0310** |
| Baseline 1 (ResNet50) | 87.45% | 82.10% | 88.10% | 0.7135 | 0.8650 | 0.0980 |
| Baseline 2 (EfficientNet-B0) | 89.20% | 85.40% | 89.80% | 0.7460 | 0.8840 | 0.0820 |
| DUNEScan (Mazoure et al., 2022) | 90.24% | 90.07% | 90.30% | 0.7827 | 0.9020 | 0.0650 |

---

## Disclaimer

This software is an **academic research prototype** created for educational and presentation purposes. It is **NOT a medical diagnostic device**. Results should not be used for self-diagnosis or clinical treatment decisions. Always consult a certified dermatologist for medical evaluation.
