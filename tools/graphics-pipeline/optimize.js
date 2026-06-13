#!/usr/bin/env node
/* GUToE graphics pipeline: on-the-fly formatting with sharp (libvips).
 *
 * Reads the generated 4D assets (animated GIFs + PNG stills) and emits
 * web-optimized variants:
 *   - animated GIF  -> animated WebP (typically 40-70% smaller)
 *   - animated GIF  -> downscaled animated WebP thumbnail (360px wide)
 *   - PNG still     -> WebP still + 480px thumbnail
 *
 * Usage:  node optimize.js --in ../../gfx/4d --out ../../gfx/4d/web
 *         npm run optimize
 *
 * sharp processes animated images natively ({ animated: true }), so a
 * 60-frame GIF converts in a single streaming pass -- this is the
 * "on the fly" path: cheap enough to run on every regeneration.
 */

import { promises as fs } from "node:fs";
import path from "node:path";
import sharp from "sharp";

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const IN_DIR = path.resolve(arg("in", "../../gfx/4d"));
const OUT_DIR = path.resolve(arg("out", path.join(IN_DIR, "web")));
const THUMB_WIDTH = parseInt(arg("thumb-width", "360"), 10);

async function bytes(p) {
  return (await fs.stat(p)).size;
}

function fmtMB(n) {
  return `${(n / 1e6).toFixed(2)} MB`;
}

async function convertGif(file) {
  const base = path.basename(file, ".gif");
  const input = sharp(file, { animated: true });

  const full = path.join(OUT_DIR, `${base}.webp`);
  await input.clone().webp({ quality: 78, effort: 4 }).toFile(full);

  const thumb = path.join(OUT_DIR, `${base}_thumb.webp`);
  await input
    .clone()
    .resize({ width: THUMB_WIDTH })
    .webp({ quality: 70, effort: 4 })
    .toFile(thumb);

  const [inB, fullB, thumbB] = await Promise.all(
    [file, full, thumb].map(bytes));
  console.log(
    `${base}.gif ${fmtMB(inB)} -> ${base}.webp ${fmtMB(fullB)} ` +
    `(${Math.round((1 - fullB / inB) * 100)}% smaller), ` +
    `thumb ${fmtMB(thumbB)}`);
}

async function convertPng(file) {
  const base = path.basename(file, ".png");
  const full = path.join(OUT_DIR, `${base}.webp`);
  await sharp(file).webp({ quality: 82 }).toFile(full);

  const thumb = path.join(OUT_DIR, `${base}_thumb.webp`);
  await sharp(file)
    .resize({ width: 480 })
    .webp({ quality: 75 })
    .toFile(thumb);

  const [inB, fullB] = await Promise.all([file, full].map(bytes));
  console.log(
    `${base}.png ${fmtMB(inB)} -> ${base}.webp ${fmtMB(fullB)} ` +
    `(${Math.round((1 - fullB / inB) * 100)}% smaller)`);
}

const entries = await fs.readdir(IN_DIR, { withFileTypes: true });
await fs.mkdir(OUT_DIR, { recursive: true });

for (const e of entries) {
  if (!e.isFile()) continue;
  const file = path.join(IN_DIR, e.name);
  try {
    if (e.name.endsWith(".gif")) await convertGif(file);
    else if (e.name.endsWith(".png")) await convertPng(file);
  } catch (err) {
    console.error(`failed on ${e.name}: ${err.message}`);
    process.exitCode = 1;
  }
}
console.log(`output -> ${OUT_DIR}`);
