#!/bin/bash

# Gmail Puller Setup Script
# This script helps you set up the Gmail Puller for first use

set -e

echo "=================================================="
echo "   Gmail Puller - Setup Script"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✅ Docker and docker-compose are installed"
echo ""

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select an existing one"
    echo "3. Enable the Gmail API"
    echo "4. Create OAuth 2.0 credentials (Desktop app)"
    echo "5. Download the credentials file"
    echo "6. Rename it to 'credentials.json' and place it here"
    echo ""
    exit 1
fi

echo "✅ credentials.json found"
echo ""

# Check if .env exists, if not create from .env.example
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created. You can edit it to customize settings."
else
    echo "✅ .env already exists"
fi
echo ""

# Check if we need initial authentication
if [ ! -f "token.json" ]; then
    echo "⚠️  First-time authentication required"
    echo ""
    echo "To authenticate, you have two options:"
    echo ""
    echo "Option 1: Run locally first (recommended)"
    echo "  pip install -r requirements.txt"
    echo "  python gmail_puller.py"
    echo "  (Press Ctrl+C after authentication completes)"
    echo ""
    echo "Option 2: Authenticate via Docker (advanced)"
    echo "  This requires port forwarding and may be complex"
    echo ""
    read -p "Would you like to run local authentication now? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Installing Python dependencies..."
        pip install -r requirements.txt
        
        echo ""
        echo "Starting authentication process..."
        echo "A browser window will open. Please sign in and grant permissions."
        echo "Press Ctrl+C after you see 'Successfully authenticated with Gmail API'"
        echo ""
        
        python gmail_puller.py
    else
        echo ""
        echo "Skipping local authentication."
        echo "You'll need to authenticate manually before using Docker."
    fi
else
    echo "✅ token.json found - authentication already completed"
fi

echo ""
echo "=================================================="
echo "   Setup Complete!"
echo "=================================================="
echo ""
echo "To start the Gmail Puller:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop the Gmail Puller:"
echo "  docker-compose down"
echo ""
