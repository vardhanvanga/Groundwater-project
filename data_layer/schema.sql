CREATE TABLE IF NOT EXISTS groundwater_observations (
    id SERIAL PRIMARY KEY,

    station_id VARCHAR(100) NOT NULL,

    district VARCHAR(100),
    tehsil VARCHAR(100),

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    observation_time TIMESTAMP NOT NULL,

    groundwater_level_m NUMERIC(10, 3),

    source VARCHAR(100),

    quality_flag VARCHAR(20) DEFAULT 'NORMAL',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_gwl_station_time
ON groundwater_observations (station_id, observation_time);

CREATE INDEX IF NOT EXISTS idx_gwl_location
ON groundwater_observations (district, tehsil);

CREATE INDEX IF NOT EXISTS idx_gwl_coordinates
ON groundwater_observations (latitude, longitude);

CREATE INDEX IF NOT EXISTS idx_gwl_quality
ON groundwater_observations (quality_flag);