import json
from flask import Flask,render_template,request,redirect,flash,url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def saveClubs(clubs):
    with open('clubs.json', 'w') as c:
        data = {"clubs":clubs}
        c.write(json.dumps(data, indent=4))


def saveCompetitions(competitions):
    with open('competitions.json', 'w') as c:
        data = {"competitions":competitions}
        c.write(json.dumps(data, indent=4))



app = Flask(__name__)
app.secret_key = 'something_special'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id, name_club, point_club):
        self.id = user_id
        self.name = name_club
        self.points = point_club

@login_manager.user_loader
def load_user(user_id):
    club = [club for club in clubs if club['email'] == user_id]
    if club:
        club = club[0]
        return User(user_id, club["name"], club["points"])
    else:
        raise ValueError("user_id isn't find in email club")

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        club = club[0]
        user = User(club["email"], club["name"], club["points"])
        login_user(user)
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        flash("Can't find a club with this email")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
@login_required
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
@login_required
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))