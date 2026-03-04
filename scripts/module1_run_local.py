from pipelines.prefect.module1_flow import module1_flow

if __name__ == "__main__":
    out = module1_flow()
    print(f"✅ Module 1 completed. Output: {out}")
