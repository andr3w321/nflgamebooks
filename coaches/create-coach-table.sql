DROP TABLE IF EXISTS coach;
CREATE TABLE coach(
    id SERIAL PRIMARY KEY,
    type VARCHAR(10) NOT NULL,
    team VARCHAR(3) NOT NULL,
    name VARCHAR(40) NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER,
    start_week INTEGER NOT NULL,
    end_week INTEGER
);
\copy coach(type, team, name, start_year, end_year, start_week, end_week) FROM './head_coaches.csv' DELIMITER ',' CSV HEADER;
