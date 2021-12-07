import pymysql

from util import *
from League_Team import *
import time

conn = pymysql.connect(host='localhost', user='root', password='Mamaitato345', db='esleague')

cur = conn.cursor()


def check(query):
    return execute_query(cur, query)
    

def view_stats():
    print("Viewing stats")
    teams = execute_query(cur, "SELECT * FROM game_team")
    for team in teams:
        print("Team Name: ", team[0].ljust(20),
              "Game Name: ".ljust(5),
              team[1].ljust(20), "Manager: ".rjust(20),
              team[2].ljust(20), "Captain: ".ljust(20),
              team[3].ljust(20), "Wins: ".ljust(5),
              str(team[4]).ljust(5), "Losses: ".ljust(5),
              str(team[5]).ljust(5))

    print()
    print()
    time.sleep(1.5)
        

def create_org():
    print("Creating team")
    team_name = input("Please enter the name of the team: ")
    owner_name = input("Please enter the name of the owner: ")
    
    if check("SELECT team_name FROM team WHERE team_name = '" + team_name + "'"):
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
    
    if check("SELECT team_name FROM team WHERE team_name = '" + org + "'"):
        cur.callproc("create_team", [org, name_of_game, manager_name, captain_name, win_amount, loss_amount])
        print("TEAM CREATED")
    else:
        print("TEAM ALREADY EXISTS.")

    
def simulate_matches():
    teams = list(execute_query(cur, "SELECT * FROM team"))
    if len(teams) < 2:
        print("Not enough teams to simulate matches")
        return

    if len(teams) % 2 != 0:
        teams = teams[:-1]
        
    for teams in batch(teams, 2):
        first_team = teams[0]
        second_team = teams[1]
        team_1 = Team(first_team[0], first_team[1])
        team_2 = Team(second_team[0], second_team[1])
        simulate_match(conn, cur, team_1, team_2)
        
    
    for _ in range(10):
        print()
        
    print("View stats to see updated scores")

def create_game():
    name = input("Please enter the name of the game: ")
    genre = input("Please enter the genre of the game: ")
    developer_name = input("Please enter the name of the developer: ")
    date_released = input("Please enter the date the game was released: ")
    
    if check("SELECT game_name FROM game WHERE game_name = '" + name + "'"):
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
    
    time.sleep(1.5)
    
def delete_entries(conn, cur):
    print("1) Delete a game")
    print("2) Delete a team")
    print("3) Delete a match")
    print("4) Delete a player")
    print("5) Delete an organization")
      
    valid = False
    while not valid:
        try:
            user_input = input(
                "Choose which table you would like to delete from: ")
            valid = int(user_input) in range(1, 6)
        except:
            print("Invalid input")
    
    if user_input == "1":
        game_name = input("Please enter the name of the game: ")
        
        if not check("SELECT game_name FROM game WHERE game_name = '" + game_name + "'"):
            print("GAME DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM game WHERE game_name = '" + game_name + "'")
            print("GAME DELETED")
            
    elif user_input == "2":
        team_name = input("Please enter the name of the team: ")
        if not check("SELECT team_name FROM team WHERE team_name = '" + team_name + "'"):
            print("TEAM DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM team WHERE team_name = '" + team_name + "'")
            print("TEAM DELETED")
            
    elif user_input == "3":
        match_name = input("Please enter the name of the match: ")
        if not check("SELECT match_name FROM match WHERE match_name = '" + match_name + "'"):
            print("MATCH DOES NOT EXIST")
            
        else:
            execute_query(cur, "DELETE FROM match WHERE match_name = '" + match_name + "'")
            print("MATCH DELETED")
            
    elif user_input == "4":
        player_name = input("Please enter the name of the player: ")
        if not check("SELECT player_name FROM player WHERE player_name = '" + player_name + "'"):
            print("PLAYER DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM player WHERE player_name = '" + player_name + "'")
            print("PLAYER DELETED")
            
    else:
        org_name = input("Please enter the name of the organization: ")
        if not check("SELECT team_name FROM team WHERE team_name = '" + org_name + "'"):
            print("ORGANIZATION DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM team WHERE team_name = '" + org_name + "'")
            print("ORGANIZATION DELETED")
            
            
    conn.commit()
    
