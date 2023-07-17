from locust import HttpUser, task, events
import os
import sys
sys.path.append("..")
import server

jsonClub = 'test_clubs.json'
jsonCompetition = 'test_competitions.json'

@events.test_start.add_listener
def on_test_start(**kwargs):
    server.jsonClub = 'test_clubs.json'
    server.jsonCompetition = 'test_competitions.json'
    server.competitions[0]['date'] = "2024-10-22 13:30:00"
    server.saveClubs(server.clubs)
    server.saveCompetitions(server.competitions)
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    server.jsonClub = 'clubs.json'
    server.jsonCompetition = 'competitions.json'
    os.remove(jsonClub)
    os.remove(jsonCompetition)

class ProjectPerfTest(HttpUser):
    
    @task
    def index(self):
        response = self.client.get("/")

    @task
    def tablePoints(self):
        response = self.client.get("/tablePoints")
        
    @task
    def login(self):
        response = self.client.post("/showSummary", {'email':"john@simplylift.co"})
        self.client.cookies = response.cookies

    @task
    def book(self):
        response = self.client.get('/book/Spring Festival/Simply Lift')

    @task
    def purchasePlaces(self):
        response = self.client.post('/purchasePlaces', {'competition':'Spring Festival', 'club':'Simply Lift', 'places':"1"})