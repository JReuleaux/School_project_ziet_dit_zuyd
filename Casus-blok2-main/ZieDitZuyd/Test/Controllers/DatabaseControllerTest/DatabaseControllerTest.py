import unittest


from DatabaseController import DatabaseController

  

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseController(":memory:")  # Use an in-memory database

    def test_insert_and_fetch(self):
        self.db.insert("users", {"name": "Alice", "age": 25})
        users = self.db.fetch_all("users")
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "Alice")

    def test_fetch_by_condition(self):
        self.db.insert("users", {"name": "Bob", "age": 30})
        result = self.db.fetch_by_condition("users", {"name": "Bob"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Bob")

    def test_update(self):
        self.db.insert("users", {"name": "Charlie", "age": 40})
        self.db.update("users", {"age": 45}, {"name": "Charlie"})
        result = self.db.fetch_by_condition("users", {"name": "Charlie"})
        self.assertEqual(result[0][2], 45)

    def test_delete(self):

        self.db.insert("users", {"name": "David", "age": 35})
        self.db.delete("users", {"name": "David"})
        result = self.db.fetch_all("users")
        self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()