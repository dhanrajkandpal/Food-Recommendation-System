#BMI CALCULATION
"""
Calculate the Body Mass Index (BMI) using the user's height and weight.
"""

def bmi_calculation(Height,Weight):
        if Height <= 0:
            raise ValueError("Height must be greater than 0.")
        elif Weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        Height = Height / 100
        BMI = Weight / (Height ** 2)
        return BMI

#BMR FUNCTION
"""
Calculate the Basal Metabolic Rate (BMR) using the Mifflin-St Jeor equation.
"""

def bmr_calculation(Age,Height,Weight,Gender):
        if Age <= 0:
            raise ValueError("Age must be greater than 0.")

        if Height <= 0:
            raise ValueError("Height must be greater than 0.")

        if Weight <= 0:
            raise ValueError("Weight must be greater than 0.")

        if Gender == "Male":
            return (10 * Weight) + (6.25 * Height) - (5 * Age) + 5

        elif Gender == "Female":
            return (10 * Weight) + (6.25 * Height) - (5 * Age) - 161

        else:
            raise ValueError("Gender must be 'Male' or 'Female'.")


#TDEE FUNCTION
"""
Calculate the Total Daily Energy Expenditure (TDEE) based on BMR and activity level.
"""

def TDEE_calculation(bmr,ActivityLevel):
    activity_factor = {
        "Sedentary": 1.20,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.90
    }

    if ActivityLevel not in activity_factor:
        raise ValueError("Invalid activity level.")

    return bmr * activity_factor[ActivityLevel]

#Target calories
"""
Determine the daily calorie target based on the user's fitness goal.
"""
def target_calories(TDEE_calculation,Goal):
    goal_adjustment = {
        "Fat Loss": -400,
        "Cut": -400,
        "Maintain Weight": 0,
        "Lean Bulk": 400,
        "Muscle Gain": 400
    }
    if Goal not in goal_adjustment:
        raise ValueError("Invalid fitness goal.")

    return TDEE_calculation + goal_adjustment[Goal]

#Intake
"""
Calculate the daily protein, carbohydrate, and fat requirements from the target calorie intake.
"""
def calculate_macros(target_calories):
    if target_calories <= 0:
        raise ValueError("Target calories must be greater than 0.")

    protein = (target_calories * 0.30) / 4
    carbohydrates = (target_calories * 0.40) / 4
    fat = (target_calories * 0.30) / 9

    return {
        "Protein": round(protein, 2),
        "Carbohydrates": round(carbohydrates, 2),
        "Fat": round(fat, 2)
    }

#Profile
"""
Generate a complete nutrition profile by combining BMI, BMR, TDEE, target calories, and macronutrient requirements.
"""
def nutrition_profile(
    Age,
    Gender,
    Height,
    Weight,
    ActivityLevel,
    Goal,
    PredictedBMIClass
):

    BMI = bmi_calculation(Height, Weight)

    BMR = bmr_calculation(Age, Height, Weight, Gender)

    TDEE_Value = TDEE_calculation(BMR, ActivityLevel)

    TargetCalories = target_calories(TDEE_Value, Goal)

    Macros = calculate_macros(TargetCalories)

    return {
        "Predicted BMI Class": PredictedBMIClass,
        "BMI": round(BMI, 2),
        "BMR": round(BMR, 2),
        "TDEE": round(TDEE_Value, 2),
        "Target Calories": round(TargetCalories, 2),
        "Protein": Macros["Protein"],
        "Carbohydrates": Macros["Carbohydrates"],
        "Fat": Macros["Fat"]
    }

