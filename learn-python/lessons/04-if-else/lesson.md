# Lesson 04 — If / Else (Decisions)

Goal: make your program *choose* what to do. This is where code gets a brain — game logic, rules, and AI choices all start here.

---

## The shape

```python
password = input("Enter the password: ")

if password == "1234":
    print("The door creaks open...")
else:
    print("Wrong password. It stays locked.")
```

Four things to learn:

### 1. `==` vs `=`  (the #1 beginner trap)

- `=`  means **"put this value in the box"** (setting):  `password = "1234"`
- `==` means **"are these two equal?"** (asking):       `if password == "1234"`

One equals = setting. Two equals = asking.

### 2. The colon `:`

The `if` line ends with `:` — "here comes the block to run."

### 3. Indentation = belonging

The indented lines run *only when the condition is true*. Python uses indentation
instead of words like "then"/"end".

> 🎮 GDScript uses this exact same indentation style.

### 4. `else:` = "if not"

Runs when the `if` condition was false.

---

## More comparisons

| Operator | Means |
|---|---|
| `==` | equal to |
| `!=` | NOT equal to |
| `>`  | greater than |
| `<`  | less than |
| `>=` | greater than or equal |
| `<=` | less than or equal |

Example — a health warning:

```python
health = 15
if health <= 20:
    print("WARNING: health critical!")
```

---

## `elif` — more than two paths

```python
score = 75
if score >= 90:
    print("Grade: A")
elif score >= 70:
    print("Grade: B")
else:
    print("Keep practicing!")
```

`elif` = "else, if..." — check another condition only if the ones above failed.

---

## ▶️ Worked example

`door.py` — a password door. Run it and type a password (try 1234, then anything else).

---

## ✅ What you learned

- `if condition:` then an indented block
- `==` asks; `=` sets
- `else:` for the "otherwise" path, `elif` for extra paths
- Comparison operators: `== != > < >= <=`

Next: **Lesson 05 — Loops** (doing things over and over without copy-paste).
