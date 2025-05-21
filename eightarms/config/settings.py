import argparse
from .presets import get_speed_preset
from ..utils.validators import parse_commits_arg

# essentially custom config setup

def create_config(speed_preset: str) -> dict:
    return get_speed_preset(speed_preset)


def create_custom_config(args) -> dict:
    return {
        'min_delay': 0.5 if args.multithreaded else 1.0,
        'max_delay': 1.5 if args.multithreaded else 3.0,
        'batch_delay': 0.2 if args.multithreaded else 1.0,
        'max_pages': args.pages,
        'commits': args.commits,
        'multithreaded': args.multithreaded,
        'max_workers': 6 if args.multithreaded else 1,
        'description': 'Custom configuration'
    }

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='EightArms - GitHub Email Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  eightarms octocat                     # Default scan
  eightarms octocat --speed fast        # Quick scan  
  eightarms octocat --speed slow        # Thorough scan
  eightarms --detailed-help             # Full help

COMMIT FORMATS:
  all          - Process all commits
  10           - Process first 10 commits  
  [10,10]      - Process first 10 and last 10 commits
  [20,0]       - Process first 20 commits only
  [0,5]        - Process last 5 commits only

SPEED PRESETS:
  fast    - Quick scan (0.2-0.8s delays, 2 pages, [5,5] commits)
  medium  - Balanced (0.5-1.5s delays, 3 pages, [10,10] commits) [DEFAULT]
  slow    - Thorough (3.0-6.0s delays, 5 pages, all commits)
        """,
        add_help=False
    )
    
    parser.add_argument('-h', '--help', action='help', 
                       help='Show this help message and exit')
    parser.add_argument('--detailed-help', action='store_true',
                       help='Show comprehensive help documentation')
    
    parser.add_argument('username', nargs='?', help='GitHub username to scrape')
    
    speed_group = parser.add_argument_group('Speed Presets')
    speed_group.add_argument('--speed', choices=['slow', 'medium', 'fast'], 
                           default='medium', help='Predefined speed settings (default: medium)')
    
    custom_group = parser.add_argument_group('Custom Options')
    custom_group.add_argument('--pages', type=int, default=3, 
                            help='Number of commit pages to fetch per repo (default: 3)')
    custom_group.add_argument('--commits', type=parse_commits_arg, default=[10, 10],
                            help='Commits to process: "all", "15", or "[10,10]" (default: [10,10])')
    custom_group.add_argument('--multithreaded', action='store_true', default=None,
                            help='Enable multithreading')
    custom_group.add_argument('--no-multithreaded', dest='multithreaded', action='store_false',
                            help='Disable multithreading')
    custom_group.add_argument('--max-repos', type=int, default=10,
                            help='Maximum number of repositories to process (default: 10)')
    
    return parser