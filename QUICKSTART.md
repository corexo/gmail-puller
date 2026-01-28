# Gmail Puller - Schnellstart / Quick Start

## 🚀 Schnellstart (Deutsch)

### Voraussetzungen
- Docker & Docker Compose installiert
- Gmail-Konto mit externen E-Mail-Konten (POP3/IMAP)
- Gmail-Passwort (oder App-Passwort bei 2FA/Workspace)

### In 5 Schritten zum Ziel:

1. **Projekt klonen**
   ```bash
   git clone https://github.com/corexo/gmail-puller.git
   cd gmail-puller
   ```

2. **Authentifizierung vorbereiten**
   
   **Private Gmail-Konten:**
   - Verwenden Sie Ihr normales Gmail-Passwort
   - App-Passwörter sind meist nicht verfügbar
   
   **Google Workspace oder 2FA-Konten:**
   - Gehe zu: https://myaccount.google.com/apppasswords
   - Erstelle ein App-Passwort für "Mail"
   - Kopiere das 16-stellige Passwort

3. **Konfiguration**
   ```bash
   cp .env.example .env
   # Bearbeite .env und trage deine Daten ein:
   # GMAIL_EMAIL=deine.email@gmail.com
   # GMAIL_PASSWORD=dein_passwort  # Normales Passwort oder App-Passwort
   ```

4. **Setup-Skript ausführen**
   ```bash
   ./setup.sh
   ```

5. **Mit Docker starten**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

**Fertig!** 🎉 Der Gmail Puller klickt jetzt jede Minute auf "Jetzt E-Mails abrufen".

---

## 🚀 Quick Start (English)

### Prerequisites
- Docker & Docker Compose installed
- Gmail account with external email accounts (POP3/IMAP)
- Gmail password (or App Password for 2FA/Workspace)

### 5 Steps to Success:

1. **Clone the project**
   ```bash
   git clone https://github.com/corexo/gmail-puller.git
   cd gmail-puller
   ```

2. **Prepare Authentication**
   
   **Private Gmail accounts:**
   - Use your regular Gmail password
   - App Passwords are typically not available
   
   **Google Workspace or 2FA accounts:**
   - Go to: https://myaccount.google.com/apppasswords
   - Create an App Password for "Mail"
   - Copy the 16-character password

3. **Configuration**
   ```bash
   cp .env.example .env
   # Edit .env and enter your credentials:
   # GMAIL_EMAIL=your.email@gmail.com
   # GMAIL_PASSWORD=your_password  # Regular password or App Password
   ```

4. **Run setup script**
   ```bash
   ./setup.sh
   ```

5. **Start with Docker**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

**Done!** 🎉 Gmail Puller is now clicking "Fetch mail now" every minute.

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
GMAIL_EMAIL=your.email@gmail.com     # Your Gmail address
GMAIL_PASSWORD=your_password         # Your password (regular or App Password)
CHECK_INTERVAL=60                    # Check interval in seconds
GMAIL_ACCOUNT_INDEX=0               # Account index (if multiple)
LOG_LEVEL=INFO                      # Logging level
TZ=Europe/Berlin                    # Timezone
HEADLESS=true                       # Browser in background
```

## 🔍 Troubleshooting

### "GMAIL_EMAIL and GMAIL_PASSWORD must be set"
→ Edit `.env` file and enter your credentials

### "Could not find 'Fetch emails now' button"
→ Make sure you have external email accounts configured in Gmail settings
→ Go to: https://mail.google.com/mail/u/0/#settings/accounts

### Login errors
→ Use your regular password for private Gmail accounts
→ Use an App Password for Google Workspace or 2FA accounts
→ Enable 2FA first: https://myaccount.google.com/security

### Container won't start
→ Check logs:
```bash
docker-compose logs
```

---

## 💡 What This Does

This script automates clicking the **"Fetch emails now"** button in Gmail settings to force Google to pull emails from external accounts (POP3/IMAP) immediately, instead of waiting 20+ minutes.

**Important:** This only works if you have external email accounts configured in Gmail!

For detailed instructions, see [README.md](README.md)
