import sqlite3
import random
import os

db_path = os.path.join(os.path.dirname(__file__), 'pet_adoption.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
breeds = ["Golden Retriever", "Labrador", "Persian Cat", "Beagle", "Poodle", "Siamese Cat", "Bulldog", "Maine Coon"]
ages = ["2 Months", "1 Year", "3 Years", "5 Months", "2 Years", "4 Years"]

c.execute("SELECT id FROM pet")
pet_ids = [row[0] for row in c.fetchall()]

for pet_id in pet_ids:
    breed = random.choice(breeds)
    age = random.choice(ages)
    c.execute("UPDATE pet SET breed=?, age=? WHERE id=?", (breed, age, pet_id))

conn.commit()
conn.close()
print("Updated breeds and ages successfully!")
