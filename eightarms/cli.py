#!/usr/bin/env python3

# commandline interface stuff
import sys
from .ui.colors import Colors
from .ui.banner import print_banner, print_config
from .config.settings import create_argument_parser, create_config, create_custom_config
from .utils.help import print_detailed_help
from .core.scraper import GitHubWebScraperCLI
from .core.filters import filter_github_emails


def main():
    print_banner()
    
    # check for detailed help first
    if len(sys.argv) > 1 and sys.argv[1] in ['--detailed-help', '--help-detailed', '--full-help']:
        print_detailed_help()
        return
    
    # parse arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if args.detailed_help:
        print_detailed_help()
        return
    
    if not args.username:
        print(f"{Colors.RED}Error: Username is required!{Colors.RESET}")
        print(f"{Colors.WHITE}Usage: {Colors.GREEN}eightarms {Colors.YELLOW}<username> {Colors.DIM}[options]{Colors.RESET}")
        print(f"{Colors.DIM}Try: {Colors.GREEN}eightarms --help{Colors.RESET}")
        sys.exit(1)
    
    # check if default config should be used and print this
    using_custom = any([
        args.pages != 3,
        args.commits != [10, 10],
        args.multithreaded is not None
    ])
    
    if using_custom:
        config = create_custom_config(args)
    else:
        config = create_config(args.speed)
    
    print_config(config, args.speed, using_custom)

    print(f"{Colors.GREEN}Target:{Colors.RESET} {Colors.PURPLE}{args.username}{Colors.RESET}")
    print(f"{Colors.GREEN}Max repos:{Colors.RESET} {Colors.YELLOW}{args.max_repos}{Colors.RESET}")
    print()
    
    # run scraper
    try:
        scraper = GitHubWebScraperCLI(config)
        emails = scraper.extract_user_emails(args.username, max_repos=args.max_repos)
        
        # filter out GitHub noreply emails
        filtered_emails = filter_github_emails(emails)
        
        # results output
        print(f"\n{Colors.BOLD}{Colors.GREEN}✨ RESULTS{Colors.RESET}")
        print(f"{Colors.BLUE}{'═' * 50}{Colors.RESET}")
        
        if filtered_emails:
            print(f"{Colors.GREEN}📧 Found {Colors.YELLOW}{len(filtered_emails)}{Colors.GREEN} unique emails for {Colors.PURPLE}{args.username}{Colors.GREEN}:{Colors.RESET}")
            print()
            for email in sorted(filtered_emails):
                print(f"  {Colors.CYAN}•{Colors.RESET} {Colors.WHITE}{email}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}📭 No public emails found for {Colors.PURPLE}{args.username}{Colors.RESET}")
            print(f"{Colors.DIM}   User may have private emails or use GitHub's noreply service{Colors.RESET}")
        
        print()
        print(f"{Colors.BLUE}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.DIM}Scan completed for {args.username}{Colors.RESET}")
    
    # exit keyboard interrupt or error

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Scraping interrupted{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()