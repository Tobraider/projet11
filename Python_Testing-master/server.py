import json
from flask import Flask,render_template,request,redirect,flash,url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

jsonClub = 'clubs.json'
jsonCompetition = 'competitions.json'

def loadClubs():
    with open(jsonClub) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open(jsonCompetition) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def saveClubs(clubs):
    with open(jsonClub, 'w') as c:
        data = {"clubs":clubs}
        c.write(json.dumps(data, indent=4))


def saveCompetitions(competitions):
    with open(jsonCompetition, 'w') as c:
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
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))

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
        return redirect(url_for('home'))
    else:
        flash("Can't find a club with this email")
        return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template('welcome.html',club=current_user,competitions=competitions)

@app.route('/book/<competition>/<club>')
@login_required
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club]
    if foundClub:
        foundClub = foundClub[0]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundCompetition:
        foundCompetition = foundCompetition[0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('home'))


@app.route('/purchasePlaces',methods=['POST'])
@login_required
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    if competition:
        competition = competition[0]
    club = [c for c in clubs if c['name'] == request.form['club']]
    if club:
        club = club[0]
    if competition and club:
        placesRequired = int(request.form['places'])
        if placesRequired > 0:
            if int(club['points']) - placesRequired >= 0:
                if int(competition['numberOfPlaces']) - placesRequired >= 0:
                    if club['name'] in competition['placesBooked']:
                        if int(competition['placesBooked'][club['name']]) + placesRequired <= 12:
                            competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
                            competition['placesBooked'][club['name']] = str(int(competition['placesBooked'][club['name']]) + placesRequired)
                            club['points'] = str(int(club['points']) - placesRequired)
                            saveClubs(clubs)
                            saveCompetitions(competitions)
                            flash('Great-booking complete!')
                        else:
                            flash(f"You can book only {12 - int(competition['placesBooked'][club['name']])} more places (limit 12)")
                    elif placesRequired <= 12:
                        competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
                        competition['placesBooked'][club['name']] = str(placesRequired)
                        club['points'] = str(int(club['points']) - placesRequired)
                        saveClubs(clubs)
                        saveCompetitions(competitions)
                        flash('Great-booking complete!')
                    else:
                        flash("You can't buy more than 12 places")
                else:
                    flash('There is no more places')
            else:
                flash("You don't have enough points")
        else:
            flash("You can't buy a negative number or zero places")
    return redirect(url_for('home'))


@app.route('/tablePoints')
def tablePoints():
    return render_template('table.html', clubs=clubs)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))