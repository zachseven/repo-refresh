# Lesson 04 — worked example: a password door
# Run me:  python3 lessons/04-if-else/door.py   (then type a password)
# Or feed it:  echo "1234" | python3 lessons/04-if-else/door.py

password = input("Enter the password: ")

if password == "1234":
    print("The door creaks open...")
else:
    print("Wrong password. It stays locked.")

# Bonus: a health check using a comparison
health = 15
if health <= 20:
    print(f"WARNING: health is {health} - critical!")
