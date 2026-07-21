function placeholderFor(field) {
  if (field.type === "array") return "1, 2, 3, 4";
  if (field.type === "arrayText") return "x + y = 5, x - y = 1";
  if (field.type === "matrix") return "1, 2\n3, 4";
  if (field.name === "expr") return "x^2 + 2*x + 1";
  if (field.name === "variable") return "x";
  return "";
}

export function FieldControl({ field, value, onChange }) {
  const id = `field-${field.name}`;
  const isTextarea = ["array", "arrayText", "matrix"].includes(field.type);
  const commonProps = {
    id,
    name: field.name,
    value,
    placeholder: placeholderFor(field),
    onChange: (event) => onChange(field.name, event.target.value),
  };

  return (
    <label className="field">
      <span>{field.label}</span>
      {isTextarea ? (
        <textarea rows={field.type === "matrix" ? 5 : 3} {...commonProps} />
      ) : (
        <input type={field.type === "number" || field.type === "numberOptional" ? "number" : "text"} {...commonProps} />
      )}
    </label>
  );
}
