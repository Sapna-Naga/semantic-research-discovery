import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipelines.prefect.module1_flow import module1_flow

if __name__ == "__main__":
    out = module1_flow()
    print(f"✅ Module 1 completed. Output: {out}")
