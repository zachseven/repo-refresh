# Lesson 01 — Hello World & Variables

Welcome to your first lesson! Goal: print things to the screen and store data in **variables**. This is the foundation of *everything* else.

---

## 1. Printing

`print()` shows text on the screen. It's the first tool you'll reach for constantly.

```python
print("Hello, world!")
```

> 🎮 **Godot/GDScript note:** This is *identical* in GDScript — `print("Hello, world!")`. You're already learning two languages at once.

---

## 2. Variables — storing data

A **variable** is a labeled box that holds a value. You make one with `name = value`.

```python
player_name = "Zach"
score = 0
print(player_name)
print(score)
```

- `player_name` holds text (called a **string** — always in quotes).
- `score` holds a number (no quotes).

Python figures out the type automatically. You can change a variable later:

```python
score = 100        # changed the box's contents
print(score)       # 100
```

> 🎮 **GDScript note:** GDScript does the same idea but you write `var score = 0`. The only difference is the word `var` in front. That's it.

> 🤖 **AI note:** In AI code, variables hold everything — model settings, data, predictions. `temperature = 0.7` controlling an AI's creativity is *literally* just a variable like the ones above.

---

## 3. Combining text and variables (f-strings)

To slot a variable into a sentence, put an `f` before the quotes and wrap the variable in `{ }`:

```python
player_name = "Zach"
score = 100
print(f"{player_name} scored {score} points!")
# Output: Zach scored 100 points!
```

This is one of the most useful tricks in Python. You'll use it daily.

---

## 4. Comments

Anything after `#` is a note for humans — Python ignores it.

```python
# This line is just a reminder, it does nothing
print("But this runs")  # comments can go at the end of a line too
```

---

## ▶️ Run the example

From the `learn-python/` folder:

```bash
python3 lessons/01-hello/hello.py
```

You should see several lines of output. Read `hello.py` alongside this lesson.

---

## ✏️ Your exercise

Open `exercise.py`. It has `TODO` comments. Fill them in, then run it:

```bash
python3 lessons/01-hello/exercise.py
```

When you're done (or stuck!), tell me and I'll review your code and explain anything that's fuzzy.

---

## ✅ What you learned

- `print()` shows output
- Variables store data with `name = value`
- Strings use quotes; numbers don't
- f-strings (`f"{var}"`) put variables inside text
- `#` makes a comment

Next up: **Lesson 02 — Numbers & Math.** Say the word when you're ready.
