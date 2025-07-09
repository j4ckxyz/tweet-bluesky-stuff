# Bluesky Twitter Bot 🐦➡️🦋

An automated Twitter bot that promotes your Bluesky starter packs, custom feeds, and reasons to join Bluesky. Tweets automatically every 2 hours with smart content rotation and character‑limit handling.

---

## Features

- **Automated Posting**  
  Tweets every 2 hours via macOS Launch Agent  
- **Smart Content Rotation**  
  Randomly selects between starter packs, feeds, and Bluesky reasons  
- **Character‑Limit Handling**  
  Automatically truncates content to fit Twitter’s 280‑character limit  
- **Link Preservation**  
  Always includes important links for starter packs and feeds  
- **Auto‑start**  
  Launches automatically when you log into your Mac  
- **Comprehensive Logging**  
  Detailed logs for monitoring and troubleshooting  

---

## Tweet Formats

### 1. Starter Packs

```text
Check out my "Tech Enthusiasts" starter pack:  
Amazing developers and tech innovators you should follow  
https://bsky.app/starter-pack/tech
````

### 2. Feeds

```text
Feed to pin!: Tech News  
Latest technology news and updates from industry leaders  
Pin here: https://bsky.app/profile/did:plc:example/feed/tech-news
```

### 3. Bluesky Reasons

```text
Bluesky gives you control over your social media experience with customizable algorithms and moderation tools.
```

---

## Prerequisites

* **macOS** (tested on 12+)
* **Python** ≥ 3.7
* **Twitter Developer Account** with API v2 access
* **Bluesky account** with starter packs and/or custom feeds

---

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/bluesky-twitter-bot.git
   cd bluesky-twitter-bot
   ```
2. **Run the setup script**

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. **Get Twitter API credentials**

   * Visit the [Twitter Developer Portal](https://developer.twitter.com/)
   * Create a new app and generate API keys
   * Update `config.json` with your credentials
4. **Configure your content**

   * `starter_packs.csv` → your Bluesky starter packs
   * `feeds.csv` → your custom feeds
   * `bluesky_reasons.txt` → reasons to join Bluesky (one per line)
5. **Test the bot**

   ```bash
   ./manage.sh test
   ```
6. **Start the automated service**

   ```bash
   ./manage.sh start
   ```

---

## Configuration

### Twitter API Setup

1. Apply for a Twitter Developer account
2. Create a new app in the Twitter Developer Portal
3. Generate your API keys and access tokens
4. Update `config.json`:

   ```json
   {
     "twitter": {
       "consumer_key":        "your_consumer_key_here",
       "consumer_secret":     "your_consumer_secret_here",
       "access_token":        "your_access_token_here",
       "access_token_secret": "your_access_token_secret_here"
     }
   }
   ```

### Content Configuration

#### Starter Packs (`starter_packs.csv`)

| name               | description                               | link                                                                     |
| ------------------ | ----------------------------------------- | ------------------------------------------------------------------------ |
| Tech Enthusiasts   | Amazing developers and tech innovators    | [https://bsky.app/starter-pack/tech](https://bsky.app/starter-pack/tech) |
| Artists & Creators | Creative minds sharing incredible content | [https://bsky.app/starter-pack/art](https://bsky.app/starter-pack/art)   |

#### Custom Feeds (`feeds.csv`)

| name         | description                            | link                                                                                                                 |
| ------------ | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Tech News    | Latest technology news and updates     | [https://bsky.app/profile/did\:plc\:example/feed/tech-news](https://bsky.app/profile/did:plc:example/feed/tech-news) |
| Creative Art | Stunning artwork from talented artists | [https://bsky.app/profile/did\:plc\:example/feed/art](https://bsky.app/profile/did:plc:example/feed/art)             |

#### Bluesky Reasons (`bluesky_reasons.txt`)

```
Bluesky gives you control over your social media experience.
Join a decentralized social network where you own your data.
Experience social media without corporate manipulation.
```

---

## Usage

The bot includes a management script with the following commands:

```bash
./manage.sh start        # Start the automated service
./manage.sh stop         # Stop the service
./manage.sh restart      # Restart the service
./manage.sh status       # Check if the service is running
./manage.sh logs         # View live logs
./manage.sh errors       # View error logs
./manage.sh test         # Run the bot once for testing
./manage.sh test-feeds   # Test feed tweet generation
```

---

## Project Structure

```
bluesky-twitter-bot/
├── bluesky_twitter_bot.py       # Main bot script
├── config.json.example          # Example configuration
├── starter_packs.csv.example    # Example starter packs
├── feeds.csv.example            # Example feeds
├── bluesky_reasons.txt.example  # Example reasons
├── requirements.txt             # Python dependencies
├── manage.sh                    # Management script
├── setup.sh                     # Setup script
├── README.md                    # This file
└── .gitignore                   # Git ignore file
```

---

## How It Works

1. **Launch Agent**: Uses macOS Launch Agent to schedule tweets every 2 hours
2. **Content Selection**: Randomly chooses between starter packs, feeds, or Bluesky reasons
3. **Tweet Generation**: Formats content according to predefined templates
4. **Character Management**: Truncates descriptions while preserving links
5. **API Integration**: Posts tweets using Twitter API v2 with OAuth 1.0a

---

## Troubleshooting

### Common Issues

* **Bot not running**

  ```bash
  ./manage.sh status
  ./manage.sh logs
  ./manage.sh restart
  ```
* **Twitter API errors**

  * Verify credentials in `config.json`
  * Check API access in Twitter Developer Portal
  * Ensure you’re not hitting rate limits
* **Python environment issues**

  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Log Files

* **Bot activity:** `~/Library/Logs/bsky-promo-tweeter.log`
* **Standard output:** `~/Library/Logs/bsky-promo-tweeter-stdout.log`
* **Errors:** `~/Library/Logs/bsky-promo-tweeter-stderr.log`

---

## Contributing

1. Fork the repository
2. Create a feature branch

   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes

   ```bash
   git commit -m "Add amazing feature"
   ```
4. Push to your branch

   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Security

* **Never commit** `config.json` with real credentials
* **Keep** your Twitter API keys secure
* **The bot** runs with your user permissions only
* **Sensitive** files are included in `.gitignore`

---

## Support

1. Check the Troubleshooting section above
2. Search existing issues
3. Open a new issue with detailed information

---

## Acknowledgments

* Built for the Bluesky community
* Uses Twitter API v2 for posting
* Inspired by the need for better social media promotion tools

---

Made with ❤️ for the Bluesky community
Help grow the open social web by promoting Bluesky starter packs and feeds!
