DROP TABLE IF EXISTS team_data;
CREATE TABLE team_data(
    team VARCHAR(3) PRIMARY KEY,
    home_stadium VARCHAR(40) NOT NULL,
    time_zone VARCHAR(3) NOT NULL,
    conference VARCHAR(3) NOT NULL,
    division VARCHAR(20) NOT NULL
);
\copy team_data(team, home_stadium, time_zone, conference, division) FROM './team-data.csv' DELIMITER ',' CSV HEADER;
