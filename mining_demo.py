#!/usr/bin/env python3
"""
Bitcoin Mining — Live Demo
==========================

This script shows you EXACTLY what's happening when a miner mines.
No abstractions, no animations — it builds a real Bitcoin-style block
header, runs it through real SHA-256, and finds a real "block" at a
deliberately-easy difficulty so you can watch it happen in a few seconds.

What you're about to see:
  1. A "block header" — 80 bytes containing a few fields (timestamp,
     previous block's hash, etc.) plus a "nonce" — a 32-bit number we
     get to change.
  2. SHA-256 hashed twice. The output is a 256-bit number, shown in hex.
  3. We change the nonce, hash again, change, hash again. Billions of
     times if we have to. We're looking for a hash that starts with
     enough zeros.
  4. When we find one, we've "mined a block."

Why is this hard? SHA-256 is a one-way function. There's no shortcut
to find a nonce that produces a specific output — you have to guess
and check. That's why it's called Proof-of-Work: the only proof you
actually did the work is showing a valid hash. Can't fake it.

Run it:
    python3 mining_demo.py
    python3 mining_demo.py --zeros 7      # harder (takes longer)
    python3 mining_demo.py --zeros 5      # easier (almost instant)

The REAL Bitcoin network requires ~20 leading hex zeros right now.
That's ~16^20 = 10^24 hashes on average — which is why it needs the
entire global mining network to find one every 10 minutes.
"""

import argparse
import hashlib
import struct
import time


def double_sha256(data: bytes) -> bytes:
    """Bitcoin uses SHA-256 applied twice. That's it. That's the whole secret."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def build_header(version: int, prev_hash: bytes, merkle_root: bytes,
                 timestamp: int, bits: int, nonce: int) -> bytes:
    """Pack the 80-byte Bitcoin block header. Same format the real network uses."""
    return (
        struct.pack("<I", version)       # 4 bytes:  block version
        + prev_hash[::-1]                 # 32 bytes: previous block's hash (reversed)
        + merkle_root[::-1]               # 32 bytes: hash summarizing all transactions
        + struct.pack("<I", timestamp)    # 4 bytes:  unix timestamp
        + struct.pack("<I", bits)         # 4 bytes:  encoded difficulty target
        + struct.pack("<I", nonce)        # 4 bytes:  the number we keep guessing
    )


def hash_to_display(h: bytes) -> str:
    """Bitcoin displays hashes reversed (little-endian). We do the same."""
    return h[::-1].hex()


def main():
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=__doc__)
    p.add_argument("--zeros", type=int, default=6,
                   help="How many leading hex zeros the hash must have. "
                        "Each extra zero makes it ~16x harder. (default: 6)")
    p.add_argument("--quiet", action="store_true",
                   help="Skip the running-attempts printout.")
    args = p.parse_args()

    target_prefix = "0" * args.zeros

    # ---- Build a realistic-looking block header ----
    # These are made-up but match the actual format Bitcoin uses.
    version = 0x20000000
    prev_hash = bytes.fromhex(
        "00000000000000000002a23d6df20eccec7b21d22e1a9eca80a2e3d5e8ab8a91"
    )
    merkle_root = bytes.fromhex(
        "e02d847b67d63b1a5c97a4f2b2e0e9b8c5d4e3f2a1b9c8d7e6f5a4b3c2d1e0f9"
    )
    timestamp = int(time.time())
    bits = 0x1d00ffff  # legacy difficulty encoding (irrelevant to this demo)

    # ---- Show what we're working with ----
    print("=" * 64)
    print(" BITCOIN MINING — LIVE DEMO")
    print("=" * 64)
    print()
    print("Block header fields we're hashing:")
    print(f"  Version:        0x{version:08x}")
    print(f"  Previous hash:  {prev_hash.hex()[:32]}...")
    print(f"  Merkle root:    {merkle_root.hex()[:32]}...  (summary of all txs)")
    print(f"  Timestamp:      {timestamp}  (Unix time)")
    print(f"  Bits:           0x{bits:08x}  (encoded difficulty)")
    print(f"  Nonce:          ??? — this is what we're searching for")
    print()
    print(f"GOAL: find a nonce where double-SHA-256(header) starts with")
    print(f"      {args.zeros} hex zeros.")
    print()
    print(f"      Real Bitcoin currently requires ~20 leading zeros.")
    print(f"      Each extra zero is ~16x harder.")
    print(f"      You're playing on EASY MODE so you can watch.")
    print()
    print("Mining...")
    print()

    nonce = 0
    start = time.time()
    last_print = start
    sample_hash = ""

    while nonce < 2**32:
        header = build_header(version, prev_hash, merkle_root,
                              timestamp, bits, nonce)
        h = double_sha256(header)
        display = hash_to_display(h)

        if display.startswith(target_prefix):
            elapsed = time.time() - start
            rate = nonce / elapsed if elapsed > 0 else 0
            print()
            print("=" * 64)
            print(" *** BLOCK FOUND! ***")
            print("=" * 64)
            print(f"  Nonce:             {nonce:,}")
            print(f"  Hash:              {display}")
            print(f"  Hashes tried:      {nonce + 1:,}")
            print(f"  Time taken:        {elapsed:.2f} seconds")
            print(f"  Your hash rate:    {rate:,.0f} hashes/second")
            print()
            print("  What just happened:")
            print(f"    Your CPU just tried {nonce+1:,} different nonces. For")
            print(f"    each one, it built the 80-byte block header, ran it")
            print(f"    through SHA-256 twice, and checked if the output")
            print(f"    started with {args.zeros} zeros. The very last one did.")
            print()
            print(f"    A modern Bitcoin ASIC (Antminer S21) does about")
            print(f"    200,000,000,000,000 (200 trillion) hashes per second.")
            print(f"    That's {200_000_000_000_000 / max(rate,1):,.0f}x faster than your CPU.")
            print()
            print(f"    The whole Bitcoin network combined does about")
            print(f"    750,000,000,000,000,000,000 hashes per second.")
            print(f"    And it still takes 10 minutes to find one block.")
            print(f"    That tells you how hard the REAL target is.")
            return

        if not args.quiet and time.time() - last_print >= 0.5:
            elapsed = time.time() - start
            rate = nonce / elapsed if elapsed > 0 else 0
            # show a sample of what attempts look like
            print(f"  nonce={nonce:>10,}  hash={display[:24]}...  "
                  f"rate={rate:>10,.0f} H/s")
            last_print = time.time()

        nonce += 1

    print("Ran out of nonces without finding a block. Try lower --zeros.")


if __name__ == "__main__":
    main()
