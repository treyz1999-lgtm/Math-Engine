export function AppHeader({ activeLabel, mode }) {
  return (
    <header className="app-header">
      <div>
        <p className="eyebrow">FastAPI + React</p>
        <h1>Math Engine</h1>
      </div>
      <div className="status-pill" aria-live="polite">
        {mode === "calculator" ? activeLabel : mode}
      </div>
    </header>
  );
}
