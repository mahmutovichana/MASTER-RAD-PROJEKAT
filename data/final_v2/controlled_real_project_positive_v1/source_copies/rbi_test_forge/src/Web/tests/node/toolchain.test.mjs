import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const packageJson = JSON.parse(await readFile(new URL("../../package.json", import.meta.url), "utf8"));
const workspace = await readFile(new URL("../../pnpm-workspace.yaml", import.meta.url), "utf8");
const webpackConfig = await readFile(new URL("../../webpack.config.cjs", import.meta.url), "utf8");

test("frontend toolchain does not depend on blocked native Vite tooling", () => {
  const dependencies = { ...packageJson.dependencies, ...packageJson.devDependencies };
  for (const name of ["vite", "nitro", "esbuild", "@vitejs/plugin-react", "@tailwindcss/vite", "@tanstack/react-start"]) {
    assert.equal(dependencies[name], undefined, `${name} must not be installed`);
  }
  assert.doesNotMatch(workspace, /esbuild/u);
});

test("Webpack serves the SPA and proxies backend routes", () => {
  assert.match(packageJson.scripts.dev, /webpack serve/u);
  assert.match(packageJson.scripts.build, /webpack/u);
  assert.match(webpackConfig, /historyApiFallback:\s*true/u);
  assert.match(webpackConfig, /"\/api"/u);
  assert.match(webpackConfig, /ts-loader/u);
});

test("global styles are preserved by Webpack tree shaking", () => {
  assert.deepEqual(packageJson.sideEffects, ["**/*.css"]);
  assert.match(webpackConfig, /style-loader/u);
  assert.match(webpackConfig, /MiniCssExtractPlugin/u);
});
