import sys
from pathlib import Path

# Add src directory to Python path for proper imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Verify the path was added
print(f"Added to sys.path: {src_path}")
print(f"sys.path now: {sys.path[:3]}")
