export function Button({ children, variant = "secondary", className = "", ...props }) {
  return (
    <button className={`button button-${variant} ${className}`.trim()} {...props}>
      {children}
    </button>
  );
}
