import requests
import json
import time
import random
import sys
from typing import Dict, Optional, Tuple, List
import logging
import re
from datetime import datetime
import os
import base64
from urllib.parse import urljoin
import hmac
import hashlib

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Color Codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'  
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Gradients for banner
    GRADIENT = [
        '\033[38;5;196m',
        '\033[38;5;202m',
        '\033[38;5;208m',
        '\033[38;5;214m',
        '\033[38;5;220m',
        '\033[38;5;226m',
        '\033[38;5;190m',
        '\033[38;5;154m',
        '\033[38;5;118m',
        '\033[38;5;46m',
    ]

class GitHubTool:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://github.com"
        self.api_url = "https://api.github.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'application/vnd.github.v3+json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        self.session.headers.update(self.headers)
        self.username = None
        self.access_token = None
        self.session_start_time = datetime.now()
        self.followed_users = []
        self.starred_repos = []
        
        
        self.github_features = {
            'follow': 'Follow users',
            'unfollow': 'Unfollow users',
            'star': 'Star repositories',
            'unstar': 'Unstar repositories',
            'watch': 'Watch repositories',
            'fork': 'Fork repositories',
            'issue': 'Create issues',
            'pull': 'Create pull requests'
        }
        
        
        self.report_categories = [
            "spam",
            "inappropriate",
            "hate_speech",
            "harassment",
            "violence",
            "copyright",
            "impersonation",
            "other"
        ]
        
        self.report_reasons = [
            "Spam or unwanted commercial content",
            "Inappropriate content or nudity",
            "Hate speech or discriminatory content",
            "Harassment or bullying",
            "Violence or harmful behavior",
            "Copyright infringement",
            "Impersonation or fake account",
            "Other violations"
        ]
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\033[H\033[J', end='')
    
    def print_banner(self):
        """Print the cool ASCII banner with gradient colors"""
        self.clear_screen()
        
        banner = [
            "   _____ _ _   _    _       _               ",
            "  / ____(_) | | |  | |     | |              ",
            " | |  __ _| |_| |__| |_   _| |__    ",
            " | | |_ | | __|  __  | | | | '_ \ ",
            " | |__| | | |_| |  | | |_| | |_) |   ",
            "  \_____|_|\__|_|  |_|\__,_|_.__/ ",
            "                                              ",
            "  ____        _                           ",
            " |  _ \      | |                       ",
            " | |_) | ___ | |_             ",
            " |  _ < / _ \| __           ",
            " | |_) | (_) | |_             ",
            " |____/ \___/ \__|               "
        ]
        
        print(f"{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}")
        for i, line in enumerate(banner):
            color_index = (i % len(Colors.GRADIENT))
            color = Colors.GRADIENT[color_index]
            print(f"{color}{line}{Colors.RESET}")
        print(f"{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}             GITHUB TOOL v3.5 - Followback Cleaner     {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_YELLOW}     Developed with  ❤️ by Illusivehacks         {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}\n")
    
    def print_header(self, text: str, color: str = Colors.BRIGHT_CYAN):
        """Print a formatted header"""
        print(f"\n{color}{'═' * 60}{Colors.RESET}")
        print(f"{color}{Colors.BOLD}✨ {text} ✨{Colors.RESET}")
        print(f"{color}{'═' * 60}{Colors.RESET}\n")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.BRIGHT_GREEN}✅ {text}{Colors.RESET}")
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.BRIGHT_RED}❌ {text}{Colors.RESET}")
    
    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.BRIGHT_YELLOW}⚠️  {text}{Colors.RESET}")
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.BRIGHT_BLUE}ℹ️  {text}{Colors.RESET}")
    
    def animate_loading(self, text: str, duration: int = 2):
        """Animate a loading spinner"""
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        
        sys.stdout.write(f"{Colors.BRIGHT_BLUE}{text} ")
        sys.stdout.flush()
        
        while time.time() < end_time:
            for char in spinner:
                sys.stdout.write(f'\r{Colors.BRIGHT_BLUE}{text} {char}{Colors.RESET}')
                sys.stdout.flush()
                time.sleep(0.1)
        
        sys.stdout.write('\r' + ' ' * (len(text) + 2) + '\r')
        sys.stdout.flush()
    
    def login_with_token(self, access_token: str) -> Tuple[bool, str]:
        """Login using GitHub Personal Access Token"""
        try:
            self.print_header("GITHUB LOGIN")
            
            self.access_token = access_token
            self.session.headers.update({
                'Authorization': f'token {access_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
            
            self.animate_loading("Authenticating with GitHub API")
            
            # Test the token
            response = self.session.get(f"{self.api_url}/user")
            
            if response.status_code == 200:
                user_data = response.json()
                self.username = user_data.get('login')
                
                # Get rate limit info
                rate_response = self.session.get(f"{self.api_url}/rate_limit")
                if rate_response.status_code == 200:
                    rate_data = rate_response.json()
                    core_limit = rate_data['resources']['core']['limit']
                    remaining = rate_data['resources']['core']['remaining']
                    
                    self.print_success(f"Welcome, @{self.username}! ✨")
                    self.print_info(f"API Rate Limit: {remaining}/{core_limit} requests remaining")
                    
                    if remaining < 100:
                        self.print_warning("Low API rate limit remaining!")
                    
                    return True, f"Logged in as @{self.username}"
                else:
                    return True, f"Logged in as @{self.username} (rate limit check failed)"
            
            elif response.status_code == 401:
                return False, "Invalid access token ❌"
            elif response.status_code == 403:
                return False, "Rate limited or token permissions insufficient 🔐"
            else:
                return False, f"Login failed: HTTP {response.status_code}"
                
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def login_with_credentials(self, username: str, password: str) -> Tuple[bool, str]:
        """Login with username and password (basic auth)"""
        try:
            self.print_header("GITHUB LOGIN")
            
            self.animate_loading("Authenticating with GitHub")
            
            # Try basic auth
            self.session.auth = (username, password)
            response = self.session.get(f"{self.api_url}/user")
            
            if response.status_code == 200:
                user_data = response.json()
                self.username = user_data.get('login')
                
                # Check if 2FA is required
                if 'X-GitHub-OTP' in response.headers:
                    return False, "Two-factor authentication required 🔐"
                
                self.print_success(f"Welcome, @{self.username}! ✨")
                return True, f"Logged in as @{self.username}"
            
            elif response.status_code == 401:
                if 'X-GitHub-OTP' in response.headers:
                    return False, "Two-factor authentication required 🔐"
                return False, "Invalid credentials ❌"
            elif response.status_code == 403:
                return False, "Rate limited or account locked 🔐"
            else:
                return False, f"Login failed: HTTP {response.status_code}"
                
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def verify_user_exists(self, username: str) -> bool:
        """Verify that a GitHub user exists"""
        try:
            response = self.session.get(f"{self.api_url}/users/{username}")
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get detailed information about a GitHub user"""
        try:
            self.animate_loading(f"Fetching info for @{username}")
            
            response = self.session.get(f"{self.api_url}/users/{username}")
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Get additional statistics
                repos_response = self.session.get(user_data['repos_url'] + "?per_page=100")
                repos_data = repos_response.json() if repos_response.status_code == 200 else []
                
                # Calculate statistics
                total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
                total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
                languages = {}
                
                for repo in repos_data:
                    lang = repo.get('language')
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1
                
                # Sort languages by frequency
                top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
                
                return {
                    'username': user_data.get('login'),
                    'name': user_data.get('name'),
                    'bio': user_data.get('bio'),
                    'company': user_data.get('company'),
                    'location': user_data.get('location'),
                    'email': user_data.get('email'),
                    'blog': user_data.get('blog'),
                    'twitter': user_data.get('twitter_username'),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'public_repos': user_data.get('public_repos', 0),
                    'public_gists': user_data.get('public_gists', 0),
                    'hireable': user_data.get('hireable', False),
                    'created_at': user_data.get('created_at'),
                    'updated_at': user_data.get('updated_at'),
                    'avatar_url': user_data.get('avatar_url'),
                    'total_stars': total_stars,
                    'total_forks': total_forks,
                    'top_languages': top_languages,
                    'avg_repo_stars': total_stars / len(repos_data) if repos_data else 0
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
    
    def follow_user(self, target_username: str) -> Tuple[bool, str]:
        """Follow a user on GitHub"""
        try:
            if not self.username or not self.access_token:
                return False, "Please login with access token first!"
            
            if target_username == self.username:
                return False, "Cannot follow yourself! 🤔"
            
            self.animate_loading(f"Preparing to follow @{target_username}")
            
            # GitHub API endpoint for following users
            follow_url = f"{self.api_url}/user/following/{target_username}"
            
            # Add random delay to mimic human behavior
            time.sleep(random.uniform(1, 3))
            
            response = self.session.put(follow_url)
            
            if response.status_code == 204:
                # Success - GitHub returns 204 No Content on success
                self.followed_users.append({
                    'username': target_username,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                return True, f"Successfully followed @{target_username}! 🤝"
            
            elif response.status_code == 404:
                return False, f"User @{target_username} not found ❌"
            
            elif response.status_code == 403:
                # Check rate limits
                rate_response = self.session.get(f"{self.api_url}/rate_limit")
                if rate_response.status_code == 200:
                    rate_data = rate_response.json()
                    remaining = rate_data['resources']['core']['remaining']
                    reset_time = rate_data['resources']['core']['reset']
                    
                    if remaining == 0:
                        reset_datetime = datetime.fromtimestamp(reset_time)
                        wait_time = reset_datetime - datetime.now()
                        return False, f"Rate limited! Try again in {wait_time.seconds // 60} minutes ⏳"
                
                return False, "Forbidden - Check your token permissions 🔐"
            
            elif response.status_code == 401:
                return False, "Unauthorized - Token may have expired 🔐"
            
            else:
                return False, f"Follow failed: HTTP {response.status_code}"
                
        except Exception as e:
            logger.error(f"Follow error: {e}")
            return False, f"Follow error: {str(e)}"
    
    def unfollow_user(self, target_username: str) -> Tuple[bool, str]:
        """Unfollow a user on GitHub"""
        try:
            if not self.username or not self.access_token:
                return False, "Please login with access token first!"
            
            self.animate_loading(f"Preparing to unfollow @{target_username}")
            
            unfollow_url = f"{self.api_url}/user/following/{target_username}"
            
            time.sleep(random.uniform(1, 3))
            
            response = self.session.delete(unfollow_url)
            
            if response.status_code == 204:
                # Remove from followed users list
                self.followed_users = [user for user in self.followed_users if user['username'] != target_username]
                return True, f"Successfully unfollowed @{target_username}! 👋"
            
            elif response.status_code == 404:
                return False, f"User @{target_username} not found ❌"
            
            elif response.status_code == 403:
                return False, "Forbidden - Check your token permissions 🔐"
            
            else:
                return False, f"Unfollow failed: HTTP {response.status_code}"
                
        except Exception as e:
            logger.error(f"Unfollow error: {e}")
            return False, f"Unfollow error: {str(e)}"
    
    def star_repository(self, repo_owner: str, repo_name: str) -> Tuple[bool, str]:
        """Star a repository on GitHub"""
        try:
            if not self.username or not self.access_token:
                return False, "Please login with access token first!"
            
            self.animate_loading(f"Preparing to star {repo_owner}/{repo_name}")
            
            star_url = f"{self.api_url}/user/starred/{repo_owner}/{repo_name}"
            
            time.sleep(random.uniform(1, 3))
            
            response = self.session.put(star_url)
            
            if response.status_code == 204:
                self.starred_repos.append({
                    'owner': repo_owner,
                    'repo': repo_name,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                return True, f"Successfully starred {repo_owner}/{repo_name}! ⭐"
            
            elif response.status_code == 404:
                return False, f"Repository {repo_owner}/{repo_name} not found ❌"
            
            else:
                return False, f"Star failed: HTTP {response.status_code}"
                
        except Exception as e:
            logger.error(f"Star error: {e}")
            return False, f"Star error: {str(e)}"
    
    def fork_repository(self, repo_owner: str, repo_name: str) -> Tuple[bool, str]:
        """Fork a repository on GitHub"""
        try:
            if not self.username or not self.access_token:
                return False, "Please login with access token first!"
            
            self.animate_loading(f"Preparing to fork {repo_owner}/{repo_name}")
            
            fork_url = f"{self.api_url}/repos/{repo_owner}/{repo_name}/forks"
            
            time.sleep(random.uniform(2, 5))
            
            response = self.session.post(fork_url, json={})
            
            if response.status_code == 202:
                fork_data = response.json()
                fork_url = fork_data.get('html_url', '')
                return True, f"Successfully forked repository! 🍴\nFork URL: {fork_url}"
            
            elif response.status_code == 403:
                # Check if already forked
                check_url = f"{self.api_url}/repos/{repo_owner}/{repo_name}"
                check_response = self.session.get(check_url)
                
                if check_response.status_code == 200:
                    repo_data = check_response.json()
                    if repo_data.get('fork'):
                        return False, "Repository is already a fork"
                
                return False, "Forbidden - Check your token permissions or repository visibility 🔐"
            
            elif response.status_code == 404:
                return False, f"Repository {repo_owner}/{repo_name} not found ❌"
            
            else:
                return False, f"Fork failed: HTTP {response.status_code}"
                
        except Exception as e:
            logger.error(f"Fork error: {e}")
            return False, f"Fork error: {str(e)}"
    
    def get_repository_info(self, repo_owner: str, repo_name: str) -> Optional[Dict]:
        """Get detailed information about a repository"""
        try:
            self.animate_loading(f"Fetching info for {repo_owner}/{repo_name}")
            
            repo_url = f"{self.api_url}/repos/{repo_owner}/{repo_name}"
            response = self.session.get(repo_url)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                # Get additional data
                languages_url = repo_data.get('languages_url')
                contributors_url = repo_data.get('contributors_url')
                
                languages = {}
                if languages_url:
                    lang_response = self.session.get(languages_url)
                    if lang_response.status_code == 200:
                        languages = lang_response.json()
                
                contributors = []
                if contributors_url:
                    contrib_response = self.session.get(contributors_url + "?per_page=10")
                    if contrib_response.status_code == 200:
                        contributors = contrib_response.json()[:5]  
                
                return {
                    'name': repo_data.get('name'),
                    'full_name': repo_data.get('full_name'),
                    'owner': repo_data.get('owner', {}).get('login'),
                    'description': repo_data.get('description'),
                    'language': repo_data.get('language'),
                    'languages': languages,
                    'stars': repo_data.get('stargazers_count', 0),
                    'watchers': repo_data.get('watchers_count', 0),
                    'forks': repo_data.get('forks_count', 0),
                    'open_issues': repo_data.get('open_issues_count', 0),
                    'license': repo_data.get('license', {}).get('name'),
                    'created_at': repo_data.get('created_at'),
                    'updated_at': repo_data.get('updated_at'),
                    'pushed_at': repo_data.get('pushed_at'),
                    'homepage': repo_data.get('homepage'),
                    'topics': repo_data.get('topics', []),
                    'contributors': contributors,
                    'size': repo_data.get('size', 0),
                    'default_branch': repo_data.get('default_branch'),
                    'archived': repo_data.get('archived', False),
                    'fork': repo_data.get('fork', False)
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting repo info: {e}")
            return None
    
    # Followback 
    
    def get_all_followers(self) -> List[str]:
        """Get all followers of the logged-in user"""
        try:
            if not self.username or not self.access_token:
                self.print_error("Please login first!")
                return []
            
            self.print_info("Fetching your followers...")
            followers = []
            page = 1
            per_page = 100  # Max per page
            
            while True:
                url = f"{self.api_url}/users/{self.username}/followers?page={page}&per_page={per_page}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        break
                    
                    for user in data:
                        followers.append(user['login'])
                    
                    self.print_info(f"Loaded {len(followers)} followers so far...")
                    
                    # Check rate limit
                    rate_response = self.session.get(f"{self.api_url}/rate_limit")
                    if rate_response.status_code == 200:
                        rate_data = rate_response.json()
                        remaining = rate_data['resources']['core']['remaining']
                        if remaining < 50:
                            self.print_warning(f"Low API rate limit: {remaining} requests remaining")
                    
                    page += 1
                    
                    # Add small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                    # Safety limit: max 2000 followers
                    if len(followers) >= 2000:
                        self.print_warning("Reached safety limit of 2000 followers")
                        break
                    
                elif response.status_code == 403:
                    self.print_error("Rate limited while fetching followers")
                    break
                elif response.status_code == 404:
                    self.print_error("User not found")
                    break
                else:
                    self.print_error(f"Failed to fetch followers: HTTP {response.status_code}")
                    break
            
            return followers
            
        except Exception as e:
            self.print_error(f"Error getting followers: {str(e)}")
            return []
    
    def get_all_following(self) -> List[str]:
        """Get all users that the logged-in user is following"""
        try:
            if not self.username or not self.access_token:
                self.print_error("Please login first!")
                return []
            
            self.print_info("Fetching users you're following...")
            following = []
            page = 1
            per_page = 100  # Max per page
            
            while True:
                url = f"{self.api_url}/users/{self.username}/following?page={page}&per_page={per_page}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        break
                    
                    for user in data:
                        following.append(user['login'])
                    
                    self.print_info(f"Loaded {len(following)} following so far...")
                    
                    # Check rate limit
                    rate_response = self.session.get(f"{self.api_url}/rate_limit")
                    if rate_response.status_code == 200:
                        rate_data = rate_response.json()
                        remaining = rate_data['resources']['core']['remaining']
                        if remaining < 50:
                            self.print_warning(f"Low API rate limit: {remaining} requests remaining")
                    
                    page += 1
                    
                    # Add small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                    # Safety limit: max 2000 following
                    if len(following) >= 2000:
                        self.print_warning("Reached safety limit of 2000 following")
                        break
                    
                elif response.status_code == 403:
                    self.print_error("Rate limited while fetching following")
                    break
                elif response.status_code == 404:
                    self.print_error("User not found")
                    break
                else:
                    self.print_error(f"Failed to fetch following: HTTP {response.status_code}")
                    break
            
            return following
            
        except Exception as e:
            self.print_error(f"Error getting following: {str(e)}")
            return []
    
    def check_follow_back_status(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Check which users don't follow back
        
        Returns:
            Tuple containing:
            - List of users who follow you back (mutual followers)
            - List of users who DON'T follow you back
            - List of users who follow you but you don't follow back
        """
        try:
            self.print_header("FOLLOWBACK ANALYSIS")
            
            # Get followers and following
            self.animate_loading("Loading your followers list", 2)
            followers = self.get_all_followers()
            
            self.animate_loading("Loading users you follow", 2)
            following = self.get_all_following()
            
            if not followers or not following:
                self.print_error("Could not fetch follow data")
                return [], [], []
            
            # Convert to sets for faster operations
            followers_set = set(followers)
            following_set = set(following)
            
            # Calculate different categories
            mutual_followers = list(followers_set.intersection(following_set))
            not_following_back = list(following_set - followers_set)  # You follow them, they don't follow back
            fans = list(followers_set - following_set)  # They follow you, you don't follow back
            
            # Sort alphabetically for better display
            mutual_followers.sort()
            not_following_back.sort()
            fans.sort()
            
            return mutual_followers, not_following_back, fans
            
        except Exception as e:
            self.print_error(f"Error in followback check: {str(e)}")
            return [], [], []
    
    def display_followback_analysis(self, mutual: List[str], not_following_back: List[str], fans: List[str]):
        """Display the followback analysis in a beautiful format"""
        
        print(f"\n{Colors.BRIGHT_CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}📊 FOLLOWBACK ANALYSIS RESULTS{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'═' * 60}{Colors.RESET}")
        
        # Summary statistics
        print(f"\n{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}                    Summary Statistics                    {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_WHITE}Your Followers:{Colors.RESET} {len(mutual) + len(fans):>4}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_WHITE}You're Following:{Colors.RESET} {len(mutual) + len(not_following_back):>3}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_WHITE}Mutual Followers:{Colors.RESET} {len(mutual):>3}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_WHITE}Don't Follow Back:{Colors.RESET} {len(not_following_back):>3}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_WHITE}Fans (You don't follow back):{Colors.RESET} {len(fans):>3}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
        
        # Display users who don't follow back
        if not_following_back:
            print(f"\n{Colors.BRIGHT_RED}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_RED}{Colors.BOLD}❌ USERS WHO DON'T FOLLOW YOU BACK ({len(not_following_back)}){Colors.RESET}")
            print(f"{Colors.BRIGHT_RED}{'─' * 60}{Colors.RESET}")
            
            # Display in columns for better readability
            cols = 3
            rows = (len(not_following_back) + cols - 1) // cols
            
            for i in range(rows):
                line = ""
                for j in range(cols):
                    idx = i + j * rows
                    if idx < len(not_following_back):
                        username = not_following_back[idx]
                        line += f"{Colors.BRIGHT_YELLOW}{idx+1:3}.{Colors.RESET} {Colors.BRIGHT_RED}@{username:<20}{Colors.RESET}"
                if line:
                    print(line)
            
            # Calculate follow-back ratio
            total_following = len(mutual) + len(not_following_back)
            if total_following > 0:
                follow_back_ratio = (len(mutual) / total_following) * 100
                print(f"\n{Colors.BRIGHT_CYAN}📈 Follow-back Ratio: {follow_back_ratio:.1f}%{Colors.RESET}")
                
                if follow_back_ratio < 30:
                    self.print_warning("⚠️  Your follow-back ratio is very low!")
                elif follow_back_ratio < 50:
                    self.print_warning("⚠️  Your follow-back ratio is low.")
                elif follow_back_ratio > 70:
                    self.print_success("✅ Great follow-back ratio!")
        
        # Display mutual followers
        if mutual:
            print(f"\n{Colors.BRIGHT_GREEN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}🤝 MUTUAL FOLLOWERS ({len(mutual)}){Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}{'─' * 60}{Colors.RESET}")
            
            if len(mutual) <= 20:  # Only show if not too many
                for i, username in enumerate(mutual[:20], 1):
                    print(f"{Colors.BRIGHT_YELLOW}{i:3}.{Colors.RESET} {Colors.BRIGHT_GREEN}@{username}{Colors.RESET}")
                if len(mutual) > 20:
                    print(f"{Colors.DIM}... and {len(mutual) - 20} more mutual followers{Colors.RESET}")
        
        # Display fans (users who follow you but you don't follow back)
        if fans:
            print(f"\n{Colors.BRIGHT_BLUE}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_BLUE}{Colors.BOLD}⭐ FANS ({len(fans)}) - They follow you{Colors.RESET}")
            print(f"{Colors.BRIGHT_BLUE}{'─' * 60}{Colors.RESET}")
            
            if len(fans) <= 15:
                for i, username in enumerate(fans[:15], 1):
                    print(f"{Colors.BRIGHT_YELLOW}{i:3}.{Colors.RESET} {Colors.BRIGHT_BLUE}@{username}{Colors.RESET}")
                if len(fans) > 15:
                    print(f"{Colors.DIM}... and {len(fans) - 15} more fans{Colors.RESET}")
        
        print(f"\n{Colors.BRIGHT_CYAN}{'═' * 60}{Colors.RESET}")
    
    def bulk_unfollow_non_followers(self, usernames: List[str], delay: int = 10) -> Dict:
        """Unfollow multiple users who don't follow back"""
        results = {
            'successful': [],
            'failed': [],
            'total': len(usernames)
        }
        
        self.print_header("BULK UNFOLLOW OPERATION")
        print(f"{Colors.BRIGHT_CYAN}📋 Unfollowing {len(usernames)} users with {delay}s delay{Colors.RESET}\n")
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Warning: Use responsibly! Unfollowing too many users at once may look suspicious.{Colors.RESET}\n")
        
        for i, username in enumerate(usernames, 1):
            print(f"\n{Colors.BRIGHT_CYAN}[{i}/{len(usernames)}]{Colors.RESET} Unfollowing @{username}")
            
            success, message = self.unfollow_user(username)
            
            if success:
                self.print_success(f"Unfollowed @{username}")
                results['successful'].append({
                    'username': username,
                    'message': message
                })
            else:
                self.print_error(f"Failed to unfollow @{username}: {message}")
                results['failed'].append({
                    'username': username,
                    'message': message
                })
            
            # Add delay between unfollows (except after the last one)
            if i < len(usernames):
                print(f"{Colors.DIM}Waiting {delay} seconds before next unfollow...{Colors.RESET}")
                for sec in range(delay, 0, -1):
                    sys.stdout.write(f"\r{Colors.DIM}Next unfollow in {sec} seconds...{Colors.RESET}")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write('\r' + ' ' * 30 + '\r')
        
        return results
    
    def handle_followback_cleaner_flow(self):
        """Handle the followback checking and cleaning flow"""
        if not self.username or not self.access_token:
            self.print_error("Please login with access token first!")
            return
        
        self.print_header("FOLLOWBACK CLEANER")
        
        while True:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}✨ Followback Cleaner Options ✨{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET} {Colors.BRIGHT_WHITE}Check who doesn't follow back{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[2]{Colors.RESET} {Colors.BRIGHT_WHITE}Unfollow users who don't follow back{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[3]{Colors.RESET} {Colors.BRIGHT_WHITE}Back to main menu{Colors.RESET}")
            
            choice = self.get_input("\nSelect option (1-3)")
            
            if choice == '1':
                # Run followback analysis
                mutual, not_following_back, fans = self.check_follow_back_status()
                
                if not_following_back or mutual or fans:
                    self.display_followback_analysis(mutual, not_following_back, fans)
                    
                    if not_following_back:
                        print(f"\n{Colors.BRIGHT_YELLOW}Found {len(not_following_back)} users who don't follow you back!{Colors.RESET}")
                        print(f"{Colors.BRIGHT_WHITE}You can use option 2 to unfollow them.{Colors.RESET}")
                else:
                    self.print_error("No follow data available or error in analysis")
            
            elif choice == '2':
                # First check who doesn't follow back
                self.print_info("First, let's check who doesn't follow you back...")
                mutual, not_following_back, fans = self.check_follow_back_status()
                
                if not not_following_back:
                    self.print_success("Great! Everyone you follow follows you back! 🎉")
                    continue
                
                # Display results
                self.display_followback_analysis(mutual, not_following_back, fans)
                
                # Ask for confirmation
                print(f"\n{Colors.BRIGHT_RED}{'!' * 60}{Colors.RESET}")
                print(f"{Colors.BRIGHT_RED}{Colors.BOLD}⚠️  IMPORTANT WARNING:{Colors.RESET}")
                print(f"{Colors.BRIGHT_RED}{'!' * 60}{Colors.RESET}")
                print(f"{Colors.BRIGHT_YELLOW}• Unfollowing {len(not_following_back)} users may look suspicious{Colors.RESET}")
                print(f"{Colors.BRIGHT_YELLOW}• GitHub may temporarily limit your account{Colors.RESET}")
                print(f"{Colors.BRIGHT_YELLOW}• Recommended: Unfollow max 50 users per session{Colors.RESET}")
                print(f"{Colors.BRIGHT_YELLOW}• Add delays between unfollows to appear human{Colors.RESET}")
                
                # Ask which users to unfollow
                print(f"\n{Colors.BRIGHT_WHITE}Select unfollow option:{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET} {Colors.BRIGHT_WHITE}Unfollow ALL users who don't follow back ({len(not_following_back)} users){Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}[2]{Colors.RESET} {Colors.BRIGHT_WHITE}Unfollow first 50 users only{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}[3]{Colors.RESET} {Colors.BRIGHT_WHITE}Select specific users to unfollow{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}[4]{Colors.RESET} {Colors.BRIGHT_WHITE}Cancel and go back{Colors.RESET}")
                
                unfollow_choice = self.get_input("\nSelect option (1-4)")
                
                users_to_unfollow = []
                
                if unfollow_choice == '1':
                    users_to_unfollow = not_following_back
                elif unfollow_choice == '2':
                    users_to_unfollow = not_following_back[:50]
                elif unfollow_choice == '3':
                    # Let user select specific users
                    print(f"\n{Colors.BRIGHT_WHITE}Enter usernames to unfollow (one per line, type 'done' when finished):{Colors.RESET}")
                    print(f"{Colors.DIM}Available users: {', '.join(not_following_back[:20])}{Colors.RESET}")
                    
                    selected_users = []
                    while True:
                        username = self.get_input("Username (or 'done'): ").strip()
                        if username.lower() == 'done':
                            break
                        if username in not_following_back and username not in selected_users:
                            selected_users.append(username)
                            self.print_success(f"Added @{username} to unfollow list")
                        elif username in selected_users:
                            self.print_warning(f"@{username} is already in the list")
                        else:
                            self.print_warning(f"@{username} is not in the list of non-followers")
                    
                    users_to_unfollow = selected_users
                elif unfollow_choice == '4':
                    continue
                else:
                    self.print_error("Invalid option!")
                    continue
                
                if not users_to_unfollow:
                    self.print_warning("No users selected for unfollowing")
                    continue
                
                # Final confirmation
                print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                print(f"{Colors.BRIGHT_MAGENTA}✨ UNFOLLOW SUMMARY ✨{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                
                print(f"\n{Colors.BRIGHT_WHITE}Users to unfollow ({len(users_to_unfollow)}):{Colors.RESET}")
                for i, username in enumerate(users_to_unfollow[:10], 1):
                    print(f"  {Colors.BRIGHT_YELLOW}{i}.{Colors.RESET} @{username}")
                
                if len(users_to_unfollow) > 10:
                    print(f"  {Colors.DIM}... and {len(users_to_unfollow) - 10} more{Colors.RESET}")
                
                delay = int(self.get_input("\nDelay between unfollows (seconds, recommended 10-30): ") or "15")
                
                confirm = self.get_input(f"\nAre you SURE you want to unfollow {len(users_to_unfollow)} users? (y/N): ").lower()
                
                if confirm == 'y':
                    results = self.bulk_unfollow_non_followers(users_to_unfollow, delay)
                    
                    # Display results
                    self.print_header("UNFOLLOW RESULTS")
                    
                    print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}                    Results Summary                     {Colors.BRIGHT_GREEN}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_GREEN}✅ Successful:{Colors.RESET} {len(results['successful']):>3}/{results['total']:<45}{Colors.BRIGHT_GREEN}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_RED}❌ Failed:{Colors.RESET}     {len(results['failed']):>3}/{results['total']:<45}{Colors.BRIGHT_GREEN}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
                    
                    if results['failed']:
                        print(f"\n{Colors.BRIGHT_YELLOW}Failed users (first 5 shown):{Colors.RESET}")
                        for fail in results['failed'][:5]:
                            print(f"  {Colors.DIM}@{fail['username']}: {fail['message']}{Colors.RESET}")
                    
                    # Update follow-back ratio
                    remaining_following = results['total'] - len(results['successful'])
                    if remaining_following > 0:
                        mutual, _, _ = self.check_follow_back_status()
                        new_ratio = (len(mutual) / remaining_following) * 100 if remaining_following > 0 else 100
                        print(f"\n{Colors.BRIGHT_CYAN}📈 New follow-back ratio: {new_ratio:.1f}%{Colors.RESET}")
                else:
                    self.print_info("Unfollow operation cancelled")
            
            elif choice == '3':
                break
            
            else:
                self.print_error("Invalid option! Please choose 1-3.")
            
            input(f"\n{Colors.BRIGHT_WHITE}Press Enter to continue...{Colors.RESET}")
            self.clear_screen()
            self.print_banner()
    
    def display_user_statistics(self, user_info: Dict):
        """Display user statistics in a beautiful format"""
        if not user_info:
            self.print_error("No user information available")
            return
        
        self.print_header("GITHUB PROFILE ANALYTICS")
        
        # Profile section
        print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_MAGENTA}{Colors.BOLD}👤 PROFILE INFORMATION{Colors.RESET:<41}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
        
        username_display = f"@{user_info.get('username', 'N/A')}"
        if user_info.get('name'):
            username_display += f" • {user_info.get('name')}"
        
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}GitHub:{Colors.RESET} {Colors.BRIGHT_WHITE}{username_display:<48}{Colors.RESET}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        
        if user_info.get('company'):
            print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}Company:{Colors.RESET} {Colors.BRIGHT_YELLOW}{user_info.get('company', 'N/A'):<48}{Colors.RESET}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        
        if user_info.get('location'):
            print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}Location:{Colors.RESET} {Colors.BRIGHT_YELLOW}{user_info.get('location', 'N/A'):<48}{Colors.RESET}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
        
        # Main statistics
        print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}📊 PROFILE STATISTICS{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        followers = user_info.get('followers', 0)
        following = user_info.get('following', 0)
        repos = user_info.get('public_repos', 0)
        gists = user_info.get('public_gists', 0)
        stars = user_info.get('total_stars', 0)
        forks = user_info.get('total_forks', 0)
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}👥 Followers:{Colors.RESET} {Colors.BRIGHT_WHITE}{followers:,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}🤝 Following:{Colors.RESET} {Colors.BRIGHT_WHITE}{following:,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}📂 Public Repos:{Colors.RESET} {Colors.BRIGHT_WHITE}{repos:,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}📝 Public Gists:{Colors.RESET} {Colors.BRIGHT_WHITE}{gists:,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}⭐ Total Stars:{Colors.RESET} {Colors.BRIGHT_WHITE}{stars:,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}🍴 Total Forks:{Colors.RESET} {Colors.BRIGHT_WHITE}{forks:,}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        # Top languages
        top_languages = user_info.get('top_languages', [])
        if top_languages:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}💻 TOP PROGRAMMING LANGUAGES{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
            
            for lang, count in top_languages[:5]:
                percentage = (count / repos) * 100 if repos > 0 else 0
                bar_length = int(percentage / 5)
                bar = '█' * bar_length + '░' * (20 - bar_length)
                
                print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_CYAN}{lang:<15}{Colors.RESET} {Colors.BRIGHT_WHITE}{bar}{Colors.RESET} {Colors.BRIGHT_MAGENTA}{percentage:.1f}%{Colors.RESET}")
            
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        # Bio section
        if user_info.get('bio'):
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}📝 BIOGRAPHY{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
            
            bio = user_info['bio']
            if len(bio) > 150:
                bio = bio[:147] + "..."
            
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
            for line in self.wrap_text(bio, 38):
                print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_CYAN}{line:<35}{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        # Links section
        print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}🔗 ADDITIONAL INFORMATION{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
        
        info_count = 0
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        if user_info.get('blog'):
            blog = user_info['blog']
            if len(blog) > 35:
                blog = blog[:32] + "..."
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Website:{Colors.RESET} {Colors.BRIGHT_CYAN}{blog:<35}{Colors.RESET}")
            info_count += 1
        
        if user_info.get('twitter'):
            twitter = f"@{user_info['twitter']}"
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Twitter:{Colors.RESET} {Colors.BRIGHT_CYAN}{twitter:<35}{Colors.RESET}")
            info_count += 1
        
        if user_info.get('email'):
            email = user_info['email']
            if len(email) > 35:
                email = email[:32] + "..."
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Email:{Colors.RESET} {Colors.BRIGHT_CYAN}{email:<35}{Colors.RESET}")
            info_count += 1
        
        if user_info.get('hireable'):
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Hireable:{Colors.RESET} {Colors.BRIGHT_GREEN}Yes{Colors.RESET}")
            info_count += 1
        
        if user_info.get('created_at'):
            created = datetime.strptime(user_info['created_at'][:10], "%Y-%m-%d")
            account_age = (datetime.now() - created).days
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Account Age:{Colors.RESET} {Colors.BRIGHT_CYAN}{account_age:,} days{Colors.RESET}")
            info_count += 1
        
        if info_count == 0:
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.DIM}No additional information available{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
    
    def display_repository_statistics(self, repo_info: Dict):
        """Display repository statistics in a beautiful format"""
        if not repo_info:
            self.print_error("No repository information available")
            return
        
        self.print_header("REPOSITORY ANALYTICS")
        
        # Repo info section
        print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_MAGENTA}{Colors.BOLD}📦 REPOSITORY INFORMATION{Colors.RESET:<39}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
        
        repo_display = f"{repo_info.get('owner', 'N/A')}/{repo_info.get('name', 'N/A')}"
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}Repository:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_display:<48}{Colors.RESET}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        
        if repo_info.get('description'):
            desc = repo_info['description']
            if len(desc) > 50:
                desc = desc[:47] + "..."
            print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}Description:{Colors.RESET} {Colors.BRIGHT_YELLOW}{desc:<48}{Colors.RESET}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
        
        # Main statistics
        print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}📊 REPOSITORY STATISTICS{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}⭐ Stars:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_info.get('stars', 0):,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}👁️ Watchers:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_info.get('watchers', 0):,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}🍴 Forks:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_info.get('forks', 0):,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}📂 Open Issues:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_info.get('open_issues', 0):,}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}💾 Size:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_info.get('size', 0):,} KB{Colors.RESET}")
        
        if repo_info.get('language'):
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}💻 Main Language:{Colors.RESET} {Colors.BRIGHT_CYAN}{repo_info['language']}{Colors.RESET}")
        
        if repo_info.get('license'):
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}📜 License:{Colors.RESET} {Colors.BRIGHT_WHITE}{repo_info['license']}{Colors.RESET}")
        
        if repo_info.get('fork'):
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}🍴 Type:{Colors.RESET} {Colors.BRIGHT_YELLOW}Forked Repository{Colors.RESET}")
        
        if repo_info.get('archived'):
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_MAGENTA}📦 Status:{Colors.RESET} {Colors.BRIGHT_RED}Archived{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        # Languages breakdown
        languages = repo_info.get('languages', {})
        if languages:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}💻 LANGUAGE DISTRIBUTION{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
            
            total_bytes = sum(languages.values())
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
            
            for lang, bytes_count in list(languages.items())[:5]:
                percentage = (bytes_count / total_bytes) * 100
                bar_length = int(percentage / 5)
                bar = '█' * bar_length + '░' * (20 - bar_length)
                
                print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_CYAN}{lang:<15}{Colors.RESET} {Colors.BRIGHT_WHITE}{bar}{Colors.RESET} {Colors.BRIGHT_MAGENTA}{percentage:.1f}%{Colors.RESET}")
            
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        # Topics
        topics = repo_info.get('topics', [])
        if topics:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}🏷️  TOPICS{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
            topics_display = ", ".join(topics[:8])
            if len(topics) > 8:
                topics_display += f" (+{len(topics) - 8} more)"
            
            for line in self.wrap_text(topics_display, 38):
                print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_CYAN}{line:<35}{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        # Dates
        print(f"\n{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}📅 TIMELINE{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
        
        if repo_info.get('created_at'):
            created = datetime.strptime(repo_info['created_at'][:10], "%Y-%m-%d")
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Created:{Colors.RESET} {Colors.DIM}{created.strftime('%Y-%m-%d')}{Colors.RESET}")
        
        if repo_info.get('updated_at'):
            updated = datetime.strptime(repo_info['updated_at'][:10], "%Y-%m-%d")
            days_ago = (datetime.now() - updated).days
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Updated:{Colors.RESET} {Colors.DIM}{updated.strftime('%Y-%m-%d')} ({days_ago} days ago){Colors.RESET}")
        
        if repo_info.get('pushed_at'):
            pushed = datetime.strptime(repo_info['pushed_at'][:10], "%Y-%m-%d")
            days_since_push = (datetime.now() - pushed).days
            print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_YELLOW}[+]{Colors.RESET} {Colors.BRIGHT_WHITE}Last Push:{Colors.RESET} {Colors.DIM}{pushed.strftime('%Y-%m-%d')} ({days_since_push} days ago){Colors.RESET}")
        
        print(f"{Colors.BRIGHT_GREEN}{' ' * 10}{Colors.BRIGHT_WHITE}{'─' * 40}{Colors.RESET}")
    
    def wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + len(current_line) <= width:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def bulk_follow_users(self, usernames: List[str], delay: int = 10) -> Dict:
        """Follow multiple users with delay between each follow"""
        results = {
            'successful': [],
            'failed': [],
            'total': len(usernames)
        }
        
        self.print_header("BULK FOLLOW OPERATION")
        print(f"{Colors.BRIGHT_CYAN}📋 Following {len(usernames)} users with {delay}s delay{Colors.RESET}\n")
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Warning: GitHub has strict rate limits! Use responsibly.{Colors.RESET}\n")
        
        for i, username in enumerate(usernames, 1):
            print(f"\n{Colors.BRIGHT_CYAN}[{i}/{len(usernames)}]{Colors.RESET} Processing @{username}")
            
            success, message = self.follow_user(username)
            
            if success:
                self.print_success(f"Followed @{username}")
                results['successful'].append({
                    'username': username,
                    'message': message
                })
            else:
                self.print_error(f"Failed to follow @{username}: {message}")
                results['failed'].append({
                    'username': username,
                    'message': message
                })
            
            # Add delay between follows (except after the last one)
            if i < len(usernames):
                print(f"{Colors.DIM}Waiting {delay} seconds before next follow...{Colors.RESET}")
                for sec in range(delay, 0, -1):
                    sys.stdout.write(f"\r{Colors.DIM}Next follow in {sec} seconds...{Colors.RESET}")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write('\r' + ' ' * 30 + '\r')
        
        return results
    
    def bulk_star_repos(self, repos: List[Tuple[str, str]], delay: int = 15) -> Dict:
        """Star multiple repositories with delay between each"""
        results = {
            'successful': [],
            'failed': [],
            'total': len(repos)
        }
        
        self.print_header("BULK STAR OPERATION")
        print(f"{Colors.BRIGHT_CYAN}📋 Starring {len(repos)} repositories with {delay}s delay{Colors.RESET}\n")
        
        for i, (owner, repo) in enumerate(repos, 1):
            print(f"\n{Colors.BRIGHT_CYAN}[{i}/{len(repos)}]{Colors.RESET} Processing {owner}/{repo}")
            
            success, message = self.star_repository(owner, repo)
            
            if success:
                self.print_success(f"Starred {owner}/{repo}")
                results['successful'].append({
                    'owner': owner,
                    'repo': repo,
                    'message': message
                })
            else:
                self.print_error(f"Failed to star {owner}/{repo}: {message}")
                results['failed'].append({
                    'owner': owner,
                    'repo': repo,
                    'message': message
                })
            
            if i < len(repos):
                print(f"{Colors.DIM}Waiting {delay} seconds before next star...{Colors.RESET}")
                for sec in range(delay, 0, -1):
                    sys.stdout.write(f"\r{Colors.DIM}Next star in {sec} seconds...{Colors.RESET}")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write('\r' + ' ' * 30 + '\r')
        
        return results
    
    def get_input(self, prompt: str, color: str = Colors.BRIGHT_CYAN, password: bool = False) -> str:
        """Get user input with styling"""
        if password:
            import getpass
            user_input = getpass.getpass(f"{color}{prompt}{Colors.BRIGHT_YELLOW}➜ {Colors.RESET}")
        else:
            user_input = input(f"{color}{prompt}{Colors.BRIGHT_YELLOW}➜ {Colors.RESET}").strip()
        return user_input
    
    def handle_login_flow(self):
        """Handle the login flow"""
        print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}✨ GitHub Login Options ✨{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
        
        print(f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET} {Colors.BRIGHT_WHITE}Login with Personal Access Token (Recommended){Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}[2]{Colors.RESET} {Colors.BRIGHT_WHITE}Login with Username/Password{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}[3]{Colors.RESET} {Colors.BRIGHT_WHITE}Back to main menu{Colors.RESET}")
        
        choice = self.get_input("\nSelect option (1-3)")
        
        if choice == '1':
            self.print_info("Get your token from: https://github.com/settings/tokens")
            self.print_info("Required scopes: user, public_repo")
            
            token = self.get_input("Personal Access Token: ", Colors.BRIGHT_RED, password=True)
            
            if token:
                success, message = self.login_with_token(token)
                if success:
                    self.print_success(message)
                else:
                    self.print_error(message)
        
        elif choice == '2':
            username = self.get_input("GitHub Username: ")
            password = self.get_input("Password: ", Colors.BRIGHT_RED, password=True)
            
            if username and password:
                success, message = self.login_with_credentials(username, password)
                if success:
                    self.print_success(message)
                else:
                    self.print_error(message)
        
        elif choice == '3':
            return
        
        else:
            self.print_error("Invalid option! Please choose 1-3.")
    
    def handle_follow_flow(self):
        """Handle the follow user flow"""
        if not self.username or not self.access_token:
            self.print_error("Please login with access token first!")
            return
        
        self.print_header("FOLLOW MANAGEMENT")
        
        while True:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}✨ Follow Options ✨{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET} {Colors.BRIGHT_WHITE}Follow a single user{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[2]{Colors.RESET} {Colors.BRIGHT_WHITE}Follow multiple users{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[3]{Colors.RESET} {Colors.BRIGHT_WHITE}Unfollow a user{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[4]{Colors.RESET} {Colors.BRIGHT_WHITE}Show followed users{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[5]{Colors.RESET} {Colors.BRIGHT_WHITE}Back to main menu{Colors.RESET}")
            
            choice = self.get_input("\nSelect option (1-5)")
            
            if choice == '1':
                target_username = self.get_input("Enter username to follow (without @)")
                if target_username:
                    success, message = self.follow_user(target_username)
                    if success:
                        self.print_success(message)
                    else:
                        self.print_error(message)
            
            elif choice == '2':
                print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                print(f"{Colors.BRIGHT_MAGENTA}✨ Enter Usernames to Follow ✨{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                print(f"{Colors.DIM}• Enter one username per line (without @)")
                print(f"• Type 'done' when finished")
                print(f"• Type 'clear' to clear the list")
                print(f"• Type 'list' to see current usernames{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
                
                usernames = []
                count = 1
                
                while True:
                    user_input = self.get_input(f"Username {count} (or 'done' when finished): ").strip()
                    
                    if user_input.lower() == 'done':
                        if not usernames:
                            self.print_warning("No usernames entered!")
                            continue
                        break
                    elif user_input.lower() == 'clear':
                        usernames = []
                        count = 1
                        self.print_success("List cleared!")
                        continue
                    elif user_input.lower() == 'list':
                        if not usernames:
                            self.print_info("No usernames added yet.")
                        else:
                            print(f"\n{Colors.BRIGHT_GREEN}Current usernames ({len(usernames)}):{Colors.RESET}")
                            for i, uname in enumerate(usernames, 1):
                                print(f"  {Colors.BRIGHT_YELLOW}{i}.{Colors.RESET} @{uname}")
                        continue
                    elif not user_input:
                        self.print_warning("Username cannot be empty!")
                        continue
                    elif user_input in usernames:
                        self.print_warning(f"@{user_input} is already in the list!")
                        continue
                    elif not self.verify_user_exists(user_input):
                        self.print_warning(f"@{user_input} doesn't seem to exist!")
                        continue
                    else:
                        usernames.append(user_input)
                        self.print_success(f"Added @{user_input} to list")
                        count += 1
                
                if usernames:
                    delay = int(self.get_input("Delay between follows (seconds, recommended 10-30): ") or "15")
                    
                    print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_MAGENTA}✨ Follow Summary ✨{Colors.RESET}")
                    print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                    
                    print(f"\n{Colors.BRIGHT_WHITE}Usernames to follow:{Colors.RESET}")
                    for i, uname in enumerate(usernames, 1):
                        print(f"  {Colors.BRIGHT_YELLOW}{i}.{Colors.RESET} @{uname}")
                    
                    print(f"\n{Colors.BRIGHT_WHITE}Total: {len(usernames)} users{Colors.RESET}")
                    print(f"{Colors.BRIGHT_WHITE}Delay: {delay} seconds between follows{Colors.RESET}")
                    
                    confirm = self.get_input(f"\nStart following {len(usernames)} users? (y/n): ").lower()
                    if confirm == 'y':
                        results = self.bulk_follow_users(usernames, delay)
                        
                        self.print_header("BULK FOLLOW RESULTS")
                        print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}                    Results Summary                     {Colors.BRIGHT_GREEN}{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_GREEN}✅ Successful:{Colors.RESET} {len(results['successful']):>3}/{results['total']:<45}{Colors.BRIGHT_GREEN}{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_RED}❌ Failed:{Colors.RESET}     {len(results['failed']):>3}/{results['total']:<45}{Colors.BRIGHT_GREEN}{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
            
            elif choice == '3':
                target_username = self.get_input("Enter username to unfollow (without @)")
                if target_username:
                    confirm = self.get_input(f"Unfollow @{target_username}? (y/n): ").lower()
                    if confirm == 'y':
                        success, message = self.unfollow_user(target_username)
                        if success:
                            self.print_success(message)
                        else:
                            self.print_error(message)
            
            elif choice == '4':
                if self.followed_users:
                    print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_MAGENTA}✨ Followed Users This Session ✨{Colors.RESET}")
                    print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
                    
                    for i, user in enumerate(self.followed_users, 1):
                        print(f"  {Colors.BRIGHT_YELLOW}{i}.{Colors.RESET} @{user['username']} - {Colors.DIM}{user['timestamp']}{Colors.RESET}")
                    
                    print(f"\n{Colors.BRIGHT_WHITE}Total: {len(self.followed_users)} users{Colors.RESET}")
                else:
                    self.print_info("No users followed in this session yet.")
            
            elif choice == '5':
                break
            
            else:
                self.print_error("Invalid option! Please choose 1-5.")
            
            input(f"\n{Colors.BRIGHT_WHITE}Press Enter to continue...{Colors.RESET}")
            self.clear_screen()
            self.print_banner()
    
    def handle_repo_flow(self):
        """Handle repository operations"""
        if not self.username or not self.access_token:
            self.print_error("Please login with access token first!")
            return
        
        self.print_header("REPOSITORY OPERATIONS")
        
        while True:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}✨ Repository Options ✨{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET} {Colors.BRIGHT_WHITE}Get repository information{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[2]{Colors.RESET} {Colors.BRIGHT_WHITE}Star a repository{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[3]{Colors.RESET} {Colors.BRIGHT_WHITE}Star multiple repositories{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[4]{Colors.RESET} {Colors.BRIGHT_WHITE}Fork a repository{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[5]{Colors.RESET} {Colors.BRIGHT_WHITE}Back to main menu{Colors.RESET}")
            
            choice = self.get_input("\nSelect option (1-5)")
            
            if choice == '1':
                repo_input = self.get_input("Enter repository (owner/repo): ")
                if '/' in repo_input:
                    owner, repo_name = repo_input.split('/', 1)
                    repo_info = self.get_repository_info(owner.strip(), repo_name.strip())
                    
                    if repo_info:
                        self.display_repository_statistics(repo_info)
                    else:
                        self.print_error("Failed to get repository information")
                else:
                    self.print_error("Please use format: owner/repository")
            
            elif choice == '2':
                repo_input = self.get_input("Enter repository to star (owner/repo): ")
                if '/' in repo_input:
                    owner, repo_name = repo_input.split('/', 1)
                    success, message = self.star_repository(owner.strip(), repo_name.strip())
                    if success:
                        self.print_success(message)
                    else:
                        self.print_error(message)
                else:
                    self.print_error("Please use format: owner/repository")
            
            elif choice == '3':
                print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                print(f"{Colors.BRIGHT_MAGENTA}✨ Enter Repositories to Star ✨{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                print(f"{Colors.DIM}• Enter one repository per line (owner/repo)")
                print(f"• Type 'done' when finished")
                print(f"• Type 'clear' to clear the list")
                print(f"• Type 'list' to see current repositories{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
                
                repos = []
                count = 1
                
                while True:
                    user_input = self.get_input(f"Repository {count} (or 'done' when finished): ").strip()
                    
                    if user_input.lower() == 'done':
                        if not repos:
                            self.print_warning("No repositories entered!")
                            continue
                        break
                    elif user_input.lower() == 'clear':
                        repos = []
                        count = 1
                        self.print_success("List cleared!")
                        continue
                    elif user_input.lower() == 'list':
                        if not repos:
                            self.print_info("No repositories added yet.")
                        else:
                            print(f"\n{Colors.BRIGHT_GREEN}Current repositories ({len(repos)}):{Colors.RESET}")
                            for i, (owner, repo) in enumerate(repos, 1):
                                print(f"  {Colors.BRIGHT_YELLOW}{i}.{Colors.RESET} {owner}/{repo}")
                        continue
                    elif not user_input:
                        self.print_warning("Repository cannot be empty!")
                        continue
                    elif '/' not in user_input:
                        self.print_warning("Please use format: owner/repository")
                        continue
                    else:
                        owner, repo_name = user_input.split('/', 1)
                        if (owner.strip(), repo_name.strip()) in repos:
                            self.print_warning(f"{owner}/{repo_name} is already in the list!")
                        else:
                            repos.append((owner.strip(), repo_name.strip()))
                            self.print_success(f"Added {owner}/{repo_name} to list")
                            count += 1
                
                if repos:
                    delay = int(self.get_input("Delay between stars (seconds, recommended 15-30): ") or "20")
                    
                    print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_MAGENTA}✨ Star Summary ✨{Colors.RESET}")
                    print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
                    
                    print(f"\n{Colors.BRIGHT_WHITE}Repositories to star:{Colors.RESET}")
                    for i, (owner, repo) in enumerate(repos, 1):
                        print(f"  {Colors.BRIGHT_YELLOW}{i}.{Colors.RESET} {owner}/{repo}")
                    
                    print(f"\n{Colors.BRIGHT_WHITE}Total: {len(repos)} repositories{Colors.RESET}")
                    print(f"{Colors.BRIGHT_WHITE}Delay: {delay} seconds between stars{Colors.RESET}")
                    
                    confirm = self.get_input(f"\nStart starring {len(repos)} repositories? (y/n): ").lower()
                    if confirm == 'y':
                        results = self.bulk_star_repos(repos, delay)
                        
                        self.print_header("BULK STAR RESULTS")
                        print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}                    Results Summary                     {Colors.BRIGHT_GREEN}{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_GREEN}✅ Successful:{Colors.RESET} {len(results['successful']):>3}/{results['total']:<45}{Colors.BRIGHT_GREEN}{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_RED}❌ Failed:{Colors.RESET}     {len(results['failed']):>3}/{results['total']:<45}{Colors.BRIGHT_GREEN}{Colors.RESET}")
                        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
            
            elif choice == '4':
                repo_input = self.get_input("Enter repository to fork (owner/repo): ")
                if '/' in repo_input:
                    owner, repo_name = repo_input.split('/', 1)
                    success, message = self.fork_repository(owner.strip(), repo_name.strip())
                    if success:
                        self.print_success(message)
                    else:
                        self.print_error(message)
                else:
                    self.print_error("Please use format: owner/repository")
            
            elif choice == '5':
                break
            
            else:
                self.print_error("Invalid option! Please choose 1-5.")
            
            input(f"\n{Colors.BRIGHT_WHITE}Press Enter to continue...{Colors.RESET}")
            self.clear_screen()
            self.print_banner()
    
    def handle_user_analysis_flow(self):
        """Handle user analysis flow"""
        self.print_header("USER ANALYSIS")
        
        while True:
            print(f"\n{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}✨ User Analysis Options ✨{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET} {Colors.BRIGHT_WHITE}Analyze your own account{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[2]{Colors.RESET} {Colors.BRIGHT_WHITE}Analyze another user{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}[3]{Colors.RESET} {Colors.BRIGHT_WHITE}Back to main menu{Colors.RESET}")
            
            choice = self.get_input("\nSelect option (1-3)")
            
            if choice == '1':
                if self.username:
                    user_info = self.get_user_info(self.username)
                    if user_info:
                        self.display_user_statistics(user_info)
                    else:
                        self.print_error("Failed to get your user information")
                else:
                    self.print_error("Please login first!")
            
            elif choice == '2':
                target_username = self.get_input("Enter username to analyze (without @): ")
                if target_username:
                    if self.verify_user_exists(target_username):
                        user_info = self.get_user_info(target_username)
                        if user_info:
                            self.display_user_statistics(user_info)
                        else:
                            self.print_error("Failed to get user information")
                    else:
                        self.print_error(f"User @{target_username} not found")
            
            elif choice == '3':
                break
            
            else:
                self.print_error("Invalid option! Please choose 1-3.")
            
            input(f"\n{Colors.BRIGHT_WHITE}Press Enter to continue...{Colors.RESET}")
            self.clear_screen()
            self.print_banner()
    
    def print_menu(self):
        """Print the main menu"""
        self.print_header("GITHUB TOOL - MAIN MENU")
        
        logged_in_status = f"{Colors.BRIGHT_GREEN}✅ @{self.username}{Colors.RESET}" if self.username else f"{Colors.BRIGHT_RED}❌ Not logged in{Colors.RESET}"
        token_status = f"{Colors.BRIGHT_GREEN}✅ Token active{Colors.RESET}" if self.access_token else f"{Colors.BRIGHT_RED}❌ No token{Colors.RESET}"
        
        print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}                     Available Options                      {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}1.{Colors.RESET} {Colors.BRIGHT_WHITE}Login to GitHub Account{Colors.RESET}                          {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}2.{Colors.RESET} {Colors.BRIGHT_WHITE}User Profile Analysis{Colors.RESET}                           {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}3.{Colors.RESET} {Colors.BRIGHT_WHITE}Follow/Unfollow Users{Colors.RESET}                          {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}4.{Colors.RESET} {Colors.BRIGHT_WHITE}Repository Operations{Colors.RESET}                          {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}5.{Colors.RESET} {Colors.BRIGHT_WHITE}Followback Checker & Cleaner{Colors.RESET}                  {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}6.{Colors.RESET} {Colors.BRIGHT_WHITE}Check Rate Limits{Colors.RESET}                              {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}7.{Colors.RESET} {Colors.BRIGHT_WHITE}Exit Tool{Colors.RESET}                                      {Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}Status:{Colors.RESET} {logged_in_status:<48}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}Token:{Colors.RESET}  {token_status:<48}{Colors.BRIGHT_GREEN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}\n")
    
    def check_rate_limits(self):
        """Check GitHub API rate limits"""
        try:
            self.print_header("API RATE LIMITS")
            
            response = self.session.get(f"{self.api_url}/rate_limit")
            
            if response.status_code == 200:
                rate_data = response.json()
                core = rate_data['resources']['core']
                search = rate_data['resources']['search']
                graphql = rate_data['resources']['graphql'] if 'graphql' in rate_data['resources'] else None
                
                print(f"{Colors.BRIGHT_GREEN}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}                    Rate Limit Status                    {Colors.BRIGHT_GREEN}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
                
                # Core API limits
                remaining_core = core['remaining']
                limit_core = core['limit']
                reset_core = datetime.fromtimestamp(core['reset']).strftime('%Y-%m-%d %H:%M:%S')
                used_percentage = (limit_core - remaining_core) / limit_core * 100
                
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}📊 Core API:{Colors.RESET}                                            {Colors.BRIGHT_GREEN}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}   {Colors.BRIGHT_WHITE}Remaining:{Colors.RESET} {remaining_core}/{limit_core} ({used_percentage:.1f}% used)    {Colors.BRIGHT_GREEN}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}   {Colors.BRIGHT_WHITE}Resets at:{Colors.RESET} {reset_core}             {Colors.BRIGHT_GREEN}{Colors.RESET}")
                
                # Search API limits
                remaining_search = search['remaining']
                limit_search = search['limit']
                reset_search = datetime.fromtimestamp(search['reset']).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}                                                          {Colors.BRIGHT_GREEN}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}🔍 Search API:{Colors.RESET}                                        {Colors.BRIGHT_GREEN}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}   {Colors.BRIGHT_WHITE}Remaining:{Colors.RESET} {remaining_search}/{limit_search}                  {Colors.BRIGHT_GREEN}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}   {Colors.BRIGHT_WHITE}Resets at:{Colors.RESET} {reset_search}             {Colors.BRIGHT_GREEN}{Colors.RESET}")
                
                # GraphQL API limits if available
                if graphql:
                    remaining_graphql = graphql['remaining']
                    limit_graphql = graphql['limit']
                    reset_graphql = datetime.fromtimestamp(graphql['reset']).strftime('%Y-%m-%d %H:%M:%S')
                    
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}                                                          {Colors.BRIGHT_GREEN}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET} {Colors.BRIGHT_CYAN}📈 GraphQL API:{Colors.RESET}                                     {Colors.BRIGHT_GREEN}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}   {Colors.BRIGHT_WHITE}Remaining:{Colors.RESET} {remaining_graphql}/{limit_graphql}                {Colors.BRIGHT_GREEN}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_GREEN}│{Colors.RESET}   {Colors.BRIGHT_WHITE}Resets at:{Colors.RESET} {reset_graphql}             {Colors.BRIGHT_GREEN}{Colors.RESET}")
                
                print(f"{Colors.BRIGHT_GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
                
                # Warning if limits are low
                if remaining_core < 100:
                    self.print_warning("⚠️  Core API limit is low! Consider waiting before making more requests.")
                if remaining_search < 10:
                    self.print_warning("⚠️  Search API limit is very low!")
                
            else:
                self.print_error("Failed to get rate limit information")
                
        except Exception as e:
            self.print_error(f"Error checking rate limits: {e}")
    
    def run(self):
        """Main execution flow"""
        self.clear_screen()
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = self.get_input("Select an option (1-7)")
            
            if choice == '1':
                self.clear_screen()
                self.print_banner()
                self.handle_login_flow()
            elif choice == '2':
                self.clear_screen()
                self.print_banner()
                self.handle_user_analysis_flow()
            elif choice == '3':
                self.clear_screen()
                self.print_banner()
                self.handle_follow_flow()
            elif choice == '4':
                self.clear_screen()
                self.print_banner()
                self.handle_repo_flow()
            elif choice == '5':
                self.clear_screen()
                self.print_banner()
                self.handle_followback_cleaner_flow()
            elif choice == '6':
                self.clear_screen()
                self.print_banner()
                self.check_rate_limits()
            elif choice == '7':
                self.clear_screen()
                self.print_banner()
                
                # Show session summary
                if self.followed_users or self.starred_repos:
                    print(f"\n{Colors.BRIGHT_CYAN}{'═' * 60}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}✨ Session Summary ✨{Colors.RESET}")
                    print(f"{Colors.BRIGHT_CYAN}{'═' * 60}{Colors.RESET}\n")
                    
                    if self.followed_users:
                        print(f"{Colors.BRIGHT_GREEN}📊 Total users followed this session: {len(self.followed_users)}{Colors.RESET}")
                    
                    if self.starred_repos:
                        print(f"{Colors.BRIGHT_BLUE}⭐ Total repositories starred this session: {len(self.starred_repos)}{Colors.RESET}")
                
                self.print_success("Thank you for using GitHub Tool! 👋")
                print(f"\n{Colors.DIM}Session duration: {(datetime.now() - self.session_start_time).seconds} seconds{Colors.RESET}\n")
                break
            else:
                self.print_error("Invalid option! Please choose 1-7.")
            
            input(f"\n{Colors.BRIGHT_WHITE}Press Enter to continue...{Colors.RESET}")
            self.clear_screen()
            self.print_banner()

def main():
    """Main function"""
    try:
        tool = GitHubTool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_YELLOW}👋 Goodbye! Thanks for using GitHub Tool!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}💥 An unexpected error occurred: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()