# FITTIN

A hybrid machine learning and mathematical optimization engine for precise nutrition planning.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit Cloud](https://img.shields.io/badge/Deployed%20on-Streamlit%20Cloud-FF4B4B)](https://streamlit.io/cloud)

**[Live Demo](https://fittin-b8fjdspvsosvbjwzy6jjxr.streamlit.app/)** · **[Project Structure](#project-structure)** · **[Run Locally](#getting-started)**

---

## About the Project

FITTIN is an end-to-end machine learning and nutrition recommendation engine. It takes basic user inputs such as age, weight, height, gender, activity level, and a fitness goal, then produces body composition metrics and a daily meal plan with exact serving sizes.

Most diet tools I came across were either static, offering the same generic meal plans for everyone, or too complicated, requiring manual macro tracking with no attention to food quality. FITTIN was my attempt to automate that whole process: classify the user's body profile with a model, group foods by their nutritional makeup, and then calculate portions that fit the user's energy needs and macro targets.

> **Note:** FITTIN is a planning tool built on statistical patterns and standard nutrition formulas. It is not medical advice, and it should not replace guidance from a doctor or a registered dietitian.

---

## Features

- Body classification (BMI category) from physical telemetry using a Random Forest model
- Goal-based blueprints: Cut, Bulk, and Sustain
- Food clustering by macronutrient profile using K-Means (k = 8)
- Micronutrient density scoring to rank foods by nutritional quality per calorie
- Exact gram-weight serving sizes that match the user's daily energy and macro targets
- Interactive Streamlit interface with real-time nutritional calculations
- Saved model artifacts (classifier, scaler, and encoders) so predictions run without retraining

---

## How It Works

```text
User Inputs (age, weight, height, gender, activity, goal)
        │
        ├──────────────────────────────┐
        ▼                              ▼
Pillar A: Biometric Classification   Pillar B: Diet Synthesis
  Scaler + Label Encoders              Micronutrient Density Scoring
  Random Forest Classifier             Macronutrient Clusters (K-Means)
        │                              │
        ▼                              ▼
  BMI Category                 Goal Blueprint (Cut / Bulk / Sustain)
        │                              │
        └──────────────┬───────────────┘
                       ▼
          Recommendation Engine
    Filters clusters, ranks foods by density,
    calculates gram-weight servings for TDEE and macros
                       │
                       ▼
          Streamlit Interface ──► Daily Meal Plan
```

The project has two machine learning pillars. The first classifies the user's BMI category. The second segments foods into nutritional clusters, which the recommendation engine then filters and ranks when it builds a meal plan. The clustering is precomputed, so the app only has to select from clusters and do the arithmetic at runtime.

---

## Data and Models

### Pillar A: Biometric Classification

The classifier predicts a user's BMI category from their physical measurements.

- **Class imbalance:** The BMI dataset is skewed toward some categories, so I used SMOTE (Synthetic Minority Over-sampling Technique) to help the model generalize across body types.
- **Encoding and scaling:** Categorical values such as gender and target class were encoded with `LabelEncoder`, and continuous features were normalized with `StandardScaler`.
- **Model:** A `RandomForestClassifier` with 100 estimators and the entropy criterion.
- **Artifacts:** `random_forest.pkl`, `scaler.pkl`, `class_encoder.pkl`, and `gender_encoder.pkl`.

### Pillar B: Diet Synthesis

Instead of recommending random foods, FITTIN groups them first.

- **Micronutrient density:** I created a custom feature that compares the daily values of key micronutrients, such as Vitamin C, Calcium, and Iron, against each food's caloric yield. This gives a rough measure of nutritional quality per calorie.
- **Clustering:** Core macronutrients (protein, fats, carbohydrates, and dietary fiber) were standardized and clustered with K-Means, using k = 8. The choice of k was checked with silhouette scores.
- **Verification:** PCA was used to visually check how well the clusters separate.
- **Recommendation logic:** The engine pulls from specific clusters (for example, lean proteins or healthy raw fats), ranks foods by micronutrient density, and computes gram-weight servings that line up with the user's Total Daily Energy Expenditure (TDEE) and macro split.

---

## Project Structure

```text
Food-Recommendation-System/
│
├── App.py                                 # Streamlit application and UI logic
├── Functions.py                           # Deterministic calculation functions
├── recommendation_engine.py               # Macro partitioning and food filtering
├── requirements.txt                       # Dependencies for local and cloud use
├── .gitignore
│
├── BMI.ipynb                              # EDA, SMOTE, and Random Forest training
├── FOOD.ipynb                             # Feature engineering, PCA, and K-Means
│
├── BMI_FINAL.csv                          # Cleaned BMI classification dataset
├── cleaned_nutrition_dataset_per100g.csv  # Standardized food dataset
├── clustered_food_database.csv            # Food dataset with K-Means labels
│
├── random_forest.pkl                      # Trained classifier
├── scaler.pkl                             # Fitted StandardScaler
├── class_encoder.pkl                      # BMI class label encoder
└── gender_encoder.pkl                     # Gender label encoder
```

---

## Getting Started

### Prerequisites

- Python 3.x
- pip

### 1. Clone the repository

```bash
git clone https://github.com/dhanrajkandpal/Food-Recommendation-System.git
cd Food-Recommendation-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run App.py
```

Streamlit will print a local URL, usually `http://localhost:8501`, which you can open in your browser.

---

## Deployment

FITTIN is deployed on **Streamlit Community Cloud**:

1. The public GitHub repository is connected to Streamlit Community Cloud.
2. The main file path is set to `App.py`.
3. Streamlit installs the Python dependencies listed in `requirements.txt`.
4. The app is live at the link at the top of this README.

---

## What I Learned

- **Imbalanced data needs care.** SMOTE helped the classifier see minority classes, but it also made me think about when resampling should happen relative to the train/test split.
- **Precomputation keeps apps responsive.** Clustering the foods ahead of time meant the app only had to filter and calculate at runtime.
- **A good model is only part of a good product.** Turning model outputs into serving sizes that a person can actually follow took as much thought as the algorithms themselves.
- **Hybrid systems are practical.** Combining a classifier, clustering, and deterministic formulas made the system easier to explain and check than a single black-box model would have been.

---

## Limitations & Future Work

FITTIN works as a planning prototype, and there are clear areas to improve:

- [ ] **Evaluation:** Confirm that SMOTE is applied only to training data, and report final metrics on an untouched test set.
- [ ] **Nutrition data:** Expand the food database and verify values against authoritative sources.
- [ ] **Micronutrient scoring:** Test whether the density formula actually improves plan quality for users.
- [ ] **Personalization:** Allow dietary restrictions and food preferences to be part of the plan.
- [ ] **Testing:** Add unit tests for the calculation functions and the recommendation engine.
- [ ] **Model updates:** Retrain and compare models as more data becomes available.

---

## Contributing

Suggestions, issues, and pull requests are welcome. If you have an idea to make FITTIN better, feel free to open an issue.

---

## Author

**Dhanraj Kandpal**
BCA student exploring machine learning, web development, and the engineering behind both.

[GitHub](https://github.com/dhanrajkandpal) · [Live Demo](https://fittin-b8fjdspvsosvbjwzy6jjxr.streamlit.app/)

---

## License

This project is open source. Add your preferred license here (e.g., MIT).
