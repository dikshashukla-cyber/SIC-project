"""
Wellness Dashboard src package.
Enables transparent importing of all root-level analytics, visualization, and utility modules.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root is in sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
