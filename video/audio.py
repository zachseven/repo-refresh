#!/usr/bin/env python3
"""Synthesize a heartbeat + ambient drone bed, synced to the visual heart-rate timeline."""
import math, wave, struct, sys

SR = 44100
DUR = 63.0
N = int(SR * DUR)

def heart_rate(t):
    if t < 18:   return 1.0
    if t < 23:   return 1.0 + (0.0 - 1.0) * ((t - 18) / 5)   # slow toward flatline
    if t < 26.5: return 0.0                                   # flatline
    if t < 29:   return 0.0 + (1.0) * ((t - 26.5) / 2.5)      # restart
    return 1.05

# precompute cumulative beat phase
STEP = 1.0 / 240
PN = int(DUR / STEP) + 2
PH = [0.0] * PN
acc = 0.0
for i in range(PN):
    PH[i] = acc
    acc += heart_rate(i * STEP) * STEP

def phase(t):
    f = t / STEP
    i = int(f)
    if i >= PN - 1: return PH[-1]
    return PH[i] + (PH[i+1] - PH[i]) * (f - i)

def thump(u, c, wd):
    d = (u - c) / wd
    return math.exp(-d * d)

try:
    import numpy as np
    have_np = True
except Exception:
    have_np = False

print("numpy:", have_np)

if have_np:
    t = np.arange(N) / SR
    # vectorized phase via interpolation table
    grid = np.arange(PN) * STEP
    ph = np.interp(t, grid, np.array(PH))
    f = ph - np.floor(ph)
    # lub-dub envelope
    env = np.exp(-((f - 0.06) / 0.045) ** 2) * 1.0 + np.exp(-((f - 0.215) / 0.055) ** 2) * 0.62
    # carrier: two low tones for body, slight downward pitch glide within each thump
    carrier = (np.sin(2 * np.pi * 58 * t) * 0.7 + np.sin(2 * np.pi * 92 * t) * 0.3)
    sub = np.sin(2 * np.pi * 44 * t) * 0.5
    beat = env * (carrier + sub)
    # soft attack transient (gives the "thud")
    transient = (np.exp(-((f - 0.06) / 0.012) ** 2) + np.exp(-((f - 0.215) / 0.012) ** 2)) \
                * np.sin(2 * np.pi * 130 * t) * 0.25
    beat = (beat + transient) * 0.85

    # ambient drone: low fifth, detuned, slow tremolo
    drone = (np.sin(2 * np.pi * 65.4 * t) + np.sin(2 * np.pi * 65.9 * t) * 0.6
             + np.sin(2 * np.pi * 98.0 * t) * 0.5)
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
    drone *= trem * 0.10

    # tension swell during the "death" of the body (18s..27s): rising shimmer that drops out
    swell_env = np.clip(np.minimum((t - 17) / 3.0, (27 - t) / 2.0), 0, 1)
    swell = np.sin(2 * np.pi * 196 * t) * 0.04 * swell_env
    # low rumble under the flatline
    rumble_env = np.clip(np.minimum((t - 22) / 1.0, (27 - t) / 1.5), 0, 1)
    rumble = (np.sin(2 * np.pi * 39 * t) + np.sin(2 * np.pi * 41 * t)) * 0.07 * rumble_env

    mix = beat + drone + swell + rumble

    # gentle global fade in/out
    fade = np.ones(N)
    fi = int(0.8 * SR); fo = int(1.0 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    mix *= fade

    # soft limiter / normalize
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.82
    mix = np.tanh(mix * 1.1) * 0.9

    pcm = (mix * 32767).astype('<i2')
    data = pcm.tobytes()
else:
    frames = bytearray()
    for i in range(N):
        tt = i / SR
        ph = phase(tt); f = ph - math.floor(ph)
        env = thump(f,0.06,0.045) + thump(f,0.215,0.055)*0.62
        carrier = math.sin(2*math.pi*58*tt)*0.7 + math.sin(2*math.pi*92*tt)*0.3
        val = env*carrier*0.6
        drone = (math.sin(2*math.pi*65.4*tt)+math.sin(2*math.pi*98*tt)*0.5)*0.08
        v = max(-1,min(1,(val+drone)))
        frames += struct.pack('<h', int(v*32767*0.82))
    data = bytes(frames)

with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'bed.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(data)
print("wrote audio,", N, "samples")
