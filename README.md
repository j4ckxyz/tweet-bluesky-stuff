# Bluesky Twitter Bot

An automated bot that promotes your Bluesky content—starter packs, custom feeds, and reasons to join—on Twitter. It tweets automatically every two hours, rotating content and handling character limits.

---

## Table of Contents

1.  [Features](#features)
2.  [Prerequisites](#prerequisites)
3.  [Quick Start](#quick-start)
4.  [Configuration](#configuration)
5.  [Usage](#usage)
6.  [How It Works](#how-it-works)
7.  [Project Structure](#project-structure)
8.  [Troubleshooting](#troubleshooting)
9.  [Contributing](#contributing)
10. [License](#license)

---

## Features

-   **Automated Tweeting**: Posts every 2 hours using `launchd` (macOS) or `systemd` (Linux).
-   **Content Rotation**: Randomly cycles through starter packs, feeds, and general reasons.
-   **Smart Truncation**: Automatically shortens text to fit Twitter's 280-character limit while preserving links.
-   **Cross-Platform**: Works on macOS and major Linux distributions.
-   **Auto-Start**: Runs automatically on system boot or user login.
-   **Detailed Logging**: Provides logs for easy monitoring and troubleshooting.

---

## Prerequisites

* **macOS** (10.15+) or **Linux** (Ubuntu 18.04+, CentOS 7+, etc.)
* **Python 3.7+**
* **Twitter Developer Account** with v2 API access.
* A **Bluesky account** to promote.

---

## Quick Start

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/bluesky-twitter-bot.git](https://github.com/yourusername/bluesky-twitter-bot.git)
    cd bluesky-twitter-bot
    ```

2.  **Run the setup script:** This creates a Python virtual environment, installs dependencies, and copies config files.
    ```bash
    ./setup.sh
    ```

3.  **Configure the bot:**
    * Add your Twitter API credentials to `config.json`.
    * Add your content to `starter_packs.csv`, `feeds.csv`, and `bluesky_reasons.txt`. (See [Configuration](#configuration) for details).

4.  **Test the bot** to post a single tweet immediately:
    ```bash
    ./manage.sh test
    ```

5.  **Start the automated service:**

    <details>
    <summary><strong>macOS</strong></summary>

    The bot runs as a Launch Agent for the current user.

    ```bash
    # Start the service (runs at login)
    ./manage.sh start

    # Check its status
    ./manage.sh status
    ```
    - **Logs**: `~/Library/Logs/bsky-promo-tweeter-*.log`
    - **Service File**: `~/Library/LaunchAgents/com.$(whoami).bsky-promo-tweeter.plist`

    </details>

    <details>
    <summary><strong>Linux</strong></summary>

    The bot runs as a system-wide `systemd` service.

    ```bash
    # Install the service file
    sudo ./manage.sh install-service

    # Start the service now
    sudo ./manage.sh start

    # Enable the service to run on system boot
    sudo ./manage.sh enable

    # Check its status
    sudo ./manage.sh status
    ```
    - **Logs**: `/var/log/bsky-promo-tweeter.log` or `journalctl -u bsky-promo-tweeter`
    - **Service File**: `/etc/systemd/system/bsky-promo-tweeter.service`

    </details>

---

## Configuration

<details>
<summary>Click to expand configuration details</summary>

### 1. Twitter API Setup

1.  Apply for a [Twitter Developer account](https://developer.twitter.com/) and create a new App.
2.  Generate your API Key & Secret and Access Token & Secret. Ensure the app has "Read & Write" permissions.
3.  Add these credentials to the `config.json` file:

    ```json
    {
      "twitter": {
        "consumer_key": "YOUR_CONSUMER_KEY",
        "consumer_secret": "YOUR_CONSUMER_SECRET",
        "access_token": "YOUR_ACCESS_TOKEN",
        "access_token_secret": "YOUR_ACCESS_SECRET"
      }
    }
    ```

### 2. Content Setup

Fill the following files with your content.

* **`starter_packs.csv`**:
    ```csv
    name,description,link
    Tech Enthusiasts,Amazing developers and tech innovators,[https://bsky.app/starter-pack/tech](https://bsky.app/starter-pack/tech)
    ```
* **`feeds.csv`**:
    ```csv
    name,description,link
    Tech News,Latest technology news and updates,[https://bsky.app/profile/did:plc:example/feed/tech](https://bsky.app/profile/did:plc:example/feed/tech)
    ```
* **`bluesky_reasons.txt`** (one reason per line):
    ```
    Bluesky gives you control over your social media experience.
    Join a decentralized social network where you own your data.
    ```

</details>

---

## Usage (`manage.sh`)

All primary actions are handled by the `./manage.sh` script.

| Command                     | macOS                | Linux                         | Description                               |
| --------------------------- | -------------------- | ----------------------------- | ----------------------------------------- |
| `test`                      | `./manage.sh test`   | `./manage.sh test`            | Posts one tweet immediately.              |
| `start`                     | `./manage.sh start`  | `sudo ./manage.sh start`      | Starts the automated 2-hour tweet service.|
| `stop`                      | `./manage.sh stop`   | `sudo ./manage.sh stop`       | Stops the service.                        |
| `restart`                   | `./manage.sh restart`| `sudo ./manage.sh restart`    | Restarts the service.                     |
| `status`                    | `./manage.sh status` | `./manage.sh status`          | Checks if the service is running.         |
| `logs`                      | `./manage.sh logs`   | `./manage.sh logs`            | Displays the latest log entries.          |
| `enable`                    | N/A                  | `sudo ./manage.sh enable`     | Enables the service to start on boot.     |
| `disable`                   | N/A                  | `sudo ./manage.sh disable`    | Disables auto-start on boot.              |
| `install-service`           | N/A                  | `sudo ./manage.sh install`    | (Re)installs the systemd service file.    |
| `help`                      | `./manage.sh help`   | `./manage.sh help`            | Shows all available commands.             |

---

## How It Works

<details>
<summary>Click to expand technical details</summary>

* **Scheduling**: `launchd` (macOS) or a `systemd` timer (Linux) triggers the main Python script every 2 hours (`7200` seconds).
* **Execution**: The `manage.sh` script is a wrapper that simplifies interaction with the respective OS service manager and the Python script.
* **Content Logic**: The `bluesky_twitter_bot.py` script randomly selects a content type (starter pack, feed, or reason), formats it into a tweet, truncates the description if necessary, and posts it via the Twitter API v2.
* **Error Handling**: The script includes basic error handling and logs API responses for troubleshooting.

</details>

---

## Troubleshooting

<details>
<summary>Click to expand troubleshooting steps</summary>

1.  **Check the logs**: The first step is always to check for errors.
    ```bash
    ./manage.sh logs
    ```
2.  **Check the service status**: Is the bot running?
    ```bash
    ./manage.sh status
    ```
3.  **Run a manual test**: This will often show API or content errors directly.
    ```bash
    ./manage.sh test
    ```
4.  **Verify API Keys**: A `401` or `403` error in the logs usually means your keys in `config.json` are incorrect or lack "Read & Write" permissions.
5.  **Python Environment**: Ensure dependencies are installed correctly by running `pip install -r requirements.txt` inside the virtual environment (`source venv/bin/activate`).

</details>


---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
