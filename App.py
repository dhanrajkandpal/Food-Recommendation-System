import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="FITTIN // Biometric & Nutrition Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State for Submission
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# High-End Cyberpunk / Obsidian & Electric Indigo Glassmorphism Theme (No All-Green Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background: #030712;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(236, 72, 153, 0.1) 0%, transparent 45%),
            linear-gradient(135deg, #030712 0%, #0F172A 50%, #0B0F19 100%);
        background-attachment: fixed;
        color: #F9FAFB;
        min-height: 100vh;
        animation: backgroundShift 18s ease infinite alternate;
    }

    @keyframes backgroundShift {
        0% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(15deg); }
        100% { filter: hue-rotate(0deg); }
    }

    /* Cybernetic Glowing Hero Banner */
    .fittin-hero {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.8) 50%, rgba(49, 46, 129, 0.7) 100%);
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 28px;
        padding: 2.75rem 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 50px rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        position: relative;
        overflow: hidden;
    }

    .fittin-hero::before {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        animation: pulseOrb 6s ease-in-out infinite alternate;
    }

    @keyframes pulseOrb {
        0% { transform: scale(1); opacity: 0.6; }
        100% { transform: scale(1.2); opacity: 1; }
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #FFFFFF 0%, #C7D2FE 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        font-weight: 400;
        line-height: 1.6;
        max-width: 900px;
    }

    /* Cyber Glass Cards */
    .fittin-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.5));
        border: 1px solid rgba(51, 65, 85, 0.7);
        border-radius: 22px;
        padding: 1.75rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: #F8FAFC;
    }

    .fittin-card:hover {
        border-color: rgba(129, 140, 248, 0.6);
        box-shadow: 0 25px 50px rgba(99, 102, 241, 0.25);
        transform: translateY(-3px);
    }

    /* Section Headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 1.75rem;
        margin-bottom: 1.0rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 1px solid rgba(51, 65, 85, 0.6);
        padding-bottom: 0.5rem;
    }

    /* Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.75rem 1.75rem;
        font-weight: 700;
        font-size: 1.05rem;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
        transition: all 0.25s ease;
        width: 100%;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }

    .metric-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.35);
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. CALCULATIONS
# ==========================================
def bmi_calculation(Height, Weight):
    if Height <= 0 or Weight <= 0:
        raise ValueError("Height and Weight must be positive.")
    return Weight / ((Height / 100) ** 2)


def bmr_calculation(Age, Height, Weight, Gender):
    if Gender == "Male":
        return (10 * Weight) + (6.25 * Height) - (5 * Age) + 5
    elif Gender == "Female":
        return (10 * Weight) + (6.25 * Height) - (5 * Age) - 161
    else:
        return (10 * Weight) + (6.25 * Height) - (5 * Age) + 5


def TDEE_calculation(bmr, ActivityLevel):
    factors = {
        "Sedentary": 1.20,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.90
    }
    return bmr * factors.get(ActivityLevel, 1.2)


def target_calories(tdee, Goal):
    adjustments = {
        "Fat Loss": -400,
        "Cut": -400,
        "Maintain Weight": 0,
        "Lean Bulk": 400,
        "Muscle Gain": 400
    }
    return tdee + adjustments.get(Goal, 0)


def calculate_macros(target_cal):
    protein = (target_cal * 0.30) / 4
    carbs = (target_cal * 0.40) / 4
    fat = (target_cal * 0.30) / 9
    return {
        "Protein": round(protein, 1),
        "Carbohydrates": round(carbs, 1),
        "Fat": round(fat, 1)
    }


def nutrition_profile(Age, Gender, Height, Weight, ActivityLevel, Goal, BodyClass):
    bmi = bmi_calculation(Height, Weight)
    bmr = bmr_calculation(Age, Height, Weight, Gender)
    tdee = TDEE_calculation(bmr, ActivityLevel)
    t_cal = target_calories(tdee, Goal)
    macros = calculate_macros(t_cal)
    return {
        "Body Class": BodyClass,
        "BMI": round(bmi, 2),
        "BMR": round(bmr, 1),
        "TDEE": round(tdee, 1),
        "Target Calories": round(t_cal, 1),
        "Protein": macros["Protein"],
        "Carbohydrates": macros["Carbohydrates"],
        "Fat": macros["Fat"]
    }


@st.cache_resource
def load_food_database():
    try:
        return pd.read_csv('clustered_food_database.csv')
    except Exception:
        return None


food_db = load_food_database()


def filter_foods(db, allowed_clusters, prep="cooked"):
    filtered = db[
        (db['clusters'].isin(allowed_clusters)) &
        (db['preparation'] == prep)
        ].copy()
    filtered = filtered[~filtered['food'].str.contains('liver|lungs|kidney|heart|spleen|ostrich|brain', case=False)]
    return filtered.sort_values(by='micronutrient_density', ascending=False)


def select_diverse_food(sorted_df, pool_size=150, num_items=1):
    if sorted_df is None or len(sorted_df) == 0:
        return None
    actual_pool = min(pool_size, len(sorted_df))
    return sorted_df.head(actual_pool).sample(n=min(num_items, actual_pool))


def calculate_serving_size(row, target_grams, macro_col):
    per_100g = row[macro_col].values[0]
    if per_100g <= 0:
        return 0
    return round((target_grams / per_100g) * 100, 1)


def get_body_class(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    elif 30 <= bmi < 35:
        return "Obese Class 1"
    elif 35 <= bmi < 40:
        return "Obese Class 2"
    else:
        return "Obese Class 3"


# ==========================================
# 2. APP HEADER
# ==========================================
st.markdown("""
<div class="fittin-hero">
    <div class="hero-title">FITTIN</div>
    <div class="hero-subtitle">
        Advanced biometric telemetry and intelligent nutritional optimization engine.
    </div>
</div>
""", unsafe_allow_html=True)

if food_db is None:
    st.error("Critical Error: `clustered_food_database.csv` not found in root directory.")
else:
    if not st.session_state.submitted:
        st.markdown("<div class='section-title'>User Biometric Intake</div>", unsafe_allow_html=True)

        with st.form("intake_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.slider("Age (Years)", 15, 80, 22)
                gender = st.selectbox("Gender", ["Male", "Female"])
                height = st.number_input("Height (cm)", 100.0, 250.0, 175.0, 0.5)
                weight = st.number_input("Weight (kg)", 30.0, 250.0, 75.0, 0.5)
            with col2:
                activity = st.selectbox(
                    "Activity Level",
                    ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"],
                    index=3
                )
                objective = st.selectbox(
                    "Primary Objective",
                    ["Fat Loss", "Cut", "Maintain Weight", "Lean Bulk", "Muscle Gain"],
                    index=3
                )

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Compute Profile & Launch Engine")

            if submit_btn:
                st.session_state.submitted = True
                st.session_state.age = age
                st.session_state.gender = gender
                st.session_state.height = height
                st.session_state.weight = weight
                st.session_state.activity = activity
                st.session_state.objective = objective
                st.rerun()

    else:
        age = st.session_state.age
        gender = st.session_state.gender
        height = st.session_state.height
        weight = st.session_state.weight
        activity = st.session_state.activity
        objective = st.session_state.objective

        bmi_val = weight / ((height / 100) ** 2)
        body_class = get_body_class(bmi_val)

        profile = nutrition_profile(
            Age=age,
            Gender=gender,
            Height=height,
            Weight=weight,
            ActivityLevel=activity,
            Goal=objective,
            BodyClass=body_class
        )

        col_nav1, col_nav2 = st.columns([6, 4])
        with col_nav1:
            view_mode = st.radio(
                "Navigation Mode",
                ["Processed Info", "Food Recommendations"],
                horizontal=True,
                label_visibility="collapsed"
            )
        with col_nav2:
            if st.button("Edit Biometric Intake"):
                st.session_state.submitted = False
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if view_mode == "Processed Info":
            st.markdown("<div class='section-title'>Metabolic Telemetry Summary</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"""
                <div class="fittin-card">
                    <span class="metric-badge">BMI INDEX</span>
                    <h2 style="font-size: 2.25rem; font-weight: 800; margin: 0.75rem 0 0.25rem 0; color: #FFFFFF;">{profile['BMI']}</h2>
                    <span style="font-size: 0.85rem; font-weight: 600; color: #34D399;">{profile['Body Class']}</span>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="fittin-card">
                    <span class="metric-badge">BASAL ENERGY</span>
                    <h2 style="font-size: 2.25rem; font-weight: 800; margin: 0.75rem 0 0.25rem 0; color: #FFFFFF;">{profile['BMR']}</h2>
                    <span style="font-size: 0.85rem; color: #94A3B8;">kcal / day at rest</span>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="fittin-card">
                    <span class="metric-badge">TOTAL EXPENDITURE</span>
                    <h2 style="font-size: 2.25rem; font-weight: 800; margin: 0.75rem 0 0.25rem 0; color: #FFFFFF;">{profile['TDEE']}</h2>
                    <span style="font-size: 0.85rem; color: #34D399;">kcal maintenance burn</span>
                </div>
                """, unsafe_allow_html=True)
            with c4:
                st.markdown(f"""
                <div class="fittin-card">
                    <span class="metric-badge">OBJECTIVE TARGET</span>
                    <h2 style="font-size: 2.25rem; font-weight: 800; margin: 0.75rem 0 0.25rem 0; color: #FFFFFF;">{profile['Target Calories']}</h2>
                    <span style="font-size: 0.85rem; font-weight: 600; color: #818CF8;">{objective} Target</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Macronutrient Distribution</div>", unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns([6, 4])
            with chart_col1:
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f"""
                    <div class="fittin-card" style="border-left: 4px solid #3B82F6; padding: 1.5rem;">
                        <span class="metric-badge" style="background: rgba(59, 130, 246, 0.15); color: #60A5FA;">PROTEIN</span>
                        <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0.5rem 0; color: #FFFFFF;">{profile['Protein']}g</h2>
                        <p style="font-size: 0.85rem; margin: 0; color: #94A3B8;">{round(profile['Protein'] * 4)} kcal (30%)</p>
                    </div>
                    """, unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""
                    <div class="fittin-card" style="border-left: 4px solid #10B981; padding: 1.5rem;">
                        <span class="metric-badge" style="background: rgba(16, 185, 129, 0.15); color: #34D399;">CARBS</span>
                        <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0.5rem 0; color: #FFFFFF;">{profile['Carbohydrates']}g</h2>
                        <p style="font-size: 0.85rem; margin: 0; color: #94A3B8;">{round(profile['Carbohydrates'] * 4)} kcal (40%)</p>
                    </div>
                    """, unsafe_allow_html=True)
                with m3:
                    st.markdown(f"""
                    <div class="fittin-card" style="border-left: 4px solid #F59E0B; padding: 1.5rem;">
                        <span class="metric-badge" style="background: rgba(245, 158, 11, 0.15); color: #FBBF24;">FATS</span>
                        <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0.5rem 0; color: #FFFFFF;">{profile['Fat']}g</h2>
                        <p style="font-size: 0.85rem; margin: 0; color: #94A3B8;">{round(profile['Fat'] * 9)} kcal (30%)</p>
                    </div>
                    """, unsafe_allow_html=True)

            with chart_col2:
                macro_fig = px.pie(
                    names=['Protein', 'Carbohydrates', 'Healthy Fats'],
                    values=[profile['Protein'] * 4, profile['Carbohydrates'] * 4, profile['Fat'] * 9],
                    hole=0.65,
                    color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B']
                )
                macro_fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#F8FAFC', family='Plus Jakarta Sans'),
                    showlegend=False,
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=220
                )
                macro_fig.update_traces(textposition='inside', textinfo='percent')
                st.plotly_chart(macro_fig, use_container_width=True)

        else:
            st.markdown("<div class='section-title'>Precision Food Recommendations & Diet Meter</div>",
                        unsafe_allow_html=True)
            st.markdown(
                "<p style='color: #94A3B8;'>Configure your macro source variety sliders directly with your food recommendations below.</p>",
                unsafe_allow_html=True)

            meter_col1, meter_col2, meter_col3, meter_col4 = st.columns([4, 2, 2, 2])
            with meter_col1:
                if st.button("Synthesize Fresh Meal Plan"):
                    st.rerun()
            with meter_col2:
                p_split = st.slider("Protein Sources", 1, 4, 3)
            with meter_col3:
                c_split = st.slider("Carb Sources", 1, 4, 2)
            with meter_col4:
                f_split = st.slider("Fat Sources", 1, 4, 2)

            st.markdown("<br>", unsafe_allow_html=True)
            rc1, rc2, rc3 = st.columns(3)

            with rc1:
                st.markdown("### Protein Sources")
                p_pool = filter_foods(food_db, [4, 5])
                p_sel = select_diverse_food(p_pool, pool_size=150, num_items=p_split)
                p_target = round(profile['Protein'] / p_split, 1)

                if p_sel is not None:
                    for _, row in p_sel.iterrows():
                        portion = calculate_serving_size(pd.DataFrame([row]), p_target, "Protein (g per 100g)")
                        st.markdown(f"""
                        <div class="fittin-card" style="margin-bottom: 1rem; padding: 1.5rem; border-left: 4px solid #3B82F6;">
                            <h4 style="color: #60A5FA; margin: 0 0 0.35rem 0; font-size: 1.15rem;">{row['food'].title()}</h4>
                            <span style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">{portion}g</span>
                            <span style="font-size: 0.85rem; display: block; margin-top: 0.25rem; color: #94A3B8;">Yields ~{p_target}g Protein</span>
                        </div>
                        """, unsafe_allow_html=True)

            with rc2:
                st.markdown("### Carbohydrate Sources")
                c_pool = filter_foods(food_db, [1, 7])
                c_sel = select_diverse_food(c_pool, pool_size=150, num_items=c_split)
                c_target = root = round(profile['Carbohydrates'] / c_split, 1)

                if c_sel is not None:
                    for _, row in c_sel.iterrows():
                        portion = calculate_serving_size(pd.DataFrame([row]), c_target, "Carbohydrates (g per 100g)")
                        st.markdown(f"""
                        <div class="fittin-card" style="margin-bottom: 1rem; padding: 1.5rem; border-left: 4px solid #10B981;">
                            <h4 style="color: #34D399; margin: 0 0 0.35rem 0; font-size: 1.15rem;">{row['food'].title()}</h4>
                            <span style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">{portion}g</span>
                            <span style="font-size: 0.85rem; display: block; margin-top: 0.25rem; color: #94A3B8;">Yields ~{c_target}g Carbs</span>
                        </div>
                        """, unsafe_allow_html=True)

            with rc3:
                st.markdown("### Healthy Fat Sources")
                f_pool = filter_foods(food_db, [2, 3], prep="raw")
                if len(f_pool) == 0:
                    f_pool = filter_foods(food_db, [2, 3], prep="other")
                f_sel = select_diverse_food(f_pool, pool_size=150, num_items=f_split)
                f_target = round(profile['Fat'] / f_split, 1)

                if f_sel is not None:
                    for _, row in f_sel.iterrows():
                        portion = calculate_serving_size(pd.DataFrame([row]), f_target, "Fat (g per 100g)")
                        st.markdown(f"""
                        <div class="fittin-card" style="margin-bottom: 1rem; padding: 1.5rem; border-left: 4px solid #F59E0B;">
                            <h4 style="color: #FBBF24; margin: 0 0 0.35rem 0; font-size: 1.15rem;">{row['food'].title()}</h4>
                            <span style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">{portion}g</span>
                            <span style="font-size: 0.85rem; display: block; margin-top: 0.25rem; color: #94A3B8;">Yields ~{f_target}g Fats</span>
                        </div>
                        """, unsafe_allow_html=True)