def update_entries(conn, cur):
    print("1) Update a game")
    print("2) Update a match")
    print("3) Update a player")
    print("4) Update an organization")
    
    valid = False
    while not valid:
        try:
            user_input = input(
                "Choose which table you would like to delete from: ")
            valid = True and int(user_input) in range(1, 6)
        except:
            print("Invalid input")
            
    if user_input == "1":
        print("Updating game")
        game_name = input("Please enter the name of the game: ")
        genre = input("Please enter the genre of the game: ")
        developer = input("Please enter the name of the developer: ")
        release_date = input("Please enter the date the game was released: ")
        
        cur.execute("UPDATE game SET genre = '" + genre + "', developer = '" + developer + "', release_date = '" + release_date + "' WHERE game_name = '" + game_name + "'")
        
    if user_input == "2":
        print("Updating match")
        key = input("Please enter the length of the match you would like to update: ")
        win_team = input("Please enter the name of the winning team: ")
        lose_team = input("Please enter the name of the losing team: ")
        match_length = int(input("Please enter the length of the match: "))
        game = input("Please enter the name of the game: ")
        MVP = input("Please enter the name of the MVP: ")
        
        cur.execute("UPDATE league_match SET win_team = '" + win_team + "', lose_team = '" + lose_team + "', match_length = '" + str(match_length) + "', game = '" + game + "', MVP = '" + MVP + "' WHERE match_length = '" + key + "'")
        
        
    if user_input == "3":
        print("Updating player")
        player_name = input("Please enter the name of the player you wish to update: ")
        game_name = input("Please enter the name of the game the player is playing: ")
        team_name = input("Please enter the name of the team the player is on: ")
        username = input("Please enter the username of the player: ")
        
        cur.execute("UPDATE player SET game_name = '" + game_name + "', team_name = '" + team_name + "', username = '" + username + "' WHERE player_name = '" + player_name + "'")
        
    if user_input == "4":
        print("Updating game")
        game_name = input("Please enter the name of the game: ")
        genre = input("Please enter the genre of the game: ")
        developer = input("Please enter the name of the developer: ")
        release_date = input("Please enter the date the game was released: ")

        cur.execute("UPDATE game SET genre = '" + genre + "', developer = '" + developer +
                    "', release_date = '" + release_date + "' WHERE game_name = '" + game_name + "'")
        
    if user_input == "5":
        print("Updating game")
        game_name = input("Please enter the name of the game: ")
        genre = input("Please enter the genre of the game: ")
        developer = input("Please enter the name of the developer: ")
        release_date = input("Please enter the date the game was released: ")

        cur.execute("UPDATE game SET genre = '" + genre + "', developer = '" + developer +
                    "', release_date = '" + release_date + "' WHERE game_name = '" + game_name + "'")
        
        
    conn.commit()
            
    
        
    

while True:
    print("1) view stats")
    print("2) view matches")
    print("3) simulate matches")
    print("4) create game")
    print("5) create team")
    print("6) create organization")
    print("7) delete entries")
    print("8) update entries")
    print("9) exit")

    user_input = input(
        "Greetings, this is the main menu. Please select an option (enter a number):")
    
    try: 
        if int(user_input) == 1:
            view_stats()
            
        if int(user_input) == 2:
            view_matches()
            
        if int(user_input) == 3:
            simulate_matches()
            
        if int(user_input) == 4:
            create_game()
        
        if int(user_input) == 5:
            create_team()
            
        if int(user_input) == 6:
            create_org()
            
        if int(user_input) == 7:
            delete_entries(conn, cur)
            
        if int(user_input) == 8:
            update_entries(conn, cur)
            
        if int(user_input) == 9:
            conn.close()
            exit()
    except:
        continue
