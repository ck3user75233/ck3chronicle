"""Read-only configuration diagnosis, using the setup validation owner."""
from . import config
from .setup import diagnose, emit, finding


def run_doctor(format='text'):
    try:
        path = config.default_config_path()
        result = diagnose(config.load_config(path), path)
    except (config.ConfigurationError, OSError, ValueError) as exc:
        result = dict(findings=[finding('configuration', 'error', exc,
            'Dependent checks unavailable.', 'Run setup or edit this exact configuration; no fallback is used.')])
    code = 2 if any(f['severity'] != 'healthy' for f in result['findings']) else 0
    result['status'] = 'attention' if code else 'healthy'
    emit(result, format)
    return code
