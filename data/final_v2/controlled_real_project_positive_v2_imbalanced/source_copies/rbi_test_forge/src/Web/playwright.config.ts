import { defineConfig, devices } from "@playwright/test";

/**
 * Visual regression + accessibility test configuration.
 *
 * Deterministic by design: fixed timezone/locale, disabled animations and
 * reduced motion, so screenshots don't flake between runs/machines.
 */
export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [["html", { outputFolder: "playwright-report", open: "never" }]],
  outputDir: "test-results",
  timeout: 30_000,
  expect: {
    timeout: 10_000,
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.02,
      animations: "disabled",
    },
  },
  use: {
    baseURL: "http://localhost:8080",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    timezoneId: "UTC",
    locale: "en-US",
    reducedMotion: "reduce",
    colorScheme: "light",
  },
  projects: [
    {
      name: "mobile-375x812",
      use: { ...devices["Desktop Chrome"], viewport: { width: 375, height: 812 } },
    },
    {
      name: "desktop-1280x900",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 900 } },
    },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:8080",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
