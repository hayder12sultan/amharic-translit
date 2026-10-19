// Browser port of amharic_translit/engine.py — same algorithm, same data
// (web/data.js, generated from the Python source of truth). Pure client
// side, no backend required.

const CONSONANT_CODES_BY_LENGTH = Object.keys(FIDEL_DATA.regularFamilies).sort(
  (a, b) => b.length - a.length
);

function buildForwardMap() {
  const forward = new Map();
  for (const [code, chars] of Object.entries(FIDEL_DATA.regularFamilies)) {
    for (const [order, suffix] of Object.entries(FIDEL_DATA.orderSuffixes)) {
      forward.set(`${code}${suffix}`, chars[Number(order) - 1]);
    }
  }
  for (const [order, suffix] of Object.entries(FIDEL_DATA.glottalSuffixes)) {
    forward.set(suffix, FIDEL_DATA.glottalFamily[Number(order) - 1]);
  }
  return forward;
}

function buildReverseMap(forward) {
  const reverse = new Map();
  for (const [latin, fidel] of forward.entries()) reverse.set(fidel, latin);
  return reverse;
}

const FORWARD_MAP = buildForwardMap();
const REVERSE_MAP = buildReverseMap(FORWARD_MAP);

const ORDER_SUFFIXES_BY_LENGTH = Object.entries(FIDEL_DATA.orderSuffixes)
  .filter(([, suf]) => suf.length > 0)
  .map(([order, suf]) => [suf, Number(order)])
  .sort((a, b) => b[0].length - a[0].length);

const GLOTTAL_SUFFIXES_BY_LENGTH = Object.entries(FIDEL_DATA.glottalSuffixes)
  .map(([order, suf]) => [suf, Number(order)])
  .sort((a, b) => b[0].length - a[0].length);

function isWordChar(ch) {
  return /[a-zA-Z]/.test(ch);
}

function matchConsonant(text, pos) {
  for (const code of CONSONANT_CODES_BY_LENGTH) {
    if (text.startsWith(code, pos)) return code;
  }
  return null;
}

function matchSuffix(text, pos, candidates) {
  for (const [suffix, order] of candidates) {
    if (suffix && text.startsWith(suffix, pos)) return [suffix, order];
  }
  return null;
}

function toFidel(text) {
  let out = "";
  let i = 0;
  const n = text.length;

  while (i < n) {
    const ch = text[i];

    if (!isWordChar(ch)) {
      out += ch;
      i += 1;
      continue;
    }

    const consonant = matchConsonant(text, i);
    if (consonant !== null) {
      const chars = FIDEL_DATA.regularFamilies[consonant];
      const after = i + consonant.length;
      const match = matchSuffix(text, after, ORDER_SUFFIXES_BY_LENGTH);
      if (match !== null) {
        const [suffix, order] = match;
        out += chars[order - 1];
        i = after + suffix.length;
      } else {
        out += chars[5]; // bare / 6th order
        i = after;
      }
      continue;
    }

    const glottalMatch = matchSuffix(text, i, GLOTTAL_SUFFIXES_BY_LENGTH);
    if (glottalMatch !== null) {
      const [suffix, order] = glottalMatch;
      out += FIDEL_DATA.glottalFamily[order - 1];
      i += suffix.length;
      continue;
    }

    out += ch;
    i += 1;
  }

  return out;
}

function toLatin(text) {
  let out = "";
  for (const ch of text) {
    out += REVERSE_MAP.has(ch) ? REVERSE_MAP.get(ch) : ch;
  }
  return out;
}

function normalize(text) {
  let result = text.trim();
  result = result.replace(/(?<=[a-zA-Z])(ee|ie)/g, "E");
  result = result.replace(/(?<=[a-zA-Z])aa/g, "a");
  result = result.replace(/(?<=[a-zA-Z])(ii|uu|oo)/g, (m) => m[0]);
  result = result.replace(/'/g, "");
  result = result.replace(/([bcdfghjklmnpqrstvwxyz])\1/gi, (_, c) => c);
  result = result.replace(/\s+/g, " ");
  return result;
}

// --- wire up the demo page -------------------------------------------------

function onConvert() {
  const input = document.getElementById("input").value;
  const direction = document.querySelector('input[name="direction"]:checked').value;
  const shouldNormalize = document.getElementById("normalize-toggle").checked;

  let text = input;
  if (direction === "to-fidel" && shouldNormalize) {
    text = normalize(text);
  }

  const result = direction === "to-fidel" ? toFidel(text) : toLatin(text);
  document.getElementById("output").value = result;
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("convert-btn").addEventListener("click", onConvert);
  document.getElementById("input").addEventListener("input", onConvert);
  document
    .querySelectorAll('input[name="direction"]')
    .forEach((el) => el.addEventListener("change", onConvert));
  document.getElementById("normalize-toggle").addEventListener("change", onConvert);
});
