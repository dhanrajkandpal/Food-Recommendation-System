from flask import Flask, render_template, request, jsonify
from pathlib import Path

from Functions import nutrition_profile
from recommendation_adapter import generate_recommendations


# =====================================================
# FLASK CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

app.config["JSON_SORT_KEYS"] = False


# =====================================================
# HOMEPAGE
# =====================================================

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# =====================================================
# ASSESSMENT PAGE
# =====================================================

@app.route("/assessment", methods=["GET"])
def assessment():
    return render_template("assessment.html")


# =====================================================
# INPUT VALIDATION
# =====================================================

def validate_assessment_data(data):

    required_fields = [
        "age",
        "gender",
        "height",
        "weight",
        "activity",
        "goal"
    ]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            raise ValueError(f"Please provide your {field}.")

    try:
        age = int(data["age"])
        height = float(data["height"])
        weight = float(data["weight"])
    except (ValueError, TypeError):
        raise ValueError("Age, height and weight must be valid numbers.")

    gender = str(data["gender"]).strip()
    activity = str(data["activity"]).strip()
    goal = str(data["goal"]).strip()

    if not 15 <= age <= 80:
        raise ValueError("Age must be between 15 and 80.")

    if not 100 <= height <= 250:
        raise ValueError("Height must be between 100 and 250 cm.")

    if not 25 <= weight <= 300:
        raise ValueError("Weight must be between 25 and 300 kg.")

    if gender not in ["Male", "Female"]:
        raise ValueError("Please select a valid gender.")

    valid_activities = [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Super Active"
    ]

    if activity not in valid_activities:
        raise ValueError("Please select a valid activity level.")

    valid_goals = [
        "Fat Loss",
        "Cut",
        "Maintain Weight",
        "Lean Bulk",
        "Muscle Gain"
    ]

    if goal not in valid_goals:
        raise ValueError("Please select a valid fitness goal.")

    return {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity": activity,
        "goal": goal
    }


# =====================================================
# BMI CLASSIFICATION
# =====================================================

def classify_bmi(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


# =====================================================
# ASSESSMENT API
# =====================================================

@app.route("/api/assessment", methods=["POST"])
def generate_profile():

    try:

        # ---------------------------------------------
        # 1. RECEIVE DATA
        # ---------------------------------------------

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid request. Please submit valid assessment data."
            }), 400


        # ---------------------------------------------
        # 2. VALIDATE DATA
        # ---------------------------------------------

        user = validate_assessment_data(data)

        age = user["age"]
        gender = user["gender"]
        height = user["height"]
        weight = user["weight"]
        activity = user["activity"]
        goal = user["goal"]


        # ---------------------------------------------
        # 3. CALCULATE BMI
        # ---------------------------------------------

        bmi = weight / ((height / 100) ** 2)

        predicted_bmi_class = classify_bmi(bmi)


        # ---------------------------------------------
        # 4. GENERATE NUTRITION PROFILE
        # ---------------------------------------------

        profile = nutrition_profile(
            age,
            gender,
            height,
            weight,
            activity,
            goal,
            predicted_bmi_class
        )


        # ---------------------------------------------
        # 5. GENERATE FOOD RECOMMENDATIONS
        # ---------------------------------------------

        recommendations = generate_recommendations(
            profile["Protein"],
            profile["Carbohydrates"],
            profile["Fat"]
        )


        # ---------------------------------------------
        # 6. RETURN RESULTS
        # ---------------------------------------------

        response = {
            **profile,
            "Recommendations": recommendations
        }

        return jsonify(response), 200


    # ---------------------------------------------
    # VALIDATION ERRORS
    # ---------------------------------------------

    except (ValueError, TypeError, KeyError) as error:

        return jsonify({
            "error": str(error)
        }), 400


    # ---------------------------------------------
    # SERVER ERRORS
    # ---------------------------------------------

    except Exception:

        app.logger.exception(
            "FITTIN assessment generation failed."
        )

        return jsonify({
            "error": (
                "Something went wrong while generating "
                "your nutrition profile. Please try again."
            )
        }), 500


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "application": "FITTIN"
    }), 200


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )