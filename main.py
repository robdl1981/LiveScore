from LiveScore2 import LiveScore
from rich import print

# incidents = LiveScore.getIncidents(1071929).incidents

# for incident in incidents:
#     print(incident)

livescore = LiveScore()

test = livescore.getGameInPlay(966795)

print(test)

