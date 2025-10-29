#!/usr/bin/env python3
"""
Visual showcase of The Listener's enhanced features
"""
import time
import os
from the_listener import Colors

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def showcase():
    clear()
    
    # Title
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║              THE LISTENER - VISUAL FEATURES SHOWCASE              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    input("\nPress Enter to see color system...")
    
    # Color System
    clear()
    print(f"\n{Colors.BOLD}1. COLOR-CODED UI ELEMENTS{Colors.END}\n")
    print(f"{Colors.BLUE}Status Labels:{Colors.END} {Colors.YELLOW}Value{Colors.END}")
    print(f"{Colors.GREEN}High Resource (70-100%){Colors.END}")
    print(f"{Colors.YELLOW}Medium Resource (40-69%){Colors.END}")
    print(f"{Colors.RED}Low Resource (0-39%){Colors.END}")
    print(f"\n{Colors.CYAN}Commands{Colors.END} │ {Colors.GRAY}Separators{Colors.END} │ {Colors.DIM}Hints{Colors.END}")
    
    input("\n\nPress Enter to see signal types...")
    
    # Signal Types
    clear()
    print(f"\n{Colors.BOLD}2. SIGNAL TYPE COLORS{Colors.END}\n")
    print(f"{Colors.CYAN}DATA_STREAM{Colors.END} - Technical information")
    print(f"{Colors.YELLOW}VOICE{Colors.END} - Disturbing audio transmissions")
    print(f"{Colors.GREEN}COORDINATES{Colors.END} - Location data")
    print(f"{Colors.BLUE}BLUEPRINT{Colors.END} - Construction schematics")
    print(f"{Colors.RED}{Colors.BOLD}WARNING{Colors.END} - Critical alerts")
    print(f"{Colors.MAGENTA}{Colors.BOLD}UNKNOWN{Colors.END} - Incomprehensible signals")
    
    input("\n\nPress Enter to see loading animations...")
    
    # Animations
    clear()
    print(f"\n{Colors.BOLD}3. ANIMATED SEQUENCES{Colors.END}\n")
    
    for text in ["Scanning", "Analyzing", "Decoding", "Transmitting"]:
        for i in range(3):
            dots = "." * ((i % 3) + 1)
            print(f"\r{Colors.CYAN}{text}{dots}   {Colors.END}", end='', flush=True)
            time.sleep(0.3)
        print(f" {Colors.GREEN}✓{Colors.END}")
        time.sleep(0.3)
    
    input("\n\nPress Enter to see box-drawing characters...")
    
    # Box Drawing
    clear()
    print(f"\n{Colors.BOLD}4. PROFESSIONAL UI ELEMENTS{Colors.END}\n")
    print(f"{Colors.CYAN}╔{'═' * 68}╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.END} {Colors.BOLD}DECODED CONTENT{Colors.END}" + " " * 52 + f"{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╠{'═' * 68}╣{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}Signal content appears here in atmospheric colors...{Colors.END}          {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚{'═' * 68}╝{Colors.END}")
    
    input("\n\nPress Enter to see sanity effects (low sanity simulation)...")
    
    # Sanity Effects
    clear()
    print(f"\n{Colors.BOLD}5. SANITY-BASED VISUAL GLITCHES{Colors.END}\n")
    
    glitch_chars = ['░', '▒', '▓', '█', '▄', '▀', '■']
    
    print("Normal text at high sanity")
    time.sleep(0.5)
    print(f"{Colors.YELLOW}Slightly distorted at medium sanity{Colors.END}")
    time.sleep(0.5)
    print(f"{Colors.RED}H{Colors.MAGENTA}e{Colors.RED}a{Colors.CYAN}v{Colors.RED}i{Colors.MAGENTA}l{Colors.RED}y corrupted at low sanity{Colors.END}")
    time.sleep(0.5)
    print(f"{Colors.RED}▓{Colors.MAGENTA}░{Colors.CYAN}▒{Colors.RED}█ Extreme corruption {Colors.CYAN}▒{Colors.MAGENTA}░{Colors.RED}▓{Colors.END}")
    
    time.sleep(1)
    input("\n\nPress Enter to see screen flicker effect...")
    
    # Screen Flicker
    clear()
    print(f"\n{Colors.BOLD}6. SCREEN FLICKER (at low sanity){Colors.END}\n")
    print("Processing signal...")
    time.sleep(1)
    
    clear()
    print("\n" * 10)
    print(f"{Colors.RED}{Colors.BLINK}{Colors.BOLD}{'T̷H̴E̸Y̵ ̴A̶R̴E̷ ̸W̶A̶T̷C̸H̷I̶N̵G̴'.center(70)}{Colors.END}")
    print("\a")
    time.sleep(0.5)
    
    clear()
    print(f"\n{Colors.BOLD}6. SCREEN FLICKER (at low sanity){Colors.END}\n")
    print(f"{Colors.GREEN}Signal processing complete{Colors.END}")
    
    input("\n\nPress Enter to see audio feedback...")
    
    # Audio
    clear()
    print(f"\n{Colors.BOLD}7. SIMULATED AUDIO FEEDBACK{Colors.END}\n")
    
    print(f"\n{Colors.YELLOW}Event: Signal decoded{Colors.END}")
    time.sleep(0.5)
    
    print(f"\n{Colors.RED}Critical event: Power failure!{Colors.END}")
    print("\a\a")
    time.sleep(0.5)
    
    print(f"\n{Colors.GRAY}[LOG]: A faint scratching sound is heard from inside the walls.{Colors.END}")
    time.sleep(0.5)
    print(f"{Colors.GRAY}[LOG]: Three distinct, slow knocks echo from the exterior hull.{Colors.END}")
    
    input("\n\nPress Enter to see exploration mode preview...")
    
    # Exploration
    clear()
    print(f"\n{Colors.BOLD}8. FIRST-PERSON EXPLORATION{Colors.END}\n")
    print(f"{Colors.CYAN}{'═' * 70}{Colors.END}")
    print(f"{Colors.BLUE}Position:{Colors.END} {Colors.CYAN}(5, 5){Colors.END} │ {Colors.BLUE}Facing:{Colors.END} {Colors.YELLOW}NORTH{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 70}{Colors.END}\n")
    
    # Simple corridor view
    print(f"        {Colors.GRAY}###########{Colors.END}")
    print(f"       {Colors.GRAY}#############{Colors.END}")
    print(f"      {Colors.GRAY}###############{Colors.END}")
    print(f"     {Colors.GRAY}#################{Colors.END}")
    print(f"    {Colors.GRAY}####################{Colors.END}")
    
    print(f"\n{Colors.CYAN}{'═' * 20}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}    [  YOU  ]{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 20}{Colors.END}")
    
    print(f"\n{Colors.DIM}W=Forward, S=Backward, A=Turn Left, D=Turn Right{Colors.END}")
    
    input("\n\nPress Enter to finish...")
    
    # Summary
    clear()
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                        FEATURES SUMMARY                            ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    print(f"\n{Colors.GREEN}✓{Colors.END} Full ANSI color support")
    print(f"{Colors.GREEN}✓{Colors.END} Animated loading sequences")
    print(f"{Colors.GREEN}✓{Colors.END} Box-drawing UI elements")
    print(f"{Colors.GREEN}✓{Colors.END} Sanity-based visual glitches")
    print(f"{Colors.GREEN}✓{Colors.END} Screen flicker effects")
    print(f"{Colors.GREEN}✓{Colors.END} Terminal bell audio feedback")
    print(f"{Colors.GREEN}✓{Colors.END} Atmospheric sound descriptions")
    print(f"{Colors.GREEN}✓{Colors.END} Color-coded status indicators")
    print(f"{Colors.GREEN}✓{Colors.END} Professional typography")
    
    print(f"\n{Colors.YELLOW}Ready to play The Listener?{Colors.END}")
    choice = input(f"{Colors.CYAN}>{Colors.END} Launch game? (y/n): ").strip().lower()
    
    if choice == 'y':
        print(f"\n{Colors.GREEN}Launching...{Colors.END}\n")
        time.sleep(1)
        import subprocess
        import sys
        subprocess.run([sys.executable, "the_listener.py"])
    else:
        print(f"\n{Colors.YELLOW}Run 'python3 the_listener.py' when ready!{Colors.END}")

if __name__ == "__main__":
    showcase()
