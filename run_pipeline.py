from cleaning import clean_data
from data_cleaning_extra import fix_and_filter
from labeling import add_soil_health_labels
from training import train_random_forest



def main():
    clean_df = clean_data()
    clean_df = fix_and_filter(clean_df)

    labeled_df = add_soil_health_labels(clean_df)

    model, mae, r2 = train_random_forest(labeled_df)
    print(f"MAE: {mae:.3f}")
    print(f"R^2: {r2:.3f}")


if __name__ == "__main__":
    main()
    