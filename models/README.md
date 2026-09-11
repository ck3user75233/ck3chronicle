# Empirical classification models

Only reviewed, immutable model revisions belong here. Runtime code must load a
model using the exact SHA-256 recorded in its manifest; “latest” is never an
implicit model identity.

## Current revision 67303093ecda779d

- model SHA-256: `0a508eb8056f37d586921bb4441099dcb71fcf89e4a9d1c0e764b1b86d4c1b89`
- semantic projection catalog SHA-256: `c287849b16447e7b154f067c918afb3e0d30563ce56a9c578b06c006f20032b4`
- semantic projection revision: `public-semantic-252-contract-evidence-v3`
- semantic projection schema: `2`
- normalizer: `ck3-empirical-template-normalizer-v4.11`
- clusterer: `ordered-token-clusterer-v4-bounded-script-layers`
- threshold: `0.72`
- training logs: 8 distinct archived `error.log` files
- training blocks: 432,847
- model clusters: 891
- projection rows: 892 (891 full-model contracts plus one composed L1/L2 contract)

The catalog supplies a total canonical disposition for every approved model
contract. One hundred reviewed contract projections classify canonical issues;
the remaining 792 projections preserve evidence explicitly as unclassified.
Contract-bound reference selectors distinguish symbols, objects, and locators
without using those values to discover a template.

Development calibration against the now-public 252-row semantic authority is
252/252 exact across accounting, category, error type, severity, confidence,
primary file/line, referenced symbols, and referenced objects. This is a
regression result, not an unseen holdout result; the same evidence participated
in model/projection refinement and is permanently ineligible for the private
release holdout.

## Historical revision 93196794a7e0115d

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
