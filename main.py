import sys
import os

SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from app.runner import main

if __name__ == "__main__":
    main()
