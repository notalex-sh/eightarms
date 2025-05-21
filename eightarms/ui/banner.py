from .colors import Colors

# cool octopus banner

def print_banner():
    banner = f"""
{Colors.CYAN}         ______
        /      \\ 
       /        \\ 
       |        |
    )  o        o   ?        {Colors.BOLD}{Colors.BLUE}EightArms{Colors.RESET}
   (    \\      /    |        {Colors.DIM}GitHub Email Intelligence{Colors.RESET}
  * \\*__/||||||\\___/ _
   \\____/ |||| \\____/ `
   ,-.___/ || \\__,-._
  /    ___/  \\__
     _/         `--{Colors.RESET}
"""
    print(banner)


def print_config(config: dict, speed_preset: str, is_custom: bool = False):
    print(f"{Colors.BOLD}{Colors.YELLOW}CONFIGURATION{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * 50}{Colors.RESET}")
    
    if is_custom:
        print(f"  {Colors.WHITE}Mode:{Colors.RESET} {Colors.PURPLE}Custom{Colors.RESET}")
    else:
        speed_colors = {
            'slow': Colors.YELLOW, 
            'medium': Colors.GREEN, 
            'fast': Colors.CYAN
        }
        speed_color = speed_colors.get(speed_preset, Colors.WHITE)
        print(f"  {Colors.WHITE}Speed:{Colors.RESET} {speed_color}{speed_preset.title()}{Colors.RESET}")
    
    print(f"  {Colors.WHITE}Delays:{Colors.RESET} {Colors.CYAN}{config['min_delay']:.1f}-{config['max_delay']:.1f}s{Colors.RESET}")
    print(f"  {Colors.WHITE}Pages per repo:{Colors.RESET} {Colors.YELLOW}{config['max_pages']}{Colors.RESET}")
    print(f"  {Colors.WHITE}Commits:{Colors.RESET} {Colors.GREEN}{config['commits']}{Colors.RESET}")
    
    threading_color = Colors.GREEN if config['multithreaded'] else Colors.RED
    threading_text = 'Yes' if config['multithreaded'] else 'No'
    print(f"  {Colors.WHITE}Multithreaded:{Colors.RESET} {threading_color}{threading_text}{Colors.RESET}")
    
    if config['multithreaded']:
        print(f"  {Colors.WHITE}Workers:{Colors.RESET} {Colors.CYAN}{config['max_workers']}{Colors.RESET}")
    
    if 'description' in config:
        print(f"  {Colors.WHITE}Description:{Colors.RESET} {Colors.DIM}{config['description']}{Colors.RESET}")
    
    print(f"{Colors.BLUE}{'─' * 50}{Colors.RESET}")
