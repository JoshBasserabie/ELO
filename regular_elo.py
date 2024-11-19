import constants
from elo_ratings import Elo_Pool
from PGNs import extract_PGN_data

fide_ratings = Elo_Pool()
for i in range(constants.PGN_DEFAULT_START, constants.PGN_DEFAULT_END):
    print("File number: " + str(i))
    games = extract_PGN_data(i)
    for game in games:
        fide_ratings.process_game(game)
        