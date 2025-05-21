import argparse
import re

# cli input validation and parsing

def parse_commits_arg(commits_str: str):
    if commits_str.lower() == 'all':
        return 'all'
    
    try:
        if commits_str.startswith('[') and commits_str.endswith(']'):
            commits_str = commits_str[1:-1]
        
        if ',' in commits_str:
            top, bottom = map(int, commits_str.split(','))
            if top < 0 or bottom < 0:
                raise ValueError("Commit counts cannot be negative")
            return [top, bottom]
        else:
            commits_count = int(commits_str)
            if commits_count < 0:
                raise ValueError("Commit count cannot be negative")
            return [commits_count, 0]
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid commits format: {commits_str}. Use 'all', '10', or '[10,10]'. {str(e)}"
        )

# check uname is valid github uname
def validate_username(username: str) -> bool:
    if not username:
        return False
    
    if len(username) > 39:
        return False
    
    if username.startswith('-') or username.endswith('-'):
        return False
    
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', username):
        return False
    
    if '--' in username:
        return False
    
    return True


def validate_max_repos(max_repos: int) -> bool:
    return 1 <= max_repos <= 100

# 20 page cap
def validate_pages(pages: int) -> bool:
    return 1 <= pages <= 20

# sanitize username in case the user cant read lol
def sanitize_username(username: str) -> str:
    if not username:
        return ""
    
    username = username.strip()
    username = re.sub(r'^https?://github\.com/', '', username)
    username = re.sub(r'^github\.com/', '', username)
    username = username.lstrip('/')
    username = username.split('/')[0]
    
    return username