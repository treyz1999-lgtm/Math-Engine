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
let uiMode = "calculator";


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
    uiMode = "calculator";
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
    uiMode = "settings";

    inputArea.innerHTML = `
        <label for="category">Category:</label>
        <select id="category"></select>
        <br><br>

        <label for="setting">Setting:</label>
        <select id="setting"></select>
        <br><br>

        <label for="value">Value:</label>
        <input id="value" type="text">
        <br><br>

        <button id="update-settings-btn">Update Setting</button>
        <button id="reset-settings-btn">Reset Settings</button>
    `;

    populateCategoryDropdown();

    document
        .getElementById("category")
        .addEventListener("change", populateSettingDropdown);

    document
        .getElementById("update-settings-btn")
        .addEventListener("click", updateSettings);

    document
        .getElementById("reset-settings-btn")
        .addEventListener("click", resetSettings);
}

function populateCategoryDropdown() {
    const categorySelect = document.getElementById("category");
    categorySelect.innerHTML = "";

    for (const category in settingsOptions) {
        categorySelect.innerHTML += `
            <option value="${category}">
                ${category}
            </option>
        `;
    }

    populateSettingDropdown();
}

function populateSettingDropdown() {
    const category =
        document.getElementById("category").value;

    const settingSelect =
        document.getElementById("setting");

    settingSelect.innerHTML = "";

    for (const setting of settingsOptions[category]) {
        settingSelect.innerHTML += `
            <option value="${setting}">
                ${setting}
            </option>
        `;
    }
}

async function renderHistoryUI() {
    try {
        uiMode = "history";
        plotDisplay.innerHTML = "";
        resultDisplay.textContent = "";

        const data = await callAPI(
            "/history/summary",
            null,
            "GET"
        );

        let html = `<h3>History</h3><br>`;

        if (data.history.length === 0) {
            html += `<p>No history yet.</p>`;
        }

        for (const entry of data.history) {
            html += `
                <div class="history-entry">
                    <strong>${entry.display_name}</strong>
                    <br><br>
                    <button onclick="replayHistory(${entry.index})">
                        Replay
                    </button>
                    <button onclick="deleteHistory(${entry.index})">
                        Delete
                    </button>
                    <br><br>
                </div>
            `;
        }

        inputArea.innerHTML = html;
    }
    catch (error) {
        resultDisplay.textContent = error.message;
    }
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

function parseSettingValue(value) {
    if (value === "true") return true;
    if (value === "false") return false;

    if (!isNaN(Number(value)) && value.trim() !== "") {
        return Number(value);
    }

    return value;
}

async function updateSettings() {
    try {
        const payload = {
            category: document.getElementById("category").value,
            setting: document.getElementById("setting").value,
            value: parseSettingValue(
                document.getElementById("value").value
            )
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
// HISTORY
// =========================

async function replayHistory(index) {
    try {
        const replayData = await callAPI(
            `/history/replay/${index}`,
            {}
        );

        const result = await callAPI(
            replayData.endpoint,
            replayData.request
        );

        if (result.result?.plot_type) {
            resultDisplay.textContent = "Plot generated.";
            renderPlot(result.result, plotDisplay);
        }
        else {
            plotDisplay.innerHTML = "";
            resultDisplay.textContent =
                renderResult(result.result);
        }
    }
    catch (error) {
        resultDisplay.textContent = error.message;
    }
}

async function deleteHistory(index) {
    try {
        await callAPI(
            `/history/${index}`,
            null,
            "DELETE"
        );

        renderHistoryUI();
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
        if (uiMode !== "calculator") {
            resultDisplay.textContent =
                "Run is only available in calculator mode.";
            return;
        }

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

document
    .getElementById("history-btn")
    ?.addEventListener("click", renderHistoryUI);

renderCalculator(calculatorConfigs.arithmetic.binary);