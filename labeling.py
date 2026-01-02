import pandas as pd

PH_MIN, PH_MAX = 5.5, 7.5            # pH
EC_MIN, EC_MAX = 200.0, 2000.0       # µS/cm
N_MIN, N_MAX   = 0.0, 2000.0         # mg/kg
P_MIN, P_MAX   = 0.0, 2000.0
K_MIN, K_MAX   = 0.0, 2000.0
M_MIN, M_MAX   = 10.0, 40.0          # % VWC
T_MIN, T_MAX   = 10.0, 35.0          # °C (soil)
AT_MIN, AT_MAX = 10.0, 40.0          # °C (air)
AH_MIN, AH_MAX = 20.0, 100.0         # % RH (air)

# Weights: 7 soil vars equal, 2 env vars equal & smaller
W_SOIL = 0.125      # 7 × 0.125 = 0.875
W_ENV  = 0.0625     # 2 × 0.0625 = 0.125

def _normalize(s: pd.Series, lo: float, hi: float) -> pd.Series:
    return (100.0 * (s - lo) / (hi - lo)).clip(lower=0.0, upper=100.0)

def add_soil_health_labels(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["pH_norm"]        = _normalize(out["pH"],          PH_MIN, PH_MAX)
    out["EC_norm"]        = _normalize(out["EC"],          EC_MIN, EC_MAX)
    out["N_norm"]         = _normalize(out["N"],           N_MIN,  N_MAX)
    out["P_norm"]         = _normalize(out["P"],           P_MIN,  P_MAX)
    out["K_norm"]         = _normalize(out["K"],           K_MIN,  K_MAX)
    out["Moisture_norm"]  = _normalize(out["SoilMoisture"], M_MIN,  M_MAX)
    out["SoilTemp_norm"]  = _normalize(out["SoilTemp"],     T_MIN,  T_MAX)
    out["AirTemp_norm"]   = _normalize(out["AirTemp"],      AT_MIN, AT_MAX)
    out["AirHumid_norm"]  = _normalize(out["AirHumidity"],  AH_MIN, AH_MAX)

    out["SoilHealth"] = (
        W_SOIL * out["pH_norm"] +
        W_SOIL * out["EC_norm"] +
        W_SOIL * out["N_norm"] +
        W_SOIL * out["P_norm"] +
        W_SOIL * out["K_norm"] +
        W_SOIL * out["Moisture_norm"] +
        W_SOIL * out["SoilTemp_norm"] +
        W_ENV  * out["AirTemp_norm"] +
        W_ENV  * out["AirHumid_norm"]
    )

    return out