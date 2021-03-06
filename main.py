import pymysql

from util import *
from League_Team import *
import time

conn = None
cur = None

def clear():
    for _ in range(10):
        print()


def check(query):
    return not len(execute_query(cur, query))


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
        conn.commit()
        print("TEAM CREATED")
    else:
        print("TEAM ALREADY EXISTS.")

    print()
    print()


def create_team():
    team_name = input("Please enter the name of the team: ")
    name_of_game = input("Please enter the name of the game: ")
    manager_name = input("Please enter the name of the manager: ")
    captain_name = input("Please enter the name of the captain: ")
    win_amount = input("Please enter the amount of wins: ")
    loss_amount = input("Please enter the amount of losses: ")

    if check("SELECT team_name FROM team WHERE team_name = '" + team_name + "'"):
        cur.callproc("insert_team", [team_name, name_of_game, manager_name, captain_name, win_amount, loss_amount])
        conn.commit()
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
    result = execute_query(cur, "SELECT * FROM league_match")
    for row in result:
        print("Win Team: ", str(row[1]).ljust(10), "Losing Team: ".ljust(10), row[2].ljust(10), "Match Length: ".ljust(10),
              str(row[3]).ljust(10), "MVP: ".ljust(10), row[5])
    print()
    print()

    time.sleep(1)


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

        if check("SELECT game_name FROM game WHERE game_name = '" + game_name + "'"):
            print("GAME DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM game WHERE game_name = '" + game_name + "'")
            print("GAME DELETED")

    elif user_input == "2":
        team_name = input("Please enter the name of the team: ")
        name_of_game = input("Please enter the name of the game you would like the organization to be removed from: ")

        if check("SELECT team_name, game_name FROM game_team WHERE team_name = '" + team_name +
                "' AND game_name = '" + name_of_game + "'"):
            print("TEAM DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM game_team WHERE team_name = '" + team_name +
                "' AND game_name = '" + name_of_game + "'")
            print("TEAM DELETED")

    elif user_input == "3":
        match_id = input("Please enter the match ID: ")
        if check("SELECT match_id FROM league_match WHERE match_id = '" + match_id + "'"):
            print("MATCH DOES NOT EXIST")

        else:
            execute_query(cur, "DELETE FROM league_match WHERE match_id = '" + match_id + "'")
            print("MATCH DELETED")

    elif user_input == "4":
        player_name = input("Please enter the name of the player: ")
        if check("SELECT player_name FROM player WHERE player_name = '" + player_name + "'"):
            print("PLAYER DOES NOT EXIST")
        else:
            execute_query(cur, "DELETE FROM player WHERE player_name = '" + player_name + "'")
            print("PLAYER DELETED")

    else:
        org_name = input("Please enter the name of the organization: ")
        if check("SELECT team_name FROM team WHERE team_name = '" + org_name + "'"):
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
                "Choose which table you would like to view from: ")
            valid = True and int(user_input) in range(1, 6)
        except:
            print("Invalid input")

    if user_input == "1":
        print("Updating game")
        game_name = input("Please enter the name of the game to update: ")
        genre = input("Please enter the updated genre of the game: ")
        developer = input("Please enter the updated name of the developer: ")

        if check("SELECT game_name FROM game WHERE game_name = '" + game_name + "'"):
            print("GAME DOES NOT EXIST")
        else:
            cur.execute(
                "UPDATE game SET genre = '" + genre + "',"
                         " developer = '" + developer + "' WHERE game_name = '" + game_name + "'")
            print("Updated Game")

    if user_input == "2":
        print("Updating match")
        key = input("Please enter the ID of the match you would like to update: ")
        win_team = input("Please enter the updated name of the winning team: ")
        lose_team = input("Please enter the updated name of the losing team: ")
        game = input("Please enter the updated name of the game: ")
        MVP = input("Please enter the updated name of the MVP: ")

        if check("SELECT match_id FROM league_match WHERE match_id = '" + key + "'"):
            print("MATCH DOES NOT EXIST")
        else:
            cur.execute(
                "UPDATE league_match SET win_team = '" + win_team + "', lose_team = '" + lose_team + "'"
                                ", game = '" + game + "', MVP = '" + MVP + "' WHERE match_id = '" + key + "'")
            print("Updated Match")

    if user_input == "3":
        print("Updating player")
        player_name = input("Please enter the name of the player you wish to update: ")
        game_name = input("Please enter the updated name of the game the player plays: ")
        team_name = input("Please enter the updated name of the team the player is on: ")
        username = input("Please enter the updated username of the player: ")

        if check("SELECT player_name FROM player WHERE player_name = '" + player_name + "'"):
            print("PLAYER DOES NOT EXIST")
        else:
            cur.execute(
                "UPDATE player SET game = '" + game_name + "', team_name = '" + team_name + "',"
                    " username = '" + username + "' WHERE player_name = '" + player_name + "'")
            print("Updated player")

    if user_input == "4":
        print("Updating Organization")
        org_name = input("Please enter the name of the organization: ")
        owner_name = input("Please enter the updated owner of the org: ")

        if check("SELECT team_name FROM team WHERE team_name = '" + org_name + "'"):
            print("ORGANIZATION DOES NOT EXIST")
        else:
            cur.execute("UPDATE team SET owner_name = '" + owner_name + "' WHERE team_name = '" + org_name + "'")
            print("Organization Updated")

    conn.commit()


