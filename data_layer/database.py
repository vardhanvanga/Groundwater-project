import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    return connection


def insert_observation(
    station_id,
    district,
    mandal,
    observation_time,
    groundwater_level_m,
    source,
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO groundwater_observations (
                station_id,
                district,
                mandal,
                observation_time,
                groundwater_level_m,
                source
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(
            query,
            (
                station_id,
                district,
                mandal,
                observation_time,
                groundwater_level_m,
                source,
            ),
        )

        connection.commit()

        print("Groundwater observation inserted successfully!")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    insert_observation(
        station_id="TEST001",
        district="Rangareddy",
        mandal="Shamshabad",
        observation_time="2026-09-15 12:00:00",
        groundwater_level_m=8.420,
        source="TEST",
    )