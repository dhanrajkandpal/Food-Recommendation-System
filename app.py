import os
import uuid
import sqlite3
import logging

from datetime import timedelta

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    g
)

from Functions import nutrition_profile
from recommendation_adapter import generate_recommendations


# =========================================================
# 1. APPLICATION CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "fittin-development-secret-key"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=365)
)

app.logger.setLevel(logging.INFO)


# =========================================================
# 2. DATABASE CONFIGURATION
# =========================================================

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

os.makedirs(INSTANCE_DIR, exist_ok=True)

DATABASE = os.path.join(
    INSTANCE_DIR,
    "fittin_visitors.db"
)


def initialize_database():
    """Create the visitor database and table if necessary."""

    connection = sqlite3.connect(DATABASE)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                visitor_id TEXT PRIMARY KEY,
                first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()


initialize_database()


def get_database():
    """Get a database connection for the current request."""

    if "database" not in g:
        g.database = sqlite3.connect(
            DATABASE,
            timeout=10
        )

        g.database.row_factory = sqlite3.Row

    return g.database


@app.teardown_appcontext
def close_database(_exception=None):
    """Close the database connection after each request."""

    database = g.pop("database", None)

    if database is not None:
        database.close()


# =========================================================
# 3. VISITOR COUNTER
# =========================================================

def get_visitor_count():
    """Return the total number of unique browser identifiers."""

    database = get_database()

    result = database.execute("""
        SELECT COUNT(*) AS total
        FROM visitors
    """).fetchone()

    return result["total"]


def register_visitor():
    """
    Register a browser once.

    Refreshing the page does not increase the count.
    A new browser session receives a new anonymous ID.
    """

    if "visitor_id" not in session:
        session["visitor_id"] = uuid.uuid4().hex

    session.permanent = True

    visitor_id = session["visitor_id"]

    database = get_database()

    database.execute("""
        INSERT OR IGNORE INTO visitors (visitor_id)
        VALUES (?)
    """, (visitor_id,))

    database.commit()

    return get_visitor_count()


@app.before_request
def track_website_visitors():
    """
    Count visitors accessing actual website pages.

    Homepage visits count towards the total, but the
    homepage template will not display the counter.
    """

    if request.endpoint in ("home", "assessment"):
        register_visitor()


# =========================================================
# 4. TEMPLATE CONTEXT
# =========================================================

@app.context_processor
def inject_visitor_count():
    """Make the visitor count available to templates."""

    return {
        "visitor_count": get_visitor_count()
    }


# =========================================================
# 5. HOMEPAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# 6. ASSESSMENT PAGE
# =========================================================

@app.route("/assessment")
def assessment():

    return render_template(
        "assessment.html",
        visitor_count=get_visitor_count()
    )


# =========================================================
# 7. VISITOR COUNT API
# =========================================================

@app.route("/api/visitor-count", methods=["GET"])
def visitor_count_api():

    return jsonify({
        "success": True,
        "visitor_count": get_visitor_count()
    })


# =========================================================
# 8. ASSESSMENT INPUT VALIDATION
# =========================================================

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

        if field not in data:
            raise ValueError(
                f"Missing required field: {field}"
            )

        if data[field] is None or str(data[field]).strip() == "":
            raise ValueError(
                f"{field.capitalize()} cannot be empty."
            )

    try:
        age = int(data["age"])
        height = float(data["height"])
        weight = float(data["weight"])

    except (ValueError, TypeError) as error:
        raise ValueError(
            "Age, height and weight must be valid numbers."
        ) from error

    gender = data["gender"]
    activity = data["activity"]
    goal = data["goal"]

    if not 15 <= age <= 100:
        raise ValueError(
            "Age must be between 15 and 100."
        )

    if not 100 <= height <= 250:
        raise ValueError(
            "Height must be between 100 and 250 cm."
        )

    if not 25 <= weight <= 300:
        raise ValueError(
            "Weight must be between 25 and 300 kg."
        )

    allowed_genders = ["Male", "Female"]

    if gender not in allowed_genders:
        raise ValueError(
            "Please select a valid gender."
        )

    allowed_activities = [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Super Active"
    ]

    if activity not in allowed_activities:
        raise ValueError(
            "Please select a valid activity level."
        )

    allowed_goals = [
        "Fat Loss",
        "Cut",
        "Maintain Weight",
        "Lean Bulk",
        "Muscle Gain"
    ]

    if goal not in allowed_goals:
        raise ValueError(
            "Please select a valid fitness goal."
        )

    return {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity": activity,
        "goal": goal
    }


# =========================================================
# 9. BMI CLASSIFICATION
# =========================================================

def classify_bmi(bmi):

    if bmi < 18.5:
        return "Underweight"

    if bmi < 25:
        return "Normal"

    if bmi < 30:
        return "Overweight"

    return "Obese"


# =========================================================
# 10. NUTRITION ASSESSMENT API
# =========================================================

@app.route("/api/assessment", methods=["POST"])
def generate_profile():

    if not request.is_json:
        return jsonify({
            "error": "Request must contain JSON data."
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid assessment data."
        }), 400

    try:

        # Validate user input.
        user = validate_assessment_data(data)

        age = user["age"]
        gender = user["gender"]
        height = user["height"]
        weight = user["weight"]
        activity = user["activity"]
        goal = user["goal"]

        # Calculate BMI.
        bmi = weight / ((height / 100) ** 2)

        predicted_bmi_class = classify_bmi(bmi)

        # Generate nutritional profile using Functions.py.
        profile = nutrition_profile(
            age,
            gender,
            height,
            weight,
            activity,
            goal,
            predicted_bmi_class
        )

        # Generate food recommendations using existing adapter.
        recommendations = generate_recommendations(
            profile["Protein"],
            profile["Carbohydrates"],
            profile["Fat"]
        )

        response_data = {
            **profile,
            "Recommendations": recommendations
        }

        return jsonify(response_data), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except (KeyError, TypeError) as error:

        app.logger.exception(
            "Invalid nutrition profile data."
        )

        return jsonify({
            "error": "Invalid nutrition profile data."
        }), 500

    except (sqlite3.Error, OSError) as error:

        app.logger.exception(
            "Database or file operation failed."
        )

        return jsonify({
            "error": "A server resource could not be accessed."
        }), 500

    # noinspection PyBroadException
    except Exception:

        app.logger.exception(
            "Unexpected assessment generation error."
        )

        return jsonify({
            "error": "Unable to generate recommendations right now."
        }), 500


# =========================================================
# 11. HEALTH CHECK
# =========================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "application": "FITTIN",
        "status": "healthy",
        "visitor_counter": "active"
    })


# =========================================================
# 12. APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )