import LiveScore

incidents = LiveScore.getIncidents(1071929).incidents

for incident in incidents:
    print(incident)

