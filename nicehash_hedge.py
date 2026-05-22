#!/usr/bin/env python3
"""
NiceHash Bitcoin Rental Hedge Calculator
========================================

You're about to rent some hashpower from NiceHash. This tells you, in plain
English, whether it's a smart move or a slot machine — and what your hedge
options look like.

Run it like:
    python3 nicehash_hedge.py
    python3 nicehash_hedge.py --hashrate 100 --hours 1
    python3 nicehash_hedge.py --hashrate 500 --hours 4 --btc-price 95000

All the "live" numbers (BTC price, NiceHash market price, network hashrate)
have defaults, but they change constantly — punch in current values for
real answers. Look them up at:
    BTC price:        coinbase.com / kraken.com
    Network hashrate: mempool.space (homepage, "Hashrate" card)
    NiceHash price:   nicehash.com/marketplace (SHA-256 "Standard" price)
"""

import argparse
import math


# --------- defaults you might want to override ---------
# These approximate the state of the world in mid-2026. They go stale fast.
DEFAULT_BTC_PRICE_USD = 100_000.0          # USD per BTC
DEFAULT_NETWORK_HASHRATE_EH = 750.0        # exahash/second across the whole network
DEFAULT_NICEHASH_BTC_PER_TH_PER_DAY = 0.00004   # what NiceHash charges, BTC/TH/day
DEFAULT_PPS_POOL_BTC_PER_TH_PER_DAY = 0.0000385 # what a PPS pool pays out, BTC/TH/day
DEFAULT_BLOCK_REWARD_BTC = 3.125           # post-2024 halving subsidy
DEFAULT_BLOCK_FEES_BTC = 0.10              # avg tx fees included in a block
DEFAULT_POOL_FEE_PCT = 2.0                 # what the pool keeps
# -------------------------------------------------------


def fmt_usd(x):
    if abs(x) >= 1000:
        return f"${x:,.0f}"
    if abs(x) >= 1:
        return f"${x:,.2f}"
    return f"${x:.4f}"


def fmt_pct_odds(p):
    """Render a probability as a '1 in N' string."""
    if p <= 0:
        return "essentially zero"
    n = 1.0 / p
    if n >= 1_000_000:
        return f"1 in {n/1_000_000:,.1f} million"
    if n >= 1_000:
        return f"1 in {n:,.0f}"
    return f"1 in {n:.1f}"


def section(title):
    print()
    print("=" * 62)
    print(f"  {title}")
    print("=" * 62)


