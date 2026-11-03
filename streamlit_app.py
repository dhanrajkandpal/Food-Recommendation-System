from flask import Flask, render_template, request, jsonify

from Functions import nutrition_profile
from recommendation_adapter import generate_recommendations

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/api/assessment", methods=["POST"])
def generate_profile():
    try:
        data = request.get_json(force=True)

        age = int(data["age"])
        gender = data["gender"]
        height = float(data["height"])
        weight = float(data["weight"])
        activity = data["activity"]
        goal = data["goal"]

        bmi = weight / ((height / 100) ** 2)

        # Current BMI category logic retained pending verified model integration.
        if bmi < 18.5:
            predicted_bmi_class = "Underweight"
        elif bmi < 25:
            predicted_bmi_class = "Normal"
        elif bmi < 30:
            predicted_bmi_class = "Overweight"
        else:
            predicted_bmi_class = "Obese"

        profile = nutrition_profile(
            age,
            gender,
            height,
            weight,
            activity,
            goal,
            predicted_bmi_class
        )

        recommendations = generate_recommendations(
            profile["Protein"],
            profile["Carbohydrates"],
            profile["Fat"]
        )

        return jsonify({**profile, "Recommendations": recommendations})

    except (ValueError, TypeError, KeyError) as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        app.logger.exception("Assessment generation failed")
        return jsonify({"error": "Unable to generate recommendations right now."}), 500


if __name__ == "__main__":
    app.run(debug=True)
