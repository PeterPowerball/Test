"""Makes "import snowproof" work in every test file, also when one file runs alone."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
