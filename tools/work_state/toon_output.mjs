// TOON 2.1.0's object-field parser searches for '[' past an unquoted key's
// colon, including inside a quoted scalar. CMT-132's "[10C ...] ...: ..."
// therefore becomes a bogus ten-item array header. Quoted keys take the
// parser's quote-aware branch. Quote simple object keys without changing any
// values, array headers, tabular rows, dependency pins or strict validation.
export function decodeTrekkerOutput(output, decode) {
  const quotedKeys = output.replace(
    /^( *)(- )?([A-Za-z_][A-Za-z0-9_]*):(?= |\r?$)/gm,
    (_, indent, listPrefix = '', key) => `${indent}${listPrefix}"${key}":`,
  );
  return decode(quotedKeys, { strict: true });
}
