import io
import pandas as pd
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os


FILE_PATH = Path("datasets/raw/Telangana_GW_Telemetry.csv")

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def prepare_observations():
    print("Loading CSV...")

    df = pd.read_csv(FILE_PATH)

    print("Raw rows:", len(df))

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

    observations["observation_time"] = pd.to_datetime(
    observations["observation_time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce",
)

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

    observations["tehsil"] = observations["tehsil"].replace("-", pd.NA)

    observations["quality_flag"] = "NORMAL"

    observations.loc[
        observations["groundwater_level_m"].abs() >= 50,
        "quality_flag"
    ] = "EXTREME"

    observations = observations.dropna(
        subset=[
            "station_id",
            "observation_time",
            "groundwater_level_m",
        ]
    )

    print("Prepared rows:", len(observations))

    return observations


def ingest_to_database(observations):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        buffer = io.StringIO()

        observations.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="\\N",
        )

        buffer.seek(0)

        cursor.copy_expert(
            """
            COPY groundwater_observations (
                station_id,
                district,
                tehsil,
                latitude,
                longitude,
                observation_time,
                groundwater_level_m,
                source,
                quality_flag
            )
            FROM STDIN
            WITH (
                FORMAT CSV,
                NULL '\\N'
            );
            """,
            buffer,
        )

        connection.commit()

        print("Database ingestion successful!")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    observations = prepare_observations()

    print("\nStarting database ingestion...")

    ingest_to_database(observations)

    print("Rows inserted:", len(observations))