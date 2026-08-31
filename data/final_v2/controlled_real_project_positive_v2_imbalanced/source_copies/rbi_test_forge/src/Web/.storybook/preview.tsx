import type { Preview } from "@storybook/react-vite";

import "../src/styles.css";

/**
 * Global Storybook preview configuration.
 *
 * - Imports the token stylesheet once so every story renders with the real
 *   semantic tokens (`--surface-*`, `--text-*`, …) instead of browser defaults.
 * - `layout: "padded"` matches how components are actually composed inside a
 *   page — never flush against the preview iframe edge.
 * - The `surface` backgrounds map 1:1 to the `data-surface` contexts used
 *   throughout the library (see `src/styles.css`), so switching background
 *   previews the same theming components rely on in the app.
 * - The a11y addon runs as part of the test pipeline (`test: "error"`), so an
 *   accessibility violation fails a story the same way a broken render would.
 */
const preview: Preview = {
  parameters: {
    layout: "padded",
    backgrounds: {
      options: {
        default: { name: "default", value: "var(--surface)" },
        subtle: { name: "subtle", value: "var(--surface-subtle)" },
        inverse: { name: "inverse", value: "var(--surface-inverse)" },
        brand: { name: "brand", value: "var(--surface-brand)" },
        corporate: { name: "corporate", value: "var(--surface-corporate)" },
      },
    },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    a11y: {
      test: "error",
    },
  },
  initialGlobals: {
    backgrounds: { value: "default" },
  },
};

export default preview;
