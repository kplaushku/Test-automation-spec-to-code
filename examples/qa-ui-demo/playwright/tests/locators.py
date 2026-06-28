"""Loads bound structural locators from config/locators.generated.json.

Raises a clear error if a locator is still an unbound __BIND__ placeholder, so a
UI run fails loudly with "run speckit.qa.bind-locators" rather than with a
cryptic selector error.
"""
import json
from pathlib import Path

_FILE = Path(__file__).parent.parent / "config" / "locators.generated.json"


class _Locators:
    def __init__(self, path: Path):
        self._data = {k: v for k, v in json.loads(path.read_text()).items()
                      if not k.startswith("_")}

    def __getitem__(self, name: str) -> str:
        value = self._data[name]
        if isinstance(value, str) and value.startswith("__BIND__:"):
            raise RuntimeError(
                f"Locator '{name}' is unbound ({value}). "
                f"Run speckit.qa.bind-locators against the live app first."
            )
        return value


L = _Locators(_FILE)
