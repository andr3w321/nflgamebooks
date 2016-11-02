DROP TABLE IF EXISTS gamebook_drive;
CREATE TABLE gamebook_drive(
    gamekey INTEGER,
    pos_team VARCHAR(3),
    drive_n INTEGER,
    quarter INTEGER,
    time_received VARCHAR(30),
    time_lost VARCHAR(30),
    pos_time INTEGER,
    how_ball_obtained VARCHAR(30),
    start_field INTEGER,
    play_count INTEGER,
    yards_gained INTEGER,
    yards_penalized INTEGER,
    net_yards INTEGER,
    first_downs INTEGER,
    result VARCHAR(30),
    PRIMARY KEY(gamekey, pos_team, drive_n)
);
