import { categories } from "../features/calculator/calculatorConfig";

export function Sidebar({ activeCategory, mode, onSelectCategory, onShowHistory, onShowSettings }) {
  return (
    <aside className="sidebar" aria-label="Math modules">
      <div className="brand">
        <div className="brand-mark">ME</div>
        <div>
          <strong>Math Engine</strong>
          <span>Computation workspace</span>
        </div>
      </div>

      <nav className="nav-list">
        {categories.map((category) => (
          <button
            key={category.id}
            className={activeCategory === category.id && mode === "calculator" ? "nav-item active" : "nav-item"}
            onClick={() => onSelectCategory(category.id)}
            type="button"
          >
            {category.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-tools">
        <button className={mode === "history" ? "nav-item active" : "nav-item"} onClick={onShowHistory} type="button">
          History
        </button>
        <button className={mode === "settings" ? "nav-item active" : "nav-item"} onClick={onShowSettings} type="button">
          Settings
        </button>
      </div>
    </aside>
  );
}
