import { pathToFileURL } from "node:url";
import path from "node:path";

const playwrightModule = process.env.PLAYWRIGHT_MODULE || "playwright";
const { chromium } = await import(playwrightModule);

const root = path.dirname(new URL(import.meta.url).pathname);
const browser = await chromium.launch({
  headless: true,
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
});
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(root, "cards.html")).href, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
for (let i = 1; i <= 7; i += 1) {
  const id = `#card-${String(i).padStart(2, "0")}`;
  await page.locator(id).screenshot({ path: path.join(root, `card-${String(i).padStart(2, "0")}.png`) });
}
await browser.close();
