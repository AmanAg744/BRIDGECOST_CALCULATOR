import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_database()
        
    def initialize_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_data (
                Material TEXT,
                BaseRate REAL,
                MaintenanceRate REAL,
                RepairRate REAL,
                DemolitionRate REAL,
                EnvironmentalFactor REAL,
                SocialFactor REAL,
                DelayFactor REAL
            )
        """)
        
        # Check if data exists
        self.cursor.execute("SELECT COUNT(*) FROM cost_data")
        if self.cursor.fetchone()[0] == 0:
            # Prepopulate with initial data
            initial_data = [
                ("Steel", 3000, 50, 200, 100, 10, 0.5, 0.3),
                ("Concrete", 2500, 75, 150, 80, 8, 0.6, 0.2)
            ]
            self.cursor.executemany("""
                INSERT INTO cost_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, initial_data)
            self.conn.commit()
    # def fetch_material_data(self, material):
    #     self.cursor.execute("SELECT * FROM cost_data WHERE Material = ?", (material,))
    #     return self.cursor.fetchone()

    def fetch_all_cost_data(self):
        self.cursor.execute("SELECT * FROM cost_data")
        return self.cursor.fetchall()

    def update_cost_data(self, material, **kwargs):
        update_fields = []
        values = []
        for field, value in kwargs.items():
            update_fields.append(f"{field} = ?")
            values.append(value)
        values.append(material)
        
        query = f"UPDATE cost_data SET {', '.join(update_fields)} WHERE Material = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    
    def fetch_material_data(self, material):
        self.cursor.execute("SELECT * FROM cost_data WHERE Material = ?", (material,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()