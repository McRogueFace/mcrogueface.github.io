// Round-trip check: decode our Python lzstring output with the REAL lz-string
// library (the same one the playground loads). Reads newline-terminated
// base64-ish tokens on argv, prints DECODED\t<sha256-of-decoded> per line so the
// python side can assert it recovered the exact source.
//
//   node tools/test_lzstring.js <compressed1> <compressed2> ...
//
// Requires the lz-string package resolvable from node. We point NODE_PATH at a
// known cached copy in test_lzstring.py.
const crypto = require('crypto');
const LZString = require('lz-string');

for (const tok of process.argv.slice(2)) {
    const decoded = LZString.decompressFromEncodedURIComponent(tok);
    const h = crypto.createHash('sha256').update(decoded, 'utf8').digest('hex');
    process.stdout.write(h + '\n');
}
