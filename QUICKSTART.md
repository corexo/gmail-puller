# Gmail Puller - Schnellstart / Quick Start

## 🚀 Schnellstart (Deutsch)

### Voraussetzungen
- Docker & Docker Compose installiert
- Google-Konto

### In 5 Schritten zum Ziel:

1. **Projekt klonen**
   ```bash
   git clone https://github.com/corexo/gmail-puller.git
   cd gmail-puller
   ```

2. **Google Credentials erstellen**
   - Gehe zu: https://console.cloud.google.com/
   - Erstelle ein Projekt und aktiviere Gmail API
   - Erstelle OAuth 2.0 Credentials (Desktop App)
   - Lade `credentials.json` herunter und lege sie im Projektverzeichnis ab

3. **Konfiguration**
   ```bash
   cp .env.example .env
   # Optional: .env bearbeiten, um Einstellungen anzupassen
   ```

4. **Erste Authentifizierung**
   ```bash
   # Setup-Skript ausführen (hilft bei der ersten Einrichtung)
   ./setup.sh
   
   # ODER manuell:
   pip install -r requirements.txt
   python gmail_puller.py
   # Nach erfolgreicher Authentifizierung: Ctrl+C drücken
   ```

5. **Mit Docker starten**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

**Fertig!** 🎉 Der Gmail Puller läuft jetzt und prüft jede Minute auf neue E-Mails.

---

## 🚀 Quick Start (English)

### Prerequisites
- Docker & Docker Compose installed
- Google Account

### 5 Steps to Success:

1. **Clone the project**
   ```bash
   git clone https://github.com/corexo/gmail-puller.git
   cd gmail-puller
   ```

2. **Create Google Credentials**
   - Go to: https://console.cloud.google.com/
   - Create a project and enable Gmail API
   - Create OAuth 2.0 Credentials (Desktop App)
   - Download `credentials.json` and place it in the project directory

3. **Configuration**
   ```bash
   cp .env.example .env
   # Optional: Edit .env to customize settings
   ```

4. **Initial Authentication**
   ```bash
   # Run setup script (helps with first-time setup)
   ./setup.sh
   
   # OR manually:
   pip install -r requirements.txt
   python gmail_puller.py
   # After successful authentication: Press Ctrl+C
   ```

5. **Start with Docker**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

**Done!** 🎉 Gmail Puller is now running and checking for new emails every minute.

---

## 📝 Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop the service
docker-compose down

# Restart the service
docker-compose restart

# Rebuild after changes
docker-compose up -d --build
```

## ⚙️ Configuration Options

Edit `.env` to customize:

```env
CHECK_INTERVAL=60      # Check interval in seconds (default: 60)
GMAIL_LABELS=INBOX     # Labels to monitor (comma-separated)
MAX_MESSAGES=10        # Max messages to fetch per check
LOG_LEVEL=INFO        # Logging level (DEBUG, INFO, WARNING, ERROR)
TZ=Europe/Berlin      # Timezone for logs
```

## 🔍 Troubleshooting

### "credentials.json not found"
→ Download credentials from Google Cloud Console

### "Access denied" or OAuth errors
→ Delete `token.json` and re-authenticate:
```bash
rm token.json
python gmail_puller.py
```

### Container won't start
→ Check logs:
```bash
docker-compose logs
```

---

For detailed instructions, see [README.md](README.md)
