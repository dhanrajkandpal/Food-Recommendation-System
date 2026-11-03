# FITTIN | Biometric & Nutrition Engine

FITTIN is a hybrid machine learning and mathematical nutrition recommendation application. It takes basic user inputs such as age, weight, height, gender, activity level, and fitness goal, then generates body-composition metrics and a personalized nutrition plan with gram-based food portions.

The system combines a trained Random Forest classifier, K-Means food clustering, and deterministic nutrition calculations to build recommendations around a user's energy requirements and macronutrient targets.

> **Note:** FITTIN is a planning tool based on statistical models and standard nutrition formulas. It is not medical advice and should not replace guidance from a doctor or registered dietitian.

---

## Features

- BMI category classification using a trained Random Forest model
- Goal-based nutrition targets for cutting, lean bulking, and maintenance
- BMI, BMR, and TDEE calculations
- Food grouping using K-Means clustering (k = 8)
- Micronutrient-density scoring to help rank foods by nutritional value per calorie
- Gram-weight serving calculations based on personalized calorie and macronutrient targets
- A multi-step Flask assessment experience and personalized results interface
- Original Streamlit application retained in `App.py`

---

## How It Works

```text
User Inputs
(age, weight, height, gender, activity level, fitness goal)
                         |
             +-----------+-----------+
             |                       |
             v                       v
  Biometric Classification     Diet Synthesis
  Scaler + Encoders            Micronutrient Density
  Random Forest                K-Means Food Clusters
             |                       |
             v                       v
       BMI Category             Food Clusters
             |                       |
             +-----------+-----------+
                         |
                         v
              Nutrition Calculations
              BMR, TDEE, calorie target,
              and macronutrient targets
                         |
                         v
              Recommendation Engine
              Filters and ranks foods,
              calculates gram-weight portions
                         |
                         v
             Personalized Nutrition Plan
```

The project has two machine-learning pillars. The first predicts a user's BMI category from physical measurements. The second groups foods by their nutritional profiles. The recommendation engine combines those outputs with deterministic calculations to produce food portions aligned with the user's calorie and macronutrient targets. Food clustering is precomputed, so the application selects from existing clusters at runtime rather than retraining the clustering model for each assessment.

---

## Machine Learning Architecture

### 1. Biometric Classification (Random Forest)

The classifier predicts a user's BMI category from physical measurements.

- **Class imbalance:** SMOTE (Synthetic Minority Over-sampling Technique) was used to address class imbalance in the BMI dataset.
- **Encoding:** Categorical variables, including gender and BMI class, were encoded using `LabelEncoder`.
- **Scaling:** Continuous features were normalized using `StandardScaler`.
- **Model:** A `RandomForestClassifier` with 100 estimators and the entropy criterion.
- **Artifacts:** The trained classifier and supporting preprocessing objects are stored as `.pkl` files.

### 2. Algorithmic Diet Synthesis (K-Means Clustering)

- **Feature engineering:** A custom `micronutrient_density` feature was created using selected micronutrient daily values, including Vitamin C, Vitamin B11, Calcium, and Iron, relative to calories.
- **Clustering:** Protein, fat, carbohydrates, and dietary fiber were standardized and grouped using K-Means with `k = 8`. The choice of cluster count was evaluated using silhouette scores.
- **Verification:** PCA was used to inspect the separation of food clusters.
- **Recommendation logic:** The recommendation engine filters precomputed food clusters, ranks candidate foods, and calculates gram-weight portions to align with personalized TDEE and macronutrient targets.

---

## Tech Stack

- **Core:** Python
- **Machine Learning:** Scikit-learn, imbalanced-learn (SMOTE)
- **Data Processing:** Pandas, NumPy
- **Backend:** Flask
- **Original interface:** Streamlit
- **Frontend:** HTML, CSS, JavaScript, Tailwind CSS
- **Data Visualization / Analysis:** Plotly, Seaborn, Matplotlib
- **Clustering and dimensionality reduction:** K-Means, PCA

