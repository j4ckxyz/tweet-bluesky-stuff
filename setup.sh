#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Setting up Bluesky Twitter Bot${NC}"
echo

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This setup script is designed for macOS. Please adapt for your system.${NC}"
    exit 1
fi

# Get current user
USER=$(whoami)
CURRENT_DIR=$(pwd)

echo -e "${BLUE}📁 Project directory: $CURRENT_DIR${NC}"
echo -e "${BLUE}👤 User: $USER${NC}"
echo

# Create virtual environment
echo -e "${YELLOW}🐍 Creating Python virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Copy example files
echo -e "${YELLOW}📄 Creating configuration files from examples...${NC}"

if [ ! -f "config.json" ]; then
    cp config.json.example config.json
    echo -e "${GREEN}✅ Created config.json${NC}"
else
    echo -e "${YELLOW}⚠️  config.json already exists, skipping${NC}"
fi

if [ ! -f "starter_packs.csv" ]; then
    cp starter_packs.csv.example starter_packs.csv
    echo -e "${GREEN}✅ Created starter_packs.csv${NC}"
else
    echo -e "${YELLOW}⚠️  starter_packs.csv already exists, skipping${NC}"
fi

if [ ! -f "feeds.csv" ]; then
    cp feeds.csv.example feeds.csv
    echo -e "${GREEN}✅ Created feeds.csv${NC}"
else
    echo -e "${YELLOW}⚠️  feeds.csv already exists, skipping${NC}"
fi

if [ ! -f "bluesky_reasons.txt" ]; then
    cp bluesky_reasons.txt.example bluesky_reasons.txt
    echo -e "${GREEN}✅ Created bluesky_reasons.txt${NC}"
else
    echo -e "${YELLOW}⚠️  bluesky_reasons.txt already exists, skipping${NC}"
fi

# Make manage.sh executable
chmod +x manage.sh

echo
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo
echo -e "${YELLOW}📋 Next steps:${NC}"
echo -e "1. ${BLUE}Get Twitter API credentials${NC} from https://developer.twitter.com/"
echo -e "2. ${BLUE}Edit config.json${NC} with your Twitter API credentials"
echo -e "3. ${BLUE}Update starter_packs.csv${NC} with your Bluesky starter packs"
echo -e "4. ${BLUE}Update feeds.csv${NC} with your Bluesky feeds"
echo -e "5. ${BLUE}Update bluesky_reasons.txt${NC} with your reasons to join Bluesky"
echo -e "6. ${BLUE}Test the bot:${NC} ./manage.sh test"
echo -e "7. ${BLUE}Start the service:${NC} ./manage.sh start"
echo
echo -e "${YELLOW}💡 Pro tip:${NC} Use './manage.sh' to see all available commands"
echo