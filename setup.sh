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

# Check if .env exists, if not create from .env.example
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created"
    echo ""
    echo "⚠️  IMPORTANT: You must edit .env and configure your Gmail credentials!"
    echo ""
    echo "Please set:"
    echo "  - GMAIL_EMAIL=your.email@gmail.com"
    echo "  - GMAIL_PASSWORD=your_password"
    echo ""
    echo "Authentication options:"
    echo "  - Private Gmail accounts: Use your regular Gmail password"
    echo "  - Google Workspace/2FA accounts: Use an App Password"
    echo ""
    echo "To create an App Password (if applicable):"
    echo "  1. Go to https://myaccount.google.com/apppasswords"
    echo "  2. Create a new App Password for 'Mail'"
    echo "  3. Copy the 16-character password"
    echo "  4. Use that in your .env file"
    echo ""
    read -p "Press Enter after you have configured .env..."
else
    echo "✅ .env already exists"
fi
echo ""

# Verify credentials are set
source .env 2>/dev/null || true

if [ -z "$GMAIL_EMAIL" ] || [ "$GMAIL_EMAIL" = "your.email@gmail.com" ]; then
    echo "⚠️  WARNING: GMAIL_EMAIL is not configured in .env"
    echo "Please edit .env and set your Gmail email address"
    exit 1
fi

if [ -z "$GMAIL_PASSWORD" ] || [ "$GMAIL_PASSWORD" = "your_password_here" ]; then
    echo "⚠️  WARNING: GMAIL_PASSWORD is not configured in .env"
    echo "Please edit .env and set your Gmail password"
    echo "  - Private accounts: Use your regular password"
    echo "  - Workspace/2FA accounts: Use an App Password"
    exit 1
fi

echo "✅ Gmail credentials are configured"
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
echo "Note: The first run will download Chrome and may take a few minutes."
echo "The script will log into Gmail and click 'Fetch emails now' every minute."
echo ""
