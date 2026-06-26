# Lesson 02 — Numbers & Math

Goal: make Python *calculate*. This powers game stats (health, score) and is the literal foundation of AI.

---

## The operators

| You type | Means | Example | Result |
|---|---|---|---|
| `+` | add | `10 + 5` | `15` |
| `-` | subtract | `10 - 5` | `5` |
| `*` | multiply | `10 * 5` | `50` |
| `/` | divide | `10 / 4` | `2.5` |
| `**` | power | `2 ** 3` | `8` |
| `%` | remainder (modulo) | `10 % 3` | `1` |

- `**` = "to the power of": `2 ** 3` is 2×2×2 = 8.
- `%` = the leftover after dividing: `10 % 3` = 1. Used for "every Nth time" logic in games.

---

## Math with variables

You usually do math on variables, not raw numbers:

```python
health = 100
damage = 30
health = health - damage   # right side runs first (100-30), then stored back
print(f"Health is now {health}")   # Health is now 70
```

Read `health = health - damage` **right-to-left**: compute `health - damage` first, then put the result back in the `health` box.

> 🎮 This is exactly how a game removes health on a hit — same idea in GDScript.
> 🤖 Neural networks are millions of `*` and `+` operations. This is the atom of AI.

---

## Shortcut: `+=` and friends

`health = health - damage` is so common Python gives a shortcut:

```python
health -= damage   # same as health = health - damage
score  += 10       # add 10 to score
gold   *= 2        # double the gold
```

---

## ▶️ Worked example

See `battle.py` — a tiny Resident Evil style fight using only math.

```bash
python3 lessons/02-numbers/battle.py
```

---

## ✅ What you learned

- The 6 math operators (`+ - * / ** %`)
- Doing math on variables, and the right-to-left rule
- The `+= -= *=` shortcuts

Next: **Lesson 03 — Strings & Input** (making your program *talk back*).
