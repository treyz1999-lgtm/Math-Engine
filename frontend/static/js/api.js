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
            row
                .split(",")
                .map(value => Number(value.trim()))
        );
}

function parseTextArray(input) {
    return input
        .split(",")
        .map(value => value.trim())
        .filter(value => value !== "");
}


// =========================
// INPUT PARSER DISPATCH
// =========================

function parseInputByType(field, inputElement) {
    if (!inputElement) {
        throw new Error(`Missing input for ${field.name}`);
    }

    const rawValue = inputElement.value;

    switch (field.type) {
        case "number": {
            const value = rawValue.trim();

            if (value === "") {
                throw new Error(`${field.label} is required`);
            }

            return Number(value);
        }

        case "numberOptional": {
            const value = rawValue.trim();

            if (value === "") {
                return undefined;
            }

            return Number(value);
        }

        case "text":
            return rawValue;

        case "array":
            return parseArray(rawValue);

        case "arrayText":
            return parseTextArray(rawValue);

        case "matrix":
            return parseMatrix(rawValue);

        default:
            throw new Error(`Unsupported field type: ${field.type}`);
    }
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
        const parsedValue = parseInputByType(field, input);

        if (parsedValue !== undefined) {
            payload[field.name] = parsedValue;
        }
    }

    return payload;
}


// =========================
// RESULT RENDERERS
// =========================

function renderResult(result) {
    if (result === null || result === undefined) {
        return "No result";
    }

    if (
        typeof result === "number" ||
        typeof result === "string" ||
        typeof result === "boolean"
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

    if (typeof result === "object") {
        return Object.entries(result)
            .map(([key, value]) => `${key}: ${JSON.stringify(value)}`)
            .join("\n");
    }

    return "Unknown result format";
}


// =========================
// PLOT HELPERS
// =========================

function renderFallbackImage(plotDisplay, png) {
    if (!png) return;

    plotDisplay.innerHTML = `
        <img src="data:image/png;base64,${png}" alt="Plot">
    `;
}

function renderLinePlot(plotDisplay, plotData) {
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

    Plotly.newPlot(plotDisplay, traces, {
        title: "Function Plot",
        xaxis: { title: "X" },
        yaxis: { title: "Y" }
    });
}


// =========================
// PLOT RENDERER
// =========================

function renderPlot(plotResponse, plotDisplay) {
    plotDisplay.innerHTML = "";

    const plotType = plotResponse.plot_type;
    const plotData = plotResponse.plot_data;
    const png = plotResponse.png;

    try {
        if (plotType === "line") {
            renderLinePlot(plotDisplay, plotData);
            return;
        }

        if (plotType === "scatter") {
            Plotly.newPlot(
                plotDisplay,
                [{
                    x: plotData.x,
                    y: plotData.y,
                    mode: "markers",
                    type: "scatter"
                }],
                {
                    title: "Scatter Plot"
                }
            );
            return;
        }

        if (plotType === "histogram") {
            Plotly.newPlot(
                plotDisplay,
                [{
                    x: plotData.data,
                    type: "histogram",
                    nbinsx: plotData.bins
                }],
                {
                    title: "Histogram"
                }
            );
            return;
        }

        if (plotType === "vector") {
            const traces = plotData.vectors.map(vector => ({
                x: [0, vector[0]],
                y: [0, vector[1]],
                mode: "lines+markers",
                type: "scatter"
            }));

            Plotly.newPlot(plotDisplay, traces, {
                title: "Vector Plot",
                xaxis: { zeroline: true },
                yaxis: { zeroline: true }
            });
            return;
        }
    }
    catch (error) {
        console.error("Plot rendering failed:", error);
    }

    renderFallbackImage(plotDisplay, png);
}