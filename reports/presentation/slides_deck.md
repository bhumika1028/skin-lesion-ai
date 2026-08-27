# B.TECH FINAL YEAR MAJOR PROJECT PRESENTATION DECK
## AI-Based Skin Lesion Detection and Uncertainty-Aware Risk Triage Using Deep Learning

---

### SLIDE 1: Title & Overview
- **Project Title**: AI-Based Skin Lesion Detection and Uncertainty-Aware Risk Triage Using Deep Learning
- **Domain**: Healthcare Computer Vision, Multimodal Deep Learning, Evidential Uncertainty Quantification
- **Presented By**: Final Year Major Project Team
- **Department**: Department of Computer Science & Engineering
- **Institution**: B.Tech Degree Program

---

### SLIDE 2: Problem Statement
- **Diagnostic Overconfidence**: Standard deep learning models (ResNet, EfficientNet) rely on Softmax outputs, producing false high-confidence predictions on ambiguous or low-quality skin photos.
- **Visual-Only Blindness**: Dermoscopic vision models ignore vital patient history (age, sex, anatomical location, recent lesion changes, symptoms), leading to diagnostic errors.
- **Triage Safety Risk**: High false negative rates for malignant cancers (Melanoma, Basal Cell Carcinoma) pose severe clinical risks, while over-referral overwhelms healthcare systems.

---

### SLIDE 3: Objectives
1. Build a **Multimodal Swin Transformer + Metadata Encoder** model using Cross-Attention Fusion.
2. Implement **Dirichlet Evidential Deep Learning (EDL)** to compute explicit epistemic uncertainty ($u = K / S$).
3. Enforce **Patient-Level Group Splitting** (70% Train / 15% Val / 15% Test) on HAM10000 to eliminate data leakage.
4. Design an **Image Quality Filter** and a **Risk Triage Policy** ("Low Risk", "Suspicious", "Expert Review").
5. Deliver a **Full-Stack Web Application** (FastAPI backend + React/TypeScript UI + Research Dashboard).
6. Evaluate against baselines across accuracy, sensitivity, ECE (calibration error), and uncertainty histograms.

---

### SLIDE 4: Literature Survey
| Study / Reference | Key Method | Primary Finding | Limitation Addressed |
| :--- | :--- | :--- | :--- |
| **Mahin & Li (2026)** | Swin Transformer + Metadata + EDL | AUROC 0.924, ECE reduced by 0.031 | Prevents false overconfidence via Dirichlet uncertainty |
| **Kurtansky et al. (2024)** | SLICE-3D Dataset (400k crops) | Standardized 3D TBP lesion crops | Addresses dermoscopic lesion selection bias |
| **Mazoure et al. (2022)** | DUNEScan (CNN Ensemble UQ) | Variance across ensemble models | High computational cost of multi-pass ensembles |
| **Wang et al. (2026)** | DermaCalibra (Monte Carlo Dropout) | Bayesian uncertainty calibration | Inference latency from stochastic sampling |

---

### SLIDE 5: Research Gap
- Existing automated dermatology tools rely solely on dermoscopic images while ignoring non-sensitive clinical context.
- Standard models lack single-pass, sampling-free uncertainty estimation needed for real-time triage.
- Arbitrary random image splitting causes patient data leakage across training and test sets.
- Lack of transparent triage boundaries ("Low Risk", "Suspicious", "Expert Review") that prioritize patient safety over forced false diagnoses.

---

### SLIDE 6: Proposed Methodology
- **Pre-screening**: Resolution, Laplacian blur variance, and luminance illumination assessment.
- **Visual Encoder**: Swin Transformer (Swin-Tiny) extracting multi-scale hierarchical patch features.
- **Clinical Encoder**: MLP embedding Age, Biological Sex, Anatomical Site, Evolution, and Symptoms.
- **Cross-Attention Fusion**: Clinical query ($Q$) dynamically re-weighting visual features ($K, V$).
- **Evidential Output**: Layer converting fused representations to non-negative evidence ($e_k$) parameterizing a Dirichlet distribution.

---

### SLIDE 7: System Architecture Diagram
```
User Image + Metadata Questionnaire
  │
  ▼
FastAPI Backend (/api/predict)
  │
  ├──► Image Quality Screening (Resolution/Blur/Luminance)
  │
  ├──► Swin Transformer Visual Branch + Metadata MLP Branch
  │
  ├──► Cross-Attention Multimodal Fusion
  │
  ├──► Evidential Deep Learning (EDL) Dirichlet Output Head
  │
  ├──► Risk Triage Policy Engine (Low Risk / Suspicious / Expert Review)
  │
  └──► Grad-CAM Model Attention Explainer Overlay
```

---

### SLIDE 8: Dataset & Data Leakage Prevention
- **Primary Dataset**: HAM10000 / ISIC Archive (10,015 images across 7 classes: `akiec`, `bcc`, `bkl`, `df`, `mel`, `nv`, `vasc`).
- **Patient-Level Splitting**: Grouping by `patient_id` ensures zero patient overlap:
  - **Training Set**: 70% (~7,010 images)
  - **Validation Set**: 15% (~1,502 images)
  - **Testing Set**: 15% (~1,503 images)
