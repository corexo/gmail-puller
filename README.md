# Gmail Puller

Automatisches Klicken auf "Jetzt E-Mails abrufen" in Gmail jede Minute mit Docker.

Automatically click "Fetch emails now" button in Gmail every minute using Docker.

## 🇩🇪 Deutsch

### Beschreibung

Dieses Projekt automatisiert das Klicken auf den Button "Jetzt E-Mails abrufen" in den Gmail-Einstellungen. Dies ist nützlich, wenn Sie externe E-Mail-Konten (POP3/IMAP) mit Gmail verbunden haben und Google die E-Mails schneller abrufen soll, als es normalerweise der Fall ist.

**Problem:** Google hat eine hohe Verzögerung beim Abrufen von E-Mails aus externen Konten (oft über 20 Minuten). Dies führt zu Problemen mit Verifizierungs-E-Mails, die bereits abgelaufen ankommen.

**Lösung:** Dieses Skript klickt automatisch jede Minute auf den "Jetzt E-Mails abrufen" Button, um Google zu zwingen, die E-Mails sofort abzurufen.

### Voraussetzungen

- Docker und Docker Compose installiert
- Ein Gmail-Konto mit verbundenen externen E-Mail-Konten
- App-Passwort für Gmail (empfohlen aus Sicherheitsgründen)

### Einrichtung

#### 1. App-Passwort erstellen (empfohlen)

Aus Sicherheitsgründen sollten Sie ein App-Passwort verwenden:

1. Gehen Sie zu [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Wählen Sie "Mail" als App
3. Wählen Sie Ihr Gerät
4. Kopieren Sie das generierte 16-stellige Passwort

#### 2. Konfiguration

1. Kopieren Sie die `.env.example` zu `.env`:
   ```bash
   cp .env.example .env
   ```

2. Bearbeiten Sie die `.env` Datei und tragen Sie Ihre Daten ein:
   ```env
   GMAIL_EMAIL=ihre.email@gmail.com
   GMAIL_PASSWORD=ihr_app_passwort_hier
   CHECK_INTERVAL=60          # Prüfintervall in Sekunden (60 = 1 Minute)
   GMAIL_ACCOUNT_INDEX=0      # Gmail Account Index (Standard: 0)
   LOG_LEVEL=INFO            # Log-Level
   TZ=Europe/Berlin          # Zeitzone
   HEADLESS=true             # Browser im Hintergrund (true/false)
   ```

#### 3. Mit Docker starten

```bash
# Setup-Skript ausführen (prüft Konfiguration)
./setup.sh

# Container bauen und starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

### Verwendung

Nach dem Start meldet sich der Container automatisch bei Gmail an und klickt jede Minute auf den "Jetzt E-Mails abrufen" Button:

```bash
docker-compose logs -f gmail-puller
```

Sie sehen Ausgaben wie:
```
gmail-puller  | 2024-01-27 12:00:00 - INFO - Successfully logged into Gmail
gmail-puller  | 2024-01-27 12:00:05 - INFO - ✓ Successfully clicked 'Jetzt E-Mails abrufen' button!
gmail-puller  | 2024-01-27 12:00:05 - INFO - ✓ Email fetch triggered successfully
```

### Fehlerbehebung

**Problem:** "GMAIL_EMAIL and GMAIL_PASSWORD must be set"
- Lösung: Bearbeiten Sie die `.env` Datei und tragen Sie Ihre Gmail-Zugangsdaten ein

**Problem:** "Could not find 'Fetch emails now' button"
- Lösung: Stellen Sie sicher, dass Sie externe E-Mail-Konten in Ihren Gmail-Einstellungen konfiguriert haben
- Der Button erscheint nur, wenn externe Konten verbunden sind

**Problem:** Login-Fehler
- Lösung: Verwenden Sie ein App-Passwort statt Ihres regulären Passworts
- Stellen Sie sicher, dass 2FA aktiviert ist, um App-Passwörter zu generieren

**Problem:** Container startet nicht
- Lösung: Prüfen Sie die Logs mit `docker-compose logs`

### Wichtige Hinweise

- Das Skript benötigt externe E-Mail-Konten, die in Gmail konfiguriert sind
- Der Button "Jetzt E-Mails abrufen" wird nur angezeigt, wenn externe Konten verbunden sind
- Aus Sicherheitsgründen wird die Verwendung eines App-Passworts empfohlen
- Die Login-Session wird persistent gespeichert, sodass nur einmal eine Anmeldung erforderlich ist

---

## 🇬🇧 English

### Description

This project automates clicking the "Fetch emails now" button in Gmail settings. This is useful when you have external email accounts (POP3/IMAP) connected to Gmail and want Google to fetch emails faster than it normally does.

**Problem:** Google has a high delay when fetching emails from external accounts (often over 20 minutes). This causes issues with verification emails that expire before they arrive.

**Solution:** This script automatically clicks the "Fetch emails now" button every minute to force Google to fetch emails immediately.

### Prerequisites

- Docker and Docker Compose installed
- A Gmail account with connected external email accounts
- App Password for Gmail (recommended for security)

### Setup

#### 1. Create App Password (recommended)

For security reasons, you should use an App Password:

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" as the app
3. Select your device
4. Copy the generated 16-character password

#### 2. Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and enter your credentials:
   ```env
   GMAIL_EMAIL=your.email@gmail.com
   GMAIL_PASSWORD=your_app_password_here
   CHECK_INTERVAL=60          # Check interval in seconds (60 = 1 minute)
   GMAIL_ACCOUNT_INDEX=0      # Gmail account index (default: 0)
   LOG_LEVEL=INFO            # Log level
   TZ=Europe/Berlin          # Timezone
   HEADLESS=true             # Run browser in background (true/false)
   ```

#### 3. Start with Docker

```bash
# Run setup script (checks configuration)
./setup.sh

# Build and start container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

### Usage

After starting, the container automatically logs into Gmail and clicks the "Fetch emails now" button every minute:

```bash
docker-compose logs -f gmail-puller
```

You'll see output like:
```
gmail-puller  | 2024-01-27 12:00:00 - INFO - Successfully logged into Gmail
gmail-puller  | 2024-01-27 12:00:05 - INFO - ✓ Successfully clicked 'Fetch mail now' button!
gmail-puller  | 2024-01-27 12:00:05 - INFO - ✓ Email fetch triggered successfully
```

### Troubleshooting

**Problem:** "GMAIL_EMAIL and GMAIL_PASSWORD must be set"
- Solution: Edit the `.env` file and enter your Gmail credentials

**Problem:** "Could not find 'Fetch emails now' button"
- Solution: Make sure you have external email accounts configured in your Gmail settings
- The button only appears when external accounts are connected

**Problem:** Login errors
- Solution: Use an App Password instead of your regular password
- Make sure 2FA is enabled to generate App Passwords

**Problem:** Container won't start
- Solution: Check the logs with `docker-compose logs`

### Important Notes

- The script requires external email accounts configured in Gmail
- The "Fetch emails now" button only appears when external accounts are connected
- Using an App Password is recommended for security
- Login session is stored persistently, so you only need to log in once

---

## 📋 Features

- ✅ Automatic button clicking every minute (configurable)
- ✅ Docker containerized for easy deployment
- ✅ Selenium-based browser automation
- ✅ Configurable via .env file
- ✅ Persistent login session
- ✅ Headless browser mode
- ✅ Multi-language support (German & English)

## 🔒 Security

- Uses App Password (no regular password storage)
- Browser profile stored in Docker volume
- Credentials only in .env file
- `.gitignore` configured to exclude sensitive files

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
