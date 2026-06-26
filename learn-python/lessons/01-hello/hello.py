# Lesson 01 — worked example
# Run me with:  python3 lessons/01-hello/hello.py

# 1. The classic first program
print("Hello, world!")

# 2. Variables: labeled boxes that hold values
player_name = "Zach"   # a string (text) — note the quotes
score = 0              # a number — no quotes

print(player_name)
print(score)

# 3. Variables can change
score = 100
print(score)

# 4. f-strings: drop variables into a sentence
print(f"{player_name} scored {score} points!")

# 5. A tiny taste of why this matters for AI:
#    these are just variables controlling an imaginary AI model
ai_temperature = 0.7   # how "creative" the AI is
ai_model = "claude"
print(f"Running model '{ai_model}' with creativity {ai_temperature}")
