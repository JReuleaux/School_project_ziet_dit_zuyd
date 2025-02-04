import unittest
from Controllers.DatabaseController import DatabaseController


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseController(":memory:")

    def test_insert_and_fetch_WhenNoTableExists(self):
        self.db.insert("gebruiker", {"Voornaam": "Alice", "Achternaam": "Jansen"})
        Gebruiker = self.db.fetch_all("gebruiker")
        self.assertEqual(Gebruiker, "Halen van records is mislukt: no such table: gebruiker")

    def test_fetch_by_condition_WhenNoTableExists(self):
        self.db.insert("gebruiker", {"name": "Bob", "Achternaam": "Jansen"})
        result = self.db.fetch_by_condition("gebruiker", {"name": "Bob", "Achternaam": "Jansen"})
        self.assertEqual(result, "Halen van een specifieke record is mislukt: no such table: gebruiker")

    def test_update_WhenNoTableExists(self):
        self.db.insert("gebruiker", {"name": "Charlie", "Achternaam": "Jansen"})
        result = self.db.fetch_by_condition("gebruiker", {"name": "Charlie"})
        self.assertEqual(result, "Halen van een specifieke record is mislukt: no such table: gebruiker")

    def test_delete_WhenNoTableExists(self):
        self.db.insert("gebruiker", {"name": "David", "Achternaam": "Jansen"})
        self.db.delete("gebruiker", {"name": "David"})
        result = self.db.fetch_all("gebruiker")
        self.assertEqual(result, "Halen van records is mislukt: no such table: gebruiker")



if __name__ == "__main__":
    unittest.main()
