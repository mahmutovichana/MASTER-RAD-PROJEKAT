const names = [
  "surface-default", "surface-subtle", "surface-muted", "surface-raised", "surface-sunken", "surface-inverse", "surface-brand", "surface-brand-subtle", "surface-corporate",
  "text-primary", "text-secondary", "text-tertiary", "text-inverse", "text-on-brand", "text-link",
  "border-default", "border-subtle", "border-strong", "background", "foreground", "card", "card-foreground", "popover", "popover-foreground", "primary", "primary-foreground", "secondary", "secondary-foreground", "muted", "muted-foreground", "accent", "accent-foreground", "destructive", "destructive-foreground", "border", "input", "ring", "sidebar", "sidebar-foreground", "sidebar-primary", "sidebar-primary-foreground", "sidebar-accent", "sidebar-accent-foreground", "sidebar-border", "sidebar-ring",
];
const colors = Object.fromEntries(names.map((name) => [name === "surface-default" ? "surface" : name, `var(--${name})`]));
module.exports = {
  content: ["./src/**/*.{ts,tsx}", "./public/index.html"],
  darkMode: ["class", '[data-theme="dark"]'],
  theme: { extend: { colors, fontFamily: { sans: ["Amalia", "Segoe UI", "sans-serif"], brand: ["Amalia", "Segoe UI", "sans-serif"] }, borderRadius: { xs: "var(--radii-xs)", sm: "var(--radii-sm)", md: "var(--radii-md)", lg: "var(--radii-lg)", pill: "var(--radii-pill)" }, boxShadow: { xs: "var(--elevation-xs)", sm: "var(--elevation-sm)", md: "var(--elevation-md)", lg: "var(--elevation-lg)", overlay: "var(--elevation-overlay)" } } },
  plugins: [],
};
