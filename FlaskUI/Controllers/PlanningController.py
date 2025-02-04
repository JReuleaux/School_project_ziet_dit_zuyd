from Controllers.DatabaseController import DatabaseController

class PlanningController:
    def __init__(self):
        self.db = DatabaseController()

    def get_all_reservations(self):
        return self.db.fetch_all("Reserveringen")

    def get_lokaal_id(self):
        lokalen = self.db.fetch_all("Lokalen")
        lokaal_ids = [lokaal[0] for lokaal in lokalen]  
        return lokaal_ids

    def get_reservation_by_id(self, reservation_id):
        return self.db.fetch_by_condition("Reserveringen", {"Reservering_id": reservation_id})

    def create_reservation(self, gebruiker_id, datum, tijd, locatie_id, voornaam, achternaam, beschrijving="", lokaal_id=""):
        self.db.insert("Reserveringen", {
            "Gebruiker_id": gebruiker_id,
            "Datum": datum,
            "Tijd": tijd,
            "Locatie_id": locatie_id,
            "Voornaam": voornaam,
            "Achternaam": achternaam,
            "Beschrijving": beschrijving,
            "Lokaal_id": lokaal_id
        })

        
        self.db.update("Beschikbaarheid", {"Beschikbaar": False}, {"Lokaal_id": lokaal_id, "Datum": datum, "Tijdvak": tijd})

    def update_reservation(self, reservation_id, datum, tijd, beschrijving, lokaal_id):
        return self.db.update("Reserveringen", {
            "Datum": datum,
            "Tijd": tijd,
            "Beschrijving": beschrijving,
            "Lokaal_id": lokaal_id  
        }, {"Reservering_id": reservation_id})

    def delete_reservation(self, reservation_id):
        reservering = self.get_reservation_by_id(reservation_id)[0]
        lokaal_id = reservering[8]  
        datum = reservering[1]  
        tijd = reservering[2]  

        
        self.db.delete("Reserveringen", {"Reservering_id": reservation_id})

       
        self.db.update("Beschikbaarheid", {"Beschikbaar": True}, {"Lokaal_id": lokaal_id, "Datum": datum, "Tijdvak": tijd})


    def get_plans_by_teacher(self, teacher_id):
        """Haalt het aantal lesplannen (reserveringen) op van een specifieke docent."""
        query = "SELECT COUNT(*) FROM Reserveringen WHERE Gebruiker_id = ?"
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (teacher_id,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0