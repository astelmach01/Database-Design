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
        

def create_org():
    print("Creating team")
    team_name = input("Please enter the name of the team: ")
    owner_name = input("Please enter the name of the owner: ")
    check = execute_query(
        cur, "SELECT team_name FROM team WHERE team_name = '" + team_name + "'")
    if len(check) == 0:
        cur.callproc("insert_org", [team_name, owner_name])
        print("TEAM CREATED")
    else:
        print("TEAM ALREADY EXISTS.")
    
    print()
    print()
    
    
def create_team():
    org = input("Please enter the name of the organization: ")
    name_of_game = input("Please enter the name of the game: ")
    manager_name = input("Please enter the name of the manager: ")
    captain_name = input("Please enter the name of the captain: ")
    win_amount = input("Please enter the amount of wins: ")
    loss_amount = input("Please enter the amount of losses: ")
    
    check = execute_query(
        cur, "SELECT team_name FROM game_team WHERE team_name = '" + org + "'")
    if len(check) == 0:
        cur.callproc("create_team", [org, name_of_game, manager_name, captain_name, win_amount, loss_amount])
        print("TEAM CREATED")
    else:
        print("TEAM ALREADY EXISTS.")

    
def simulate_matches():
    teams = execute_query(cur, "SELECT * FROM team")
    for teams in batch(list(teams), 2):
        first_team = teams[0]
        second_team = teams[1]
        team_1 = Team(first_team[0], first_team[1])
        team_2 = Team(second_team[0], second_team[1])
        simulate_match(conn, cur, team_1, team_2)

def create_game():
    name = input("Please enter the name of the game: ")
    genre = input("Please enter the genre of the game: ")
    developer_name = input("Please enter the name of the developer: ")
    date_released = input("Please enter the date the game was released: ")
    
    check = execute_query(
        cur, "SELECT game_name FROM game WHERE game_name = '" + name + "'")
    if len(check) == 0:
        cur.callproc("insert_game", [name, genre, developer_name, date_released])
        conn.commit()
        print("GAME CREATED")
    else:
        print("GAME ALREADY EXISTS.")
        
    print()
    
        
def view_matches():
    print("Viewing matches")
    cur.callproc("view_match", [input("Please enter the name of the first team: "), input("Please enter the name of the second team: "), input("Please enter the name of the game played: ")])
    result = cur.fetchall()[0]
    print("Win Team: ", result[0].ljust(10), "Losing Team: ".ljust(10), result[1].ljust(10), "Match Length: ".ljust(10), str(result[2]).ljust(10), "MVP: ".ljust(10), result[4])
    print()
    print()

while True:
    print("1) view stats")
    print("2) create game")
    print("3) create team")
    print("4) simulate matches")
    print("5) create organization")
    print("6) view matches")

    print("7) exit")

    user_input = input(
        "Greetings, this is the main menu. Please select an option (enter a number):")
    
    if int(user_input) in range(1, 5):
        valid_input = True
        
    if int(user_input) == 1:
        view_stats()
        
    if int(user_input) == 2:
        create_game()
        
    if int(user_input) == 3:
        create_team()
        
    if int(user_input) == 4:
        simulate_matches()
    
    if int(user_input) == 5:
        create_org()
        
    if int(user_input) == 6:
        view_matches()
        
    if int(user_input) == 7:
        conn.close()
        exit()
