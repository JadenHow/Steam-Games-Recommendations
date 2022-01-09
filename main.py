"""Main"""

import os
import display
import read

# INSTRUCTION: Make sure that the steam.csv file is in the right location. It should be in a
# folder named 'datasets'. read.py, compute.py, display.py, main.py, and datasets folder should
# be in the same folder. When inserting your games, you should refer to the game name on steam.
# Capital letters and symbols matter when you are inputting the game name. For example:
# 'Counter-Strike' should not be spelled 'counter-strike', 'counter - strike', or 'Counter-strike'.
# The similarity score is calculated based on your preference, whether it be the category, genre,
# tag, or developer of the game. It can be one or even all! When the question asks for the number
# of games or maximum price, please input the number but not the spelling of the number. Our
# rating score of the game is calculated by the number of positive ratings over the sum of the
# number of positive ratings and the number of negative ratings multiply by 100. There is also an
# option for you to input the minimum rating score for your recommended games.
# It can be from 0 to 100. That is all there is for the instruction. Have fun using it!

game_graph = None
if os.path.exists("datasets/steam.csv"):
    game_graph = read.load_game_graph("datasets/steam.csv")
else:
    print("File not found, please ensure your file is in the right location.")
    exit()


print("Welcome to Steam games recommendation app!")

while True:
    # Game
    games = input("Please type in the games you have played.")
    list_of_games = [(game1.strip(), "game") for game1 in games.split(",")]

    for game in list_of_games:
        try:
            game_graph.get_vertex(game[0], "game")
        except ValueError:
            print(f"Invalid game input: {game[0]}, please try again.")
            exit()

    # Category
    requirements = \
        input("Please type in the categories you want to compare. [category, genre, tag, developer]"
              )
    requirements.replace(" ", "")

    requirements_list = [requirement for requirement in requirements.split(",") if requirement in
                         ['category', 'genre', 'tag', 'developer']]

    if requirements == '' or requirements_list == []:
        requirements_list = ["category", "genre", "tag", "developer"]

    # Limit
    limit = int(input("How many games would you like to see? Please type in a number."))

    # Max Price
    max_price = input("Is there a maximum price you would like to set? If not press enter.")

    if max_price != '':
        max_price = float(max_price)
    else:
        max_price = None

    # Platform
    platforms = input("Which platforms are you playing on? [windows, mac, linus]")
    platforms.replace(" ", "")
    platform_list = [platform for platform in platforms.split(",")
                     if platforms in ["windows", "mac", "linus"]]

    if platform_list is None:
        print("Please type in windows, mac, or linus.")

    # Minimum rating score
    min_rating_score = \
        input("Is there a minimum rating score you would like to set? If not press enter.")

    if min_rating_score:
        min_rating_score = float(min_rating_score)
    else:
        min_rating_score = None

    # Recommend
    recommend_list = game_graph.recommend_multiple_games(list_of_games,
                                                         limit, requirements_list, max_price,
                                                         platform_list, min_rating_score)

    if recommend_list == []:
        print("No games found based on input, try again.")
    else:
        display.display_result(game_graph, recommend_list)

    while True:
        answer = input("Do you want to continue? [yes or no]")

        if answer.lower() == "no":
            exit()
        elif answer.lower() == "yes":
            print("=================================================")
            break
        else:
            print("Sorry, I don't understand your input")
