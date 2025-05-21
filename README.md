# 🐙 EightArms - GitHub Email Intelligence Tool

An OSINT tool for extracting publicly available email addresses from GitHub repositories through commit history analysis. EightArms enables security researchers and investigators to gather intelligence while maintaining operational anonymity.

## Overview

EightArms performs automated reconnaissance on GitHub user accounts by analyzing publicly accessible commit metadata across their repository ecosystem. The tool extracts email addresses from commit headers, signatures, and collaboration records without requiring authentication or leaving forensic traces.

## Key Capabilities

- **Comprehensive Email Discovery** - Extracts emails from target repositories and associated development networks
- **Intelligent Filtering** - Removes invalid, fake, and system-generated addresses while preserving legitimate contacts
- **Configurable Speed Profiles** - Adjustable scanning intensity from rapid reconnaissance to thorough investigation
- **Concurrent Processing** - Multi-threaded analysis for efficient large-scale data collection
- **Rate Limiting Protection** - Built-in delays and retry mechanisms to avoid detection and service disruption
- **Anonymity Preservation** - Operates through standard HTTP requests without requiring authentication
- **Context Tracking** - Records source repositories and commit frequency for intelligence analysis

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- a cloned copy of this repo

### Setup Process
```bash
# Navigate to project directory
cd eightarms

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Verify installation
eightarms --help
```

## Usage

### Basic Operation
```bash
# Standard reconnaissance scan
eightarms <target_username>

# Rapid reconnaissance
eightarms <target_username> --speed fast

# Comprehensive investigation
eightarms <target_username> --speed slow
```

### Configuration Parameters

#### Speed Profiles

| Profile | Request Delay | Pages/Repo | Commits Analyzed | Concurrent Workers | Application |
|---------|---------------|------------|------------------|-------------------|-------------|
| `fast` | 0.2-0.8s | 2 | First/Last 5 | 6 | Quick reconnaissance |
| `medium` | 0.5-1.5s | 3 | First/Last 10 | 4 | Standard investigation |
| `slow` | 3.0-6.0s | 5 | All available | 1 | Comprehensive analysis |

#### Advanced Configuration
```bash
# Repository scope control
--max-repos N                 # Maximum repositories to analyze (default: 10)
--pages N                     # Commit pages per repository (default: 3)

# Commit selection patterns
--commits FORMAT              # Commit processing strategy (see below)

# Performance tuning
--multithreaded               # Enable concurrent processing
--no-multithreaded           # Single-threaded operation
```

#### Commit Selection Formats
- `all` - Process complete commit history (resource intensive)
- `15` - Analyze first 15 commits only
- `[10,10]` - Process first 10 and last 10 commits (recommended)
- `[20,0]` - Analyze first 20 commits only
- `[0,5]` - Process last 5 commits only

### Operational Examples

```bash
# Maximum coverage investigation
eightarms target --speed slow --max-repos 50 --commits all

# Balanced reconnaissance
eightarms target --commits [20,10] --max-repos 15

# Stealth operation
eightarms target --speed slow --no-multithreaded

# Targeted analysis
eightarms target --pages 5 --commits [15,5] --max-repos 8
```

## Technical Operation

### Data Collection Process

EightArms operates through a structured reconnaissance methodology:

1. **Target Enumeration** - Identifies public repositories associated with the target username
2. **Commit History Analysis** - Systematically retrieves commit metadata from repository timelines
3. **Patch Acquisition** - Downloads commit patches containing author and contributor information
4. **Email Extraction** - Parses commit headers using pattern matching algorithms
5. **Data Sanitization** - Applies filtering rules to remove invalid and system-generated addresses
6. **Intelligence Compilation** - Consolidates unique email addresses with source attribution

### Information Sources

The tool extracts contact information from multiple commit metadata fields:
- **Author Headers** - Primary commit authors and their configured email addresses
- **Committer Headers** - Users who performed the actual commit operations
- **Signed-off-by Lines** - Contributors who formally reviewed and approved changes
- **Co-authored-by Lines** - Collaborative contributors and pair programming participants

### Filtering Mechanisms

EightArms automatically excludes:
- GitHub noreply addresses (users.noreply.github.com)
- Malformed email addresses
- Common testing and placeholder addresses
- Obviously generated or temporary addresses

## OSINT Applications

### Anonymity Preservation

EightArms maintains operational security through several mechanisms:
- **No Authentication Required** - Operates using public GitHub interfaces without login
- **Standard HTTP Requests** - Uses legitimate web scraping patterns indistinguishable from normal browsing
- **Configurable Request Timing** - Adjustable delays to mimic human interaction patterns
- **User Agent Rotation** - Multiple browser identities to avoid fingerprinting
- **No Persistent Sessions** - Each request appears isolated without correlation markers

### Result Analysis

Collected email addresses require verification and analysis:
- Cross-reference with other intelligence sources
- Analyze commit frequency patterns to identify primary addresses
- Examine repository diversity to assess collaboration networks
- Validate through breach databases and data leak repositories
- Consider temporal patterns in commit activity

## Example Operation

```
    \    ______
     \  /      \ 
       /        \ 
       |        |
    )  o        o   ?        EightArms
   (    \      /    |        GitHub Email Intelligence
  * \*__/||||||\___/ _
   \____/ |||| \____/ `
   ,-.___/ || \__,-._
  /    ___/  \__
     _/         `--

CONFIGURATION
--------------------------------------------------
  Speed: Medium
  Delays: 0.5-1.5s
  Pages per repo: 3
  Commits: [10, 10]
  Multithreaded: Yes
  Workers: 4
--------------------------------------------------

Target: security_researcher

Found 12 repositories for security_researcher
Analyzing 89 commit patches...
Analysed 89 patches

RESULTS
==================================================
Found 6 unique emails for security_researcher:

  • researcher@security-firm.com
  • john.doe@university.edu
  • contributor@opensec.org
  • analyst@redteam.co
  • security@consulting.net
  • research@infosec.institute

==================================================
Scan completed for security_researcher
```

## Troubleshooting

### No Results Obtained
- Target may have no public repositories or commit history
- Email addresses may be configured as private in GitHub settings
- Increase `--max-repos` parameter or use `slow` speed profile
- Verify target username accuracy

### Rate Limiting Encountered
- Reduce request frequency using `slow` speed profile
- Disable concurrent processing with `--no-multithreaded`
- Implement delays between reconnaissance sessions
- Consider using different network egress points

### Excessive Results
- Normal behavior - tool discovers entire development ecosystem
- Focus analysis on emails appearing across multiple repositories
- Apply additional filtering based on commit frequency
- Correlate with external intelligence sources for relevance assessment

## Legal Notice

This tool is designed for legitimate security research, penetration testing, and OSINT investigations. Users must ensure compliance with applicable laws, terms of service, and ethical guidelines. The developers assume no responsibility for misuse or unauthorized activities.