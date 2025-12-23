# 🎯 OctoVision: AI-based Medical Imaging Platform

## 🧠 Project Goal
To develop a distributed, full-stack platform capable of detecting cancer from medical images (MRI/IRM). The system allows doctors to visualize scans, perform annotations, and receive AI-driven predictions for cancer localization.

---

## 🧩 Global Architecture


### 1️⃣ Frontend (UI/UX)
- **Tech:** React + Tailwind CSS
- **Key Features:**
  - Medical image visualization (DICOM/MRI support)
  - Interactive annotation tools for cancer zones
  - Prediction dashboard (Cancer vs. No Cancer)
  - RBAC (Role-Based Access Control) for Users and Admins

### 2️⃣ Backend & Data Layer
- **API Framework:** FastAPI (Python)
- **Metadata Storage:** MongoDB (NoSQL) — Stores user profiles, logs, and annotation coordinates.
- **Image Storage:** Hadoop (HDFS) — Handles large-scale distributed storage of medical images with replication and fault tolerance.

### 3️⃣ Data Processing & AI
- **Processing:** Apache Spark (PySpark) — Large-scale image preprocessing and normalization.
- **Models:** Deep Learning (CNNs) — Utilizing specialized architectures for medical imaging, potentially fine-tuning pretrained models from Hugging Face.
- **Data Source:** TCIA (The Cancer Imaging Archive) & MBIA.

---

## 🚀 DevOps & Deployment
- **Containerization:** Every service (Backend, Spark, Mongo, Hadoop) is containerized via **Docker**.
- **Orchestration:** Managed through **Docker Compose** for easy local and staging deployment.
- **CI/CD:** GitHub Actions & Jenkins pipelines for automated testing and image building.

---

## 🚦 Team Workflow (The "Rules")

### 🌿 Git & Jira Integration
We use the **OC** project key to link code to Jira tickets. 
- **Branch Naming:** `OC-XX-description` (e.g., `OC-1-setup-hdfs`).
- **Commit Messages:** Must include the key, e.g., `OC-5: Added normalization script`.
- **Pull Requests:** Titles must start with `OC-XX:`.

### 🛡️ Quality Gate
- All PRs require at least **one peer review**.
- All PRs must pass the **Jira Issue Key Validator** (GitHub Action) before merging.

---

## 🧪 Bonus Goals
- Dataset versioning (tracking model performance across data iterations).
- High scalability for multi-node Hadoop clusters.
- Real-time prediction logs for admins.
