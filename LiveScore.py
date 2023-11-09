import httpx
from dataclasses import dataclass
from typing import List

@dataclass
class Event:
    id: int
    home_team: str
    away_team: str
    start_time: int

@dataclass
class Stage:
    name: str
    country: str
    events: List[Event]

@dataclass
class Incident:
    minute: int
    team: int
    player: str
    type: str

@dataclass
class ScoreBoard:
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    status: str
    incidents: List[Incident]

@dataclass
class Incidents:
    home_score: int
    away_score: int
    incidents: List[Incident]

@dataclass
class Result:
    id: int
    date: int
    time: int

def convertType(type):
    match type:
        case 36:
            return 'Goal'
        case 37:
            return 'Penalty Goal'
        case 38:
            return 'Penalty Miss'
        case 39:
            return 'Own Goal'
        case 43:
            return 'Yellow Card'
        case 44:
            return 'Second Yellow Card'
        case 45:
            return 'Red Card'
        case 62:
            return 'VAR'
        case 63:
            return 'Assist'

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

            events.append(Event(id, home_team, away_team, start_time))

        stages.append(Stage(name, country, events))

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
                type = convertType(inc['IT'])

                if type != 'Assist' or includeAssists == True:
                    incidents.append(Incident(minute, team, player, type))
            else:
                for subInc in inc['Incs']:
                    player = subInc['Pn']
                    type = convertType(subInc['IT'])

                    if type != 'Assist' or includeAssists == True:
                        incidents.append(Incident(minute, team, player, type))
    
    return ScoreBoard(home_team, away_team, home_score, away_score, status, incidents)

def getIncidents(id, includeAssists = False):
    resp = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/incidents/soccer/{id}?locale=en')
    json = resp.json()

    home_score = json['Tr1']
    away_score = json['Tr2']

    incidents = []

    if 'Incs' in json:
        for n in json['Incs']:
            for inc in json['Incs'][n]:
                minute = inc['Min']
                team = inc['Nm']

                if 'Pn' in inc and 'IT' in inc:
                    player = inc['Pn']
                    type = convertType(inc['IT'])

                    if type != 'Assist' or includeAssists == True:
                        incidents.append(Incident(minute, team, player, type))
                else:
                    for subInc in inc['Incs']:
                        player = subInc['Pn']
                        type = convertType(subInc['IT'])

                        if type != 'Assist' or includeAssists == True:
                            incidents.append(Incident(minute, team, player, type))

        return Incidents(home_score, away_score, incidents)
    else:
        return None

def findGame(date, team):
    stages = getStages(date)

    for stage in stages:
        for event in stage.events:
            if event.home_team == team or event.away_team == team:
                return Result(int(event.id), int(str(event.start_time)[:8]), int(str(event.start_time)[8:12]))
    
    return None