from cs50 import SQL

db = SQL("sqlite:///database.db")

slots = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']

for i in range(len(slots)):
    db.execute("INSERT INTO times (time) VALUES (:time)", time = 'sun ' + slots[i])
    
SELECT * FROM user_info
JOIN courses ON user_info.id = courses.id
JOIN availability on availability.id = user_info.id
JOIN times ON times.slot_id = availability.slot_id
WHERE courses.dept = "phys" AND courses.number = 16 AND courses.id != 2
AND time IN(SELECT time FROM times JOIN availability
ON times.slot_id = availability.slot_id WHERE id = 2)