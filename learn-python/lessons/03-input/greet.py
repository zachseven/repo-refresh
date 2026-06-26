# Lesson 03 — worked example: an interactive greeting
# Run me:  python3 lessons/03-input/greet.py   (then type your name)
# Or feed input: echo "Zach" | python3 lessons/03-input/greet.py

name = input("What is your name? ")
print(f"Well hello there {name}!")

# Bonus: input is always text, so convert with int() to do math
age = input("How old are you? ")
age = int(age)
print(f"Next year you will be {age + 1}.")
