"""Pytest bootstrap: make the project root importable.

When pytest starts, this file adds the project root directory to Python's
module search path so the `markbridge` package can be imported reliably.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