def main():
    p = argparse.ArgumentParser(
        description="Plain-English NiceHash rental analyzer + hedge advisor.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--hashrate", type=float, default=100.0,
                   help="How much hashpower you're renting, in TH/s (default: 100)")
    p.add_argument("--hours", type=float, default=1.0,
                   help="How long you're renting it for, in hours (default: 1)")
    p.add_argument("--btc-price", type=float, default=DEFAULT_BTC_PRICE_USD,
                   help=f"Current BTC price in USD (default: {DEFAULT_BTC_PRICE_USD:,.0f})")
    p.add_argument("--nicehash-price", type=float, default=DEFAULT_NICEHASH_BTC_PER_TH_PER_DAY,
                   help=f"NiceHash SHA-256 price, BTC per TH per day (default: {DEFAULT_NICEHASH_BTC_PER_TH_PER_DAY})")
    p.add_argument("--pps-price", type=float, default=DEFAULT_PPS_POOL_BTC_PER_TH_PER_DAY,
                   help=f"PPS pool payout, BTC per TH per day (default: {DEFAULT_PPS_POOL_BTC_PER_TH_PER_DAY})")
    p.add_argument("--network-hashrate", type=float, default=DEFAULT_NETWORK_HASHRATE_EH,
                   help=f"Total Bitcoin network hashrate in EH/s (default: {DEFAULT_NETWORK_HASHRATE_EH})")
    p.add_argument("--block-reward", type=float, default=DEFAULT_BLOCK_REWARD_BTC,
                   help=f"Block subsidy in BTC (default: {DEFAULT_BLOCK_REWARD_BTC})")
    p.add_argument("--block-fees", type=float, default=DEFAULT_BLOCK_FEES_BTC,
                   help=f"Average tx fees per block in BTC (default: {DEFAULT_BLOCK_FEES_BTC})")
    p.add_argument("--pool-fee-pct", type=float, default=DEFAULT_POOL_FEE_PCT,
                   help=f"Pool fee percentage (default: {DEFAULT_POOL_FEE_PCT}%%)")
    p.add_argument("--bankroll", type=float, default=None,
                   help="Your total BTC bankroll in USD (used for Kelly sizing; optional)")
    args = p.parse_args()

    # ---- core numbers ----
    hours = args.hours
    days = hours / 24.0
    th = args.hashrate

    # what you pay
    rental_btc = th * args.nicehash_price * days
    rental_usd = rental_btc * args.btc_price

    # what a PPS pool would pay you (steady, predictable, after pool fee)
    pps_btc = th * args.pps_price * days * (1 - args.pool_fee_pct / 100)
    pps_usd = pps_btc * args.btc_price
    pps_net_usd = pps_usd - rental_usd

    # solo-mining lottery math
    # network is in EH/s = 1,000,000 TH/s. So your share is th / (network_eh * 1e6).
    network_th = args.network_hashrate * 1_000_000
    share = th / network_th
    blocks_per_hour = 6.0  # bitcoin targets 10 min/block
    expected_blocks = share * blocks_per_hour * hours
    # Poisson: probability of hitting at least one block
    p_at_least_one = 1.0 - math.exp(-expected_blocks)

    block_payout_btc = (args.block_reward + args.block_fees) * (1 - args.pool_fee_pct / 100)
    block_payout_usd = block_payout_btc * args.btc_price

    solo_ev_btc = expected_blocks * block_payout_btc
    solo_ev_usd = solo_ev_btc * args.btc_price
    solo_net_ev_usd = solo_ev_usd - rental_usd

    # ---- header ----
    section("YOUR RENTAL")
    print(f"  You're renting:  {th:,.0f} TH/s for {hours:g} hour(s)")
    print(f"  This costs:      {rental_btc:.8f} BTC  ({fmt_usd(rental_usd)})")
    print(f"  At BTC price:    {fmt_usd(args.btc_price)}")
    print()
    print(f"  (For scale: a single new Antminer S21 does ~200 TH/s. Bitcoin's")
    print(f"   entire network is doing {args.network_hashrate:,.0f} EH/s right now, which is")
    print(f"   {network_th/th:,.0f}x more than what you're renting.)")

    # ---- scenario A: steady pool ----
    section("OPTION A: Point it at a STEADY pool (PPS)")
    print(f"  You'd earn about: {fmt_usd(pps_usd)}")
    print(f"  You paid:         {fmt_usd(rental_usd)}")
    verdict = "PROFIT" if pps_net_usd > 0 else "LOSS"
    print(f"  Net:              {fmt_usd(pps_net_usd)}  ({verdict})")
    print()
    print("  Plain English: This is the boring path. The pool pays you a")
    print("  steady tiny amount based on how much work your rental did. No")
    print("  surprises. The NiceHash market is pretty efficient, so this is")
    print(f"  almost always a small {'loss' if pps_net_usd < 0 else 'gain'} — the 'house edge.'")

    # ---- scenario B: solo lottery ----
    section("OPTION B: Point it at a SOLO pool (the lottery)")
    print(f"  Chance of hitting a block:  {fmt_pct_odds(p_at_least_one)}")
    print(f"  If you hit, you win:        ~{fmt_usd(block_payout_usd)}")
    print(f"  On average you'd earn:      {fmt_usd(solo_ev_usd)}")
    print(f"  You paid:                   {fmt_usd(rental_usd)}")
    verdict = "POSITIVE EV" if solo_net_ev_usd > 0 else "NEGATIVE EV"
    print(f"  Expected net:               {fmt_usd(solo_net_ev_usd)}  ({verdict})")
    print()
    # compare to powerball
    powerball_odds = 1 / 292_201_338
    powerball_jackpot = 20_000_000  # typical starting jackpot
    your_dollars_per_odds = rental_usd / p_at_least_one if p_at_least_one > 0 else float("inf")
    powerball_dollars_per_odds = 2.0 / powerball_odds  # $2 ticket
    print(f"  Reality check vs. Powerball:")
    print(f"    Powerball: 1 in 292 million to win ~$20M (costs $2/ticket)")
    print(f"    Your bet:  {fmt_pct_odds(p_at_least_one)} to win ~{fmt_usd(block_payout_usd)} "
          f"(costs {fmt_usd(rental_usd)})")
    if your_dollars_per_odds < powerball_dollars_per_odds:
        ratio = powerball_dollars_per_odds / your_dollars_per_odds
        print(f"    Your odds-per-dollar are ~{ratio:,.0f}x BETTER than Powerball.")
    print()
    print("  Plain English: This IS gambling, but it's quantifiable gambling.")
    print("  Most of the time you get nothing. A tiny fraction of the time")
    print("  you hit a block and it's life-changing for the rental cost.")

    # ---- hedge options ----
    section("YOUR HEDGE OPTIONS")

    # Hedge 1: blended split — show the tradeoff curve
    print()
    print("  HEDGE #1 — The blended split (pick your spot on the curve)")
    print("  ----------------------------------------------------------")
    print("  Split your rental between a steady PPS pool and a solo pool.")
    print("  More PPS = smaller guaranteed loss. More solo = bigger lottery shot.")
    print()
    print(f"  {'Solo %':>7} | {'Guaranteed':>11} | {'Lottery odds':>20} | {'If hit':>11}")
    print(f"  {'-'*7}-+-{'-'*11}-+-{'-'*20}-+-{'-'*11}")
    for solo_pct in (0, 25, 50, 75, 100):
        solo_frac = solo_pct / 100.0
        pps_frac = 1 - solo_frac
        guaranteed = pps_frac * pps_usd - rental_usd  # PPS half pays, full rental still due
        share_x = (solo_frac * th) / network_th
        exp_blocks = share_x * blocks_per_hour * hours
        px = 1.0 - math.exp(-exp_blocks)
        odds_str = fmt_pct_odds(px) if px > 0 else "n/a"
        print(f"  {solo_pct:>6}% | {fmt_usd(guaranteed):>11} | {odds_str:>20} | "
              f"{fmt_usd(block_payout_usd):>11}")
    print()
    print("  How to read this table:")
    print("    - 'Guaranteed' is what you net after PPS payout minus rental cost,")
    print("       regardless of whether the solo half hits.")
    print("    - 'Lottery odds' is your chance the solo half hits a block.")
    print("    - 'If hit' is the payout on top of the guaranteed line.")
    print("  Pick the row that matches your tolerance for boring vs. spicy.")

    # Hedge 2: just PPS
    print()
    print("  HEDGE #2 — The 'don't be dumb' hedge")
    print("  ------------------------------------")
    print(f"  Just use PPS. Accept the small {fmt_usd(abs(pps_net_usd))} "
          f"{'loss' if pps_net_usd < 0 else 'gain'} as the cost of curiosity.")
    print(f"  No variance, no excitement, no big surprises.")

    # Hedge 3: Kelly
    print()
    print("  HEDGE #3 — Kelly sizing (how much SHOULD you bet?)")
    print("  --------------------------------------------------")
    # Kelly fraction for a binary bet: f* = (p*b - q) / b, where b = win/loss ratio
    # Treating "all rental on solo" as the bet.
    if rental_usd > 0:
        b = block_payout_usd / rental_usd  # multiple-of-stake you win
        q = 1 - p_at_least_one
        kelly_frac = (p_at_least_one * b - q) / b
    else:
        kelly_frac = 0.0
    if kelly_frac <= 0:
        print(f"  Kelly says: bet $0. The expected value is negative, so the")
        print(f"  math says don't play. (If you play anyway, treat it as")
        print(f"  entertainment spending, not investment.)")
    else:
        print(f"  Kelly says: max {kelly_frac*100:.4f}% of your bankroll per bet.")
        if args.bankroll:
            print(f"  With a {fmt_usd(args.bankroll)} bankroll, that's "
                  f"{fmt_usd(args.bankroll * kelly_frac)} max stake.")
        else:
            print(f"  (Pass --bankroll <USD> to convert that into a dollar amount.)")

    # Hedge 4: BTC price hedge
    print()
    print("  HEDGE #4 — The BTC price hedge")
    print("  ------------------------------")
    print(f"  Your rental costs are in BTC. If BTC moves while you're renting,")
    print(f"  your USD cost moves with it. To neutralize that, on a perp")
    print(f"  exchange (Binance, Bybit, etc.) you'd short:")
    print(f"      ~{rental_btc:.8f} BTC (about {fmt_usd(rental_usd)} notional)")
    print(f"  Honest take: for a {hours:g}-hour rental this is overkill — BTC")
    print(f"  isn't moving 50% in an hour. Worth it for multi-day rentals.")

    # ---- bottom line ----
    section("BOTTOM LINE")
    if solo_net_ev_usd >= 0 and pps_net_usd >= 0:
        print("  Both options are profitable on average. Rare. Double-check inputs.")
    elif solo_net_ev_usd < 0 and pps_net_usd < 0:
        print("  Both options lose money on average. This is normal — NiceHash")
        print("  is an efficient market. You're paying for entertainment, not")
        print("  investment.")
        print()
        print(f"  If you want to play: use Hedge #1 (blended split). You'll")
        print(f"  cap your loss near zero and still get a real lottery ticket.")
    print()


if __name__ == "__main__":
    main()
