import pymysql

from util import *
from League_Team import *

conn = pymysql.connect(host='localhost', user='root', password='Mamaitato345', db='esleague')

cur = conn.cursor()


def view_stats():
    print("Viewing stats")
    teams = execute_query(cur, "SELECT * FROM game_team")
    for team in teams:
        print("Team Name: ", team[0].ljust(10), "Game Name: ".ljust(
            10), team[1].ljust(10), "Manager: ".rjust(10), team[2].ljust(10), "Captain: ".ljust(10), team[3].ljust(10), "Wins: ".ljust(10), str(team[4]).ljust(10), "Losses: ".ljust(10), str(team[5]).ljust(10))
        
    print()
    print()
        

def create_team():
    print("Creating team")
    team_name = input("Please enter the name of the team: ")
    owner_name = input("Please enter the name of the owner: ")
    check = execute_query(
        cur, "SELECT team_name FROM team WHERE team_name = '" + team_name + "'")
    if len(check) == 0:
        cur.execute("INSERT INTO team VALUES (%s, %s)",
                    (team_name, owner_name))
        conn.commit()
        print("TEAM CREATED")
    else:
        print("TEAM ALREADY EXISTS.")
    
    print()
    print()

    


def simulate_matches():
    teams = execute_query(cur, "SELECT * FROM team")
    for teams in batch(list(teams), 2):
        first_team = teams[0]
        second_team = teams[1]
        team_1 = Team(first_team[0], first_team[1])
        team_2 = Team(second_team[0], second_team[1])
        simulate_match(conn, cur, team_1, team_2)
        

while True:
    print("1) view stats")
    print("2) create team")
    print("3) simulate matches")
    print("4) exit")

    user_input = input(
        "Greetings, this is the main menu. Please select an option (enter a number):")
    
    if int(user_input) in range(1, 5):
        valid_input = True
        
    if int(user_input) == 1:
        view_stats()
        
    if int(user_input) == 2:
        create_team()
        
    if int(user_input) == 3:
        simulate_matches()
        
    if int(user_input) == 4:
        conn.close()
        exit()
