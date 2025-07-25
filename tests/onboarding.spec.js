import { test, expect } from "@playwright/test";

test("Open Playwright on Wikipedia and verify Microsoft is visible", async ({
  page,
}) => {
  // Navigate to Wikipedia
  await page.goto("https://www.wikipedia.org");
  
  // Enter search term
  const searchInput = page.locator('input[name="search"]');
  await searchInput.fill("playwright");
  await searchInput.press("Enter");

  // Open search result and assert
  await page.getByRole("link", { name: "Playwright (software)" }).click();
  await expect(page.getByText("Microsoft", { exact: true }).first()).toBeVisible();
});