from tests.conftest import client

import os
import sys
import time
sys.path.append("..")
import server
# from server import saveClubs, saveCompetitions

jsonClub = 'test_clubs.json'
jsonCompetition = 'test_competitions.json'


def setup_module():
    server.jsonClub = 'test_clubs.json'
    server.jsonCompetition = 'test_competitions.json'
    server.competitions[1]['date'] = "2023-10-22 13:30:00"
    server.saveClubs(server.clubs)
    server.saveCompetitions(server.competitions)
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()


def teardown_module():
    os.remove(jsonClub)
    os.remove(jsonCompetition)


def test_integration(client):
    reponseIndex = client.get('/')
    email = 'john@simplylift.co'
    reponseSummary = client.post('/showSummary', data={'email':email})
    reponseHome = client.get('/home')
    reponseBook = client.get('/book/Fall Classic/Simply Lift')
    foundCompetition = [c for c in server.competitions if c['name'] == 'Fall Classic']
    if foundCompetition:
        foundCompetition = foundCompetition[0]
    place_debut = foundCompetition['numberOfPlaces']
    reponsePurchase = client.post('/purchasePlaces', data={'competition':'Fall Classic', 'club':'Simply Lift', 'places':"3"})
    reponseLogout = client.get('/logout')
    reponseHomeLogout = client.get('/home')
    assert reponseIndex.status_code == 200
    assert reponseSummary.status_code == 302
    assert reponseHome.status_code == 200
    assert reponseBook.status_code == 200
    assert reponsePurchase.status_code == 302
    assert int(place_debut)-3 == int(foundCompetition['numberOfPlaces'])
    assert reponseLogout.status_code == 302
    assert reponseHomeLogout.status_code == 302
    
