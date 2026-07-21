import { Button } from "../../components/Button";
import { settingsOptions } from "./settingsConfig";
import { labelize } from "../../utils/formatters";

export function SettingsPanel({ category, setting, value, onCategoryChange, onSettingChange, onValueChange, onUpdate, onReset, loading }) {
  return (
    <form className="settings-form" onSubmit={onUpdate}>
      <div className="control-grid">
        <label className="field">
          <span>Category</span>
          <select value={category} onChange={(event) => onCategoryChange(event.target.value)}>
            {Object.keys(settingsOptions).map((item) => (
              <option key={item} value={item}>
                {labelize(item)}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Setting</span>
          <select value={setting} onChange={(event) => onSettingChange(event.target.value)}>
            {settingsOptions[category].map((item) => (
              <option key={item} value={item}>
                {labelize(item)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <label className="field">
        <span>Value</span>
        <input value={value} onChange={(event) => onValueChange(event.target.value)} placeholder="degrees, radians, true, false, or a number" />
      </label>

      <div className="form-footer">
        <Button variant="primary" type="submit" disabled={loading}>
          {loading ? "Updating..." : "Update Setting"}
        </Button>
        <Button type="button" onClick={onReset} disabled={loading}>
          Reset Settings
        </Button>
      </div>
    </form>
  );
}
