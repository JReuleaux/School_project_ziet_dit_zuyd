from Controllers.DatabaseController import DatabaseController

db = DatabaseController.DatabaseController()

gebruikers = db.fetch_all("Gebruiker")
print(gebruikers)

#db.insert("Gebruiker", {"Voornaam": "John", "Achternaam": "guetta","Email":"john.guetta@gmail.com","Rol_id":2,"Wachtwoord":"test"})

#db.update("Gebruiker", {"Rol_id": 1}, {"Voornaam": "John"})

#updated_employee = db.fetch_by_condition("Gebruiker", {"Voornaam": "John"})
#print("Updated Gebruiker:", updated_employee)

#db.delete("Gebruiker", {"Voornaam": "John"})


