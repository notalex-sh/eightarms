import re
from typing import Set

# remove junk

def filter_github_emails(emails: Set[str]) -> Set[str]:
    return {email for email in emails if not email.endswith('users.noreply.github.com')}


def filter_invalid_emails(emails: Set[str]) -> Set[str]:
    valid_emails = set()

    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    for email in emails:
        # Basic validation
        if email_pattern.match(email):
            # Additional checks
            if not email.startswith('.') and not email.endswith('.'):
                if '@.' not in email and '..' not in email:
                    valid_emails.add(email)
    
    return valid_emails


def filter_common_fake_emails(emails: Set[str]) -> Set[str]:
    fake_patterns = [
        r'.*@example\.com$',
        r'.*@test\.com$',
        r'.*@localhost$',
        r'test@.*',
        r'fake@.*',
        r'noreply@.*',
        r'.*@noreply\..*',
    ]
    
    filtered_emails = set()
    
    for email in emails:
        is_fake = False
        for pattern in fake_patterns:
            if re.match(pattern, email, re.IGNORECASE):
                is_fake = True
                break
        
        if not is_fake:
            filtered_emails.add(email)
    
    return filtered_emails


def apply_all_filters(emails: Set[str]) -> Set[str]:
    filtered = emails
    filtered = filter_github_emails(filtered)
    filtered = filter_invalid_emails(filtered)
    filtered = filter_common_fake_emails(filtered)
    return filtered