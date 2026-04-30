import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'pet_adoption.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("UPDATE pet SET breed='Mixed / Unknown', age='Unknown'")
conn.commit()
conn.close()
print("Reverted breeds to Generic successfully!")
