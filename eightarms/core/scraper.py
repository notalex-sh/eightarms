import requests
import time
import re
from bs4 import BeautifulSoup
from typing import Set, List
import random
import concurrent.futures
from threading import Lock
import sys
import warnings
from urllib3.exceptions import InsecureRequestWarning
from ..ui.colors import Colors
from ..ui.progress import ProgressSpinner

# core scraping functionality

# Suppress SSL warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')


class GitHubWebScraper:
    def __init__(self, max_workers=5):
        self.session = requests.Session()
        self.max_workers = max_workers
        self.lock = Lock()
        self.progress = ProgressSpinner()

        # here we use a random user agent for anonymity

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
        ]
        
    def get_random_delay(self, min_delay=0.5, max_delay=1.5):
        return random.uniform(min_delay, max_delay)
    
    # retry if fail
    def get_page_with_retry(self, url: str, max_retries: int = 2) -> requests.Response:
        for attempt in range(max_retries):
            try:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    time.sleep(30)
                    
            except Exception:
                pass
                
            if attempt < max_retries - 1:
                time.sleep(self.get_random_delay())
        
        return None
    
    # multi-strategy approach for pulling repos
    def get_user_repositories(self, username: str) -> List[str]:
        repos = []
        
        urls_to_try = [
            f"https://github.com/{username}?tab=repositories",
            f"https://github.com/{username}?tab=repositories&type=public",
            f"https://github.com/{username}"
        ]
        
        for url in urls_to_try:
            response = self.get_page_with_retry(url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            repo_names = set()
            
            # pull repo links via <a>
            repo_links = soup.find_all('a', href=True)
            for link in repo_links:
                href = link.get('href', '')
                repo_match = re.match(f'^/{re.escape(username)}/([^/]+)/?$', href)
                if repo_match:
                    repo_name = repo_match.group(1)
                    if repo_name not in ['followers', 'following', 'repositories', 'projects', 'packages', 'stars']:
                        repo_names.add(repo_name)
            
            # search divs for keywords
            repo_items = soup.find_all(['div', 'li'], class_=re.compile(r'repo|repository', re.I))
            for item in repo_items:
                links = item.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    repo_match = re.match(f'^/{re.escape(username)}/([^/]+)/?$', href)
                    if repo_match:
                        repo_name = repo_match.group(1)
                        if repo_name not in ['followers', 'following', 'repositories', 'projects', 'packages', 'stars']:
                            repo_names.add(repo_name)
            
            if repo_names:
                repos = list(repo_names)
                break
            
            time.sleep(self.get_random_delay())
        
        return repos
    
    # multi-strategy approach for pulling SHAs (to get patches later on)
    def get_commit_shas(self, username: str, repo: str, max_pages: int = 2) -> List[str]:
        commits = []
        
        def fetch_page(page_num):
            url = f"https://github.com/{username}/{repo}/commits?page={page_num}"
            response = self.get_page_with_retry(url)
            page_commits = []
            
            if not response:
                return page_commits
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # use commit link attribute
            commit_elements = soup.find_all(attrs={'data-commit-link': True})
            for element in commit_elements:
                commit_link = element.get('data-commit-link', '')
                if '/commit/' in commit_link:
                    sha = commit_link.split('/commit/')[-1]
                    if sha and len(sha) >= 7:
                        page_commits.append(sha)
            
            # pull <a> and check regex
            if not page_commits:
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    href = link.get('href', '')
                    if f'/{username}/{repo}/commit/' in href:
                        sha = href.split('/commit/')[-1].split('?')[0].split('#')[0]
                        if sha and len(sha) >= 7 and re.match(r'^[a-f0-9]+$', sha, re.IGNORECASE):
                            page_commits.append(sha)
            
            return page_commits
        
        # fetch pages with max workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_page = {executor.submit(fetch_page, page): page for page in range(1, max_pages + 1)}
            
            for future in concurrent.futures.as_completed(future_to_page):
                page_commits = future.result()
                commits.extend(page_commits)
        
        unique_commits = []
        seen = set()
        for commit in commits:
            if commit not in seen:
                unique_commits.append(commit)
                seen.add(commit)
                
        return unique_commits
    
    def get_commit_patch(self, username: str, repo: str, sha: str) -> str:
        url = f"https://github.com/{username}/{repo}/commit/{sha}.patch"
        response = self.get_page_with_retry(url)
        
        if response:
            return response.text
        return ""
    
    # NOTE: here we pull ALL emails associated with REPO, may generate false positives

    def extract_emails_from_patch(self, patch_content: str) -> Set[str]:

        email_patterns = [
            r'From: .* <(.+@.+\..+)>',
            r'Author: .* <(.+@.+\..+)>',
            r'Committer: .* <(.+@.+\..+)>',
            r'Signed-off-by: .* <(.+@.+\..+)>',
            r'Co-authored-by: .* <(.+@.+\..+)>',
        ]
        
        emails = set()
        for pattern in email_patterns:
            matches = re.findall(pattern, patch_content, re.IGNORECASE)
            emails.update(matches)
            
        return emails

# interface CLI and scraper (basically puts stuff into functions)

class GitHubWebScraperCLI(GitHubWebScraper):
    def __init__(self, config):
        if config['multithreaded']:
            max_workers = config.get('max_workers', 4)
        else:
            max_workers = 1
        
        super().__init__(max_workers)
        self.config = config
    
    def get_random_delay(self, min_delay=None, max_delay=None):
        if min_delay is None:
            min_delay = self.config['min_delay']
        if max_delay is None:
            max_delay = self.config['max_delay']
        return random.uniform(min_delay, max_delay)
    
    def get_commit_shas(self, username: str, repo: str, max_pages: int = None) -> List[str]:
        if max_pages is None:
            max_pages = self.config.get('max_pages', 2)
        return super().get_commit_shas(username, repo, max_pages)
    
    def process_repo_commits(self, username: str, repo: str) -> Set[str]:
        repo_emails = set()
        
        commits = self.get_commit_shas(username, repo)
        selected_commits = self.get_commit_range(commits, self.config['commits'])
        
        if not selected_commits:
            return repo_emails
        
        def fetch_commit_emails(sha):
            patch = self.get_commit_patch(username, repo, sha)
            emails = set()
            if patch:
                emails = self.extract_emails_from_patch(patch)
            
            with self.lock:
                self.progress.increment()
            
            return emails
        
        if self.config['multithreaded'] and len(selected_commits) > 5:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_sha = {executor.submit(fetch_commit_emails, sha): sha for sha in selected_commits}
                
                for i, future in enumerate(concurrent.futures.as_completed(future_to_sha)):
                    try:
                        emails = future.result()
                        repo_emails.update(emails)
                    except Exception:
                        pass
                    
                    if i % 5 == 0:
                        time.sleep(self.config['batch_delay'])
        else:
            for i, sha in enumerate(selected_commits):
                emails = fetch_commit_emails(sha)
                repo_emails.update(emails)
                
                if i < len(selected_commits) - 1:
                    time.sleep(self.get_random_delay())
        
        return repo_emails
    
    def get_commit_range(self, commits, commit_spec):
        if commit_spec == 'all':
            return commits
        
        if isinstance(commit_spec, list):
            top, bottom = commit_spec
            if top == 0 and bottom == 0:
                return []
            elif bottom == 0:
                return commits[:top]
            elif top == 0:
                return commits[-bottom:]
            else:
                if len(commits) <= (top + bottom):
                    return commits
                else:
                    return commits[:top] + commits[-bottom:]
        
        return commits
    
    def extract_user_emails(self, username: str, max_repos: int = 6) -> Set[str]:

        repos = self.get_user_repositories(username)
        if not repos:
            return set()
        
        if max_repos:
            repos = repos[:max_repos]
            
        all_emails = set()
        
        total_commits_to_process = 0
        for repo in repos:
            commits = self.get_commit_shas(username, repo)
            selected_commits = self.get_commit_range(commits, self.config['commits'])
            total_commits_to_process += len(selected_commits)

        self.progress.set_total(total_commits_to_process)
        
        print(f"{Colors.BLUE}Found {Colors.YELLOW}{len(repos)}{Colors.BLUE} repositories for {Colors.PURPLE}{username}{Colors.RESET}")
        print(f"{Colors.GREEN}Analysing {Colors.YELLOW}{total_commits_to_process}{Colors.GREEN} commit patches...{Colors.RESET}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_repo = {executor.submit(self.process_repo_commits, username, repo): repo for repo in repos}
            
            for future in concurrent.futures.as_completed(future_to_repo):
                try:
                    repo_emails = future.result()
                    all_emails.update(repo_emails)
                except Exception:
                    pass
        
        print()  
        self.progress.finish() 
        return all_emails
