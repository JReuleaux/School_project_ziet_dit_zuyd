from flask import Flask, render_template, request, redirect, session
from Controllers.DatabaseController import DatabaseController
from Controllers.PlanningController import PlanningController
from auth import login_required

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Nodig voor sessiebeheer

db = DatabaseController()


def get_user_by_email(email):
    db = DatabaseController()  # Open een nieuwe databaseverbinding
    users = db.fetch_by_condition("Gebruiker", {"Email": email})
    return users[0] if users else None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)

        if user and user[5] == password:  # user[5] is het wachtwoord
            session['user_id'] = user[0]  # user[0] is de ID
            session['role'] = user[4]  # user[4] is de rol_id
            return redirect('/dashboard')

        return "Ongeldige login!", 403

    return render_template('login.html')


@app.route('/dashboard')
@login_required()
def dashboard():
    rol = session['role']
    user_id = session.get('user_id')
    gebruiker = get_user_by_id(user_id)

    # Haal alle gebruikers en reserveringen op
    alle_gebruikers = get_all_users()
    alle_reserveringen = planning_controller.get_all_reservations()

    if rol == 3:  # Beheerder
        total_users = len(alle_gebruikers)
        total_admins = len([user for user in alle_gebruikers if user[4] == 2])
        total_blocked = len([user for user in alle_gebruikers if user[4] == -1])

        return render_template('dashboard_beheerder.html',
                               total_users=total_users,
                               total_admins=total_admins,
                               total_blocked=total_blocked,
                               gebruikers=alle_gebruikers,  # Overzicht gebruikers
                               reservaties=alle_reserveringen,  # Overzicht planning
                               user_voornaam=gebruiker[1],
                               user_achternaam=gebruiker[2])

    elif rol == 2:  # Administrator
        total_users = len(alle_gebruikers)
        total_admins = len([user for user in alle_gebruikers if user[4] == 2])
        total_blocked = len([user for user in alle_gebruikers if user[4] == -1])

        return render_template('dashboard_admin.html',
                               total_users=total_users,
                               total_admins=total_admins,
                               total_blocked=total_blocked,
                               gebruikers=alle_gebruikers,  # Overzicht gebruikers
                               reservaties=alle_reserveringen,  # Overzicht planning
                               user_voornaam=gebruiker[1],
                               user_achternaam=gebruiker[2])

    elif rol == 1:  # Docent
        total_students = len([user for user in alle_gebruikers if user[4] == 0])
        total_plans = len(alle_reserveringen)

        return render_template('dashboard_docent.html',
                               total_students=total_students,
                               total_plans=total_plans,
                               reservaties=alle_reserveringen,  # Alleen reserveringen
                               user_voornaam=gebruiker[1],
                               user_achternaam=gebruiker[2])

    elif rol == 0:  # Gebruiker
        total_students = len([user for user in alle_gebruikers if user[4] == 0])

        return render_template('dashboard_gebruiker.html',
                               total_students=total_students,
                               user_voornaam=gebruiker[1],
                               user_achternaam=gebruiker[2],
                               reservaties=alle_reserveringen)  # Voeg reserveringen toe voor de gebruiker

    else:
        return redirect('/')


@app.route('/beheerder')
@login_required(role=3)  # Alleen beheerder mag dit zien
def beheerder_panel():
    return render_template('beheerder_panel.html')


@app.route('/admin')
@login_required(role=2)  # Alleen admin mag dit zien
def admin_panel():
    return render_template('admin_panel.html')


