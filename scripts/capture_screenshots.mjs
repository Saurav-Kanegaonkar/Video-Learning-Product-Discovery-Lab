import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const outDir = join(root, "docs", "images");
const workDir = join(tmpdir(), "video-learning-product-discovery-lab-shots");

const index = readFileSync(join(root, "index.html"), "utf8");
const css = readFileSync(join(root, "src", "styles.css"), "utf8");
const app = readFileSync(join(root, "src", "app.js"), "utf8");
const payload = readFileSync(join(root, "analysis", "outputs", "app_payload.json"), "utf8");

mkdirSync(outDir, { recursive: true });
mkdirSync(workDir, { recursive: true });

const shots = [
  ["cockpit", ""],
  ["evidence", "evidence"],
  ["prd", "prd"],
  ["launch", "launch"],
];

for (const [name, view] of shots) {
  const viewClick = view
    ? `setTimeout(() => document.querySelector('[data-view="${view}"]').click(), 300);`
    : "";
  const html = index
    .replace('<link rel="stylesheet" href="src/styles.css">', `<style>${css}</style>`)
    .replace(
      '<script src="src/app.js"></script>',
      `<script>window.fetch = async () => ({ json: async () => (${payload}) });</script><script>${app}</script><script>${viewClick}</script>`,
    );
  const htmlPath = join(workDir, `${name}.html`);
  const imagePath = join(outDir, `${name}.png`);
  writeFileSync(htmlPath, html);
  const result = spawnSync(
    chrome,
    [
      "--headless=new",
      "--disable-gpu",
      "--hide-scrollbars",
      "--no-first-run",
      "--no-default-browser-check",
      "--window-size=1440,980",
      "--virtual-time-budget=2000",
      `--screenshot=${imagePath}`,
      pathToFileURL(htmlPath).href,
    ],
    { encoding: "utf8" },
  );
  if (result.status !== 0) {
    throw new Error(`Screenshot failed for ${name}: ${result.stderr || result.stdout}`);
  }
}

rmSync(workDir, { recursive: true, force: true });
console.log("Captured portfolio artifact screenshots.");
