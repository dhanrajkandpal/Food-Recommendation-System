# FITTIN | Biometric & Nutrition Engine

FITTIN is an end-to-end machine learning application designed to optimize personal nutrition through biometric telemetry and algorithmic food recommendation. 

By taking basic user inputs (age, weight, height, gender, activity level, and goals), the engine leverages a trained Random Forest classifier for body composition analysis and a K-Means clustering algorithm to dynamically synthesize macro-calibrated, high-micronutrient diet plans.

## Machine Learning Architecture

This project is built on a two-pillar machine learning backend, heavily focusing on data engineering, feature scaling, and unsupervised clustering.

### 1. Biometric Classification (Random Forest)
* **Objective:** Accurately classify a user's body mass index (BMI) category based on standard physical metrics.
* **Pipeline:** 
  * Addressed class imbalance within the BMI dataset using **SMOTE** (Synthetic Minority Over-sampling Technique).
  * Encoded categorical variables (Gender, BMI Class) using `LabelEncoder`.
  * Normalized continuous features via `StandardScaler`.
  * Trained a `RandomForestClassifier` (100 estimators, entropy criterion) to predict classifications with high precision, saving the model as a `.pkl` artifact for production inference.

### 2. Algorithmic Diet Synthesis (K-Means Clustering)
* **Feature Engineering:** Developed a custom `micronutrient_density` feature by mapping daily values (DVs) of Vitamin C, Vitamin B11, Calcium, and Iron, calculating the percentage yielded per calorie.
* **Clustering:** 
  * Extracted core macros (Protein, Fats, Carbs, Dietary Fiber).
  * Applied `StandardScaler` and utilized **K-Means Clustering** (k=8, validated via Silhouette Score) to group foods into distinct nutritional profiles.
  * Verified cluster separability using Principal Component Analysis (PCA).
* **Recommendation Engine:** The frontend dynamically filters these pre-computed clusters (e.g., clusters `4` & `5` for lean proteins, `2` & `3` for healthy raw fats) and calculates exact gram-weight serving sizes to hit the user's personalized Total Daily Energy Expenditure (TDEE) and macro splits.

## Key Features

* **Metabolic Telemetry:** Instantly computes BMI, Basal Metabolic Rate (BMR), and maintenance TDEE adjusted for specific fitness objectives (e.g., Lean Bulk, Fat Loss).
* **Precision Ingredient Allowance:** Users can adjust the variety of their macro sources (e.g., 3 protein sources, 2 carb sources) via a "Diet Meter," and the engine mathematically partitions the daily macro targets across diverse, high-density foods.
* **Modern UI/UX:** Features a custom CSS glassmorphism interface (Obsidian & Electric Indigo) built entirely within Streamlit, utilizing Plotly for dynamic data visualization.

## Tech Stack

* **Core:** Python
* **Machine Learning:** Scikit-Learn, Imbalanced-learn (SMOTE)
* **Data Processing:** Pandas, NumPy
* **Frontend / UI:** Streamlit
* **Data Visualization:** Plotly, Seaborn, Matplotlib

## Repository Structure

```text
├── .gitignore
├── App.py                                   # Main Streamlit application and UI/UX logic
├── BMI.ipynb                                # EDA, SMOTE, and Random Forest training pipeline
├── BMI_FINAL.csv                            # Cleaned dataset for BMI classification
├── FOOD.ipynb                               # Feature engineering, PCA, and K-Means clustering pipeline
├── Functions.py                             # Deterministic mathematical calculation functions
├── class_encoder.pkl                        # Pickled BMI Class Label Encoder
├── cleaned_nutrition_dataset_per100g.csv    # Intermediate standardized food dataset
├── clustered_food_database.csv              # Final engineered dataset with K-Means labels
├── gender_encoder.pkl                       # Pickled Gender Label Encoder
├── random_forest.pkl                        # Pickled RF classifier (generated via BMI.ipynb)
└── recommendation_engine.py                 # Backend logic for macro partitioning and food filtering

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/dhanrajkandpal/FITTIN.git](https://github.com/dhanrajkandpal/FITTIN.git)
   cd FITTIN
2. pip install streamlit pandas numpy scikit-learn imbalanced-learn plotly seaborn matplotlib
3. Run the application : streamlit run App.py
