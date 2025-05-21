from ..ui.colors import Colors

# hella long docs (thanks ChatGPT!)
def print_detailed_help():
    help_text = f"""
{Colors.BOLD}{Colors.BLUE}🐙 EIGHTARMS - COMPREHENSIVE HELP GUIDE{Colors.RESET}
{Colors.BLUE}======================================={Colors.RESET}

{Colors.BOLD}WHAT IS EIGHTARMS?{Colors.RESET}
EightArms is a GitHub intelligence tool that extracts public email addresses
from user repositories by analyzing commit history. It uses advanced web
scraping techniques to gather publicly available contact information.

{Colors.BOLD}BASIC USAGE:{Colors.RESET}
  {Colors.GREEN}eightarms {Colors.YELLOW}<username> {Colors.DIM}[options]{Colors.RESET}

{Colors.BOLD}QUICK EXAMPLES:{Colors.RESET}
  {Colors.GREEN}eightarms {Colors.PURPLE}octocat{Colors.RESET}                    # Default medium speed
  {Colors.GREEN}eightarms {Colors.PURPLE}octocat {Colors.CYAN}--speed fast{Colors.RESET}       # Quick scan
  {Colors.GREEN}eightarms {Colors.PURPLE}octocat {Colors.CYAN}--speed slow{Colors.RESET}       # Thorough scan
  {Colors.GREEN}eightarms {Colors.PURPLE}octocat {Colors.CYAN}--max-repos 20{Colors.RESET}     # Scan more repos

{Colors.BOLD}SPEED PRESETS:{Colors.RESET}
  {Colors.YELLOW}fast{Colors.RESET}    - Quick scan (0.2-0.8s delays, 2 pages, [5,5] commits)
           Best for: Quick reconnaissance
  {Colors.YELLOW}medium{Colors.RESET}  - Balanced scan (0.5-1.5s delays, 3 pages, [10,10] commits) [DEFAULT]
           Best for: Regular use, good balance of speed and thoroughness
  {Colors.YELLOW}slow{Colors.RESET}    - Thorough scan (3.0-6.0s delays, 5 pages, all commits)
           Best for: Comprehensive analysis, being polite to GitHub

{Colors.BOLD}COMMIT SELECTION FORMATS:{Colors.RESET}
  {Colors.CYAN}all{Colors.RESET}       - Process all commits (can be very slow for large repos)
  {Colors.CYAN}15{Colors.RESET}        - Process only the first 15 commits
  {Colors.CYAN}[10,10]{Colors.RESET}   - Process first 10 AND last 10 commits (recommended)
  {Colors.CYAN}[20,0]{Colors.RESET}    - Process first 20 commits only
  {Colors.CYAN}[0,5]{Colors.RESET}     - Process last 5 commits only

{Colors.BOLD}ADVANCED OPTIONS:{Colors.RESET}
  {Colors.WHITE}--pages N{Colors.RESET}         Number of commit pages per repo (default: 3)
  {Colors.WHITE}--commits FORMAT{Colors.RESET}  Which commits to process (default: [10,10])
  {Colors.WHITE}--max-repos N{Colors.RESET}     Limit repositories to scan (default: 10)
  {Colors.WHITE}--multithreaded{Colors.RESET}   Enable concurrent processing (faster)
  {Colors.WHITE}--no-multithreaded{Colors.RESET} Disable concurrent processing (more polite)

{Colors.BOLD}CUSTOM CONFIGURATION EXAMPLES:{Colors.RESET}
  {Colors.GREEN}eightarms {Colors.PURPLE}username {Colors.CYAN}--pages 5 --commits all --multithreaded{Colors.RESET}
  {Colors.GREEN}eightarms {Colors.PURPLE}username {Colors.CYAN}--pages 2 --commits [20,5] --no-multithreaded{Colors.RESET}
  {Colors.GREEN}eightarms {Colors.PURPLE}username {Colors.CYAN}--commits 25 --max-repos 15{Colors.RESET}

{Colors.BOLD}WHAT EIGHTARMS FINDS:{Colors.RESET}
  {Colors.GREEN}✓{Colors.RESET} Author emails from commit headers
  {Colors.GREEN}✓{Colors.RESET} Committer emails from commit metadata  
  {Colors.GREEN}✓{Colors.RESET} Signed-off-by emails from commit messages
  {Colors.GREEN}✓{Colors.RESET} Co-authored-by emails from commit messages

{Colors.BOLD}WHAT GETS FILTERED OUT:{Colors.RESET}
  {Colors.RED}✗{Colors.RESET} GitHub noreply emails (users.noreply.github.com)
  {Colors.RED}✗{Colors.RESET} Invalid email formats
  {Colors.RED}✗{Colors.RESET} Common fake/test email addresses

{Colors.BOLD}HOW IT WORKS:{Colors.RESET}
  1. {Colors.BLUE}Discovers{Colors.RESET} public repositories for the target username
  2. {Colors.BLUE}Scrapes{Colors.RESET} commit history from repository pages
  3. {Colors.BLUE}Downloads{Colors.RESET} commit patches containing email metadata
  4. {Colors.BLUE}Extracts{Colors.RESET} email addresses using pattern matching
  5. {Colors.BLUE}Filters{Colors.RESET} and deduplicates the results

{Colors.BOLD}RATE LIMITING & POLITENESS:{Colors.RESET}
  • Built-in delays between requests to avoid overwhelming GitHub
  • Randomized user agent rotation
  • Configurable speed settings for different use cases
  • Automatic retry logic with exponential backoff

{Colors.BOLD}LIMITATIONS:{Colors.RESET}
  {Colors.RED}•{Colors.RESET} Only finds emails that users have made public
  {Colors.RED}•{Colors.RESET} Requires public repositories to analyze
  {Colors.RED}•{Colors.RESET} GitHub may rate-limit aggressive requests
  {Colors.RED}•{Colors.RESET} Some developers exclusively use GitHub's noreply emails
  {Colors.RED}•{Colors.RESET} Private repositories are not accessible

{Colors.BOLD}ETHICAL USAGE GUIDELINES:{Colors.RESET}
  {Colors.GREEN}✓{Colors.RESET} Only scrapes publicly available information
  {Colors.GREEN}✓{Colors.RESET} Respects GitHub's Terms of Service
  {Colors.GREEN}✓{Colors.RESET} Uses reasonable rate limiting
  {Colors.GREEN}✓{Colors.RESET} Provides clear attribution in User-Agent headers
  {Colors.YELLOW}⚠{Colors.RESET}  Use responsibly and for legitimate purposes only
  {Colors.YELLOW}⚠{Colors.RESET}  Consider reaching out directly before mass scraping
  {Colors.YELLOW}⚠{Colors.RESET}  Respect privacy and applicable laws

{Colors.BOLD}TROUBLESHOOTING:{Colors.RESET}
  {Colors.WHITE}No emails found?{Colors.RESET}
    - User may not have public repositories
    - User may use only private email settings
    - Try increasing --max-repos or using --speed slow
  
  {Colors.WHITE}Getting rate limited?{Colors.RESET}
    - Use --speed slow for more polite delays
    - Use --no-multithreaded to reduce concurrent requests
    - Wait a few minutes before retrying
  
  {Colors.WHITE}Connection errors?{Colors.RESET}
    - Check your internet connection
    - Try --no-multithreaded to reduce load
    - Verify the username is correct

{Colors.BOLD}INSTALLATION:{Colors.RESET}
  {Colors.GREEN}pip install eightarms{Colors.RESET}
  {Colors.DIM}# Or for development:{Colors.RESET}
  {Colors.GREEN}pip install -e .{Colors.RESET}

{Colors.BOLD}EXAMPLES OF OUTPUT:{Colors.RESET}
  {Colors.GREEN}📧 Found 3 unique emails for octocat:{Colors.RESET}
    {Colors.CYAN}•{Colors.RESET} {Colors.WHITE}octocat@github.com{Colors.RESET}
    {Colors.CYAN}•{Colors.RESET} {Colors.WHITE}support@octocat.org{Colors.RESET}
    {Colors.CYAN}•{Colors.RESET} {Colors.WHITE}contact@example.com{Colors.RESET}
"""
    print(help_text)