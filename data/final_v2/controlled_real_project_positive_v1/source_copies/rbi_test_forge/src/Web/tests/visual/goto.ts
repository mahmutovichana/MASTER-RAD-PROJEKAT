import type { Page } from "@playwright/test";

/**
 * Set the app's locale the same way it resolves it at runtime: the
 * `rbi.locale` preference cookie (see src/localization/config/locale-resolution.ts).
 * Must run before navigation since the provider only reads the cookie on boot.
 */
export async function gotoLocalized(page: Page, path: string, locale: string): Promise<void> {
  await page.context().addCookies([
    {
      name: "rbi.locale",
      value: locale,
      url: "http://localhost:8080",
    },
  ]);
  await page.goto(path);
  await waitForLocalizedContent(page);
}

/** Wait until the localization loading spinner (`role="status"`) is gone. */
export async function waitForLocalizedContent(page: Page): Promise<void> {
  await page.locator('[role="status"][aria-live="polite"]').waitFor({ state: "detached" });
  await page.waitForLoadState("networkidle");
}