def view_info_about_league():
    print("1) view stats of teams")
    print("2) view a video game")
    print("3) view admins of the league")
    print("4) view all matches")
    print("5) view all players")
    print("6) view teams and their owners")

    valid = False
    while not valid:
        try:
            user_input = input(
                "Choose which table you would like to view: ")
            valid = int(user_input) in range(1, 7)
        except:
            print("Invalid input, choose again")

    if user_input == "1":
        view_stats()

    if user_input == "2":
        result = execute_query(cur, "SELECT * FROM game")
        for row in result:
            print("Game Name: " + row[0].ljust(20), "Genre: " + row[1].ljust(20), "Developer: " +
                  row[2].ljust(20), "Release Date: " + row[3].strftime("%m/%d/%Y"))

    if user_input == "3":
        result = execute_query(
            cur, "SELECT administrator, game_or_genre FROM league")
        for row in result:
            print("Administrator: " + row[0].ljust(20), "Game or Genre: " + row[1].ljust(20))

    if user_input == "4":
        view_matches()

    if user_input == "5":
        result = execute_query(cur, "SELECT * FROM player")
        for row in result:
            print("Player Name: " + row[0].ljust(15), "Game: " + row[1].ljust(20), "Team Name: " + row[2].ljust(10), "Username: " + row[3])

    if user_input == "6":
        result = execute_query(cur, "SELECT * FROM team")
        for row in result:
            print("Team Name: " + row[0].ljust(20), "Owner Name: " + row[1])



    time.sleep(1.5)
    print()
    print()


def run(given=None):
    global conn, cur
    
    if given is None:
        conn = pymysql.connect(host='localhost', user='root',
                               password='Mamaitato345', db='esleague')
    else:
        conn = given
        
    cur = conn.cursor()
    
    
    while True:

        print("1) View info about the League")
        print("2) simulate matches")
        print("3) create game")
        print("4) create team")
        print("5) create organization")
        print("6) delete entries")
        print("7) update entries")
        print("8) exit")

        user_input = input(
            "Greetings, this is the main menu. Please select an option (enter a number):")

        try:
            if int(user_input) == 1:
                    clear()
                    view_info_about_league()

            if int(user_input) == 2:
                    clear()
                    simulate_matches()
                    view_matches()

            if int(user_input) == 3:
                    clear()
                    create_game()

            if int(user_input) == 4:
                    clear()
                    create_team()

            if int(user_input) == 5:
                    clear()
                    create_org()

            if int(user_input) == 6:
                    clear()
                    delete_entries(conn, cur)

            if int(user_input) == 7:
                    clear()
                    update_entries(conn, cur)

            if int(user_input) == 8:
                    conn.close()
                    exit()
                    
        except:
            clear()
            print("Invalid input, please try again")
            continue



if __name__ == "__main__":
    run()