import { test, expect } from "@playwright/test";

import { matrix } from "./matrix";
import { gotoLocalized } from "./goto";

/**
 * Visual regression: one screenshot per route × locale, run once per
 * viewport project (see playwright.config.ts projects).
 */
for (const { route, locale, viewport } of matrix) {
  const projectName = `${viewport.name}-${viewport.width}x${viewport.height}`;

  test(`${route} @ ${locale} (${projectName})`, async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== projectName, "Runs only on its matching viewport project");

    await gotoLocalized(page, route, locale);

    const name = `${route.replace(/\//g, "_") || "root"}-${locale}-${projectName}.png`;
    await expect(page).toHaveScreenshot(name, { fullPage: true });
  });
}
