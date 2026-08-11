# DocGuard Live Flow Router Changes 2026-08

## Change

`docguard_hybrid/signal_extractor.py` now treats `default_page_size` as a configuration-default change only when it appears on an added or removed diff line (`+default_page_size` or `-default_page_size`) or when the legacy synthetic scenario is explicitly `changed_default_config_value`.

## Reason

The first live-flow run exposed a false positive on `LIVE-NEG-FORMATTING`. The old signal considered any occurrence of `default_page_size` in the diff text a configuration change, even when it was unchanged context in a formatting-only case.

## Scope

This is a minimal signal precision fix. It does not change gold labels, does not retrain any model, and does not add new Deep-JIT behavior.
