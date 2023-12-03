from LiveScore import LiveScore, Game, GameInPlay
from rich import print
from typing import List

# incidents = LiveScore.getIncidents(1071929).incidents

# for incident in incidents:
#     print(incident)

livescore = LiveScore()

# games: List[Game] = livescore.getGames('20231202', 'Arsenal')

games: List[Game] = livescore.getGames()

print(games)

game_id = games[0].game_id

game: GameInPlay = livescore.getGameInPlay(game_id)

print(game)

