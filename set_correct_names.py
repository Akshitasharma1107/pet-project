import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'pet_adoption.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

correct_names = {
    1: "Buster",
    2: "Charlie",
    3: "Whiskers",
    4: "Thumper",
    5: "Max",
    6: "Oreo",
    7: "Bandit",
    8: "Luna",
    9: "Garfield",
    10: "Simba",
    11: "Bella",
    12: "Snowball",
    13: "Buddy & Chloe",
    14: "Peanut & Butter",
    15: "Shadow"
}

for i in range(1, 16):
    name = correct_names[i]
    image_url = f"images/image{i}.jpg"
    c.execute("UPDATE pet SET name=? WHERE image_url=?", (name, image_url))

conn.commit()
conn.close()
print("Updated database with REAL names!")
