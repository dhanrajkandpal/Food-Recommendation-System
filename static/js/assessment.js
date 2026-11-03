document.addEventListener("DOMContentLoaded", () => {
    // ==========================================
    // DOM ELEMENTS
    // ==========================================

    const form = document.getElementById("assessmentForm");
    const steps = document.querySelectorAll(".form-step");
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

    // ==========================================
    // CONFIGURATION
    // ==========================================

    const stepNames = [
        "Personal Details",
        "Your Lifestyle",
        "Your Goals"
    ];

    const totalSteps = steps.length;
    let currentStep = 0;

    const numberFormatter = new Intl.NumberFormat("en-IN", {
        maximumFractionDigits: 1
    });

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

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

    function showError(message) {
        if (!formError) return;

        formError.textContent = message;
        formError.hidden = false;
    }

    function hideError() {
        if (!formError) return;

        formError.textContent = "";
        formError.hidden = true;
    }

    function createElement(tag, className, text = "") {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        element.textContent = text;

        return element;
    }

    // ==========================================
    // MULTI-STEP FORM
    // ==========================================

    function showStep(step) {
        if (step < 0 || step >= totalSteps) return;

        currentStep = step;

        steps.forEach((element, index) => {
            element.classList.toggle("active", index === step);
        });

        stepDots.forEach((dot, index) => {
            dot.classList.toggle("active", index <= step);
        });

        if (progressFill) {
            const progress = ((step + 1) / totalSteps) * 100;
            progressFill.style.width = `${progress}%`;
        }

        if (stepLabel) {
            stepLabel.textContent = `STEP ${step + 1} OF ${totalSteps}`;
        }

        if (stepName) {
            stepName.textContent = stepNames[step];
        }

        if (previousBtn) {
            previousBtn.hidden = step === 0;
        }

        if (nextBtn) {
            nextBtn.hidden = step === totalSteps - 1;
        }

        if (submitBtn) {
            submitBtn.hidden = step !== totalSteps - 1;
        }

        hideError();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    // ==========================================
    // FORM VALIDATION
    // ==========================================

    function validateStep() {
        const activeStep = steps[currentStep];

        if (!activeStep) return false;

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

    // ==========================================
    // NAVIGATION
    // ==========================================

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            if (!validateStep()) return;

            showStep(currentStep + 1);
        });
    }

    if (previousBtn) {
        previousBtn.addEventListener("click", () => {
            showStep(currentStep - 1);
        });
    }

    // ==========================================
    // FORM SUBMISSION
    // ==========================================

    if (form) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            if (!validateStep()) return;

            hideError();

            const originalButtonText = submitBtn.textContent;

            submitBtn.disabled = true;
            submitBtn.textContent = "Calculating your profile...";

            const payload = {
                age: Number(form.elements["age"].value),
                gender: form.elements["gender"].value,
                height: Number(form.elements["height"].value),
                weight: Number(form.elements["weight"].value),
                activity: form.elements["activity"].value,
                goal: form.elements["goal"].value
            };

            try {
                const response = await fetch("/api/assessment", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(
                        result.error || "Unable to calculate your profile."
                    );
                }

                displayResults(result);

            } catch (error) {
                console.error("Assessment error:", error);

                showError(
                    error.message ||
                    "Something went wrong. Please try again."
                );

            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalButtonText;
            }
        });
    }

    // ==========================================
    // DISPLAY RESULTS
    // ==========================================

    function displayResults(profile) {
        if (!profile || typeof profile !== "object") {
            showError("Invalid response received. Please try again.");
            return;
        }

        form.hidden = true;
        resultSection.hidden = false;

        hideError();

        renderMetrics(profile);
        renderMacros(profile);
        renderRecommendations(profile.Recommendations);

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    // ==========================================
    // METRIC CARDS
    // ==========================================

    function renderMetrics(profile) {
        resultGrid.replaceChildren();

        const metrics = [
            {
                label: "BMI Classification",
                value: profile["Predicted BMI Class"] ?? "N/A",
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
                String(metric.value)
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

    // ==========================================
    // MACRONUTRIENT BREAKDOWN
    // ==========================================

    function renderMacros(profile) {
        macroResults.replaceChildren();

        const targetCalories = Number(profile["Target Calories"]);

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
            const validGrams = Number.isFinite(macro.grams)
                ? macro.grams
                : 0;

            const calories = validGrams * macro.caloriesPerGram;

            const percentage =
                Number.isFinite(targetCalories) && targetCalories > 0
                    ? (calories / targetCalories) * 100
                    : 0;

            const row = createElement(
                "div",
                `macro-row ${macro.className}`
            );

            const header = createElement("div", "macro-header");

            const name = createElement(
                "span",
                "macro-name",
                macro.name
            );

            const amount = createElement(
                "strong",
                "macro-amount",
                `${formatNumber(validGrams)} g`
            );

            header.append(name, amount);

            const track = createElement("div", "macro-track");

            const bar = createElement("div", "macro-bar");

            bar.style.width = `${Math.min(100, Math.max(0, percentage))}%`;

            track.appendChild(bar);

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

            details.append(calorieText, percentageText);

            row.append(header, track, details);

            macroResults.appendChild(row);
        });
    }

    // ==========================================
    // FOOD RECOMMENDATIONS
    // ==========================================

    function renderRecommendations(recommendations) {
        recommendationResults.replaceChildren();

        const categories = [
            {
                title: "Protein Sources",
                key: "Protein",
                className: "protein"
            },
            {
                title: "Carbohydrate Sources",
                key: "Carbohydrates",
                className: "carbs"
            },
            {
                title: "Fat Sources",
                key: "Fat",
                className: "fat"
            }
        ];

        if (!recommendations || typeof recommendations !== "object") {
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
            const foods = Array.isArray(recommendations[category.key])
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

                const serving = createElement(
                    "p",
                    "food-serving",
                    `${formatNumber(food.serving, 0)} g serving`
                );

                const macro = createElement(
                    "p",
                    "food-macro",
                    `${formatNumber(food.macro)} g ${category.key === "Carbohydrates" ? "carbs" : category.key.toLowerCase()}`
                );

                card.append(name, serving, macro);
                grid.appendChild(card);
            });

            group.appendChild(grid);
            recommendationResults.appendChild(group);
        });
    }

    // ==========================================
    // EDIT ASSESSMENT
    // ==========================================

    if (editAssessment) {
        editAssessment.addEventListener("click", () => {
            resultSection.hidden = true;
            form.hidden = false;

            showStep(0);
        });
    }

    // ==========================================
    // INITIALIZE
    // ==========================================

    showStep(0);
});