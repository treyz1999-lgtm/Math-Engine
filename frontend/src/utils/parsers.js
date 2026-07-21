export function parseArray(input) {
  const values = input
    .split(",")
    .map((value) => Number(value.trim()));

  if (values.length === 0 || values.some((value) => Number.isNaN(value))) {
    throw new Error("Enter a comma-separated list of numbers.");
  }

  return values;
}

export function parseMatrix(input) {
  const rows = input
    .trim()
    .split("\n")
    .filter(Boolean)
    .map((row) =>
      row.split(",").map((value) => {
        const number = Number(value.trim());
        if (Number.isNaN(number)) {
          throw new Error("Enter a matrix as rows of comma-separated numbers.");
        }
        return number;
      }),
    );

  if (rows.length === 0) {
    throw new Error("Matrix input is required.");
  }

  const width = rows[0].length;
  if (rows.some((row) => row.length !== width)) {
    throw new Error("Each matrix row must have the same number of columns.");
  }

  return rows;
}

export function parseTextArray(input) {
  const values = input
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);

  if (values.length === 0) {
    throw new Error("Enter at least one comma-separated value.");
  }

  return values;
}

export function parseFieldValue(field, rawValue) {
  const value = rawValue.trim();

  if (field.type !== "numberOptional" && value === "") {
    throw new Error(`${field.label} is required.`);
  }

  switch (field.type) {
    case "number": {
      const number = Number(value);
      if (Number.isNaN(number)) throw new Error(`${field.label} must be a valid number.`);
      return number;
    }
    case "numberOptional": {
      if (value === "") return undefined;
      const number = Number(value);
      if (Number.isNaN(number)) throw new Error(`${field.label} must be a valid number.`);
      return number;
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

export function parseSettingValue(value) {
  const trimmed = value.trim();
  if (trimmed === "true") return true;
  if (trimmed === "false") return false;
  if (trimmed !== "" && !Number.isNaN(Number(trimmed))) return Number(trimmed);
  return value;
}
