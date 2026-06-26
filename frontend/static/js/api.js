// =========================
// PARSERS
// =========================

function parseArray(input) {
    return input
        .split(",")
        .map(value => Number(value.trim()))
        .filter(value => !isNaN(value));
}

function parseMatrix(input) {
    return input
        .trim()
        .split("\n")
        .map(row =>
            row.split(",").map(value => Number(value.trim()))
        );
}


// =========================
// API HELPERS
// =========================

async function callAPI(endpoint, payload) {
    const response = await fetch(BASE_URL + endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "API request failed");
    }

    return data;
}

function buildPayload(config) {
    const payload = {};

    const operationSelect = document.getElementById("operation-select");

    if (operationSelect) {
        payload.operation = operationSelect.value;
    }

    for (const field of config.fields) {
        const input = document.getElementById(field.name);

        if (field.type === "number") {
            payload[field.name] = Number(input.value);
        }
        else if (field.type === "text") {
            payload[field.name] = input.value;
        }
        else if (field.type === "array") {
            payload[field.name] = parseArray(input.value);
        }
        else if (field.type === "matrix") {
            payload[field.name] = parseMatrix(input.value);
        }
    }

    return payload;
}


// =========================
// RESULT RENDERERS
// =========================

function renderResult(result) {
    if (
        typeof result === "number" ||
        typeof result === "string"
    ) {
        return String(result);
    }

    if (Array.isArray(result)) {
        return JSON.stringify(result, null, 2);
    }

    if (typeof result === "object") {
        return JSON.stringify(result, null, 2);
    }

    return "Unknown result format";
}

function renderPlot(plotResponse, plotDisplay) {
    plotDisplay.innerHTML = "";

    const plotType = plotResponse.plot_type;
    const plotData = plotResponse.plot_data;
    const png = plotResponse.png;

    if (plotType === "line") {
        plotDisplay.innerHTML = `
            <h3>Line Plot</h3>
            <p>${plotData.x.length} points plotted</p>
        `;
        return;
    }

    if (plotType === "histogram") {
        plotDisplay.innerHTML = `
            <h3>Histogram</h3>
            <p>Bins: ${plotData.bins}</p>
        `;
        return;
    }

    if (plotType === "scatter") {
        plotDisplay.innerHTML = `
            <h3>Scatter Plot</h3>
            <p>${plotData.x.length} points plotted</p>
        `;
        return;
    }

    if (plotType === "vector") {
        plotDisplay.innerHTML = `
            <pre>${JSON.stringify(plotData, null, 2)}</pre>
        `;
        return;
    }

    if (png) {
        plotDisplay.innerHTML = `
            <img src="data:image/png;base64,${png}" alt="Plot">
        `;
    }
}