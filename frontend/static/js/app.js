// =========================
// DOM REFERENCES
// =========================

const inputArea = document.getElementById("input-area");
const resultDisplay = document.getElementById("result-display");
const plotDisplay = document.getElementById("plot-display");
const runButton = document.getElementById("run-btn");

// Sidebar buttons
const arithmeticBtn = document.getElementById("arithmetic-btn");
const plotBtn = document.getElementById("plot-btn");


// =========================
// APP STATE
// =========================

let activeCategory = "arithmetic";
let activeCalculator = calculatorConfigs.arithmetic.binary;


// =========================
// UI RENDER FUNCTIONS
// =========================

function renderSubcategorySelector(categoryName) {
    const category = calculatorConfigs[categoryName];
    const subKeys = Object.keys(category);

    let html = `
        <label for="subcategory-select">Mode:</label>
        <select id="subcategory-select">
    `;

    for (const key of subKeys) {
        html += `
            <option value="${key}">
                ${key}
            </option>
        `;
    }

    html += `
        </select>
        <br><br>
    `;

    return html;
}


function renderCalculator(config) {
    activeCalculator = config;

    let html = "";

    // Subcategory selector first
    html += renderSubcategorySelector(activeCategory);

    // Operation selector
    html += `
        <label for="operation-select">Operation:</label>
        <select id="operation-select">
    `;

    for (const operation of config.operations) {
        html += `
            <option value="${operation}">
                ${operation}
            </option>
        `;
    }

    html += `
        </select>
        <br><br>
    `;

    // Dynamic input fields
    for (const field of config.fields) {
        html += `<label for="${field.name}">${field.label}:</label><br>`;

        if (field.type === "number") {
            html += `<input id="${field.name}" type="number">`;
        }
        else if (field.type === "text") {
            html += `<input id="${field.name}" type="text">`;
        }
        else if (field.type === "array") {
            html += `
                <textarea id="${field.name}" rows="3"
                placeholder="1,2,3,4"></textarea>
            `;
        }
        else if (field.type === "matrix") {
            html += `
                <textarea id="${field.name}" rows="4"
                placeholder="1,2\n3,4"></textarea>
            `;
        }

        html += "<br><br>";
    }

    inputArea.innerHTML = html;

    // IMPORTANT:
    // Because innerHTML replaces the DOM,
    // we must reattach the event listener after rendering.
    const subcategorySelect = document.getElementById("subcategory-select");

    subcategorySelect.addEventListener("change", function () {
        const selectedSubcategory = subcategorySelect.value;
        const newConfig = calculatorConfigs[activeCategory][selectedSubcategory];
        renderCalculator(newConfig);
    });
}


// =========================
// SIDEBAR CATEGORY HANDLERS
// =========================

arithmeticBtn.addEventListener("click", function () {
    activeCategory = "arithmetic";
    renderCalculator(calculatorConfigs.arithmetic.binary);
});

plotBtn.addEventListener("click", function () {
    activeCategory = "plot";
    renderCalculator(calculatorConfigs.plot.function);
});


// =========================
// RUN BUTTON HANDLER
// =========================

runButton.addEventListener("click", async function () {
    try {
        resultDisplay.textContent = "Computing...";
        plotDisplay.innerHTML = "";

        const payload = buildPayload(activeCalculator);

        const data = await callAPI(
            activeCalculator.endpoint,
            payload
        );

        if (data.result?.plot_type) {
            resultDisplay.textContent = "Plot generated.";
            renderPlot(data.result, plotDisplay);
        }
        else {
            plotDisplay.innerHTML = "";
            resultDisplay.textContent = renderResult(data.result);
        }

    } catch (error) {
        resultDisplay.textContent = `Error: ${error.message}`;
        plotDisplay.innerHTML = "";
    }
});


// =========================
// APP INIT
// =========================

renderCalculator(calculatorConfigs.arithmetic.binary);