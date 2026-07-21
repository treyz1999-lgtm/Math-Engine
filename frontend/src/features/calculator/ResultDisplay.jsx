import { renderResult } from "../../utils/formatters";
import { PlotDisplay } from "../plot/PlotDisplay";

export function ResultDisplay({ result, plot, error, loading }) {
  return (
    <div className="results-stack">
      {error && (
        <div className="message error" role="alert">
          {error}
        </div>
      )}

      <div className={loading ? "result-box loading" : "result-box"} aria-live="polite">
        {loading ? "Computing..." : result === null && !error ? "Choose an operation, enter values, and run a calculation." : renderResult(result)}
      </div>

      <PlotDisplay plot={plot} />
    </div>
  );
}
