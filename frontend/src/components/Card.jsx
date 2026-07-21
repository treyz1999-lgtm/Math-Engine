export function Card({ title, eyebrow, actions, children, className = "" }) {
  return (
    <section className={`card ${className}`.trim()}>
      {(title || eyebrow || actions) && (
        <div className="card-header">
          <div>
            {eyebrow && <p className="eyebrow">{eyebrow}</p>}
            {title && <h2>{title}</h2>}
          </div>
          {actions && <div className="card-actions">{actions}</div>}
        </div>
      )}
      {children}
    </section>
  );
}