---

## Project Structure

```text
Food-Recommendation-System/
├── app.py                              # Flask application entry point
├── App.py                              # Original Streamlit application
├── Functions.py                        # Deterministic nutrition calculations
├── recommendation_engine.py            # Food filtering and recommendation logic
├── recommendation_adapter.py           # Adapter between Flask and recommendation engine
├── requirements.txt                    # Python dependencies
├── package.json                        # Tailwind CSS scripts and frontend dependencies
├── templates/
│   ├── index.html                      # Flask homepage
│   └── assessment.html                 # Multi-step assessment interface
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── assessment.css
│   │   └── tailwind.css                # Generated Tailwind output
│   ├── js/
│   │   ├── main.js
│   │   └── assessment.js
│   └── src/
│       └── input.css                   # Tailwind input
├── BMI.ipynb                           # BMI EDA, SMOTE, and model training
├── FOOD.ipynb                          # Food feature engineering, PCA, and clustering
├── BMI_FINAL.csv                       # Cleaned BMI classification dataset
├── cleaned_nutrition_dataset_per100g.csv
├── clustered_food_database.csv         # Food dataset with cluster labels
├── random_forest.pkl                   # Trained Random Forest classifier
├── scaler.pkl                          # Fitted feature scaler
├── class_encoder.pkl                   # BMI class encoder
└── gender_encoder.pkl                  # Gender encoder
```

---

## Getting Started

### Prerequisites

- Python 3.x
- pip
- Node.js and npm (for the Flask frontend's Tailwind CSS build)

### 1. Clone the repository

```bash
git clone https://github.com/dhanrajkandpal/Food-Recommendation-System.git
cd Food-Recommendation-System
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Flask application

```bash
python app.py
```

In a **second terminal**, install the frontend dependencies and start the Tailwind CSS watcher:

```bash
npm install
npm run dev:css
```

Then open:

```text
http://127.0.0.1:5000
```

`App.py` is the original Streamlit application and has been left untouched. The Flask application entry point is `app.py`.

### Run the original Streamlit application

The original Streamlit interface is still available:

```bash
streamlit run App.py
```

---

## Deployment

The original Streamlit application has been deployed on Streamlit Community Cloud:

[Open the Streamlit demo](https://fittin-b8fjdspvsosvbjwzy6jjxr.streamlit.app/)

The Flask interface can be run locally by following the instructions above.

---

## What I Learned

- **Imbalanced data needs care.** Applying SMOTE requires care around the train/test split so that evaluation remains meaningful.
- **Precomputation keeps applications responsive.** Clustering foods ahead of time allows the recommendation engine to filter and calculate portions at runtime.
- **A good model is only part of a good product.** Turning model outputs into practical serving sizes requires clear deterministic calculations alongside machine learning.
- **Hybrid systems are practical.** Combining classification, clustering, and formulas makes the recommendation process easier to inspect than relying on one black-box model.
- **Frontend and backend integration matters.** Moving from a Streamlit-only interface to a Flask-based experience introduced a separate frontend workflow and Tailwind CSS build process.

---

## Limitations & Future Work

- [ ] Verify that SMOTE is applied only to the training data and report final metrics on an untouched test set.
- [ ] Expand the food database and verify nutritional values against authoritative sources.
- [ ] Evaluate whether the micronutrient-density score improves recommendation quality.
- [ ] Add dietary restrictions and food preferences to the personalization process.
- [ ] Add unit tests for nutrition calculations and recommendation logic.
- [ ] Retrain and compare models as more data becomes available.

---

## Contributing

Suggestions, issues, and pull requests are welcome. If you have an idea to improve FITTIN, feel free to open an issue.

---

## Author

**Dhanraj Kandpal**

BCA student exploring machine learning, web development, and the engineering behind both.

[GitHub](https://github.com/dhanrajkandpal)

---

## License

No license file is currently specified in this repository. Add a license if you want to define the terms under which others may use, modify, and distribute the project.
