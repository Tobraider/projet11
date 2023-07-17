from tests.conftest import client, connecte

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


def test_index(client):
    reponse = client.get('/')
    assert reponse.status_code == 200


def test_tablePoints(client):
    reponse = client.get('/tablePoints')
    assert reponse.status_code == 200


def test_showSummary(client):
    email = 'john@simplylift.co'
    reponse = client.post('/showSummary', data={'email':email})
    assert reponse.status_code == 302


def test_showSummaryNOK(client):
    email = 'izefhiz@hdiah.fehhf'
    reponse = client.post('/showSummary', data={'email':email})
    assert reponse.status_code == 302


def test_book(client):
    reponse = client.get('/book/Spring Festival/Simply Lift')
    assert reponse.status_code == 401


def test_purchasePlaces(client):
    reponse = client.post('/purchasePlaces')
    assert reponse.status_code == 401


def test_logout(client):
    reponse = client.get('/logout')
    assert reponse.status_code == 401


# TEST CONNECTE
def test_home(connecte):
    reponse = connecte.get('/home')
    assert reponse.status_code == 200


def test_book(connecte):
    reponse = connecte.get('/book/Spring Festival/Simply Lift')
    assert reponse.status_code == 200


def test_bookError(connecte):
    reponse = connecte.get('/book/Spring Festival/Siply Lift')
    assert reponse.status_code == 302


def test_purchasePlaces(connecte):
    foundCompetition = [c for c in server.competitions if c['name'] == 'Spring Festival']
    if foundCompetition:
        foundCompetition = foundCompetition[0]
    place_debut = foundCompetition['numberOfPlaces']
    reponse = connecte.post('/purchasePlaces', data={'competition':'Spring Festival', 'club':'Simply Lift', 'places':"11"})
    assert reponse.status_code == 302
    assert int(place_debut) == int(foundCompetition['numberOfPlaces'])


def test_purchasePlacesEncore(connecte):
    foundCompetition = [c for c in server.competitions if c['name'] == 'Fall Classic']
    if foundCompetition:
        foundCompetition = foundCompetition[0]
    place_debut = foundCompetition['numberOfPlaces']
    reponse = connecte.post('/purchasePlaces', data={'competition':'Fall Classic', 'club':'Simply Lift', 'places':"1"})
    assert reponse.status_code == 302
    assert int(place_debut)-1 == int(foundCompetition['numberOfPlaces'])


def test_logout(connecte):
    reponse = connecte.get('/logout')
    assert reponse.status_code == 302
