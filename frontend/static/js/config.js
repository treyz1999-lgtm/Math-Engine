// =========================
// CONFIG / CONSTANTS
// =========================

const BASE_URL = "http://127.0.0.1:8000";

const calculatorConfigs = {
    arithmetic: {
        binary: {
            endpoint: "/arithmetic/binary",
            operations: ["add", "subtract", "multiply", "divide", "mod", "root"],
            fields: [
                { name: "value1", label: "Value 1", type: "number" },
                { name: "value2", label: "Value 2", type: "number" }
            ]
        },

        power: {
            endpoint: "/arithmetic/power",
            operations: ["power"],
            fields: [
                { name: "base", label: "Base", type: "number" },
                { name: "exponent", label: "Exponent", type: "number" }
            ]
        },

        other: {
            endpoint: "/arithmetic/other",
            operations: ["abs", "factorial"],
            fields: [
                { name: "value1", label: "Value", type: "number" }
            ]
        }
    },

    plot: {
        function: {
            endpoint: "/plot/function",
            operations: ["function"],
            fields: [
                { name: "expr", label: "Expression", type: "text" },
                { name: "variable", label: "Variable", type: "text" }
            ]
        }
    }
};