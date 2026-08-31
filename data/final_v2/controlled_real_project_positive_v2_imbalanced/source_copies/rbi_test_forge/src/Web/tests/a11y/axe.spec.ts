import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

import { a11yMatrix } from "../visual/matrix";
import { gotoLocalized } from "../visual/goto";

/**
 * Accessibility smoke test: every route × locale at desktop width must have
 * no "serious" or "critical" axe violations.
 */
const desktopProject = "desktop-1280x900";

for (const { route, locale } of a11yMatrix) {
  test(`${route} @ ${locale} has no serious/critical a11y violations`, async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== desktopProject, "Runs only on the desktop project");

    await gotoLocalized(page, route, locale);

    const results = await new AxeBuilder({ page }).analyze();
    const blocking = results.violations.filter(
      (violation) => violation.impact === "serious" || violation.impact === "critical",
    );

    expect(blocking, JSON.stringify(blocking, null, 2)).toEqual([]);
  });
}
