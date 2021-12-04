import random
from util import execute_query

class Team:
    
    def __init__(self, name, owner_name) -> None:
        self.name = name
        self.owner_name = owner_name


def simulate_match(conn, cur, team1: Team, team2: Team):
    if random.random() < 0.5:
        execute_query(
            cur, f"UPDATE game_team SET wins = wins + 1 WHERE team_name = '{team1.name}'")
        execute_query(
            cur, f"UPDATE game_team SET losses = losses + 1 WHERE team_name = '{team2.name}'")
    else:
        execute_query(
            cur, f"UPDATE game_team SET wins = wins + 1 WHERE team_name = '{team2.name}'")
        execute_query(
            cur, f"UPDATE game_team SET losses = losses + 1 WHERE team_name = '{team1.name}'")

    conn.commit()