@app.route('/docent')
@login_required(role=1)  # Alleen docent en hoger mogen dit zien
def docent_panel():
    return render_template('docent_panel.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def get_all_users():
    return db.fetch_all("Gebruiker")


def get_user_by_id(user_id):
    users = db.fetch_by_condition("Gebruiker", {"Gebruiker_id": user_id})
    return users[0] if users else None


@app.route('/gebruikers')
@login_required(role=2)  # Alleen admin en beheerder mogen dit zien
def gebruikers_overzicht():
    gebruikers = get_all_users()  # Dit haalt alle gebruikers op uit de database
    return render_template('gebruikers.html', gebruikers=gebruikers)


@app.route('/gebruikers/toevoegen', methods=['GET', 'POST'])
@login_required(role=2)
def gebruikers_toevoegen():
    if request.method == 'POST':
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        email = request.form['email']
        rol = int(request.form['rol'])

        # Controleer of de beheerder geen hogere rol kan aanmaken dan hijzelf
        if session['role'] == 2 and rol >= 2:
            return "Geen toestemming om deze rol aan te maken!", 403

        # Standaard wachtwoord instellen, kan verder worden aangepast
        wachtwoord = request.form['wachtwoord'] if 'wachtwoord' in request.form else 'default'

        # Voeg gebruiker toe via databasecontroller
        db.insert("Gebruiker", {
            "Voornaam": voornaam,
            "Achternaam": achternaam,
            "Email": email,
            "Rol_id": rol,
            "Wachtwoord": wachtwoord
        })

        # Redirect naar gebruikersoverzicht
        return redirect('/gebruikers')

    return render_template('gebruiker_toevoegen.html')


@app.route('/gebruikers/verwijderen/<int:id>', methods=['POST'])
@login_required(role=2)  # Alleen admin en beheerder mogen dit doen
def gebruikers_verwijderen(id):
    gebruiker = get_user_by_id(id)
    if not gebruiker:
        return "Gebruiker niet gevonden", 404

    if session['role'] == 2 and gebruiker[4] >= 2:
        return "Geen toestemming om deze gebruiker te verwijderen!", 403

    db.delete("Gebruiker", {"gebruiker_id": id})
    return redirect('/gebruikers')


@app.route('/gebruikers/blokkeren/<int:id>', methods=['POST'])  # Voeg methods=['POST'] toe
@login_required(role=2)  # Alleen admin en beheerder mogen dit doen
def gebruikers_blokkeren(id):
    gebruiker = get_user_by_id(id)
    if not gebruiker:
        return "Gebruiker niet gevonden", 404

    if session['role'] == 2 and gebruiker[4] >= 2:
        return "Geen toestemming om deze gebruiker te blokkeren!", 403

    db.update("Gebruiker", {"Rol_id": -1}, {"Gebruiker_id": id})
    return redirect('/gebruikers')


@app.route('/gebruikers/onblokkeren/<int:id>', methods=['POST'])
@login_required(role=2)  # Alleen admin en beheerder mogen dit doen
def gebruikers_onblokkeren(id):
    gebruiker = get_user_by_id(id)
    if not gebruiker:
        return "Gebruiker niet gevonden", 404

    if session['role'] == 2 and gebruiker[4] >= 2:
        return "Geen toestemming om deze gebruiker te onblokkeren!", 403

    # Zet de rol van de gebruiker terug naar een normale rol (bijv. 1 voor gebruiker)
    db.update("Gebruiker", {"Rol_id": 0}, {"Gebruiker_id": id})  # Pas de rol aan naar de standaardwaarde
    return redirect('/gebruikers')



planning_controller = PlanningController()


@app.route('/planning')
@login_required(role=0)  # Minimaal rol 0 (gebruiker) vereist
def planning():
    reservaties = planning_controller.get_all_reservations()
    rollen = session.get('role')  # Haal de rol uit de sessie
    lokalen = planning_controller.get_lokaal_id()  # Haal de lokalen op
    return render_template('planning.html', reservaties=reservaties, rollen=rollen, lokalen=lokalen)


@app.route('/planning/toevoegen', methods=['POST'])
@login_required(role=1)
def planning_toevoegen():
    gebruiker_id = session.get('user_id')
    datum = request.form['datum']
    tijd = request.form['tijd']
    locatie_id = request.form['locatie_id']
    beschrijving = request.form['beschrijving']  # Haal beschrijving op
    lokaal_id = request.form['lokaal_id']

    # Haal de gebruiker op om naam toe te voegen
    gebruiker = get_user_by_id(gebruiker_id)
    voornaam = gebruiker[1]
    achternaam = gebruiker[2]

    # Voeg de reservering toe via de PlanningController
    planning_controller.create_reservation(gebruiker_id, datum, tijd, locatie_id, voornaam, achternaam, beschrijving, lokaal_id)

    return redirect('/planning')


@app.route('/planning/wijzigen/<int:id>', methods=['GET', 'POST'])
@login_required(role=2)  # Alleen admins en beheerders mogen reserveringen wijzigen
def planning_wijzigen(id):
    reservering = planning_controller.get_reservation_by_id(id)
    if not reservering:
        return "Reservering niet gevonden", 404

    # Haal alle beschikbare lokalen op
    lokalen = planning_controller.get_lokaal_id()

    if request.method == 'POST':
        datum = request.form['datum']
        tijd = request.form['tijd']
        beschrijving = request.form['beschrijving']
        lokaal_id = request.form['lokaal_id']  # Haal het lokaal_id op uit het formulier

        # Update de reservering, inclusief het lokaal_id
        planning_controller.update_reservation(id, datum, tijd, beschrijving, lokaal_id)
        return redirect('/planning')

    return render_template('planning_wijzigen.html', reservering=reservering[0], lokalen=lokalen)




@app.route('/planning/verwijderen', methods=['POST'])
@login_required(2)  # Minimaal administrator nodig
def planning_verwijderen():
    reservering_id = request.form['reservering_id']
    planning_controller.delete_reservation(reservering_id)
    return redirect('/planning')  # Redirect naar planning-overzicht

