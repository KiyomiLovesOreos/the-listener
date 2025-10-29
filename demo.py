#!/usr/bin/env python3
"""
Quick demo of The Listener game
"""
import subprocess
import sys

print("=" * 70)
print("                    THE LISTENER - DEMO")
print("=" * 70)
print("\nThis is a cosmic horror survival game with two modes:")
print("\n1. TERMINAL MODE - Process deep space signals")
print("   Commands: scan, analyze <n>, decode, submit")
print("\n2. EXPLORATION MODE - Navigate the station in first-person ASCII")
print("   Commands: explore, then use WASD to move, Q to exit")
print("\n" + "=" * 70)
print("\nGame features:")
print("  ✓ Signal processing with sanity effects")
print("  ✓ Resource management (power, oxygen, supplies)")
print("  ✓ First-person ASCII station navigation")
print("  ✓ Random events and system failures")
print("  ✓ Multiple signal types with horror content")
print("\n" + "=" * 70)

choice = input("\nReady to play? (y/n): ").strip().lower()

if choice == 'y':
    print("\nLaunching The Listener...\n")
    subprocess.run([sys.executable, "the_listener.py"])
else:
    print("\nTo play later, run: python3 the_listener.py")
    print("Type 'help' in-game for all commands.")
