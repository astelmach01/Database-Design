DROP DATABASE IF EXISTS ESleague;
CREATE DATABASE ESleague;

USE ESleague;
CREATE TABLE league_user(
username VARCHAR(20) PRIMARY KEY UNIQUE NOT NULL,
user_password VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE game(
game_name VARCHAR(40) PRIMARY KEY UNIQUE NOT NULL,
genre VARCHAR(50) NOT NULL,
developer VARCHAR(40) NOT NULL,
release_date DATE NOT NULL
);

CREATE TABLE league(
administrator VARCHAR(50) NOT NULL,
game_or_genre VARCHAR(40) NOT NULL,
leagueID INT AUTO_INCREMENT PRIMARY KEY,
FOREIGN KEY (administrator) REFERENCES league_user(username) ON DELETE CASCADE,
FOREIGN KEY (game_or_genre) REFERENCES game(game_name) ON DELETE CASCADE
);


INSERT INTO game (game_name, genre, developer, release_date) VALUES
('Valorant', 'FPS', 'Riot Games', '20200602'),
('CS:GO', 'FPS', 'Valve', '20120821'),
('League of Legends', 'MOBA', 'Riot Games', '20091027'),
('Super Smash Bros: Ultimate', 'Fighter', 'BANDAI NAMCO Studios', '20181207');

INSERT INTO league_user (username, user_password) VALUES
('KapLeague221', 'llj$kamb2'),
('AStealmach1', 'g#dr5s7yh'),
('Exampleuser8823', 'password'),
('ronaldomessifan', 'soccer4life');

INSERT INTO league (administrator, game_or_genre) VALUES
('KapLeague221', 'Valorant'),
('AStealmach1', 'CS:GO'),
('Exampleuser8823', 'League of Legends'),
('ronaldomessifan', 'Super Smash Bros: Ultimate');

CREATE TABLE team(
team_name VARCHAR(30) PRIMARY KEY NOT NULL UNIQUE,
owner_name VARCHAR(40) NOT NULL
);

INSERT INTO team (team_name, owner_name) VALUES
('100 Thieves', 'Matthew Haag'),
('Sentinels', 'Rob Moore'),
('Golden Guardians', 'Joe Lacob'),
('Cloud9', 'Jack Etienne'),
('FaZe Clan', 'Thomas Oliveira'),
('G2', 'Carlos Rodriguez'),
('T1', 'Joe Marsh'),
('TSM', 'Andy Dinh');


CREATE TABLE game_team(
team_name VARCHAR(40) NOT NULL UNIQUE,
game_name VARCHAR(40) NOT NULL,
manager VARCHAR(40) NOT NULL,
captain VARCHAR(40) PRIMARY KEY NOT NULL UNIQUE,
wins INT,
losses INT,
FOREIGN KEY (team_name) REFERENCES team(team_name) ON DELETE CASCADE,
FOREIGN KEY (game_name) REFERENCES game(game_name) ON DELETE CASCADE
);

INSERT INTO game_team (team_name, game_name, manager, captain, wins, losses) VALUES
('100 Thieves', 'Valorant', 'PapaSmithy', 'Hiko', 0, 1),
('Sentinels', 'Valorant', 'Kez', 'ShahZaM', 1, 0),
('FaZe Clan', 'CS:GO', 'RobbaN', 'karrigan', 0, 1),
('G2', 'CS:GO', 'NiaK', 'nexa', 1, 0),
('T1', 'League of Legends', 'Moon Kyung-nam', 'N/A', 1, 0),
('TSM', 'League of Legends', 'Leena', 'Spica', 0, 1),
('Cloud9', 'Super Smash Bros: Ultimate', 'Young Kim', 'Mang0', 1, 0),
('Golden Guardians', 'Super Smash Bros: Ultimate', 'N/A', 'Zain', 0, 1);

CREATE TABLE player(
player_name VARCHAR(40) NOT NULL UNIQUE,
game VARCHAR(40) NOT NULL,
team_name VARCHAR(30) NOT NULL,
username VARCHAR(40) PRIMARY KEY  NOT NULL,
FOREIGN KEY (game) REFERENCES game(game_name) ON DELETE CASCADE,
FOREIGN KEY (team_name) REFERENCES team(team_name) ON DELETE CASCADE
);


INSERT INTO player (player_name, game, team_name, username) VALUES
('Tyson Ngo', 'Valorant', 'Sentinels', 'TenZ'),
('Peter Mazuryk', 'Valorant', '100 Thieves', 'Asuna'),
('Olof Gustafsson', 'CS:GO', 'FaZe Clan', 'Olofmeister'),
('Kenny Schrub', 'CS:GO', 'G2', 'kennyS'),
('Lee Sang-hyeok', 'League of Legends', 'T1', 'Faker'),
('Søren Bjerg', 'League of Legends', 'TSM', 'Bjergsen'),
('Joseph Marquez', 'Super Smash Bros: Ultimate', 'Cloud9', 'Mang0'),
('Zain Naghmi', 'Super Smash Bros: Ultimate', 'Golden Guardians', 'Zain');



CREATE TABLE league_match(
win_team VARCHAR(40) NOT NULL,
lose_team VARCHAR(40) NOT NULL,
match_length INT,
game VARCHAR(40) NOT NULL,
MVP VARCHAR(40) NOT NULL,
FOREIGN KEY (game) REFERENCES game(game_name),
FOREIGN KEY (win_team) REFERENCES team(team_name) ON DELETE CASCADE,
FOREIGN KEY (lose_team) REFERENCES team(team_name) ON DELETE CASCADE
);

INSERT INTO league_match (game, win_team, lose_team, match_length, MVP) VALUES
('Valorant', 'Sentinels', '100 Thieves', 121, 'TenZ'),
('CS:GO', 'G2', 'FaZe Clan', 165, 'kennyS'),
('League of Legends', 'T1', 'TSM', 80, 'Faker'),
('Super Smash Bros: Ultimate', 'Cloud9', 'Golden Guardians', 43, 'Mang0');



#Create Procedures to trasnlate to the methods (use the flow chart for reference)






