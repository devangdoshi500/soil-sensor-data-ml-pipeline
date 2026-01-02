from pathlib import Path

EXCEL_PATH = "data/all_data.xlsx"

RAW_COLUMNS = ["Air Temp","Air Humidity","Soil Temp","Soil Moisture","EC","PhVal","N","P","K"]

COLUMN_MAP = {
    "Air Temp": "AirTemp",
    "Air Humidity": "AirHumidity",
    "Soil Temp": "SoilTemp",
    "Soil Moisture": "SoilMoisture",
    "EC": "EC",
    "PhVal": "pH",
    "N": "N",
    "P": "P",
    "K": "K",
}


OUTPUT_DIR = EXCEL_PATH.parent
CLEAN_CSV_NAME = "cleaned_soil_data.csv"
MODEL_NAME = "rf_soilhealth_model.pkl"


