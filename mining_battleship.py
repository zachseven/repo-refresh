#!/usr/bin/env python3
"""
Bitcoin Mining — Battleship Edition
===================================

You vs. the rest of the network. A "block" is hidden somewhere on the grid.
Each turn, you guess one cell. The network guesses several cells (you have
10% of the network's hashpower, so they guess 9 cells for every 1 of yours).
First to find the block wins the block reward.

This is what Bitcoin mining literally is:
  - The grid = the space of possible nonces (in reality 4 billion cells,
    not 100 — and only a handful are "hits")
  - Each guess = one SHA-256 hash attempt
  - The hidden block = a nonce that produces a valid low-enough hash
  - More hashpower = more guesses per turn = better odds of finding first
  - You CAN'T be smart about it. Every guess is independent. Best strategy
    is just guess more.

Play:
    python3 mining_battleship.py                   # one round, interactive
    python3 mining_battleship.py --rounds 10       # 10 rounds, see variance
    python3 mining_battleship.py --auto --rounds 100  # auto-play 100 rounds
    python3 mining_battleship.py --hashrate-share 0.25  # you have 25% of network
"""

import argparse
import random
import time

GRID_SIZE = 10  # 10x10 grid = 100 cells
COLS = "ABCDEFGHIJ"


def render_grid(player_guesses, network_guesses, block, reveal=False):
    """Pretty-print the grid. Player guesses = P, network = N, block = B if revealed."""
    lines = []
    lines.append("       " + " ".join(COLS))
    lines.append("     +" + "-" * (GRID_SIZE * 2 + 1))
    for r in range(GRID_SIZE):
        row_cells = []
        for c in range(GRID_SIZE):
            if reveal and (c, r) == block:
                row_cells.append("B")
            elif (c, r) in player_guesses:
                row_cells.append("P" if (c, r) != block else "*")
            elif (c, r) in network_guesses:
                row_cells.append("n" if (c, r) != block else "*")
            else:
                row_cells.append(".")
        lines.append(f"  {r+1:2} | " + " ".join(row_cells))
    lines.append("")
    lines.append("    P = your guess   n = network guess   . = unexplored")
    if reveal:
        lines.append("    B = block (was hidden)   * = block found!")
    return "\n".join(lines)


def parse_cell(s):
    """Parse 'C5' -> (2, 4). Returns None if invalid."""
    s = s.strip().upper()
    if len(s) < 2 or len(s) > 3:
        return None
    if s[0] not in COLS:
        return None
    try:
        row = int(s[1:]) - 1
    except ValueError:
        return None
    if not (0 <= row < GRID_SIZE):
        return None
    return (COLS.index(s[0]), row)


def cell_name(cell):
    return f"{COLS[cell[0]]}{cell[1]+1}"


def random_unused_cell(used):
    """Pick a random cell that hasn't been guessed yet."""
    while True:
        c = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if c not in used:
            return c


def play_round(network_per_turn, auto=False, round_num=1, total_rounds=1):
    """Play one round. Returns 'player' or 'network'."""
    block = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    player_guesses = set()
    network_guesses = set()
    turn = 0

    print()
    print("=" * 64)
    print(f" ROUND {round_num} of {total_rounds}")
    print(f" One block hidden somewhere in 100 cells. First to find wins.")
    print(f" You guess 1 cell per turn. Network guesses {network_per_turn}.")
    print("=" * 64)

    while True:
        turn += 1

        if not auto:
            print()
            print(render_grid(player_guesses, network_guesses, block, reveal=False))
            print()
            print(f"  Turn {turn}.  You've made {len(player_guesses)} guesses, "
                  f"network has made {len(network_guesses)}.")

        # --- player's guess ---
        if auto:
            cell = random_unused_cell(player_guesses | network_guesses)
        else:
            while True:
                raw = input("  Your guess (e.g. C5, or 'r' for random): ").strip()
                if raw.lower() in ("r", "random", ""):
                    cell = random_unused_cell(player_guesses | network_guesses)
                    print(f"  Picked randomly: {cell_name(cell)}")
                    break
                parsed = parse_cell(raw)
                if parsed is None:
                    print("  Bad format. Use letter+number like C5, or 'r' for random.")
                    continue
                if parsed in player_guesses or parsed in network_guesses:
                    print("  That cell was already guessed. Try another.")
                    continue
                cell = parsed
                break

        player_guesses.add(cell)

        if cell == block:
            if not auto:
                print()
                print(render_grid(player_guesses, network_guesses, block, reveal=True))
                print()
                print(f"  *** YOU FOUND THE BLOCK at {cell_name(cell)}! ***")
                print(f"  You hashed {len(player_guesses)} times. "
                      f"Network hashed {len(network_guesses)} times.")
                ratio = len(player_guesses) / (len(player_guesses) + len(network_guesses))
                print(f"  You did {ratio*100:.1f}% of the work and got 100% of the reward.")
                print(f"  That's variance in your favor!")
            return "player", len(player_guesses), len(network_guesses)

        if not auto:
            print(f"  Your guess {cell_name(cell)}: MISS")

        # --- network's guesses (made in parallel; they each get a chance) ---
        net_hits_this_turn = []
        for _ in range(network_per_turn):
            if len(player_guesses) + len(network_guesses) >= GRID_SIZE * GRID_SIZE:
                break
            nc = random_unused_cell(player_guesses | network_guesses)
            network_guesses.add(nc)
            if nc == block:
                net_hits_this_turn.append(nc)
                break  # network found it; stop guessing

        if net_hits_this_turn:
            hit = net_hits_this_turn[0]
            if not auto:
                print(f"  Network guessed {len(net_hits_this_turn)} cells this turn "
                      f"and FOUND the block at {cell_name(hit)}.")
                print()
                print(render_grid(player_guesses, network_guesses, block, reveal=True))
                print()
                print(f"  *** NETWORK FOUND THE BLOCK ***")
                print(f"  You hashed {len(player_guesses)} times. "
                      f"Network hashed {len(network_guesses)} times.")
                ratio = len(player_guesses) / (len(player_guesses) + len(network_guesses))
                print(f"  You did {ratio*100:.1f}% of the work. "
                      f"Network got the reward.")
            return "network", len(player_guesses), len(network_guesses)

        if not auto:
            print(f"  Network guessed {network_per_turn} cells: all MISS")


