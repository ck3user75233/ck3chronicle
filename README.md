# ck3chronicle

> Preserve and triage Crusader Kings III runtime logs and crash evidence.

## Quick start

```bash
pip install -e ".[dev]"
ck3chronicle doctor          # health check
ck3chronicle ingest          # ingest from default CK3 logs folder
ck3chronicle ingest --logs /path/to/logs
ck3chronicle sessions        # list recorded sessions
```

## Configuration

On first run, `ck3chronicle doctor` creates a default config file at:

- **Windows:** `%LOCALAPPDATA%\ck3chronicle\config.toml`
- **Linux/macOS:** `~/.local/share/ck3chronicle/config.toml`

Edit any `[paths]` entry to override the OS default.  Leave a value as `""`
to keep the OS default.
