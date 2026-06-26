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
            const value = input.value.trim();

            if (value === "") {
                throw new Error(`${field.label} is required`);
            }

            payload[field.name] = Number(value);
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
        const isMatrix = result.every(row => Array.isArray(row));

        if (isMatrix) {
            return result
                .map(row => row.join("    "))
                .join("\n");
        }

        return result.join(", ");
    }

    if (typeof result === "object" && result !== null) {
        let output = "";

        for (const key in result) {
            output += `${key}: ${JSON.stringify(result[key])}\n`;
        }

        return output;
    }

    return "Unknown result format";
}

function renderPlot(plotResponse, plotDisplay) {
    plotDisplay.innerHTML = "";

    const plotType = plotResponse.plot_type;
    const plotData = plotResponse.plot_data;
    const png = plotResponse.png;

    let trace;
    let layout;

    try {
        if (plotType === "line") {
            const traces = [
                {
                    x: plotData.x,
                    y: plotData.y,
                    mode: "lines",
                    type: "scatter",
                    name: "Function"
                }
            ];

            if (plotData.critical_x) {
                traces.push({
                    x: plotData.critical_x,
                    y: plotData.critical_y,
                    mode: "markers",
                    type: "scatter",
                    name: "Critical Points",
                    marker: { size: 10 }
                });
            }

            if (plotData.extrema) {
                traces.push({
                    x: plotData.extrema.map(point => point.x),
                    y: plotData.extrema.map(point => point.y),
                    mode: "markers",
                    type: "scatter",
                    name: "Extrema",
                    marker: { size: 10 }
                });
            }

            if (plotData.inflections) {
                traces.push({
                    x: plotData.inflections.map(point => point.x),
                    y: plotData.inflections.map(point => point.y),
                    mode: "markers",
                    type: "scatter",
                    name: "Inflection Points",
                    marker: { size: 10 }
                });
            }

            layout = {
                title: "Function Plot",
                xaxis: { title: "X" },
                yaxis: { title: "Y" }
            };

            Plotly.newPlot(plotDisplay, traces, layout);
            return;
        }

        if (plotType === "scatter") {
            trace = {
                x: plotData.x,
                y: plotData.y,
                mode: "markers",
                type: "scatter"
            };

            layout = {
                title: "Scatter Plot"
            };

            Plotly.newPlot(plotDisplay, [trace], layout);
            return;
        }

        if (plotType === "histogram") {
            trace = {
                x: plotData.data,
                type: "histogram",
                nbinsx: plotData.bins
            };

            layout = {
                title: "Histogram"
            };

            Plotly.newPlot(plotDisplay, [trace], layout);
            return;
        }

        if (plotType === "vector") {
            const traces = [];

            for (const vector of plotData.vectors) {
                traces.push({
                    x: [0, vector[0]],
                    y: [0, vector[1]],
                    mode: "lines+markers",
                    type: "scatter"
                });
            }

            layout = {
                title: "Vector Plot",
                xaxis: { zeroline: true },
                yaxis: { zeroline: true }
            };

            Plotly.newPlot(plotDisplay, traces, layout);
            return;
        }
    }
    catch (error) {
        console.error("Plot rendering failed:", error);
    }

    // PNG fallback
    if (png) {
        plotDisplay.innerHTML = `
            <img src="data:image/png;base64,${png}" alt="Plot">
        `;
    }
}