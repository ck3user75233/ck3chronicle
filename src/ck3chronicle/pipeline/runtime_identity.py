"""Process-start identity for shared handler admission; not Run lineage."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys


@lru_cache(maxsize=1)
def application_identity():
    root = Path(__file__).resolve().parents[1]
    digest = hashlib.sha256()
    for file in sorted(root.rglob('*.py')):
        digest.update(file.relative_to(root).as_posix().encode())
        digest.update(file.read_bytes())
    from .catalog import selected_models_root
    return dict(application_sha256=digest.hexdigest(), application_root=str(root),
                python=str(Path(sys.executable).resolve()), models_root=str(selected_models_root().resolve()))


def runtime_identity():
    from ..config import default_config_path, load_config
    document = load_config()
    encoded = json.dumps(document, sort_keys=True, default=str).encode()
    return dict(application_identity(), config=str(default_config_path()),
                config_sha256=hashlib.sha256(encoded).hexdigest())
