# Lesson 02 — worked example: a tiny battle using only math
# Run me:  python3 lessons/02-numbers/battle.py

health = 100
print(f"Starting health: {health}")

zombie_bite = 35
health -= zombie_bite                      # shortcut for health = health - zombie_bite
print(f"Ouch! A zombie bit you for {zombie_bite}. Health: {health}")

health -= zombie_bite
print(f"Bitten again! Health: {health}")

heal = 50
health += heal                             # used a herb
print(f"You used a herb (+{heal}). Health: {health}")

# Bonus: score with multiplication
zombies_killed = 7
points_each = 150
score = zombies_killed * points_each
print(f"You killed {zombies_killed} zombies for {score} points!")
