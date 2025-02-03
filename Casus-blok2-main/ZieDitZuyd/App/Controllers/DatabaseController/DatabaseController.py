import sqlite3

class  DatabaseController:
    def __init__(self, db_name="C:/Users/milan/OneDrive/Documenten/zuyd/casus2/Data Engineering/uitwerking database/databaseCasus2Invetarisatie.sqlite3"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()


    def insert(self, table_name, data):
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            values = tuple(data.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Record succesvol opgeslagen")
            return self.cursor.lastrowid
        except Exception as e:
            return(f"toevoegen van record is mislukt: {e}")
        finally:
            self.connection.close()

        

    def fetch_all(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            return(f"halen van record is mislukt: {e}")
        finally:
            self.connection.close()


    def fetch_by_condition(self, table_name, conditions):
        try:
            where_clause = " AND ".join([f"{col} = ?" for col in conditions])
            values = tuple(conditions.values())

            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            self.cursor.execute(query, values)
            print("get van record is succesvol")
            return self.cursor.fetchall()
        except Exception as e:
            return(f"halen van een specefieke record is mislukt: {e}")
        finally:
            self.connection.close()

    def update(self, table_name, data, conditions):
        try:
            set_clause = ", ".join([f"{col} = ?" for col in data])
            where_clause = " AND ".join([f"{col} = ?" for col in conditions])

            values = tuple(data.values()) + tuple(conditions.values())

            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("update is succesvol")
        except Exception as e:
            return(f"update van de record is mislukt: {e}")
        finally:
            self.connection.close()

    def delete(self, table_name, conditions):
        try:
            where_clause = " AND ".join([f"{col} = ?" for col in conditions])
            values = tuple(conditions.values())

            query = f"DELETE FROM {table_name} WHERE {where_clause}"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("delete van record is succesvol")
        except Exception as e:
            return(f"delete van record is mislukt: {e}")
        finally:
            self.connection.close()

