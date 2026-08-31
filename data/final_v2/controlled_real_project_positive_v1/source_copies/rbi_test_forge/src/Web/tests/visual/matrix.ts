/**
 * Shared route/locale/viewport matrix for visual regression tests.
 *
 * Add a route by adding one entry to `routes` below — every locale and
 * viewport combination is generated automatically.
 */

export interface Viewport {
  readonly name: string;
  readonly width: number;
  readonly height: number;
}

export const routes = [
  "/",
  "/foundations",
  "/components",
  "/patterns",
  "/applications/admin",
  "/applications/api",
  "/architecture",
] as const;

export const locales = ["en", "de", "bs"] as const;

export const viewports: readonly Viewport[] = [
  { name: "mobile", width: 375, height: 812 },
  { name: "desktop", width: 1280, height: 900 },
];

export type Route = (typeof routes)[number];
export type Locale = (typeof locales)[number];

export interface MatrixEntry {
  readonly route: Route;
  readonly locale: Locale;
  readonly viewport: Viewport;
}

export const matrix: readonly MatrixEntry[] = routes.flatMap((route) =>
  locales.flatMap((locale) => viewports.map((viewport) => ({ route, locale, viewport }))),
);

/** Routes covered once per locale at a single (desktop) viewport, for a11y checks. */
export const a11yMatrix = routes.flatMap((route) => locales.map((locale) => ({ route, locale })));
