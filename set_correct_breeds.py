import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'pet_adoption.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

correct_data = {
    1: ("Brown Pitbull Mix", "2 Years"),
    2: ("Shih Tzu Mix", "4 Years"),
    3: ("Graphic Art Cat", "Unknown"),
    4: ("Brown & White Rabbit", "1 Year"),
    5: ("Tan Terrier Mix", "3 Years"),
    6: ("Black & White Rabbit", "6 Months"),
    7: ("Cattle Dog Mix", "1.5 Years"),
    8: ("Grey & White Cat", "2 Years"),
    9: ("Orange Fluffy Cat", "3 Years"),
    10: ("Tabby Kitten", "3 Months"),
    11: ("White & Brown Cat", "4 Years"),
    12: ("Cream Kitten", "2 Months"),
    13: ("Dog & Cat Bonded Pair", "2 Years"),
    14: ("Guinea Pigs", "1 Year"),
    15: ("Black Lab Mix Puppy", "4 Months")
}

for i in range(1, 16):
    image_url = f"images/image{i}.jpg"
    breed, age = correct_data[i]
    c.execute("UPDATE pet SET breed=?, age=? WHERE image_url=?", (breed, age, image_url))

conn.commit()
conn.close()
print("Updated database with CORRECT matching breeds and ages!")
