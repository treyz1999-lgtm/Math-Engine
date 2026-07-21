export function labelize(value) {
  return value
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/[_-]/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function renderResult(result) {
  if (result === null || result === undefined) return "No result";

  if (["number", "string", "boolean"].includes(typeof result)) {
    return String(result);
  }

  if (Array.isArray(result)) {
    const isMatrix = result.every((row) => Array.isArray(row));
    return isMatrix ? result.map((row) => row.join("    ")).join("\n") : result.join(", ");
  }

  if (typeof result === "object") {
    return Object.entries(result)
      .map(([key, value]) => `${labelize(key)}: ${JSON.stringify(value)}`)
      .join("\n");
  }

  return "Unknown result format";
}
