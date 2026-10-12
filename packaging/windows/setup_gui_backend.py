"""JSON adapter for the Windows Forms presentation, using Pipeline's setup API."""
from __future__ import annotations

import json
from pathlib import Path
import sys


def execute(request):
    from ck3chronicle import config, setup
    config.configure(request.get("config"))
    selected = config.default_config_path()
    operation = request["operation"]
    if operation == "load":
        suggested = setup.suggest_paths()
        inventory = setup.model_choices()
        saved = config.load_config(selected) if selected.exists() else {}
        diagnosis = setup.diagnose(saved, selected) if saved else {}
        inputs = {} if saved else dict(suggested.get("candidates", {}))
        if not saved and request.get("data_root"):
            inputs["data_root"] = request["data_root"]
        document, _, preview = setup.prepare(selected, inputs)
        return dict(config=str(selected), existing=bool(saved), suggestions=suggested,
                    models=inventory, saved=diagnosis, defaults=document, preview=preview)
    if operation == "paths":
        roots = {}
        for field in setup.EXTERNAL:
            value = request["inputs"].get(field, "")
            if not value or not Path(value).is_absolute():
                raise ValueError("Choose a full folder path for " + field)
            roots[field] = Path(value)
        return dict(findings=setup.inspect_paths(roots))
    if operation in {"preview", "apply"}:
        inputs = dict(request["inputs"])
        inputs["ripgrep"] = str(Path(__file__).resolve().parent / "tools/rg.exe")
        accepted = request.get("accepted", [])
        if operation == "preview":
            _, _, result = setup.prepare(selected, inputs, accepted)
            return result
        result, code = setup.apply_setup(selected, inputs, accepted)
        result["exit_code"] = code
        return result
    if operation == "doctor":
        return setup.diagnose(config.load_config(selected), selected)
    raise ValueError("Unknown setup operation")


if __name__ == "__main__":
    try:
        value = execute(json.load(sys.stdin))
        print(json.dumps(value, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
