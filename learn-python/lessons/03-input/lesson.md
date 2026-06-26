# Lesson 03 — Strings & Input

Goal: make your program *talk back* — ask a question, capture the answer, respond. This is the skeleton of every chatbot.

---

## 1. `print()` is a function — call it with `()`

```python
print("What is your name?")
```

Not `print = ...`. You *call* it by putting the value inside parentheses.

The `f` only goes on the quotes when you're inserting a variable: `f"Hi {name}"`. A plain message doesn't need it.

---

## 2. `input()` — the new superpower

`input()` shows a prompt, waits for the person to type, and hands back the text. Store it in a variable:

```python
name = input("What is your name? ")
```

Read it right-to-left: `input(...)` collects the typed text, then `=` drops it into `name`.

---

## 3. Use it with an f-string

```python
print(f"Well hello there {name}!")
```

`{name}` is Python's "insert a variable here." (Other languages use `$` — Python uses `{ }`.)

---

## Full program

```python
name = input("What is your name? ")
print(f"Well hello there {name}!")
```

See `greet.py`. (Because it needs typed input, run it and type when prompted —
or feed it input: `echo "Zach" | python3 lessons/03-input/greet.py`)

---

## ⚠️ One gotcha: input is always TEXT

Whatever `input()` returns is a **string**, even if the person types a number.
To do math on it, convert with `int()`:

```python
age = input("Your age? ")     # "30" as text
age = int(age)                # 30 as a real number
print(f"Next year you'll be {age + 1}")
```

---

## 🤖 AI tie-in

`ask a question -> capture the text -> respond` is the exact loop a chatbot uses.
Swap the greeting for "send the text to an AI model and print its reply" and you've
built a ChatGPT-style app.

## ✅ What you learned

- `print()` is a function you call with `()`
- `input("...")` asks and returns what the user types
- `{var}` inserts variables in f-strings
- `input()` returns text — use `int()` to turn it into a number

Next: **Lesson 04 — If / Else** (making decisions).
