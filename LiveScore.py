import httpx
from dataclasses import dataclass
from typing import List

@dataclass
class __Event:
    id: int
    home_team: str
    away_team: str
    start_time: int

@dataclass
class __Stage:
    name: str
    country: str
    events: List[__Event]

@dataclass
class __Incident:
    minute: int
    team: int
    player: str
    type: str

@dataclass
class __ScoreBoard:
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    status: str
    incidents: List[__Incident]

@dataclass
class __Incidents:
    home_score: int
    away_score: int
    incidents: List[__Incident]

def __convertType(type):
    match type:
        case 36:
            return 'Goal'
        case 43:
            return 'Yellow Card'
        case 44:
            return 'Second Yellow Card'
        case 45:
            return 'Red Card'
        case 63:
            return 'Assist'
        case 37:
            return 'Penalty Goal'
        case 39:
            return 'Own Goal'

def getStages(date):
    resp = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/date/soccer/{date}/1?countryCode=GB&locale=en')
    json = resp.json()

    stages = []

    for stage in json['Stages']:
        name = stage['Snm']
        country = stage['Cnm']
        
        eventsJson = stage['Events']

        events = []

        for event in eventsJson:
            id = event['Eid']
            home_team = event['T1'][0]['Nm']
            away_team = event['T2'][0]['Nm']
            start_time = event['Esd']

            events.append(__Event(id, home_team, away_team, start_time))

        stages.append(__Stage(name, country, events))

    return stages

def getScoreBoard(id, includeAssists = False):
    resp = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/scoreboard/soccer/{id}?locale=en')
    json = resp.json()

    home_team = json['T1'][0]['Nm']
    away_team = json['T2'][0]['Nm']
    home_score = json['Tr1']
    away_score = json['Tr2']
    status = json['Eps']

    incidents = []

    for n in json['Incs-s']:
        for inc in json['Incs-s'][n]:
            minute = inc['Min']
            team = inc['Nm']

            if 'Pn' in inc and 'IT' in inc:
                player = inc['Pn']
                type = __convertType(inc['IT'])

                if type != 'Assist' or includeAssists == True:
                    incidents.append(__Incident(minute, team, player, type))
            else:
                for subInc in inc['Incs']:
                    player = subInc['Pn']
                    type = __convertType(subInc['IT'])

                    if type != 'Assist' or includeAssists == True:
                        incidents.append(__Incident(minute, team, player, type))
    
    return __ScoreBoard(home_team, away_team, home_score, away_score, status, incidents)

def getIncidents(id, includeAssists = False):
    resp = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/incidents/soccer/{id}?locale=en')
    json = resp.json()

    home_score = json['Tr1']
    away_score = json['Tr2']

    incidents = []

    for n in json['Incs']:
        for inc in json['Incs'][n]:
            minute = inc['Min']
            team = inc['Nm']

            if 'Pn' in inc and 'IT' in inc:
                player = inc['Pn']
                type = __convertType(inc['IT'])

                if type != 'Assist' or includeAssists == True:
                    incidents.append(__Incident(minute, team, player, type))
            else:
                for subInc in inc['Incs']:
                    player = subInc['Pn']
                    type = __convertType(subInc['IT'])

                    if type != 'Assist' or includeAssists == True:
                        incidents.append(__Incident(minute, team, player, type))

    return __Incidents(home_score, away_score, incidents)