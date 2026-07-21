import { Button } from "../../components/Button";

export function HistoryPanel({ entries, loading, onReplay, onDelete, onRefresh, onClear }) {
  return (
    <div className="history-panel">
      <div className="panel-toolbar">
        <Button type="button" onClick={onRefresh}>
          Refresh
        </Button>
        <Button type="button" onClick={onClear}>
          Clear
        </Button>
      </div>

      {loading && <div className="empty-state compact">Loading history...</div>}

      {!loading && entries.length === 0 && <div className="empty-state compact">No calculations have been saved yet.</div>}

      {!loading && entries.length > 0 && (
        <div className="history-list">
          {entries.map((entry) => (
            <article className="history-entry" key={entry.index}>
              <div>
                <strong>{entry.display_name}</strong>
                <span>#{entry.index}</span>
              </div>
              <div className="row-actions">
                <Button type="button" onClick={() => onReplay(entry.index)}>
                  Replay
                </Button>
                <Button type="button" onClick={() => onDelete(entry.index)}>
                  Delete
                </Button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
