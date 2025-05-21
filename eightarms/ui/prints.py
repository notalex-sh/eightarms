from .colors import Colors

# other output/ui utility-ish function (but not in utilities)

def print_results_header():
    print(f"\n{Colors.BOLD}{Colors.GREEN}RESULTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'═' * 50}{Colors.RESET}")


def print_results_footer(username: str):
    print()
    print(f"{Colors.BLUE}{'═' * 50}{Colors.RESET}")
    print(f"{Colors.DIM}Scan completed for {username}{Colors.RESET}")


def print_error(message: str):
    print(f"{Colors.RED}Error: {message}{Colors.RESET}")


def print_success(message: str):
    print(f"{Colors.GREEN}{message}{Colors.RESET}")


def print_warning(message: str):
    print(f"{Colors.YELLOW}{message}{Colors.RESET}")


def print_info(message: str):
    print(f"{Colors.BLUE}{message}{Colors.RESET}")