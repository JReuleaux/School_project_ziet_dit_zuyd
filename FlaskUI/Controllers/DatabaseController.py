import sqlite3

class DatabaseController:
    def __init__(self, db_name="Zie_Dit_Zuyd.db3"):
        self.db_name = db_name  

    def get_connection(self):
        """Maakt en retourneert een nieuwe databaseverbinding voor elke request."""
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def insert(self, table_name, data):
        """Voegt een nieuw record in de opgegeven tabel in."""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            values = tuple(data.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            connection.commit()

            print("Record succesvol opgeslagen")
            return cursor.lastrowid
        except Exception as e:
            return f"Toevoegen van record is mislukt: {e}"
        finally:
            connection.close()  

    def fetch_all(self, table_name):
        """Haalt alle records op uit de opgegeven tabel."""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()

            return result
        except Exception as e:
            return f"Halen van records is mislukt: {e}"
        finally:
            connection.close()

    def fetch_by_condition(self, table_name, conditions):
        """Haalt records op op basis van de opgegeven voorwaarden."""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            where_clause = " AND ".join([f"{col} = ?" for col in conditions])
            values = tuple(conditions.values())

            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            cursor.execute(query, values)
            result = cursor.fetchall()

            print("Get van record is succesvol")
            return result
        except Exception as e:
            return f"Halen van een specifieke record is mislukt: {e}"
        finally:
            connection.close()



    def update(self, table_name, data, conditions):
        """Wijzigt een record in de opgegeven tabel op basis van de voorwaarden."""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            set_clause = ", ".join([f"{col} = ?" for col in data])
            where_clause = " AND ".join([f"{col} = ?" for col in conditions])

            values = tuple(data.values()) + tuple(conditions.values())

            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            cursor.execute(query, values)
            connection.commit()

            print("Update is succesvol")
        except Exception as e:
            return f"Update van de record is mislukt: {e}"
        finally:
            connection.close()

    def delete(self, table_name, conditions):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            where_clause = " AND ".join([f"{col} = ?" for col in conditions])
            values = tuple(conditions.values())

            query = f"DELETE FROM {table_name} WHERE {where_clause}"
            cursor.execute(query, values)
            connection.commit()

            print("Delete van record is succesvol")
        except Exception as e:
            return f"Delete van record is mislukt: {e}"
        finally:
            connection.close()
