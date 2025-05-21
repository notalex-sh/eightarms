# some colors

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.RESET}"
    
    @staticmethod
    def bold(text: str) -> str:
        """Make text bold"""
        return f"{Colors.BOLD}{text}{Colors.RESET}"
    
    @staticmethod
    def dim(text: str) -> str:
        """Make text dim"""
        return f"{Colors.DIM}{text}{Colors.RESET}"