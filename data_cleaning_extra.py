import pandas as pd

def fix_and_filter(df: pd.DataFrame) -> pd.DataFrame:
    total_before = len(df)
    print(f"Rows before cleaning: {total_before}")

    # 1) pH×10 fix
    ph_fix_count = (df["pH"] > 14).sum()
    if ph_fix_count:
        df.loc[df["pH"] > 14, "pH"] /= 10.0
        print(f"pH÷10 applied to {ph_fix_count} rows")

    # 2) Remove out-of-range values
    valid_ranges = {
        "AirTemp": (-10.0, 50.0),
        "AirHumidity": (0.0, 100.0),
        "SoilTemp": (-5.0, 45.0),
        "SoilMoisture": (0.0, 100.0),
        "EC": (200.0, 2000.0),  # µS/cm
        "pH": (3.5, 9.0),
        "N": (0.0, 2000.0),
        "P": (0.0, 2000.0),
        "K": (0.0, 2000.0),
    }

    for col, (lo, hi) in valid_ranges.items():
        before = len(df)
        df = df[(df[col] >= lo) & (df[col] <= hi)]
        removed = before - len(df)
        if removed:
            print(f"{col}: removed {removed} rows outside [{lo}, {hi}]")

    total_after = len(df)
    total_removed = total_before - total_after
    print(f"Rows after cleaning: {total_after}")
    print(f"Total removed: {total_removed}")

    return df.reset_index(drop=True)
