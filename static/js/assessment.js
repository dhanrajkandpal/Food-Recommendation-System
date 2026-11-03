document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    // =====================================================
    // 1. DOM ELEMENTS
    // =====================================================

    const form = document.getElementById("assessmentForm");

    const steps = Array.from(
        document.querySelectorAll(".form-step")
    );

    const stepDots = document.querySelectorAll(".step-dot");

    const previousBtn = document.getElementById("previousBtn");

    const nextBtn = document.getElementById("nextBtn");

    const submitBtn = document.getElementById("submitBtn");

    const progressFill = document.getElementById("progressFill");

    const stepLabel = document.getElementById("stepLabel");

    const stepName = document.getElementById("stepName");

    const formError = document.getElementById("formError");

    const resultSection = document.getElementById("resultSection");

    const resultGrid = document.getElementById("resultGrid");

    const macroResults = document.getElementById("macroResults");

    const recommendationResults = document.getElementById(
        "recommendationResults"
    );

    const editAssessment = document.getElementById("editAssessment");


    // =====================================================
    // 2. CONFIGURATION
    // =====================================================

    const totalSteps = steps.length;

    const stepNames = [
        "Personal Details",
        "Your Lifestyle",
        "Your Goals"
    ];

    let currentStep = 0;

    let isSubmitting = false;


    const numberFormatter = new Intl.NumberFormat("en-IN", {
        maximumFractionDigits: 1
    });


    // =====================================================
    // 3. ELEMENT VALIDATION
    // =====================================================

    if (
        !form ||
        totalSteps !== 3 ||
        !previousBtn ||
        !nextBtn ||
        !submitBtn ||
        !resultSection ||
        !resultGrid ||
        !macroResults ||
        !recommendationResults
    ) {

        console.error(
            "FITTIN: Required assessment elements are missing."
        );

        return;
    }


    // =====================================================
    // 4. HELPER FUNCTIONS
    // =====================================================

    function formatNumber(value, decimals = 1) {

        const number = Number(value);

        if (!Number.isFinite(number)) {
            return "N/A";
        }

        return new Intl.NumberFormat("en-IN", {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(number);

    }


    function createElement(tag, className = "", text = "") {

        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        element.textContent = text;

        return element;

    }


    function showError(message) {

        if (!formError) return;

        formError.textContent = message;

        formError.hidden = false;

        formError.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }


    function hideError() {

        if (!formError) return;

        formError.textContent = "";

        formError.hidden = true;

    }


    function scrollToTop() {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }


    // =====================================================
    // 5. MULTI-STEP NAVIGATION
    // =====================================================

    function showStep(step) {

        if (step < 0 || step >= totalSteps) {
            return;
        }

        currentStep = step;


        // Display active step

        steps.forEach((element, index) => {

            element.classList.toggle(
                "active",
                index === step
            );

        });


        // Update progress indicators

        stepDots.forEach((dot, index) => {

            dot.classList.toggle(
                "active",
                index <= step
            );

        });


        // Update progress bar

        if (progressFill) {

            const progress =
                ((step + 1) / totalSteps) * 100;

            progressFill.style.width = `${progress}%`;

        }


        // Update step label

        if (stepLabel) {

            stepLabel.textContent =
                `STEP ${step + 1} OF ${totalSteps}`;

        }


        // Update step name

        if (stepName) {

            stepName.textContent =
                stepNames[step];

        }


        // Previous button

        previousBtn.hidden = step === 0;


        // Continue button

        nextBtn.hidden = step === totalSteps - 1;


        // Submit button

        submitBtn.hidden = step !== totalSteps - 1;


        hideError();

        scrollToTop();

    }


    // =====================================================
    // 6. VALIDATE CURRENT STEP
    // =====================================================

    function validateCurrentStep() {

        const activeStep = steps[currentStep];

        if (!activeStep) {
            return false;
        }


        const inputs = activeStep.querySelectorAll(
            "input, select, textarea"
        );


        for (const input of inputs) {

            if (!input.checkValidity()) {

                input.reportValidity();

                return false;

            }

        }


        return true;

    }


    // =====================================================
    // 7. NEXT BUTTON
    // =====================================================

    nextBtn.addEventListener("click", () => {

        if (!validateCurrentStep()) {
            return;
        }

        if (currentStep < totalSteps - 1) {

            showStep(currentStep + 1);

        }

    });


    // =====================================================
    // 8. PREVIOUS BUTTON
    // =====================================================

    previousBtn.addEventListener("click", () => {

        if (currentStep > 0) {

            showStep(currentStep - 1);

        }

    });


    // =====================================================
    // 9. COLLECT FORM DATA
    // =====================================================

    function collectAssessmentData() {

        const formData = new FormData(form);

        return {

            age: Number(formData.get("age")),

            gender: formData.get("gender"),

            height: Number(formData.get("height")),

            weight: Number(formData.get("weight")),

            activity: formData.get("activity"),

            goal: formData.get("goal")

        };

    }


    // =====================================================
    // 10. SUBMIT ASSESSMENT
    // =====================================================

    form.addEventListener("submit", async (event) => {

        event.preventDefault();


        if (isSubmitting) {
            return;
        }


        if (!validateCurrentStep()) {
            return;
        }


        hideError();


        const payload = collectAssessmentData();


        // Prevent incomplete submission

        for (const [key, value] of Object.entries(payload)) {

            if (
                value === null ||
                value === "" ||
                value === undefined ||
                (
                    typeof value === "number" &&
                    !Number.isFinite(value)
                )
            ) {

                showError(
                    `Please provide a valid value for ${key}.`
                );

                return;

            }

        }


        // Loading state

        isSubmitting = true;

        const originalButtonText = submitBtn.textContent;

        submitBtn.disabled = true;

        submitBtn.textContent =
            "Calculating your profile...";


        try {

            // ---------------------------------------------
            // API REQUEST
            // ---------------------------------------------

            const response = await fetch("/api/assessment", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });


            // ---------------------------------------------
            // READ RESPONSE
            // ---------------------------------------------

            const result = await response.json();


            if (!response.ok) {

                throw new Error(
                    result.error ||
                    "Unable to calculate your nutrition profile."
                );

            }


            // ---------------------------------------------
            // VALIDATE RESPONSE
            // ---------------------------------------------

            if (!result || typeof result !== "object") {

                throw new Error(
                    "The server returned an invalid response."
                );

            }


            const requiredResults = [
                "Predicted BMI Class",
                "BMI",
                "BMR",
                "TDEE",
                "Target Calories",
                "Protein",
                "Carbohydrates",
                "Fat"
            ];


            for (const key of requiredResults) {

                if (
                    result[key] === undefined ||
                    result[key] === null
                ) {

                    throw new Error(
                        `The server response is missing ${key}.`
                    );

                }

            }


            // ---------------------------------------------
            // DISPLAY RESULTS
            // ---------------------------------------------

            displayResults(result);


        } catch (error) {

            console.error(
                "FITTIN assessment error:",
                error
            );

            showError(
                error.message ||
                "Something went wrong. Please try again."
            );


        } finally {

            isSubmitting = false;

            submitBtn.disabled = false;

            submitBtn.textContent = originalButtonText;

        }

    });


    // =====================================================
    // 11. DISPLAY RESULTS
    // =====================================================

    function displayResults(profile) {

        if (!profile || typeof profile !== "object") {

            showError(
                "Unable to display your nutrition profile."
            );

            return;

        }


        // Hide form

        form.hidden = true;


        // Show results

        resultSection.hidden = false;


        hideError();


        // Generate result sections

        renderMetrics(profile);

        renderMacros(profile);

        renderRecommendations(
            profile.Recommendations
        );


        scrollToTop();

    }


    // =====================================================
    // 12. BIOMETRIC METRICS
    // =====================================================

    function renderMetrics(profile) {

        resultGrid.replaceChildren();


        const metrics = [

            {
                label: "BMI Classification",

                value: profile["Predicted BMI Class"],

                unit: "",

                featured: false

            },

            {
                label: "Body Mass Index",

                value: formatNumber(profile.BMI),

                unit: "BMI",

                featured: false

            },

            {
                label: "Basal Metabolic Rate",

                value: formatNumber(profile.BMR, 0),

                unit: "kcal/day",

                featured: false

            },

            {
                label: "Daily Energy Expenditure",

                value: formatNumber(profile.TDEE, 0),

                unit: "kcal/day",

                featured: false

            },

            {
                label: "Daily Calorie Target",

                value: formatNumber(profile["Target Calories"], 0),

                unit: "kcal/day",

                featured: true

            }

        ];


        metrics.forEach((metric) => {

            const card = createElement(
                "article",
                `result-item${metric.featured ? " featured" : ""}`
            );


            const label = createElement(
                "span",
                "result-label",
                metric.label
            );


            const value = createElement(
                "strong",
                "result-value",
                String(metric.value ?? "N/A")
            );


            const unit = createElement(
                "span",
                "result-unit",
                metric.unit
            );


            card.append(label, value, unit);

            resultGrid.appendChild(card);

        });

    }


    // =====================================================
    // 13. MACRONUTRIENT BREAKDOWN
    // =====================================================

    function renderMacros(profile) {

        macroResults.replaceChildren();


        const targetCalories =
            Number(profile["Target Calories"]);


        const macros = [

            {
                name: "Protein",

                grams: Number(profile.Protein),

                caloriesPerGram: 4,

                className: "protein"

            },

            {
                name: "Carbohydrates",

                grams: Number(profile.Carbohydrates),

                caloriesPerGram: 4,

                className: "carbs"

            },

            {
                name: "Fat",

                grams: Number(profile.Fat),

                caloriesPerGram: 9,

                className: "fat"

            }

        ];


        macros.forEach((macro) => {

            const grams = Number.isFinite(macro.grams)
                ? macro.grams
                : 0;


            const calories =
                grams * macro.caloriesPerGram;


            const percentage =
                Number.isFinite(targetCalories) &&
                targetCalories > 0

                    ? (calories / targetCalories) * 100

                    : 0;


            // Main row

            const row = createElement(
                "div",
                `macro-row ${macro.className}`
            );


            // Header

            const header = createElement(
                "div",
                "macro-header"
            );


            const name = createElement(
                "span",
                "macro-name",
                macro.name
            );


            const amount = createElement(
                "strong",
                "macro-amount",
                `${formatNumber(grams)} g`
            );


            header.append(name, amount);


            // Progress bar

            const track = createElement(
                "div",
                "macro-track"
            );


            const bar = createElement(
                "div",
                "macro-bar"
            );


            bar.style.width =
                `${Math.min(100, Math.max(0, percentage))}%`;


            track.appendChild(bar);


            // Details

            const details = createElement(
                "div",
                "macro-details"
            );


            const calorieText = createElement(
                "span",
                "macro-calories",
                `${formatNumber(calories, 0)} kcal`
            );


            const percentageText = createElement(
                "span",
                "macro-percentage",
                `${formatNumber(percentage)}%`
            );


            details.append(
                calorieText,
                percentageText
            );


            row.append(
                header,
                track,
                details
            );


            macroResults.appendChild(row);

        });

    }


    // =====================================================
    // 14. FOOD RECOMMENDATIONS
    // =====================================================

    function renderRecommendations(recommendations) {

        recommendationResults.replaceChildren();


        const categories = [

            {
                title: "Protein Sources",

                key: "Protein",

                className: "protein",

                macroLabel: "protein"

            },

            {
                title: "Carbohydrate Sources",

                key: "Carbohydrates",

                className: "carbs",

                macroLabel: "carbs"

            },

            {
                title: "Fat Sources",

                key: "Fat",

                className: "fat",

                macroLabel: "fat"

            }

        ];


        if (
            !recommendations ||
            typeof recommendations !== "object"
        ) {

            recommendationResults.appendChild(
                createElement(
                    "p",
                    "recommendation-empty",
                    "No food recommendations are available right now."
                )
            );

            return;

        }


        categories.forEach((category) => {


            const foods = Array.isArray(
                recommendations[category.key]
            )

                ? recommendations[category.key]

                : [];


            const group = createElement(
                "section",
                `recommendation-group ${category.className}`
            );


            const heading = createElement(
                "h3",
                "recommendation-heading",
                category.title
            );


            group.appendChild(heading);


            if (foods.length === 0) {

                group.appendChild(
                    createElement(
                        "p",
                        "recommendation-empty",
                        "No recommendations available in this category."
                    )
                );

                recommendationResults.appendChild(group);

                return;

            }


            const grid = createElement(
                "div",
                "recommendation-grid"
            );


            foods.forEach((food) => {


                const card = createElement(
                    "article",
                    "recommendation-card"
                );


                const name = createElement(
                    "h4",
                    "food-name",
                    food.food ?? "Unknown food"
                );


                const servingValue = Number(food.serving);

                const serving = createElement(
                    "p",
                    "food-serving",
                    Number.isFinite(servingValue)

                        ? `${formatNumber(servingValue, 0)} g serving`

                        : "Serving size unavailable"
                );


                const macroValue = Number(food.macro);

                const macro = createElement(
                    "p",
                    "food-macro",
                    Number.isFinite(macroValue)

                        ? `${formatNumber(macroValue)} g ${category.macroLabel}`

                        : "Macro information unavailable"
                );


                card.append(
                    name,
                    serving,
                    macro
                );


                grid.appendChild(card);

            });


            group.appendChild(grid);

            recommendationResults.appendChild(group);

        });

    }


    // =====================================================
    // 15. EDIT ASSESSMENT
    // =====================================================

    if (editAssessment) {

        editAssessment.addEventListener("click", () => {

            resultSection.hidden = true;

            form.hidden = false;


            // Retain previously entered values

            showStep(0);

        });

    }


    // =====================================================
    // 16. INITIALIZE APPLICATION
    // =====================================================

    showStep(0);


    console.log(
        "FITTIN assessment interface initialized successfully."
    );

});