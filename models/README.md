# Retained native models

[selection.json](selection.json) is the explicit active package pin. It currently
selects `4ac4e8ee92346e6d14eacfbf` after the owner-authorized 2026-10-05 cutover. The combined package
`4ac4e8ee92346e6d14eacfbf` is retained under `releases/` and registered at model
publication order 8. Its manifest pin is
`839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
Pipeline receiving and the coordinated runtime switch are complete. The wheel's
independent [packaged default](../packaging/models/selection.json) and checkout
selection now agree. New-package live ingestion/lifecycle remains pending a natural
unique capture; see the [activation receipt](../docs/learner-next-release/PIPELINE_RECEIVING.md#production-activated--2026-10-05).
See the [R3 packaging receipt](../docs/learner-next-release/PIPELINE_RECEIVING.md#r3-packaging-closed--2026-10-05).

Earlier v58 package `f23424ed8aa4d910bf4d3223` (order 7) is retained history. The [combined learner/decoder release packet](../docs/learner-next-release/README.md)
owns the new v61/v1.8 package and receiving status. Parser v1.8 requires the shared
application `ck3chronicle.decoder.decode_fragment` module; ship the application
artifact and its current contract renderer with the model. Known-UTF-8 processing
does not import a detector. Automatic physical-source detection uses the declared
chardet dependency. Do not activate the earlier v58 selection.

The replacement contains 394 templates (296 supported, 98 provisional), runtime
model `789219fdbd81c8dab950bc93`, model schema 6, matcher API
`ck3-native-matcher-v3`, selector `complete-assignment-v2`, and parser
`ck3-lossless-v1.8`. Model, parser, matcher helpers and owner rules are hash-covered
immutable payloads. The application decoder and renderer ship in the verified
application wheel linked from the combined release packet.

Use `ck3chronicle.pipeline.catalog.load_selected_classifier`. Selection validates
the manifest pin and loads that package's own authenticated matcher bootstrap;
there is no implicit latest-package selection or mutable-learner fallback.
Complete supported and provisional assignments retain their respective statuses.

The wheel includes selection/catalog files and every retained available runtime
package. Earlier packages remain available for historical Run lineage and explicit
selection. Immutable manifests retain their original publication-time text;
current production registration and activation are recorded by the catalog and
selection, without rewriting package bytes.

The replacement requires the current application contract renderer for repeated
location entries and exact game-date literal choices. See the
[pipeline handoff](../docs/LEARNER_PARSER_PIPELINE_HANDOFF.md) for verification,
activation status and the running handler compatibility requirement. Registration
does not restart services, ingest logs or change existing Runs.