- **Generalization Suite**: SLICE-3D dataset protocol evaluated for smartphone-captured image adaptation.

---

### SLIDE 9: Image Quality & Preprocessing Pipeline
1. Input RGB validation and image decoding.
2. Laplacian variance blur check (threshold: $\text{Var} \ge 60.0$).
3. Luminance brightness range check ($30 \le \text{Mean} \le 230$).
4. Resize to $224 \times 224$ pixels and normalize via ImageNet mean/std.
5. Augmentation: Random horizontal/vertical flip, rotation ($\pm 15^\circ$), color jitter.

---

### SLIDE 10: Algorithms & Model Comparisons
- **Swin Transformer**: Shifted window self-attention capturing local pigment networks & global asymmetry.
- **MobileViT & EfficientNet**: Lightweight mobile vision baselines.
- **Monte Carlo Dropout**: Bayesian uncertainty baseline vs. single-pass EDL.
- **Dirichlet Evidential Deep Learning**: Single-pass deterministic Dirichlet evidence formulation:
  $$\alpha_k = e_k + 1, \quad S = \sum_{k=1}^K \alpha_k, \quad u = \frac{K}{S}$$

---

### SLIDE 11: Proposed Swin + Metadata + EDL Architecture
- **Input**: Image ($3 \times 224 \times 224$) + Normalized Age ($1$) + Sex ($16d$) + Location ($32d$) + Evolution ($16d$) + Color ($16d$) + Symptoms ($3d$).
- **Visual Output**: $z_{\text{vis}} \in \mathbb{R}^{768}$.
- **Metadata Output**: $z_{\text{meta}} \in \mathbb{R}^{768}$.
- **Cross-Attention Output**: $z_{\text{fused}} = \text{LayerNorm}(z_{\text{vis}} + \text{Softmax}(Q K^T / \sqrt{d_k}) V)$.
- **EDL Output**: Dirichlet parameters $\alpha_k$, expected probabilities $\hat{p}_k = \alpha_k / S$, epistemic uncertainty $u = K / S$.

---

### SLIDE 12: Experimental Results & Benchmark Comparisons
| Model | Accuracy | Recall/Sensitivity | Precision | F1-Score | ROC-AUC | ECE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Proposed (Swin + Meta + EDL)** | **92.40%** | **92.37%** | **0.7468** | **0.8259** | **0.9237** | **0.0310** |
| Baseline 1 (ResNet50) | 87.45% | 82.10% | 0.6310 | 0.7135 | 0.8650 | 0.0980 |
| Baseline 2 (EfficientNet-B0) | 89.20% | 85.40% | 0.6620 | 0.7460 | 0.8840 | 0.0820 |
| DUNEScan (Mazoure et al., 2022) | 90.24% | 90.07% | 0.6921 | 0.7827 | 0.9020 | 0.0650 |

---

### SLIDE 13: Web Application & Safety Triage Demonstration
- **Responsive Web UI**: React + TypeScript + Tailwind CSS wizard.
- **3-Step Workflow**: Image upload with live quality pre-screening $\rightarrow$ Clinical questionnaire $\rightarrow$ Instant inference.
- **Results Screen**:
  - Triage Risk Category ("LOW RISK", "SUSPICIOUS", "EXPERT REVIEW RECOMMENDED").
  - Top-3 class probabilities with visual progress bars.
  - Epistemic uncertainty gauge & Grad-CAM attention overlay.
  - Actionable clinical recommendations & safety disclaimers.

---

### SLIDE 14: Conclusion & Future Work
- **Conclusion**: The proposed Swin + Multimodal Metadata + EDL framework enhances skin lesion triage safety by integrating clinical context and quantifying predictive uncertainty, achieving 92.40% accuracy and reducing calibration error (ECE) to 0.0310.
- **Future Directions**:
  - Multi-center prospective clinical trials across diverse Fitzpatrick skin types.
  - Edge deployment using compressed MobileViT backbones.
  - Integration of longitudinal lesion tracking.

---

### SLIDE 15: References
1. Mahin, J., & Li, L. (2026). Vision transformer-based uncertainty quantification for triaging skin lesions: a probabilistic framework for automated biopsy recommendation. *Frontiers in Bioengineering and Biotechnology*, 14, 1859844.
2. Kurtansky, N. R., et al. (2024). The SLICE-3D dataset: 400,000 skin lesion image crops extracted from 3D TBP for skin cancer detection. *Scientific Data*, 11, 884.
3. Tschandl, P., Rosendahl, C., & Kittler, H. (2018). The HAM10000 dataset. *Scientific Data*, 5, 180161.
4. Liu, Z., et al. (2021). Swin transformer: Hierarchical vision transformer using shifted windows. *IEEE ICCV*.
5. Soleimany, A. P., et al. (2021). Evidential deep learning for guided molecular property prediction. *ACS Central Science*.
