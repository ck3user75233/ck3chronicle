# Empirical classification models

Only reviewed, immutable model revisions belong here. Runtime code must load a
model using the exact SHA-256 recorded in its manifest; “latest” is never an
implicit model identity.

## Revision 93196794a7e0115d

- model SHA-256: `3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3`
- normalizer: `ck3-empirical-template-normalizer-v4.6`
- clusterer: `ordered-token-clusterer-v4-bounded-script-layers`
- threshold: `0.72`
- training logs: 7 distinct archived `error.log` files
- training blocks: 404,716
- clusters: 822

Independent release evidence excluded from training:

| Evidence | Eligible occurrences | Exact full | L1 or full | Unknown | Locator failures |
|---|---:|---:|---:|---:|---:|
| 3 reviewed holdouts | 67,445 | 99.5107% | 99.5923% | 275 | 0 |
| 2 untouched candidates | 126,577 | 99.9431% | 99.9929% | 9 | 0 |

These measurements authorize versioned, revisable classification. They do not
authorize discarding raw evidence, suppressing unknowns, or automatic mod
edits.
