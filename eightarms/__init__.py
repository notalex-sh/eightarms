"""
EightArms - GitHub Email Scraper
"""

__version__ = "1.0.0"
__author__ = "Not Alex"

from .core.scraper import GitHubWebScraper, GitHubWebScraperCLI
from .core.filters import filter_github_emails, filter_invalid_emails
from .config.settings import create_config, create_custom_config
from .config.presets import SPEED_PRESETS

__all__ = [
    "GitHubWebScraper",
    "GitHubWebScraperCLI", 
    "filter_github_emails",
    "filter_invalid_emails",
    "create_config",
    "create_custom_config",
    "SPEED_PRESETS",
]