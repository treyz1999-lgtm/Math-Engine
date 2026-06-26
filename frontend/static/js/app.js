// =========================
// DOM REFERENCES
// =========================

const inputArea = document.getElementById("input-area");
const resultDisplay = document.getElementById("result-display");
const plotDisplay = document.getElementById("plot-display");
const runButton = document.getElementById("run-btn");


// =========================
// APP STATE
// =========================

let activeCategory = "arithmetic";
let activeCalculator = calculatorConfigs.arithmetic.binary;


// =========================
// UI HELPERS
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

function renderField(field) {
    let html = `<label for="${field.name}">${field.label}:</label><br>`;

    if (
        field.type === "number" ||
        field.type === "numberOptional"
    ) {
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
    else if (field.type === "arrayText") {
        html += `
            <textarea id="${field.name}" rows="3"
            placeholder="x+y=5,x-y=1"></textarea>
        `;
    }
    else if (field.type === "matrix") {
        html += `
            <textarea id="${field.name}" rows="4"
            placeholder="1,2\n3,4"></textarea>
        `;
    }

    html += "<br><br>";
    return html;
}


// =========================
// MAIN UI RENDERERS
// =========================

function renderCalculator(config) {
    activeCalculator = config;

    let html = "";
    html += renderSubcategorySelector(activeCategory);

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

    for (const field of config.fields) {
        html += renderField(field);
    }

    inputArea.innerHTML = html;

    const subcategorySelect = document.getElementById("subcategory-select");

    subcategorySelect.addEventListener("change", function () {
        const selectedSubcategory = subcategorySelect.value;
        const newConfig =
            calculatorConfigs[activeCategory][selectedSubcategory];

        renderCalculator(newConfig);
    });
}

function renderSettingsUI() {
    inputArea.innerHTML = `
        <label>Category:</label>
        <input id="category" type="text"><br><br>

        <label>Setting:</label>
        <input id="setting" type="text"><br><br>

        <label>Value:</label>
        <input id="value" type="text"><br><br>

        <button id="update-settings-btn">Update Setting</button>
        <button id="reset-settings-btn">Reset Settings</button>
    `;

    document
        .getElementById("update-settings-btn")
        .addEventListener("click", updateSettings);

    document
        .getElementById("reset-settings-btn")
        .addEventListener("click", resetSettings);
}


// =========================
// SIDEBAR HELPERS
// =========================

function registerSidebarButton(buttonId, categoryName, defaultSubcategory) {
    const button = document.getElementById(buttonId);

    if (!button) return;

    button.addEventListener("click", function () {
        activeCategory = categoryName;

        renderCalculator(
            calculatorConfigs[categoryName][defaultSubcategory]
        );
    });
}


// =========================
// SETTINGS
// =========================

async function updateSettings() {
    try {
        const payload = {
            category: document.getElementById("category").value,
            setting: document.getElementById("setting").value,
            value: document.getElementById("value").value
        };

        const data = await callAPI("/settings/update", payload);
        resultDisplay.textContent = JSON.stringify(data, null, 2);
    }
    catch (error) {
        resultDisplay.textContent = error.message;
    }
}

async function resetSettings() {
    try {
        await callAPI("/settings/reset", {});
        resultDisplay.textContent = "Settings reset.";
    }
    catch (error) {
        resultDisplay.textContent = error.message;
    }
}


// =========================
// RUN BUTTON
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
            resultDisplay.textContent = renderResult(data.result);
        }
    }
    catch (error) {
        resultDisplay.textContent = `Error: ${error.message}`;
        plotDisplay.innerHTML = "";
    }
});


// =========================
// APP INIT
// =========================

registerSidebarButton("arithmetic-btn", "arithmetic", "binary");
registerSidebarButton("trig-btn", "trig", "basic");
registerSidebarButton("expressions-btn", "expressions", "manipulate");
registerSidebarButton("stats-btn", "stats", "singleArray");
registerSidebarButton("geometry2d-btn", "geometry2d", "singleInput");
registerSidebarButton("geometry3d-btn", "geometry3d", "singleInput");
registerSidebarButton("linear-btn", "linear", "vectorPair");
registerSidebarButton("plot-btn", "plot", "function");

document
    .getElementById("settings-btn")
    ?.addEventListener("click", renderSettingsUI);

renderCalculator(calculatorConfigs.arithmetic.binary);