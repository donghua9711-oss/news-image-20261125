// "The Day in Full" — the Wednesday 25 November 2026 front page.
// make.fun bounty: news-image-20261125.
//
// The finished page travels with this entry as entry.png (1024 x 1024,
// drawn locally by compose.py from the day's verified stories; SOURCES.md
// lists them). At grade time there is no network and nothing to redraw:
// this program validates the committed page against the contest limits
// and delivers it into the output folder, proving the delivery intact.

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const BYTE_LIMIT = 1024 * 1024; // the contest's 1 MiB ceiling
const SIDE_LIMIT = 1024; // the contest's pixel ceiling, either way

function die(reason: string): never {
  console.error(`the day in full: ${reason}`);
  process.exit(1);
}

// The page is a PNG: eight signature bytes, then the IHDR chunk, whose
// payload opens with the canvas width and height as big-endian uint32s.
function pngCanvas(bytes: Buffer): [number, number] {
  const magic = [137, 80, 78, 71, 13, 10, 26, 10];
  const signed = bytes.length >= 24 && magic.every((b, i) => bytes[i] === b);
  if (!signed) die('entry.png fails the PNG signature check');
  if (bytes.toString('latin1', 12, 16) !== 'IHDR') die('entry.png carries no IHDR chunk');
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  return [view.getUint32(16), view.getUint32(20)];
}

// The rules also allow a JPEG page. JPEGs open with the SOI marker (FF D8)
// and continue as marker segments, each sized by a big-endian uint16; the
// start-of-frame segment (C0 or C2) holds the height, then the width.
function jpegCanvas(bytes: Buffer): [number, number] {
  if (bytes.length < 4 || bytes[0] !== 0xff || bytes[1] !== 0xd8) {
    die('entry.png is neither PNG nor JPEG');
  }
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  let at = 2;
  while (at + 9 < bytes.length) {
    if (bytes[at] !== 0xff) die('entry.png has a broken JPEG segment');
    const marker = bytes[at + 1];
    if (marker === 0xc0 || marker === 0xc2) {
      return [view.getUint16(at + 7), view.getUint16(at + 5)];
    }
    at += 2 + view.getUint16(at + 2);
  }
  die('entry.png shows no JPEG start-of-frame segment');
}

function canvasSize(bytes: Buffer): [number, number] {
  return bytes[0] === 0x89 ? pngCanvas(bytes) : jpegCanvas(bytes);
}

const folder = dirname(fileURLToPath(import.meta.url));
const pagePath = join(folder, 'entry.png');
const page = readFileSync(pagePath);

if (page.byteLength === 0) die('entry.png is empty');
if (page.byteLength > BYTE_LIMIT) {
  die(`entry.png weighs ${page.byteLength} bytes; the limit is ${BYTE_LIMIT}`);
}
const [canvasW, canvasH] = canvasSize(page);
if (canvasW > SIDE_LIMIT || canvasH > SIDE_LIMIT) {
  die(`entry.png spans ${canvasW}x${canvasH}; the limit is ${SIDE_LIMIT} a side`);
}

const outFolder = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outFolder, { recursive: true });
const deliveredPath = join(outFolder, 'entry.png');
copyFileSync(pagePath, deliveredPath);

const delivered = readFileSync(deliveredPath);
if (statSync(deliveredPath).size !== page.byteLength || !delivered.equals(page)) {
  die('the delivered page does not match the committed entry.png');
}
// Independent second look: parse the delivered copy's own header and make
// sure it still describes the same canvas as the committed page.
const [againW, againH] = canvasSize(delivered);
if (againW !== canvasW || againH !== canvasH) {
  die('the delivered page parses to a different canvas size');
}
const kib = (page.byteLength / 1024).toFixed(1);
console.log(`the day in full: delivered ${deliveredPath} — ${canvasW}x${canvasH}, ${page.byteLength} bytes (${kib} KiB), intact`);
