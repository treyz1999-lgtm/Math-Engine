import { FieldControl } from "../../components/FieldControl";
import { Button } from "../../components/Button";
import { labelize } from "../../utils/formatters";

export function CalculatorPanel({
  category,
  subcategory,
  config,
  inputs,
  operation,
  categoryConfig,
  onSubcategoryChange,
  onOperationChange,
  onInputChange,
  onSubmit,
  loading,
}) {
  return (
    <form className="calculator-form" onSubmit={onSubmit}>
      <div className="control-grid">
        <label className="field">
          <span>Mode</span>
          <select value={subcategory} onChange={(event) => onSubcategoryChange(event.target.value)}>
            {Object.keys(categoryConfig).map((key) => (
              <option key={key} value={key}>
                {labelize(key)}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Operation</span>
          <select value={operation} onChange={(event) => onOperationChange(event.target.value)}>
            {config.operations.map((item) => (
              <option key={item} value={item}>
                {labelize(item)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="field-grid">
        {config.fields.map((field) => (
          <FieldControl key={`${category}-${subcategory}-${field.name}`} field={field} value={inputs[field.name] || ""} onChange={onInputChange} />
        ))}
      </div>

      <div className="form-footer">
        <Button variant="primary" type="submit" disabled={loading}>
          {loading ? "Computing..." : "Run Calculation"}
        </Button>
      </div>
    </form>
  );
}
