class Elo_Pool():
    def __init__(self):
        self.data = {}
    
    def add_player(self, fide_id: str, name: str, initial_elo=1400.0):
        self.data[fide_id] = {
            "name": name,
            "elo": initial_elo,
            "k_data": {
                "games_played": 0,
                "hit_2400": False if initial_elo < 2400 else True
            }
        }
    
    def calculate_k(self, k_data):
        if k_data["hit_2400"]:
            k = 10
        elif k_data["games_played"] >= 30:
            k = 20
        else:
            k = 40
        return k

    def process_game(self, game):
        # Add the players if they don't exist already
        for colour in ["White", "Black"]:
            if game[colour + "FideId"] not in self.data:
                try:
                    self.add_player(game[colour + "FideId"], game[colour], float(game[colour + "Elo"]))
                except ValueError:
                    self.add_player(game[colour + "FideId"], game[colour])
        
        # Update elo for both players according to the formula
        rating_gap = self.data[game["WhiteFideId"]]["elo"] - self.data[game["BlackFideId"]]["elo"]
        rating_gap = max(min(rating_gap, 400), -400)

        white_expected = 1 / (1 + 10 ** (-rating_gap / 400))
        black_expected = 1 / (1 + 10 ** (rating_gap / 400))

        white_k = self.calculate_k(self.data[game["WhiteFideId"]]["k_data"])
        black_k = self.calculate_k(self.data[game["BlackFideId"]]["k_data"])

        white_change = white_k * (game["WhiteScore"] - white_expected)
        black_change = black_k * ((1 - game["WhiteScore"]) - black_expected)

        self.data[game["WhiteFideId"]]["elo"] += white_change
        self.data[game["BlackFideId"]]["elo"] += black_change

        # if game["WhiteFideId"] == "1503014":
        #     print("Opponent: " + str(self.data[game["BlackFideId"]]["name"]))
        #     print("Rating gap: " + str(rating_gap))
        #     print("Expected score: " + str(white_expected))
        #     print("Actual score: " + str(game["WhiteScore"]))
        #     print("k factor: " + str(white_k))
        #     print("Rating change: " + str(white_change))
        #     print("New elo: " + str(self.data[game["WhiteFideId"]]["elo"]) + '\n')
        # if game["BlackFideId"] == "1503014":
        #     print("Opponent: " + str(self.data[game["WhiteFideId"]]["name"]))
        #     print("Rating gap: " + str(-rating_gap))
        #     print("Expected score: " + str(black_expected))
        #     print("Actual score: " + str((1 - game["WhiteScore"])))
        #     print("k factor: " + str(black_k))
        #     print("Rating change: " + str(black_change))
        #     print("New elo: " + str(self.data[game["BlackFideId"]]["elo"]) + '\n')

        # Update k-factor data for both players
        for colour in ["White", "Black"]:
            self.data[game[colour + "FideId"]]["k_data"]["games_played"] += 1
            if self.data[game[colour + "FideId"]]["elo"] >= 2400:
                self.data[game[colour + "FideId"]]["k_data"]["hit_2400"] = True
