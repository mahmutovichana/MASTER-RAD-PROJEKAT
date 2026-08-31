import { mergeConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";
import type { StorybookConfig } from "@storybook/react-vite";

/**
 * Storybook 9 configuration for the RBI design system.
 *
 * This is intentionally a plain Vite config, not the app's
 * `@lovable.dev/vite-tanstack-config` — Storybook renders isolated components,
 * not routes, so the TanStack Start/router plugin and SSR/nitro wiring must
 * stay out of this build. Path aliases (`@/...`) are restored with
 * `vite-tsconfig-paths` so stories can import the same way app code does.
 */
const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)", "../src/**/*.mdx"],
  addons: ["@storybook/addon-docs", "@storybook/addon-a11y"],
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  viteFinal: async (viteConfig) =>
    mergeConfig(viteConfig, {
      plugins: [tsconfigPaths()],
    }),
};

export default config;
