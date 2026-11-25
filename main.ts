// The Day in Full — Wednesday 25 November 2026.
// Entry for make.fun bounty news-image-20261125.
//
// The picture itself is committed beside this file as entry.png: a single
// 1024x1024 front page composed from the day's verified stories (see
// SOURCES.md for the story list and compose.py for how the page is drawn).
// This program's whole job at grade time is to deliver that picture to the
// output folder, after checking it still obeys the contest's caps.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1_048_576; // 1 MiB
const MAX_SIDE = 1024; // pixels, either dimension

function fail(message: string): never {
  console.error(`entry: ${message}`);
  process.exit(1);
}

function pngSize(bytes: Buffer): { width: number; height: number } {
  // A PNG opens with an 8-byte signature; the IHDR chunk follows and its
  // first eight data bytes are the width and the height, big-endian.
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (bytes.length < 24) fail('entry.png is too small to be a PNG');
  for (let i = 0; i < signature.length; i++) {
    if (bytes[i] !== signature[i]) fail('entry.png does not start with the PNG signature');
  }
  if (bytes.toString('ascii', 12, 16) !== 'IHDR') fail('entry.png has no IHDR chunk');
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

function jpegSize(bytes: Buffer): { width: number; height: number } {
  // The contest also accepts JPEG. A JPEG opens with SOI (FF D8) and then a
  // chain of marker segments; the start-of-frame segment (C0 or C2) carries
  // the height and width, big-endian, after its length and precision bytes.
  if (bytes.length < 4 || bytes[0] !== 0xff || bytes[1] !== 0xd8) {
    fail('entry.png is neither a PNG nor a JPEG');
  }
  let offset = 2;
  while (offset + 9 < bytes.length) {
    if (bytes[offset] !== 0xff) fail('entry.png has a corrupt JPEG segment');
    const marker = bytes[offset + 1];
    if (marker === 0xc0 || marker === 0xc2) {
      return { height: bytes.readUInt16BE(offset + 5), width: bytes.readUInt16BE(offset + 7) };
    }
    offset += 2 + bytes.readUInt16BE(offset + 2);
  }
  fail('entry.png has no JPEG start-of-frame segment');
}

function pictureSize(bytes: Buffer): { width: number; height: number } {
  return bytes[0] === 0x89 ? pngSize(bytes) : jpegSize(bytes);
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const picturePath = join(here, 'entry.png');
  const picture = readFileSync(picturePath);

  if (picture.length > MAX_BYTES) {
    fail(`entry.png is ${picture.length} bytes, over the ${MAX_BYTES} byte cap`);
  }
  if (picture.length === 0) fail('entry.png is empty');
  const { width, height } = pictureSize(picture);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`entry.png is ${width}x${height}, over the ${MAX_SIDE} pixel cap`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, 'entry.png');
  copyFileSync(picturePath, target);
  // Read the delivered file back and compare it byte for byte with the
  // committed picture, so a truncated copy can never pass silently; then
  // re-parse the delivered copy's header as a second, independent check.
  const delivered = readFileSync(target);
  if (!delivered.equals(picture)) fail('the delivered copy differs from entry.png');
  const deliveredSize = pictureSize(delivered);
  if (deliveredSize.width !== width || deliveredSize.height !== height) {
    fail('the delivered copy parses to different dimensions');
  }
  const kib = (picture.length / 1024).toFixed(1);
  console.log(`entry: wrote ${target} (${width}x${height}, ${picture.length} bytes = ${kib} KiB, verified)`);
}

main();
