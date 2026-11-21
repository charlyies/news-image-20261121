// main.ts -- entry program for the news-image-20261121 bounty.
//
// Copies the pre-rendered front page (entry.png, built at authoring time
// by compose.py) into the grader output directory. The copy is checked
// byte-for-byte so a corrupt or wrong-sized asset fails loudly instead of
// silently shipping a broken entry.
//
// Plain JavaScript only (no TypeScript annotations) so `node --check`
// passes. Node 22 standard library only; no network, no randomness, no
// timestamps -- the output is identical on every run.

const fs = require("node:fs");
const path = require("node:path");

const MAX_BYTES = 1048576; // 1 MiB cap from the bounty rules
const MAX_DIMENSION = 1024; // 1024 x 1024 cap from the bounty rules

// The eight bytes every PNG file starts with.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function fail(message) {
  console.error("main.ts: " + message);
  process.exit(1);
}

// Read the width and height out of the IHDR chunk (bytes 16-23 of a PNG).
// Returns an object like { width: 1024, height: 1024 }.
function readPngSize(buffer) {
  if (buffer.length < 33) {
    fail("entry.png is too short to be a PNG (" + buffer.length + " bytes)");
  }
  if (!buffer.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail("entry.png does not start with the PNG signature bytes");
  }
  const chunkType = buffer.toString("latin1", 12, 16);
  if (chunkType !== "IHDR") {
    fail("entry.png first chunk is " + chunkType + ", expected IHDR");
  }
  return {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20),
  };
}

function main() {
  const here = __dirname;
  const sourcePath = path.join(here, "entry.png");
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const targetPath = path.join(outputDir, "entry.png");

  // Never let the output path resolve back onto the source asset.
  if (path.resolve(targetPath) === path.resolve(sourcePath)) {
    fail("MAKEFUN_OUTPUT_DIR points at the repo itself; refusing to overwrite entry.png");
  }

  if (!fs.existsSync(sourcePath)) {
    fail("missing asset: " + sourcePath);
  }
  const image = fs.readFileSync(sourcePath);

  if (image.length > MAX_BYTES) {
    fail(
      "entry.png is " + image.length + " bytes, over the " +
        MAX_BYTES + " byte cap"
    );
  }
  const size = readPngSize(image);
  if (size.width > MAX_DIMENSION || size.height > MAX_DIMENSION) {
    fail(
      "entry.png is " + size.width + "x" + size.height +
        ", over the " + MAX_DIMENSION + "x" + MAX_DIMENSION + " cap"
    );
  }

  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(targetPath, image);

  // Confirm the file on disk matches what we validated, byte for byte.
  const written = fs.readFileSync(targetPath);
  if (!written.equals(image)) {
    fail("verification failed: written file differs from entry.png");
  }

  console.log(
    "wrote " + targetPath + " (" + size.width + "x" + size.height +
      ", " + image.length + " bytes)"
  );
}

main();