def main():
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=__doc__)
    p.add_argument("--rounds", type=int, default=1,
                   help="How many rounds to play (default: 1)")
    p.add_argument("--hashrate-share", type=float, default=0.10,
                   help="Your share of total network hashpower, 0-1 (default: 0.10)")
    p.add_argument("--auto", action="store_true",
                   help="Auto-play with random guesses (no prompts). "
                        "Useful with --rounds 100+ to see variance.")
    args = p.parse_args()

    if not (0 < args.hashrate_share < 1):
        print("--hashrate-share must be between 0 and 1 (exclusive)")
        return

    # If you have share s, then for every 1 guess you make, the rest of the
    # network makes (1-s)/s guesses. So network_per_turn = round((1-s)/s).
    network_per_turn = max(1, round((1 - args.hashrate_share) / args.hashrate_share))

    print()
    print(f"  Your hashrate share: {args.hashrate_share*100:.1f}% of the network")
    print(f"  Per turn: you guess 1 cell, network guesses {network_per_turn} cells")
    print(f"  Expected win rate over many rounds: ~{args.hashrate_share*100:.1f}%")

    player_wins = 0
    network_wins = 0
    player_hashes_total = 0
    network_hashes_total = 0
    start = time.time()

    for i in range(args.rounds):
        winner, ph, nh = play_round(network_per_turn, auto=args.auto,
                                    round_num=i + 1, total_rounds=args.rounds)
        if winner == "player":
            player_wins += 1
        else:
            network_wins += 1
        player_hashes_total += ph
        network_hashes_total += nh

    elapsed = time.time() - start

    print()
    print("=" * 64)
    print(" FINAL STATS")
    print("=" * 64)
    print(f"  Rounds played:        {args.rounds}")
    print(f"  Your wins:            {player_wins}  ({player_wins/args.rounds*100:.1f}%)")
    print(f"  Network wins:         {network_wins}  ({network_wins/args.rounds*100:.1f}%)")
    print(f"  Expected win rate:    {args.hashrate_share*100:.1f}%")
    print()
    print(f"  Total guesses you made:      {player_hashes_total:,}")
    print(f"  Total guesses network made:  {network_hashes_total:,}")
    actual_share = player_hashes_total / max(player_hashes_total + network_hashes_total, 1)
    print(f"  Your actual hash share:      {actual_share*100:.1f}%")
    print(f"  Time elapsed:                {elapsed:.1f}s")
    print()

    expected_wins = args.rounds * args.hashrate_share
    diff = player_wins - expected_wins
    if args.rounds >= 10:
        print(f"  You were expected to win ~{expected_wins:.1f} rounds.")
        print(f"  You actually won {player_wins}.")
        if diff > 0:
            print(f"  Variance was in YOUR favor by {diff:.1f} rounds.")
        elif diff < 0:
            print(f"  Variance was AGAINST you by {abs(diff):.1f} rounds.")
        else:
            print(f"  You hit expectation exactly. Very rare.")

    if args.rounds == 1:
        print()
        print("  Try --rounds 100 --auto to see how variance smooths out")
        print("  over many rounds. That's the law of large numbers in action.")


if __name__ == "__main__":
    main()
