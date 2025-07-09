#!/usr/bin/env python3
"""
Bluesky Twitter Bot

An automated Twitter bot that promotes Bluesky starter packs, custom feeds,
and reasons to join Bluesky. Posts tweets every 2 hours with smart content
rotation and character limit handling.
"""

import csv
import json
import logging
import os
import platform
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from requests_oauthlib import OAuth1Session

# Version information
__version__ = "1.0.0"
__author__ = "Your Name"

def setup_logging():
    """Setup cross-platform logging configuration"""
    
    # Determine log directory based on platform
    system = platform.system()
    
    if system == "Darwin":  # macOS
        log_dir = Path.home() / "Library" / "Logs"
    elif system == "Linux":
        log_dir = Path("/var/log")
        # Fall back to user logs if no write permission
        if not os.access(log_dir, os.W_OK):
            log_dir = Path.home() / ".local" / "share" / "logs"
    else:
        # Windows or other systems
        log_dir = Path.home() / "logs"
    
    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    log_file = log_dir / "bsky-promo-tweeter.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Log file: {log_file}")
    logger.info(f"Platform: {system} {platform.release()}")
    logger.info(f"Python: {sys.version}")
    
    return logger

# Initialize logger
logger = setup_logging()

class BlueskyTwitterBot:
    """
    Main bot class for automated Bluesky promotion on Twitter.
    
    This bot randomly selects between starter packs, feeds, and Bluesky reasons
    to create engaging tweets that promote the Bluesky platform.
    """
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the bot with configuration.
        
        Args:
            config_path (str): Path to configuration file
        """
        logger.info(f"Initializing Bluesky Twitter Bot v{__version__}")
        
        # Get the directory where the script is located
        self.script_dir = Path(__file__).parent
        
        # Load config from script directory if relative path
        if not Path(config_path).is_absolute():
            config_path = self.script_dir / config_path
            
        self.config = self.load_config(config_path)
        self.twitter = self.setup_twitter_client()
        self.starter_packs = self.load_starter_packs()
        self.feeds = self.load_feeds()
        self.bluesky_reasons = self.load_bluesky_reasons()
        
        # Log summary of loaded content
        logger.info(f"Content loaded - Starter packs: {len(self.starter_packs)}, "
                   f"Feeds: {len(self.feeds)}, Reasons: {len(self.bluesky_reasons)}")
        
    def load_config(self, config_path):
        """
        Load configuration from JSON file.
        
        Args:
            config_path (Path): Path to configuration file
            
        Returns:
            dict: Configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file has invalid JSON
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required configuration keys
            required_keys = ['twitter']
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"Missing required configuration key: {key}")
            
            # Validate Twitter configuration
            twitter_keys = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
            for key in twitter_keys:
                if key not in config['twitter']:
                    raise ValueError(f"Missing required Twitter configuration key: {key}")
            
            logger.info(f"Configuration loaded successfully from {config_path}")
            return config
            
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            logger.error("Please create config.json from config.json.example")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
            
    def setup_twitter_client(self):
        """
        Setup Twitter API v2 client with OAuth 1.0a.
        
        Returns:
            OAuth1Session: Configured Twitter API client
        """
        try:
            client = OAuth1Session(
                self.config['twitter']['consumer_key'],
                client_secret=self.config['twitter']['consumer_secret'],
                resource_owner_key=self.config['twitter']['access_token'],
                resource_owner_secret=self.config['twitter']['access_token_secret']
            )
            logger.info("Twitter API client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            raise
    
    def load_starter_packs(self):
        """
        Load starter packs from CSV file.
        
        Returns:
            list: List of starter pack dictionaries
        """
        packs = []
        csv_path = self.script_dir / self.config.get('starter_packs_csv', 'starter_packs.csv')
        
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, 1):
                    # Validate required fields
                    required_fields = ['name', 'description', 'link']
                    if not all(field in row and row[field].strip() for field in required_fields):
                        logger.warning(f"Skipping invalid starter pack at row {row_num}")
                        continue
                    
                    packs.append({
                        'name': row['name'].strip(),
                        'description': row['description'].strip(),
                        'link': row['link'].strip()
                    })
            
            logger.info(f"Loaded {len(packs)} starter packs from {csv_path}")
            return packs
            
        except FileNotFoundError:
            logger.warning(f"Starter packs CSV file not found: {csv_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading starter packs: {e}")
            return []
    
    def load_feeds(self):
        """
        Load feeds from CSV file.
        
        Returns:
            list: List of feed dictionaries
        """
        feeds = []
        csv_path = self.script_dir / self.config.get('feeds_csv', 'feeds.csv')
        
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, 1):
                    # Validate required fields
                    required_fields = ['name', 'description', 'link']
                    if not all(field in row and row[field].strip() for field in required_fields):
                        logger.warning(f"Skipping invalid feed at row {row_num}")
                        continue
                    
                    feeds.append({
                        'name': row['name'].strip(),
                        'description': row['description'].strip(),
                        'link': row['link'].strip()
                    })
            
            logger.info(f"Loaded {len(feeds)} feeds from {csv_path}")
            return feeds
            
        except FileNotFoundError:
            logger.warning(f"Feeds CSV file not found: {csv_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading feeds: {e}")
            return []
    
    def load_bluesky_reasons(self):
        """
        Load reasons to join Bluesky from text file.
        
        Returns:
            list: List of reason strings
        """
        reasons_path = self.script_dir / self.config.get('bluesky_reasons_file', 'bluesky_reasons.txt')
        
        try:
            with open(reasons_path, 'r', encoding='utf-8') as f:
                reasons = [line.strip() for line in f.readlines() if line.strip()]
            
            logger.info(f"Loaded {len(reasons)} Bluesky reasons from {reasons_path}")
            return reasons
            
        except FileNotFoundError:
            logger.warning(f"Bluesky reasons file not found: {reasons_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading Bluesky reasons: {e}")
            return []
    
    def create_starter_pack_tweet(self, pack):
        """
        Create a tweet for a starter pack.
        
        Args:
            pack (dict): Starter pack dictionary with name, description, and link
            
        Returns:
            str: Formatted tweet text
        """
        # Calculate available space for description
        base_text = f"Check out my \"{pack['name']}\" starter pack: "
        link_space = len(pack['link']) + 1  # +1 for space
        available_space = 280 - len(base_text) - link_space
        
        # Truncate description if needed
        description = pack['description']
        if len(description) > available_space:
            description = description[:available_space-3] + "..."
        
        tweet = f"{base_text}{description} {pack['link']}"
        return tweet
    
    def create_feed_tweet(self, feed):
        """
        Create a tweet for a feed.
        
        Args:
            feed (dict): Feed dictionary with name, description, and link
            
        Returns:
            str: Formatted tweet text
        """
        # Format: Feed to pin!: [name]\n[description]\nPin here:[link]
        base_text = f"Feed to pin!: {feed['name']}\n"
        footer_text = f"\nPin here:{feed['link']}"
        
        # Calculate available space for description
        fixed_length = len(base_text) + len(footer_text)
        available_space = 280 - fixed_length
        
        # Truncate description if needed
        description = feed['description']
        if len(description) > available_space:
            description = description[:available_space-3] + "..."
        
        tweet = f"{base_text}{description}{footer_text}"
        return tweet
    
    def create_bluesky_reason_tweet(self, reason):
        """
        Create a tweet with a reason to join Bluesky.
        
        Args:
            reason (str): Reason to join Bluesky
            
        Returns:
            str: Formatted tweet text
        """
        if len(reason) <= 280:
            return reason
        else:
            return reason[:277] + "..."
    
    def post_tweet(self, text):
        """
        Post a tweet using Twitter API v2.
        
        Args:
            text (str): Tweet text to post
            
        Returns:
            bool: True if successful, False otherwise
        """
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": text}
        
        try:
            response = self.twitter.post(url, json=payload)
            
            if response.status_code == 201:
                logger.info(f"Tweet posted successfully: {text[:50]}...")
                return True
            else:
                logger.error(f"Failed to post tweet: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
    
    def get_next_tweet_content(self):
        """
        Randomly choose between starter pack, feed, and Bluesky reason.
        
        Returns:
            str: Tweet content, or None if no content available
        """
        # Create a list of available content types
        content_types = []
        
        if self.starter_packs:
            content_types.append('starter_pack')
        if self.feeds:
            content_types.append('feed')
        if self.bluesky_reasons:
            content_types.append('reason')
        
        if not content_types:
            logger.warning("No content available to tweet")
            return None
        
        # Randomly select content type
        content_type = random.choice(content_types)
        
        if content_type == 'starter_pack':
            pack = random.choice(self.starter_packs)
            logger.info(f"Selected starter pack: {pack['name']}")
            return self.create_starter_pack_tweet(pack)
        elif content_type == 'feed':
            feed = random.choice(self.feeds)
            logger.info(f"Selected feed: {feed['name']}")
            return self.create_feed_tweet(feed)
        elif content_type == 'reason':
            reason = random.choice(self.bluesky_reasons)
            logger.info(f"Selected Bluesky reason: {reason[:50]}...")
            return self.create_bluesky_reason_tweet(reason)
    
    def run_once(self):
        """
        Run one iteration of the bot.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Running bot iteration...")
        
        tweet_content = self.get_next_tweet_content()
        if tweet_content:
            logger.info(f"Generated tweet ({len(tweet_content)} chars): {tweet_content[:100]}...")
            success = self.post_tweet(tweet_content)
            if success:
                logger.info("Bot iteration completed successfully")
                return True
            else:
                logger.error("Bot iteration failed - tweet not posted")
                return False
        else:
            logger.warning("No content to tweet")
            return False
    
    def run_continuous(self):
        """
        Run the bot continuously every 2 hours.
        
        This method runs indefinitely until interrupted.
        """
        logger.info("Starting continuous bot execution...")
        logger.info("Bot will tweet every 2 hours. Press Ctrl+C to stop.")
        
        while True:
            try:
                self.run_once()
                logger.info("Sleeping for 2 hours...")
                time.sleep(7200)  # 2 hours = 7200 seconds
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                logger.info("Waiting 5 minutes before retrying...")
                time.sleep(300)  # Sleep 5 minutes before retrying

def print_help():
    """Print help information"""
    print(f"Bluesky Twitter Bot v{__version__}")
    print(f"Author: {__author__}")
    print()
    print("Usage:")
    print("  python bluesky_twitter_bot.py [options]")
    print()
    print("Options:")
    print("  --once    Run the bot once and exit")
    print("  --help    Show this help message")
    print("  --version Show version information")
    print()
    print("Default behavior: Run continuously every 2 hours")

def main():
    """Main function"""
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print_help()
            return
        elif sys.argv[1] == "--version":
            print(f"Bluesky Twitter Bot v{__version__}")
            return
        elif sys.argv[1] == "--once":
            mode = "once"
        else:
            logger.error(f"Unknown argument: {sys.argv[1]}")
            print_help()
            return
    else:
        mode = "continuous"
    
    try:
        bot = BlueskyTwitterBot()
        
        if mode == "once":
            logger.info("Running bot once...")
            success = bot.run_once()
            sys.exit(0 if success else 1)
        else:
            bot.run_continuous()
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()