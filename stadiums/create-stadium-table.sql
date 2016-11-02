DROP TABLE IF EXISTS stadium;
CREATE TABLE stadium(
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    stadium_type VARCHAR(40) NOT NULL,
    city VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    country VARCHAR(20) NOT NULL,
    home_teams VARCHAR(20) NOT NULL,
    time_zone VARCHAR(3) NOT NULL
);
\copy stadium(name, stadium_type, city, state, country, home_teams, time_zone) FROM './stadiums.csv' DELIMITER ',' CSV HEADER;
