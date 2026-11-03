from flask import Flask, render_template, request, jsonify
from pathlib import Path

from Functions import nutrition_profile
from recommendation_adapter import generate_recommendations


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

app.config["JSON_SORT_KEYS"] = False


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ==========================================
# ASSESSMENT PAGE
# ==========================================

@app.route("/assessment", methods=["GET"])
def assessment():
    return render_template("assessment.html")


# ==========================================
# NUTRITION PROFILE API
# ==========================================

@app.route("/api/assessment", methods=["POST"])
def generate_profile():

    try:

        # ----------------------------------
        # READ REQUEST
        # ----------------------------------

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid request. Please submit assessment data."
            }), 400

        # ----------------------------------
        # EXTRACT USER INPUT
        # ----------------------------------

        age = int(data["age"])

        gender = str(data["gender"]).strip()

        height = float(data["height"])

        weight = float(data["weight"])

        activity = str(data["activity"]).strip()

        goal = str(data["goal"]).strip()

        # ----------------------------------
        # VALIDATE INPUT
        # ----------------------------------

        if not 15 <= age <= 80:
            raise ValueError("Age must be between 15 and 80.")

        if gender not in ["Male", "Female"]:
            raise ValueError("Please select a valid gender.")

        if not 100 <= height <= 250:
            raise ValueError("Height must be between 100 and 250 cm.")

        if not 25 <= weight <= 300:
            raise ValueError("Weight must be between 25 and 300 kg.")

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

        # ----------------------------------
        # BMI CALCULATION
        # ----------------------------------

        bmi = weight / ((height / 100) ** 2)

        # Existing BMI classification logic retained.
        # Your Random Forest integration can be added
        # separately once its preprocessing pipeline is verified.

        if bmi < 18.5:
            predicted_bmi_class = "Underweight"

        elif bmi < 25:
            predicted_bmi_class = "Normal"

        elif bmi < 30:
            predicted_bmi_class = "Overweight"

        else:
            predicted_bmi_class = "Obese"

        # ----------------------------------
        # NUTRITION PROFILE
        # ----------------------------------

        profile = nutrition_profile(
            age,
            gender,
            height,
            weight,
            activity,
            goal,
            predicted_bmi_class
        )

        # ----------------------------------
        # FOOD RECOMMENDATIONS
        # ----------------------------------

        recommendations = generate_recommendations(
            profile["Protein"],
            profile["Carbohydrates"],
            profile["Fat"]
        )

        # ----------------------------------
        # FINAL RESPONSE
        # ----------------------------------

        response = {
            **profile,
            "Recommendations": recommendations
        }

        return jsonify(response), 200

    # --------------------------------------
    # INPUT ERRORS
    # --------------------------------------

    except KeyError as error:

        return jsonify({
            "error": f"Missing required field: {error.args[0]}"
        }), 400

    except (ValueError, TypeError) as error:

        return jsonify({
            "error": str(error)
        }), 400

    # --------------------------------------
    # SERVER ERRORS
    # --------------------------------------

    except Exception:

        app.logger.exception(
            "An error occurred while generating the nutrition profile."
        )

        return jsonify({
            "error": "Unable to generate your nutrition profile right now. Please try again."
        }), 500


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "application": "FITTIN"
    }), 200


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )