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

let activeCalculator = calculatorConfigs.arithmeticBinary;


// =========================
// UI RENDER FUNCTIONS
// =========================

function renderCalculator(config) {
    activeCalculator = config;

    let html = "";

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
}


// =========================
// EVENT HANDLERS
// =========================

runButton.addEventListener("click", async function () {
    try {
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

renderCalculator(calculatorConfigs.arithmeticBinary);