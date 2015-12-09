DELETE FROM gamebook WHERE season_year = '2015' and week = 13;
\copy gamebook FROM './output-week.csv' DELIMITER ',' CSV HEADER;
