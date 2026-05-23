CREATE TABLE routes (
    route_id VARCHAR(50) PRIMARY KEY,
    route_name VARCHAR(150),
    priority_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stops (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_name VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE passenger_counts (
    id BIGSERIAL PRIMARY KEY,
    operating_day DATE NOT NULL,
    line_id VARCHAR(50) NOT NULL REFERENCES routes(route_id),
    stop_id VARCHAR(50) REFERENCES stops(stop_id),
    arrival TIMESTAMP,
    departure TIMESTAMP,
    vehicle_seats NUMERIC(10, 2) NOT NULL,
    passengers NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bi_transport_daily (
    id BIGSERIAL PRIMARY KEY,
    operating_day DATE NOT NULL,
    line_id VARCHAR(50) NOT NULL,
    hour INT NOT NULL,
    day_name VARCHAR(20),
    day_type VARCHAR(20),
    hour_category VARCHAR(30),
    total_passengers NUMERIC(12, 2),
    avg_occupancy_rate NUMERIC(8, 2),
    route_priority VARCHAR(20),
    weather_dummy VARCHAR(30),
    operational_cost NUMERIC(14, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fleet_recommendations (
    id BIGSERIAL PRIMARY KEY,
    recommendation_date DATE NOT NULL,
    line_id VARCHAR(50) NOT NULL,
    hour_category VARCHAR(30) NOT NULL,
    predicted_passengers NUMERIC(12, 2) NOT NULL,
    vehicle_capacity NUMERIC(10, 2) NOT NULL,
    recommended_fleet INT NOT NULL,
    priority_level VARCHAR(20) NOT NULL,
    estimated_cost NUMERIC(14, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
