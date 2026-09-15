import pandas as pd
from pathlib import Path


FILE_PATH = Path("datasets/raw/Telangana_GW_Telemetry.csv")


def load_groundwater_data():
    df = pd.read_csv(FILE_PATH)
    return df


def prepare_observations(df):
    observations = df[
        [
            "Station",
            "District",
            "Tehsil",
            "Latitude",
            "Longitude",
            "Data Acquisition Time",
            "Groundwater Level Telemetry 6 Hourly (meter)",
            "Agency",
        ]
    ].copy()
    

    observations = observations.rename(
        columns={
            "Station": "station_id",
            "District": "district",
            "Tehsil": "tehsil",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Data Acquisition Time": "observation_time",
            "Groundwater Level Telemetry 6 Hourly (meter)": "groundwater_level_m",
            "Agency": "source",
        }
    )

    # Convert timestamps
    observations["observation_time"] = pd.to_datetime(
    observations["observation_time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce",
)

    # Convert numeric fields
    observations["groundwater_level_m"] = pd.to_numeric(
        observations["groundwater_level_m"],
        errors="coerce",
    )

    observations["latitude"] = pd.to_numeric(
        observations["latitude"],
        errors="coerce",
    )

    observations["longitude"] = pd.to_numeric(
        observations["longitude"],
        errors="coerce",
    )

    # Convert "-" placeholders to missing values
    observations["tehsil"] = observations["tehsil"].replace("-", pd.NA)

    observations["quality_flag"] = "NORMAL"

    observations.loc[
        observations["groundwater_level_m"].abs() >= 50,
        "quality_flag"
    ] = "EXTREME"

    # Remove observations missing required fields
    observations = observations.dropna(
        subset=[
            "station_id",
            "observation_time",
            "groundwater_level_m",
        ]
    )

    return observations


def inspect_prepared_data(observations):
    print("\n===== PREPARED DATA =====")

    print("Rows available:", len(observations))
    print("Columns:", len(observations.columns))

    print("\n===== DATA TYPES =====")
    print(observations.dtypes)

    print("\n===== MISSING VALUES =====")
    print(observations.isna().sum())

    print("\n===== FIRST 5 RECORDS =====")
    print(observations.head().to_string(index=False))

    print("\n===== LAST 5 RECORDS =====")
    print(observations.tail().to_string(index=False))

    print("\n===== QUALITY FLAGS =====")
    print(observations["quality_flag"].value_counts())


if __name__ == "__main__":
    df = load_groundwater_data()

    print("Raw rows:", len(df))

    observations = prepare_observations(df)

    inspect_prepared_data(observations)