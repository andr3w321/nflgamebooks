DELETE FROM gamebook WHERE season_year = '2015' and season_type = 'Postseason' and week = 1;
\copy gamebook FROM './output-week.csv' DELIMITER ',' CSV HEADER;
